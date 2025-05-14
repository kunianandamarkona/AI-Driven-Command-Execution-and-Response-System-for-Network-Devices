AI-Driven Command Execution and Response System

This project is an AI-powered application designed for executing SSH commands on remote devices and interpreting their outputs. It leverages Streamlit for the user interface, DSPy for managing datasets and integrating machine learning models, and Scrapli for SSH communication. The application also integrates LLaMA (Large Language Model Meta AI) as its foundation model for natural language understanding and generation.



Features

User-friendly Interface: Built with Streamlit to provide an intuitive question-and-answer workflow.
Dataset Matching: Searches for the best match in a historical dataset to respond to user queries.
LLaMA API Integration: Queries LLaMA 3.1 for generating responses when no dataset match is found.
SSH Command Execution: Runs commands on a remote device via SSH and returns the output.
Output Interpretation: Summarizes the command output into human-readable information using the LLaMA 3.2 model.


Requirements

This application is compatible with Python 3.12.10. While most libraries in this project fully support Python 3.12, some dependencies may require additional validation. See the Compatibility Notes section for details.


Key Requirements

Python Version: 3.12.10 (or Python 3.11 if compatibility issues arise)
CSV File: A sample.csv file containing historical questions and answers with columns:
question
answer
Foundation Model: LLaMA (Large Language Model Meta AI) for advanced NLP tasks:
Model: LLaMA 3.1 (for querying the API)
Model: LLaMA 3.2 (1b-instruct-fp16) (for interpreting SSH responses)
LLaMA API: A running instance of the LLaMA API, accessible at http://localhost:11434.


Installation

Clone the Repository:

bash
Copy Code
git clone <repository_url>
cd <repository_folder>
Set Up a Python Virtual Environment (recommended):

bash
Copy Code
python3 -m venv venv
source venv/bin/activate
Install Dependencies: Use the provided requirements.txt file to install the necessary libraries:

bash
Copy Code
pip install -r requirements.txt
Prepare the Dataset: Ensure the file sample.csv is present in the same directory. It should have at least two columns:

question: The user query.
answer: The associated command to be executed via SSH.
Verify the LLaMA API:

Ensure the LLaMA API is running on http://localhost:11434.
Modify the API endpoint in the code if necessary.


Compatibility Notes

This project is designed for Python 3.12.10, but it may also work in Python 3.11 if compatibility issues arise.


Key Considerations for Python 3.12 Compatibility

Streamlit (1.44.1): Fully supports Python 3.12.
Pandas (2.2.2): Fully compatible.
DSPy (0.1.5) and dspy-ai (2.4.5): Ensure these versions work correctly in your environment.
Scrapli (2023.7.30): Compatible, but upgrading to 2023.10.30 is recommended:
bash
Copy Code
pip install --upgrade scrapli\[ssh\]
Requests (2.32.3): Fully compatible.
Ollama (0.3.2): Works with Python 3.12, but confirm compatibility with your LLaMA API setup.


Usage

Start the Application:

bash
Copy Code
streamlit run <script_name>.py
Interact with the Application:

Navigate to the app in your web browser (usually http://localhost:8501).
Enter your question in the sidebar input field.
The app will:
Search for a matching question in the dataset.
Execute the corresponding SSH command or query the LLaMA 3.1 model if no match is found.
Provide a summarized, human-readable interpretation of the command output using LLaMA 3.2 (1b-instruct-fp16).


File Structure

plaintext
Copy Code
project/
├── sample.csv                 # Historical dataset \(user-provided\)
├── script.py                  # Main application code
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation


Example CSV File (sample.csv)

question	answer
What is the CPU usage?	show processes cpu
What interfaces are up?	show ip interface brief


Troubleshooting

Common Issues and Solutions

Missing Dependencies:

Ensure all required packages are installed:
bash
Copy Code
pip install -r requirements.txt
LLaMA API Issues:

Verify the LLaMA API server is running at http://localhost:11434.
SSH Connection Errors:

Ensure SSH credentials (hostname, username, and password) are correct.
Check network connectivity to the remote device.
Python Compatibility:

If errors occur in Python 3.12, consider downgrading to Python 3.11:
bash
Copy Code
pyenv install 3.11.10
pyenv global 3.11.10


Future Improvements

Add support for additional machine learning models.
Enhance error handling and logging.
Improve the user interface with more interactive features.
Provide support for multiple LLMs (e.g., OpenAI models).


License

This project is licensed under the MIT License. See the LICENSE file for more details.



Acknowledgments

Streamlit for the interactive UI.
DSPy for dataset and AI model management.
Scrapli for SSH command execution.
Meta AI for the LLaMA foundation models.
