
# **AI-Driven Command Execution and Response System**

This project is an **AI-powered application** designed to execute SSH commands on remote devices and interpret their outputs. It leverages the following technologies:

- **Streamlit**: For a user-friendly interface.
- **DSPy**: To manage datasets and integrate machine learning models.
- **Scrapli**: For SSH communication.
- **LLaMA (Large Language Model Meta AI)**: As the foundation for natural language understanding and generation.

---

## **Features**

- **User-Friendly Interface**: Built with Streamlit for an intuitive Q&A workflow.
- **Dataset Matching**: Searches for the best match in a historical dataset to respond to user queries.
- **LLaMA API Integration**: Queries **LLaMA 3.1** for generating responses when no dataset match is found.
- **SSH Command Execution**: Executes commands on remote devices via SSH and retrieves the output.
- **Output Interpretation**: Summarizes SSH command output into human-readable information using **LLaMA 3.2**.

---

## **Requirements**

This project is compatible with **Python 3.12.10**. While most libraries fully support Python 3.12, some dependencies may require additional validation (see the **Compatibility Notes** section).

### **Key Requirements**

- **Python Version**: `3.12.10` (or `3.11` if compatibility issues arise)
- **CSV File**: A `sample.csv` file containing historical questions and answers with the following structure:
  - `question`: The user query.
  - `answer`: The associated command to be executed via SSH.
- **Foundation Model**:
  - **LLaMA 3.1**: For generating responses via the LLaMA API.
  - **LLaMA 3.2 (1b-instruct-fp16)**: For interpreting SSH command outputs.
- **LLaMA API**: A running instance of the LLaMA API, accessible at `http://localhost:11434`.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <repository_folder>
```

### **2. Set Up a Python Virtual Environment** (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
Use the provided `requirements.txt` file to install the necessary libraries:
```bash
pip install -r requirements.txt
```

### **4. Prepare the Dataset**
Ensure the file `sample.csv` is present in the same directory. It should have at least two columns:
- `question`: The user query.
- `answer`: The command to be executed via SSH.

### **5. Verify the LLaMA API**
- Ensure the LLaMA API is running on `http://localhost:11434`.
- Modify the API endpoint in the code if necessary.

---

## **Usage**

### **Start the Application**
Run the following command to launch the Streamlit app:
```bash
streamlit run <script_name>.py
```

### **Interact with the Application**
1. Open the app in your browser (usually at `http://localhost:8501`).
2. Enter your question in the sidebar input field.
3. The app will:
   - Search for a matching question in the dataset.
   - Execute the corresponding SSH command or query the **LLaMA 3.1** model if no match is found.
   - Summarize the output using **LLaMA 3.2 (1b-instruct-fp16)**.

---

## **File Structure**

```plaintext
project/
├── sample.csv                 # Historical dataset (user-provided)
├── script.py                  # Main application code
├── requirements.txt           # Dependency list
├── README.md                  # Project documentation
```

---

## **Example CSV File (`sample.csv`)**

| Question                      | Answer                  |
|-------------------------------|-------------------------|
| What is the CPU usage?        | show processes cpu      |
| What interfaces are up?       | show ip interface brief |

---

## **Compatibility Notes**

This project is designed for **Python 3.12.10** but may also work in **Python 3.11**. Below are compatibility considerations:

- **Streamlit**: Fully supports Python 3.12.
- **Pandas**: Fully compatible.
- **DSPy**: Ensure `dspy==0.1.5` and `dspy-ai==2.4.5` work correctly in your environment.
- **Scrapli**: The installed version (`2023.7.30`) is compatible, but upgrading to `2023.10.30` is recommended:
  ```bash
  pip install --upgrade scrapli[ssh]
  ```
- **Requests**: Fully compatible.
- **Ollama**: Confirm compatibility with your LLaMA API setup.

### **Verifying Compatibility**
To ensure all libraries work correctly in Python 3.12, run:
```bash
pip check
```

If issues arise, consider downgrading to Python 3.11:
```bash
pyenv install 3.11.10
pyenv global 3.11.10
```

---

## **Troubleshooting**

### **Common Issues and Solutions**

1. **Missing Dependencies**:
   - Ensure all required packages are installed using:
     ```bash
     pip install -r requirements.txt
     ```

2. **LLaMA API Issues**:
   - Verify the LLaMA API server is running at `http://localhost:11434`.

3. **SSH Connection Errors**:
   - Ensure SSH credentials (hostname, username, and password) are correct.
   - Check network connectivity to the remote device.

4. **Python Compatibility Issues**:
   - If errors occur in Python 3.12, consider downgrading to Python 3.11:
     ```bash
     pyenv install 3.11.10
     pyenv global 3.11.10
     ```

---

## **Future Improvements**

- Add support for additional machine learning models.
- Enhance error handling and logging.
- Improve the user interface with more interactive features.
- Provide support for multiple LLMs (e.g., OpenAI models).

---

## **License**

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## **Acknowledgments**

- **Streamlit** for the interactive UI.
- **DSPy** for dataset and AI model management.
- **Scrapli** for SSH command execution.
- **Meta AI** for the **LLaMA** foundation models.
```

---

