# AEO Validator:All the different ways we look for the same things

The main idea behind Ag2_AEO is to create all the different possibilites a user will look up for a particular company. The idea is to optimise search, there are multiple ways to look for your company's information and the idea is to use this tool to make sure we highlight your comapny, we can also work with agents you can also architect queries in different languages. The idea is use this tool for Answer Engine Optimisation, using agentic frameworks to market a website so whenever someone looks for a company using LLMs they are sent to your website.

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
🔑 Setup
1. Clone the repository.
2. Create a virtual env and pip install the requirements
3. CD into the folder src
4. Create a .env file with OPENAI_API_KEY in the src folder with your OpenAI API key.
5. Run "python main.py"

---
I'm sharing a video on how to run the project:
https://youtu.be/SNCaqAqn9Bk

Things I want to work on for this project:
1. Prompt evaluation
2. Fine-tuning models
3. Access to a bunch of different apis, integrating LLMs based on their compute ability

Bugs to fix:
1. Sometimes the model hallucinates and directs you to example.com, cancel the running process immedieatly and start the process again.
2. The validation agent doesn't always give the most accurate results event and sometimes will not coordinate with other agents, I would reccomend clearing up your cache or looking up a different website link

