import streamlit as st
import json
import os
from src.main import run_workflow
import time

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
                {"type": "Position", "value": "Lead Research Analyst"},
                {"type": "Objective",
                 "value": "Find most suitable travel places in summer in Canada."},
                {"type": "Background",
                 "value": "You belong to a leading travel research institution. Your expertise lies in uncovering emerging travel trends and insights. You excel in dissecting detailed data and providing practical, actionable recommendations."}
            ],
            "task_prompt": "Conduct a comprehensive review of the latest advancements in travel and tourism for 2024. Identify key trends, innovations, and their effects on different travel destinations and experiences."
        },
        "writers": [
            {
                "role": "Travel Enthusiast Blogger",
                "goal": "Encourage exploration by sharing captivating stories about undiscovered travel spots and unique destinations.",
                "backstory": "Having traveled extensively, you bring diverse cultures and stunning landscapes to life through engaging narratives and personal experiences."
            },
            {
                "role": "Freelance Lifestyle Journalist",
                "goal": "Offer useful tips for achieving a stylish and balanced travel lifestyle.",
                "backstory": "From the newest travel accessories to wellness advice for travelers, your writings help readers enjoy a fulfilling and stylish travel experience."
            }
        ],
        "writer_task_prompt": "Using the provided insights, craft an engaging blog post that showcases the most notable travel innovations. Your article should be both informative and easy to understand, appealing to a travel-enthusiastic audience. Aim for a cool tone and steer clear of overly technical language..\n\nInsights:\n{{ parent_outputs['research'] }}",
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
        result, log_file = run_workflow()

        # Stream the log file content
        with output_placeholder.container():
            while True:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        content = f.read()
                        st.text_area("Workflow Output:", value=content, height=300)
                    if "All Done!" in content:  # Assuming this is how we know the workflow is complete
                        break
                time.sleep(1)  # Wait for 1 second before checking again

        st.success("Workflow completed!")

        if result:
            result_placeholder.subheader("Workflow Result:")
            result_placeholder.write(result)
        os.remove(log_file)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Setup", "Run"])

    if page == "Setup":
        setup_page()
    elif page == "Run":
        run_page()

if __name__ == "__main__":
    main()
