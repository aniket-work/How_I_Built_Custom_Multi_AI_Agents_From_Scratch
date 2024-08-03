 # 🏢 Let's Build: A Simple Platform to Create Custom AI Agents for Any Task 🏢


Full Article : https://medium.com/@learn-simplified/lets-build-a-simple-platform-to-create-custom-ai-agents-for-any-task-d6c8e83549fa

## What is this article about?
This article is about a sophisticated AI-powered content creation system. It describes a flexible and customizable workflow that combines AI research and writing capabilities. The system uses a team of AI agents: a researcher who gathers information on a given topic, and multiple writers who create diverse content based on this research.
The article explains how this system is built using advanced AI libraries and tools. It shows how the workflow can be easily configured through a simple file, allowing users to adjust the AI agents' behaviors, prompts, and output styles without needing to change the underlying code. This makes it adaptable for various content needs, from blog posts to reports on different topics.
The system demonstrates how AI can be used to automate and enhance the content creation process, potentially revolutionizing how businesses approach content marketing, research, and communication.

## Prerequisites:

* Python 3.7+ installed on your system
* Basic understanding of Python programming
* Familiarity with command-line interfaces
* Basic knowledge of virtual environments

## Steps:

1. **Virtual Environment Setup:**

   Virtual environments help isolate project dependencies. Let's create one for our AI agent.

   - Open your terminal or command prompt
   - Navigate to your project directory
   - Create a new virtual environment:
   
     ```bash
     python -m venv How_I_Built_Custom_Multi_AI_Agents_From_Scratch 
     ```

   - Activate the environment:
   
     * On Windows:
        ```bash
        How_I_Built_Custom_Multi_AI_Agents_From_Scratch\Scripts\activate
        ```
     * On Unix or MacOS:
        ```bash
        source How_I_Built_Custom_Multi_AI_Agents_From_Scratch/bin/activate
        ```

   You should now see your terminal prompt change, indicating the virtual environment is active.

2. **Install Project Dependencies:**

   We'll use several Python libraries for our AI agent. Let's install them:

   - Ensure you're in your project directory with the virtual environment activated
   - Create a file named `requirements.txt` with the following content:
     ```
     streamlit
     requests
     ```
   - Install the dependencies using pip:
   
     ```bash
     pip install -r requirements.txt
     ```

   This will install Streamlit for creating the web interface and LangChain for building the AI agent.

3. **Setup Ollama:**

   Ollama is an easy-to-use framework for running large language models locally.

   - Download Ollama from https://ollama.com/download
   - Install Ollama following the instructions for your operating system
   - Once installed, open a new terminal and pull the LLaMA model:
    ```bash
    ollama pull llama3
    ```
   This may take some time depending on your internet connection.



4. **Run the AI Agent:**

   Now that we have our script ready, let's run it:

   - Ensure your virtual environment is activated
   - In your terminal, navigate to your project directory
   - Run the Streamlit app:
   
     ```bash
     streamlit run streamlit_app.py
     ```

Remember to always activate your virtual environment when working on this project, and feel free to modify the script to add more features or improve the analysis capabilities.
