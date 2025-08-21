# AEO Validator:All the different ways we look for the same things

The core idea behind AG2_AEO is to generate and validate all the different ways a user might search for a particular company. Traditional SEO focuses on keywords, but Answer Engine Optimization (AEO) focuses on ensuring your company is discoverable across natural language queries, multiple languages, and varied search intents.

By leveraging agentic frameworks, AG2_AEO:

i. Architects diverse queries that real users might use when looking for your company.

ii. Optimizes search visibility by testing whether your website appears for those queries.

iii. Expands reach across languages and contexts, making your company visible no matter how people ask.

iv. Highlights your company in LLM-driven answer engines (Google’s SGE, Bing Copilot, ChatGPT browsing, etc.), ensuring users are directed to your site when they ask questions about your brand or industry.

In short, AG2_AEO helps transform your website from being just another search result into the primary answer that AI systems and modern search engines deliver.

AEO Validator is an automated multi-agent pipeline designed to **validate search engine visibility** for a given company’s website.  
It leverages [AG2.ai's framework](https://ag2.ai/#hero) to coordinate multiple conversational agents that perform:

1. **Homepage Summarization (Tech Agent)**  
   - Opens the target website and generates a YAML summary.  

2. **Prompt Generation (Prompt Agent)**  
   - Reads the summary and produces **5 optimized search queries**.  

3. **Search Validation (Validation Agent)**  
   - Executes the queries on Google/Bing.  
   - Checks whether the company’s domain appears in the first-page results.  
   - Records results (Y/N + notes).  

The agents are orchestrated using a **round-robin pattern** to enforce sequential handoffs until the task is complete.

---
## 🚀 Features
- Automated **SEO/Visibility validation** workflow.
- Multi-agent setup using **ConversableAgent** from AutoGen.
- Uses **BrowserUseTool** for web browsing & SERP scraping.
- **Context tracking** for summaries, prompts, and validation results.
- YAML-based summaries for structured data reuse.
- Configurable with different foundational models.
---
## 🔑 Setup
1. Clone the repository.
2. Create a virtual env and pip install the requirements
3. CD into the folder src
4. Create a .env file with OPENAI_API_KEY in the src folder with your OpenAI API key.
5. Run "python main.py"
---
## 🐞 Bugs to fix:
1. Sometimes the model hallucinates and directs you to example.com, cancel the running process immedieatly and start the process again.
2. The validation agent doesn't always give the most accurate results event and sometimes will not coordinate with other agents, I would reccomend clearing up your cache or looking up a different website link
---
## 💡 Things I want to work on for this project:
1. Prompt evaluation
2. Fine-tuning models
3. Access to a bunch of different apis, integrating LLMs based on their compute ability
---
## 🎮 Demo:
I'm sharing a video on how to run the project:
https://youtu.be/SNCaqAqn9Bk






