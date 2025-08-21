# AEO Validator

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
- Configurable with different OpenAI models.

---
🔑 Setup
1. Clone the repository.
2. Create a .env file in the project root with your OpenAI API key.
3. CD into the folder src
4. Create a virtual env and pip install the requirementw
5. Run "python main.py"

---
I'm sharing a video on how to run and use the project:
https://youtu.be/SNCaqAqn9Bk

Common issues:
1. Sometimes the model hallucinates and directs you to example.com, cancel the running process immedieatly and start the process again

