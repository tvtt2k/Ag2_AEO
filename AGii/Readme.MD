# AEO Validator: All the different ways we look for the same things

The main idea behind Ag2_AEO is to create all the different possibilites a user will look up for a particular company. I'm targeting answer engine optimisation solutions; as LLMs become the go to for search, there should be a focus on marketing to agents and we are leveraging agents' ability to generate new phrases everytime to see how they pick up target keywords, which ideally should be leading to target company's website. In case it doesn't, we should be able to figure out why and make changes accordingly. We can also use agents to simulate how people search your company in different languages and in all possible ways!


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
1. Clone the repository
2. Create a virtual env and pip install the requirements
3. CD into the folder src
4. Create a .env file in the src folder and put your OpenAI key in "OPENAI_API_KEY"
5. Run "python main.py"
---
 ## 🐞 Bugs to fix
1. Sometimes the agent pullup with example.com, cancel the process and start again - Incase you keep facing that issue again and again, please clean up your cache or try a different link
2. There are issues with Agent Orchestration, sometimes the Validator agent will not run - Run the code again
---
## 💡 Ideas I want to implement for better cost-optimisation
1. Use strcutrued query
2. Use different LLM configs based on task difficutly
3. Have agents converse in different languages
---
## 🎮 Demo
I'm sharing a video on how to run the project:
https://youtu.be/SNCaqAqn9Bk

