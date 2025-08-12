import os
from datetime import datetime
import contextlib
import io

def create_project_folder(topic):
    safe_topic = topic.strip().replace(" ", "_").replace("?", "").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{safe_topic}_{date_str}"
    path = os.path.join("memory", folder_name)

    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "plots"), exist_ok=True)

    return path

def save_to_file(topic, content, filename="summary.md"):
    project_folder = create_project_folder(topic)
    file_path = os.path.join(project_folder, filename)

    # Ensure subfolder exists if filename contains folders
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def exec_and_capture_output(code, topic=None):


    project_folder = create_project_folder(topic) if topic else None

    # Redirect output
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
    except Exception as e:
        return f"❌ Retry also failed:\n{e}"

    result = output.getvalue()

    # Save retry result
    if topic:
        save_to_file(topic, code, "refined_code.py")
        save_to_file(topic, result, "refined_output.md")

    return result
