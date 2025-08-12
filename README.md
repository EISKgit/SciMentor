# SciMentor – AI Research Assistant

SciMentor is a local, self-hosted AI-powered research assistant that helps automate:
- Breaking down a topic into smaller research questions
- Generating Python experiments and running them locally
- Producing visual plots from the experiments
- Saving all outputs in a structured folder for future reference

The goal is to speed up research experiments by combining automated reasoning, code generation, and result visualization in one tool.

---

## Features

- Automatically generates a research plan for any topic.
- Writes and executes Python experiments without relying on internet access or extra datasets.
- Always produces three types of output for each topic:
  - `agent_summary.md` – research plan and findings
  - `experiment_code.py` – generated Python code
  - plots – stored in `/plots/`
- Saves all results in a separate folder under `/memory/` for each topic.
- Can retry failed code runs and fix errors automatically before giving final results.
- Simple Streamlit interface to run and review experiments.

---

## Project Structure

SciMentor/
│
├── app.py # Streamlit UI
├── agents.py # Coordinates the agents
├── research_agent.py # Research, code generation, and summarization
├── utils.py # File handling and helper functions
├── memory/ # Saved results
│ └── {topic_name}/
│ ├── agent_summary.md
│ ├── experiment_code.py
│ ├── plots/
│ └── plot_01.png
│
└── requirements.txt



---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SciMentor.git
cd SciMentor

Create a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Install the required packages:
pip install -r requirements.txt


Add API keys in a .env file:
GROQ_API_KEY=your_groq_api_key
SERPAPI_API_KEY=your_serpapi_api_key


Running the Application
Start the Streamlit app:

streamlit run app.py

Steps:
Enter a research topic in the text box.
Click “Run Agent Pipeline”.
Wait for the research plan, Python code, and plots to be generated.
View and download results from the sidebar.

Example Topics for Testing
These topics produce interesting results for demonstration:
Analyze the spread of a flu outbreak in a city and suggest prevention measures
Optimize solar panel performance under changing weather conditions
Predict traffic congestion patterns and suggest improvements
Model the effect of climate change on polar ice melting rates

License
This project is licensed under the MIT License.

Notes
The app is designed for local use and does not require deployment.
All outputs are stored in the memory folder for each topic.
Make sure you have matplotlib installed for plot generation.



