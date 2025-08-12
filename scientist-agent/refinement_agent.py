from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def improve_code(subproblem, broken_code, error_msg):
    SYSTEM_PROMPT = """
You are a Python assistant. Your job is to fix broken scientific experiment code.

Rules:
- ONLY return the improved Python code (no explanations).
- Focus on fixing the error mentioned.
- Add necessary imports if missing.
- Ensure matplotlib saves output if plots are present.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Subproblem: {subproblem}"),
        HumanMessage(content=f"Error: {error_msg}"),
        HumanMessage(content=f"Broken code:\n```python\n{broken_code}\n```")
    ]

    llm = ChatGroq(model="llama3-70b-8192", temperature=0.2)
    stream = llm.stream(messages)
    fixed = "".join(chunk.content for chunk in stream if hasattr(chunk, "content"))

    # Extract the Python code block only
    if "```python" in fixed:
        return fixed.split("```python")[1].split("```")[0].strip()
    return fixed.strip()
