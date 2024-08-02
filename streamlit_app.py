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
            "id": "researcher",
            "rules": [
                {"type": "Position", "value": "Lead Travel Researcher"},
                {"type": "Objective",
                 "value": "Discover innovative advancements in artificial intelligence and data analytics."},
                {"type": "Background",
                 "value": "You are part of a prominent technology research institute. Your speciality is spotting new trends. You excel at analyzing intricate data and delivering practical insights."}
            ],
            "task_prompt": "Perform a detailed examination of the newest developments in AI as of 2024. Pinpoint major trends, breakthroughs, and their implications for various industries."
        },
        "writers": [
            {
                "role": "Travel Adventure Blogger",
                "goal": "Inspire wanderlust with stories of hidden gems and exotic locales",
                "backstory": "With a passport full of stamps, you bring distant cultures and breathtaking scenes to life through vivid storytelling and personal anecdotes."
            },
            {
                "role": "Lifestyle Freelance Writer",
                "goal": "Share practical advice on living a balanced and stylish life",
                "backstory": "From the latest trends in home decor to tips for wellness, your articles help readers create a life that feels both aspirational and attainable."
            }
        ],
        "writer_task_prompt": "Using insights provided, develop an engaging blog post that highlights the most significant AI advancements. Your post should be informative yet accessible, catering to a tech-savvy audience. Make it sound cool, avoid complex words so it doesn't sound like AI.\n\nInsights:\n{{ parent_outputs['research'] }}",
        "end_task_prompt": "State: All Done!"
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
