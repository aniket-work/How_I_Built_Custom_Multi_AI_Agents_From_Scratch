import streamlit as st
import json
import os
import time
from src.main import run_workflow
import threading
import queue

def load_config():
    config_path = 'config/config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    os.makedirs('config', exist_ok=True)
    with open('config/config.json', 'w') as f:
        json.dump(config, f, indent=4)

def setup_page():
    st.title("Configuration Setup")

    config = load_config() or {
    "search_tool": {"max_results": 5},
    "ollama": {"model": "llama3"},
    "researcher": {
        "id": "explorer",
        "rules": [
            {"type": "Position", "value": "Chief Travel Explorer"},
            {"type": "Objective",
             "value": "Uncover the latest travel trends and destination insights."},
            {"type": "Background",
             "value": "You are a part of a leading travel consultancy. Your expertise lies in discovering new travel experiences and trends. You have a knack for turning data into compelling travel recommendations."}
        ],
        "task_prompt": "Conduct an in-depth analysis of current travel trends and emerging destinations for 2024. Highlight key trends, must-visit places, and their appeal to different types of travelers."
    },
    "writers": [
        {
            "role": "Cultural Travel Writer",
            "goal": "Reveal the rich cultural experiences of various destinations",
            "backstory": "Having explored numerous countries, you immerse readers in the traditions, festivals, and daily lives of the places you visit."
        },
        {
            "role": "Adventure Travel Enthusiast",
            "goal": "Guide thrill-seekers to the best adventure destinations",
            "backstory": "From mountain climbing to deep-sea diving, you share firsthand experiences and tips for adrenaline-filled adventures."
        }
    ],
    "writer_task_prompt": "Using the provided insights, craft a captivating blog post that explores the hottest travel trends and destinations of 2024. Your article should be engaging and easy to read, appealing to a broad audience of travel enthusiasts. Infuse it with excitement and avoid overly technical language.\n\nInsights:\n{{ parent_outputs['research'] }}",
    "end_task_prompt": "State: Adventure Awaits!"
}


    with st.form("config_form"):
        st.subheader("Search Tool")
        config["search_tool"]["max_results"] = st.number_input("Max Results",
                                                               value=config["search_tool"]["max_results"], min_value=1)

        st.subheader("Ollama")
        config["ollama"]["model"] = st.text_input("Model", value=config["ollama"]["model"])

        st.subheader("Researcher")
        config["researcher"]["id"] = st.text_input("Researcher ID", value=config["researcher"]["id"])
        for i, rule in enumerate(config["researcher"]["rules"]):
            st.text(f"Rule {i + 1}")
            rule["type"] = st.text_input(f"Type {i + 1}", value=rule["type"], key=f"researcher_rule_type_{i}")
            rule["value"] = st.text_area(f"Value {i + 1}", value=rule["value"], key=f"researcher_rule_value_{i}")
        config["researcher"]["task_prompt"] = st.text_area("Task Prompt", value=config["researcher"]["task_prompt"])

        st.subheader("Writers")
        for i, writer in enumerate(config["writers"]):
            st.text(f"Writer {i + 1}")
            writer["role"] = st.text_input(f"Role {i + 1}", value=writer["role"], key=f"writer_role_{i}")
            writer["goal"] = st.text_input(f"Goal {i + 1}", value=writer["goal"], key=f"writer_goal_{i}")
            writer["backstory"] = st.text_area(f"Backstory {i + 1}", value=writer["backstory"],
                                               key=f"writer_backstory_{i}")

        config["writer_task_prompt"] = st.text_area("Writer Task Prompt", value=config["writer_task_prompt"])
        config["end_task_prompt"] = st.text_input("End Task Prompt", value=config["end_task_prompt"])

        if st.form_submit_button("Save Configuration"):
            save_config(config)
            st.success("Configuration saved successfully!")

def run_page():
    st.title("Run Workflow")

    config = load_config()
    if config is None:
        st.error("Configuration not found. Please set up the configuration first.")
        return

    output_placeholder = st.empty()
    result_placeholder = st.empty()

    if st.button("Run Workflow"):
        output_placeholder.text("Running workflow...")

        # Run the workflow in a separate thread to avoid blocking the UI
        def run_workflow_thread(queue):
            result, log_file = run_workflow()
            queue.put((result, log_file))

        workflow_queue = queue.Queue()
        threading.Thread(target=run_workflow_thread, args=(workflow_queue,)).start()

        log_file = None
        while True:
            try:
                if not workflow_queue.empty():
                    result, log_file = workflow_queue.get()
                    break
            except queue.Empty:
                pass

            if log_file and os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    content = f.read()
                    output_placeholder.text_area("Workflow Output:", value=content, height=300)
                if "All Done!" in content:  # Assuming this is how we know the workflow is complete
                    break
            time.sleep(1)  # Wait for 1 second before checking again

        st.success("Workflow completed!")

        if result:
            result_placeholder.subheader("Workflow Result:")
            result_placeholder.write(result)
        if log_file:
            try:
                os.remove(log_file)
            except PermissionError:
                st.error("The log file is still in use and cannot be removed.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Setup", "Run"])

    if page == "Setup":
        setup_page()
    elif page == "Run":
        run_page()

if __name__ == "__main__":
    main()
