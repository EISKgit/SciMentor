from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from research_agent import search_web_for
from dotenv import load_dotenv
from utils import save_to_file  # import inside function for safety
from research_agent import run_experiment,generate_research_plan
load_dotenv()


# Shared model
llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.5,
    )

# 🧑‍🔬 Researcher Agent
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a scientific researcher. Break this topic into subproblems and suggest methods or experiments."),
    ("human", "{input}")
])
research_chain = research_prompt | llm

# 💻 Coder Agent
coder_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python coder. Write simple experiments or simulations for the researcher's ideas."),
    ("human", "{input}")
])
coder_chain = coder_prompt | llm

# 🧾 Summarizer Agent
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a summarizer. Given the research and experiment, summarize the findings in clear points."),
    ("human", "{input}")
])
summary_chain = summary_prompt | llm

# 🔗 Full Agent Chain
agent_team = RunnableSequence(first=research_chain, last=coder_chain | summary_chain)

from research_agent import run_experiment, search_web_for
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
import os

def run_full_agent_pipeline(topic):
    # 1️⃣ Generate research plan
    research_plan = generate_research_plan(topic)
    save_to_file(topic, research_plan, "agent_summary.md")

    # 2️⃣ Run experiment with enforced retries for all outputs
    experiment_result = None
    retries = 0
    while retries < 3:
        experiment_result = run_experiment(subproblem=topic, topic=topic, max_retries=2)

        # Check if code, summary, and plot exist
        project_folder = os.path.join("memory", topic.replace(" ", "_"))
        code_path = os.path.join(project_folder, "experiment_code.py")
        summary_path = os.path.join(project_folder, "agent_summary.md")
        plot_folder = os.path.join(project_folder, "plots")
        plot_exists = os.path.exists(plot_folder) and any(f.endswith(".png") for f in os.listdir(plot_folder))

        if os.path.exists(code_path) and os.path.exists(summary_path) and plot_exists:
            break  # ✅ all files exist
        retries += 1

    # 3️⃣ Merge outputs for UI
    final_output = ""
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            final_output += f.read()

    if experiment_result and "output" in experiment_result:
        final_output += "\n\n" + experiment_result["output"]

    return {
        "status": "success",
        "output": final_output,
        "retries": retries
    }
