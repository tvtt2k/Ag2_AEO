
import os
import re
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from urllib.parse import urlparse
from typing import Annotated

from dotenv import load_dotenv

from autogen import ConversableAgent, LLMConfig
from autogen.agentchat import initiate_group_chat
from autogen.agentchat.group.patterns import RoundRobinPattern
from autogen.agentchat.group import ReplyResult, ContextVariables
from autogen.tools.experimental import BrowserUseTool


class AEOValidator:
    """
    Flow:
      tech_agent -> prompt_agent -> validation_agent
    Tech summarizes homepage to YAML and stores it via save_summary.
    Prompt agent reads summary and stores 5 queries via save_prompts.
    Validator reads queries, checks Google, records results.

    Notes:
    - Tools are staticmethods (plain callables).
    - RoundRobin rotation is enforced by low max_consecutive_auto_reply
      for tech and prompt agents.
    """

    def __init__(self, model: str = "gpt-4o-mini", headless: bool = False) -> None:
        load_dotenv(dotenv_path=Path(__file__).resolve().parents[0] / ".env")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not set. Create a .env with OPENAI_API_KEY=... next to this script."
            )

        self.model = model
        self.headless = headless
        self.llm_config = LLMConfig(
            api_type="openai", model=self.model, api_key=api_key
        )

        self.support_context: ContextVariables | None = None
        self.tech_agent: ConversableAgent | None = None
        self.prompt_agent: ConversableAgent | None = None
        self.validation_agent: ConversableAgent | None = None
        self.user_agent: ConversableAgent | None = None
        self.browser_use_tool: BrowserUseTool | None = None
        self.pattern: RoundRobinPattern | None = None

    # ---------- utils ----------
    @staticmethod
    def _normalize_domain(url: str) -> str:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc

    def _init_context(self, company_name: str, website_url: str) -> None:
        if not website_url.startswith(("http://", "https://")):
            website_url = "https://" + website_url
        domain = self._normalize_domain(website_url)
        self.support_context = ContextVariables(
            data={
                "website": website_url,
                "company": company_name,
                "domain": domain,
                "summaries": [],
                "prompts": [],
                "validation_results": [],
            }
        )

    # ---------- tools (as staticmethods) ----------
    @staticmethod
    def _proj_root() -> Path:
        """Directory containing ref.py (stable even if CWD changes)."""
        return Path(__file__).resolve().parent

    @staticmethod
    def _read_prompt_file(path: Path) -> str:
        """Read a prompt file as UTF-8 and strip optional wrapping triple quotes."""
        txt = path.read_text(encoding="utf-8").strip()
        return txt

    @staticmethod
    def save_summary(
        summary: Annotated[str, "The website summary to save (YAML ONLY)"],
        context_variables: ContextVariables,
    ) -> ReplyResult:
        summaries = context_variables.get("summaries", [])
        summaries.append(summary)
        context_variables["summaries"] = summaries
        return ReplyResult(
            message=f"Saved summary: {summary[:800]}...",
            context_variables=context_variables,
        )

    @staticmethod
    def read_summaries(context_variables: ContextVariables) -> str:
        summaries = context_variables.get("summaries", [])
        return "No summaries available." if not summaries else "\n---\n".join(summaries)

    @staticmethod
    def save_prompts(
        prompts: Annotated[
            str, "Prompts generated for search engine (newline-separated, exactly 5)"
        ],
        context_variables: ContextVariables,
    ) -> ReplyResult:
        lst = context_variables.get("prompts", [])
        lst.extend([p.strip() for p in prompts.split("\n") if p.strip()])
        context_variables["prompts"] = lst
        return ReplyResult(
            message=f"Saved {len(lst)} prompts.",
            context_variables=context_variables,
        )

    @staticmethod
    def read_prompts(context_variables: ContextVariables) -> str:
        prompts = context_variables.get("prompts", [])
        return "No prompts found." if not prompts else "\n".join(prompts)


    @staticmethod
    def check_urls_and_record(
        prompt: Annotated[str, "Original search query used on Google/Bing"],
        serp_text: Annotated[str, "Raw text or copied URLs from the SERP (top results)"],
        context_variables: ContextVariables,
    ) -> ReplyResult:
        target = (context_variables.get("domain", "") or "").lower()

        # collect candidate URLs (handles mixed text)
        url_candidates = re.findall(r"https?://[^\s)'\"<>]+", serp_text, flags=re.IGNORECASE)

        def host_from_any(url: str) -> str | None:
            try:
                u = urlparse(url)
                if "google.com" in u.netloc and u.path.startswith("/url"):
                    q = parse_qs(u.query).get("q", [])
                    if q:
                        return urlparse(q[0]).netloc.lower()
                return u.netloc.lower()
            except Exception:
                return None

        def norm(h: str) -> str:
            return h[4:] if h and h.startswith("www.") else h

        found_url = None
        for u in url_candidates:
            host = norm(host_from_any(u) or "")
            if not host:
                continue
            if host == target or host.endswith("." + target):
                found_url = u
                break

        result = "Y" if found_url else "N"
        notes = f"match: {found_url}" if found_url else "not on first page"

        vr = context_variables.get("validation_results", [])
        vr.append({"prompt": prompt, "result": result, "notes": notes})
        context_variables["validation_results"] = vr

        return ReplyResult(
            message=f"Validation {result} for '{prompt[:80]}...' ({notes})",
            context_variables=context_variables,
        )
    # ---------- agents ----------
    def _build_agents(self) -> None:
        assert self.support_context is not None, "Context must be initialized first"

        base = self._proj_root() / "prompts"
        tech_system, prompt_system, validation_system = [
            self._read_prompt_file(base / fname)
            for fname in ("tech.txt", "prompt_agent.txt", "validation.txt")
        ]

        # Agents with tight auto-reply caps to force rotation
        self.tech_agent = ConversableAgent(
            name="tech_agent",
            system_message=tech_system,
            llm_config=self.llm_config,
            functions=[self.save_summary],  # pass callable, don't call
            max_consecutive_auto_reply=4,  # action, then handoff
        )
        self.prompt_agent = ConversableAgent(
            name="prompt_agent",
            system_message=prompt_system,
            llm_config=self.llm_config,
            functions=[self.read_summaries, self.save_prompts],
            max_consecutive_auto_reply=4,  # action, then handoff
        )
        self.validation_agent = ConversableAgent(
            name="validation_agent",
            system_message=validation_system,
            llm_config=self.llm_config,
            functions=[self.read_prompts, self.check_urls_and_record],
            max_consecutive_auto_reply=12,  # enough to process all queries
        )

        # Human proxy (executes BrowserUseTool actions)
        self.user_agent = ConversableAgent(name="user", human_input_mode="ALWAYS")

        # Browser tool wiring
        self.browser_use_tool = BrowserUseTool(
            llm_config=self.llm_config,
            browser_config={"headless": self.headless},
        )
        self.browser_use_tool.register_for_llm(self.tech_agent)  # summarizer can browse
        self.browser_use_tool.register_for_llm(
            self.validation_agent
        )  # validator can browse SERPs
        self.browser_use_tool.register_for_execution(
            self.user_agent
        )  # human executes actions

        # Round-robin coordination
        self.pattern = RoundRobinPattern(
            initial_agent=self.tech_agent,
            agents=[self.tech_agent, self.prompt_agent, self.validation_agent],
            user_agent=self.user_agent,
            context_variables=self.support_context,
            group_manager_args={"llm_config": self.llm_config},
        )

    # ---------- run ----------
    def run(
        self,
        company_name: str | None = None,
        website_url: str | None = None,
        max_rounds: int = 30,
    ) -> None:
        if company_name is None:
            company_name = input("Enter company name: ").strip()
        if website_url is None:
            website_url = input("Enter the company's url: ").strip()

        self._init_context(company_name, website_url)
        self._build_agents()

        kickoff = (
            f"Open {self.support_context['website']}, summarize the homepage; then generate 5 search prompts "
            f"Using the search prompts look if the company is found through those prompts, validate it. Follow the HANDOFF/DONE protocol strictly."
        )

        with self.llm_config:
            result, context, last_agent = initiate_group_chat(
                pattern=self.pattern,
                messages=kickoff,
                max_rounds=max_rounds,
            )

        print("\n=== Final Result ===")
        print(result)
        print("\n=== Last Agent ===")
        print(last_agent.name)

        print("\n=== Validation Results ===")
        for item in context.get("validation_results", []):
            print(
                f"- Prompt: {item['prompt']}\n  Result: {item['result']}\n  Notes: {item.get('notes','')}\n"
            )

        print("\n=== Saved Summaries ===")
        print(context.get("summaries", []))

        print("\n=== Saved Prompts ===")
        print(context.get("prompts", []))


if __name__ == "__main__":
    app = AEOValidator(model="gpt-4o-mini", headless=False)
    app.run()
