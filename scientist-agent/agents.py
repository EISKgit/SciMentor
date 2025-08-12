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

    # 2️⃣ Run experiment with enforced retries
    experiment_result = None
    retries = 0
    while retries < 3:
        experiment_result = run_experiment(subproblem=topic, topic=topic, max_retries=2)

        # Check if code, summary, and plot exist
        project_folder = os.path.join("memory", topic.replace(" ", "_"))
        code_path = os.path.join(project_folder, "experiment_code.py")
        plot_folder = os.path.join(project_folder, "plots")
        plot_exists = os.path.exists(plot_folder) and any(f.endswith(".png") for f in os.listdir(plot_folder))

        if os.path.exists(code_path) and plot_exists:
            break  # ✅ all required files exist
        retries += 1

    # 3️⃣ Merge into one rich summary file
    final_output = f"# Research Plan\n{research_plan}\n\n"

    if experiment_result and "output" in experiment_result:
        final_output += f"# Experiment Output\n{experiment_result['output']}\n"

    # Save the merged file as agent_summary.md
    save_to_file(topic, final_output, "agent_summary.md")

    return {
        "status": "success",
        "output": final_output,
        "retries": retries
    }
