from research_agent import generate_research_plan, run_experiment
from refinement_agent import improve_code
from utils import save_to_file, create_project_folder
import os
from research_agent import search_web_for
from agents import run_full_agent_pipeline
from utils import exec_and_capture_output

def main():
    print("🧠 Welcome to SciMentor: Your AI Research Assistant")
    print("1️⃣ Generate a research plan")
    print("2️⃣ Run an experiment from a subproblem")
    print("3️⃣ Search the web for live data")
    print("4️⃣ Run full Researcher → Coder → Summarizer pipeline")
    print("0️⃣ Exit")

    choice = input("\n🔘 Enter your choice (0-2): ").strip()

    if choice == "1":
        topic = input("\n🔍 Enter your research topic: ").strip()
        if not topic:
            print("❗Please enter a valid topic.")
            return

        print("\n⏳ Researching, please wait...\n")
        plan = generate_research_plan(topic)

        filepath = save_to_file(topic, plan, "research_plan.md")
        print(f"\n✅ Research plan saved to {filepath}")

    elif choice == "2":
        topic = input("\n🔍 Enter the topic/project name for this experiment: ").strip()
        if not topic:
            print("❗Please enter a valid topic.")
            return

        subproblem = input("\n💡 Enter the experiment or subproblem you'd like to test: ").strip()
        if not subproblem:
            print("❗Please enter a valid subproblem.")
            return

        print("\n🧪 Generating and running experiment...\n")


        result = run_experiment(subproblem, topic)

        if isinstance(result, dict) and result.get("status") == "error":
             
             print("🛠️ Error detected. Retrying...")

             fixed_code = improve_code(subproblem, result["original_code"], result["error"])

             # Run the improved version
           
             final_output = exec_and_capture_output(fixed_code, topic)

             print(final_output)

        else:
            print(result["output"])


        # Auto-number experiment files
        project_folder = create_project_folder(topic)
        existing_experiments = [f for f in os.listdir(project_folder) if f.startswith("experiment_") and f.endswith(".md")]
        exp_number = len(existing_experiments) + 1
        filename = f"experiment_{exp_number}.md"

        filepath = save_to_file(topic, result, filename)
        print(f"\n📊 Experiment result saved to {filepath}")

    elif choice == "3":
        query = input("\n🌐 What do you want to search for?\n> ")
        result = search_web_for(query)
        print(result)

    elif choice == "4":
   
        topic = input("🧪 Enter a research topic for the full agent pipeline:\n> ")
        result = run_full_agent_pipeline(topic)
        print("\n🤖 Agent Team Output:\n")
        print(result)


    elif choice == "0":
        print("👋 Exiting. See you next time!")
        return

    else:
        print("❌ Invalid choice. Please enter 0, 1, or 2.")

if __name__ == "__main__":
    main()
