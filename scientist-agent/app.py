import streamlit as st
from agents import run_full_agent_pipeline
from utils import save_to_file
import os
from datetime import datetime
import zipfile
import io

MEMORY_DIR = "memory"

st.set_page_config(page_title="SciMentor", layout="wide")

st.sidebar.title("🗃️ Past Projects")

# List all folders inside /memory/
if os.path.exists(MEMORY_DIR):
    project_folders = sorted(
        [f for f in os.listdir(MEMORY_DIR) if os.path.isdir(os.path.join(MEMORY_DIR, f))],
        reverse=True
    )

    selected_project = st.sidebar.selectbox("📂 Select a project", project_folders)

    if selected_project:
        selected_path = os.path.join(MEMORY_DIR, selected_project)
        st.sidebar.markdown(f"📁 **{selected_project}**")

        # Export as ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files_in_dir in os.walk(selected_path):
                for file in files_in_dir:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=selected_path)
                    zipf.write(file_path, arcname)
        zip_buffer.seek(0)

        st.sidebar.download_button(
            label="⬇️ Download Project as ZIP",
            data=zip_buffer,
            file_name=f"{selected_project}.zip",
            mime="application/zip"
        )

        # List all .md, .png, .py files
        files = sorted([
            f for f in os.listdir(selected_path)
            if f.endswith((".md", ".png", ".py"))
        ], reverse=True)

        selected_file = st.sidebar.selectbox("📄 Select a file", files)

        if selected_file:
            file_path = os.path.join(selected_path, selected_file)

            if selected_file.endswith(".md"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.subheader(f"📄 {selected_file}")
                st.markdown(content)

            elif selected_file.endswith(".png"):
                st.subheader(f"🖼️ {selected_file}")
                st.image(file_path, use_column_width=True)

            elif selected_file.endswith(".py"):
                with open(file_path, "r", encoding="utf-8") as f:
                    code_content = f.read()
                st.subheader(f"💻 {selected_file}")
                st.code(code_content, language="python")

            # Optional download
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download file",
                    data=f,
                    file_name=selected_file
                )
else:
    st.sidebar.warning("No memory folder found yet.")

st.title("🧠 SciMentor: AI Research Assistant")
st.markdown("Enter a topic and let the Researcher → Coder → Summarizer agents work for you.")

topic = st.text_input("🔍 Enter your research topic")

if st.button("Run Agent Pipeline"):
    if topic:
        with st.spinner("Running agents..."):
            result = run_full_agent_pipeline(topic)

            st.success("✅ Done!")
            st.subheader("📋 Final Agent Summary")
            st.markdown(result.content if hasattr(result, "content") else result["output"])

            # Show retry attempts if available
            if isinstance(result, dict) and "retries" in result:
                st.info(f"♻ Retry attempts: {result['retries']}")

            filepath = save_to_file(
                topic,
                result.content if hasattr(result, "content") else result["output"],
                "agent_summary.md"
            )
            st.caption(f"💾 Saved to: `{filepath}`")
    else:
        st.warning("Please enter a topic first.")
