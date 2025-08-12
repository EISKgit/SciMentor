from langchain_groq import ChatGroq
from serpapi import GoogleSearch
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import io
import contextlib
import os
from datetime import datetime
from utils import create_project_folder

load_dotenv()


def generate_research_plan(topic):
    SYSTEM_PROMPT = """
You are an expert scientific researcher who knows how to break down any complex question into smaller parts and create a step-by-step research strategy.

Instructions:
- Break the topic into clear sub-questions
- For each, suggest a research method
- If needed, suggest an experiment or dataset
- End with a 1-line research goal or expected outcome
"""

    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=topic)]

    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.5,
    )

    stream = llm.stream(messages)
    result = "".join(chunk.content for chunk in stream if hasattr(chunk, "content"))

    return result

# Autonomous code generator + executor
def run_experiment(subproblem, topic=None, max_retries=3):
    from utils import save_to_file

    SYSTEM_PROMPT = """
You are a Python scientific coder. For the given subproblem, write a short, working experiment or simulation using Python.
Rules:
- Must include at least one matplotlib plot.
- Must save the plot with plt.savefig() (not plt.show()).
- Code must run without needing internet or external APIs.
- Only output code. No explanations. Wrap code inside ```python ... ``` markdown.
"""

    llm = ChatGroq(model="llama3-70b-8192", temperature=0.4)

    # 1️⃣ Get code from LLM
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=subproblem)]
    stream = llm.stream(messages)
    response = "".join(chunk.content for chunk in stream if hasattr(chunk, "content"))

    if "```python" in response:
        code = response.split("```python")[1].split("```")[0].strip()
    else:
        code = response.strip()

    if topic:
        save_to_file(topic, code, "experiment_code.py")

    project_folder = create_project_folder(topic) if topic else None
    plot_folder = os.path.join(project_folder, "plots") if project_folder else "plots"
    os.makedirs(plot_folder, exist_ok=True)

    # Ensure plot saving
    if "matplotlib" in code and "plt.savefig" not in code:
        timestamp = datetime.now().strftime("%H-%M-%S")
        img_path = os.path.join(plot_folder, f"plot_{timestamp}.png")
        code += f"\nimport matplotlib.pyplot as plt\nplt.savefig(r'{img_path}')"

    # 2️⃣ Retry until code runs & plot is saved
    attempt = 1
    while attempt <= max_retries:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, {})

            output_text = buf.getvalue()

            # Check if plot exists
            if not any(fname.endswith(".png") for fname in os.listdir(plot_folder)):
                raise RuntimeError("No plot file generated — retrying.")

            # Save output text
            if topic and output_text.strip():
                save_to_file(topic, output_text, "experiments.md")

            # Append plot previews
            for file in os.listdir(plot_folder):
                if file.endswith(".png"):
                    output_text += f"\n\n![Experiment Plot](plots/{file})"

            return {"status": "success", "output": output_text}

        except Exception as e:
            if attempt < max_retries:
                fix_prompt = f"""
The following Python code failed:
ERROR: {str(e)}

CODE:
{code}

Fix it so that:
1. It runs without internet or extra packages.
2. It produces at least one matplotlib plot.
Return only corrected Python code.
"""
                fix_messages = [
                    SystemMessage(content="You are a helpful Python fixer."),
                    HumanMessage(content=fix_prompt)
                ]
                fix_stream = llm.stream(fix_messages)
                fixed_response = "".join(chunk.content for chunk in fix_stream if hasattr(chunk, "content"))
                if "```python" in fixed_response:
                    code = fixed_response.split("```python")[1].split("```")[0].strip()
                else:
                    code = fixed_response.strip()
            else:
                # 3️⃣ Fallback plot if all retries fail
                import matplotlib.pyplot as plt
                plt.figure()
                plt.plot([1, 2, 3], [4, 5, 6])
                plt.title(f"Auto-generated fallback plot for {topic or 'Unknown Topic'}")
                fallback_path = os.path.join(plot_folder, f"fallback_plot_{datetime.now().strftime('%H-%M-%S')}.png")
                plt.savefig(fallback_path)

                output_text = f"⚠️ Code failed after {max_retries} attempts.\nA fallback plot has been generated.\n\n![Fallback Plot](plots/{os.path.basename(fallback_path)})"
                save_to_file(topic, output_text, "experiments.md")
                return {"status": "error", "output": output_text, "original_code": code}
        attempt += 1



# Reserved for Day 5 (Web Search Agent)
def search_web_for(query, num_results=5):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "⚠️ SerpAPI key not found. Add SERPAPI_API_KEY to .env file."

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])

    output = f"🔍 Top {len(organic)} Web Search Results for: **{query}**\n\n"
    for idx, result in enumerate(organic):
        title = result.get("title", "No title")
        link = result.get("link", "")
        snippet = result.get("snippet", "No description")
        output += f"{idx+1}. **{title}**\n{snippet}\n🔗 {link}\n\n"

    return output if organic else "❌ No results found."