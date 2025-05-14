import streamlit as st
import pandas as pd
import dspy
from dspy.datasets.dataset import Dataset
import requests
import json
from difflib import SequenceMatcher
from scrapli.driver.core import IOSXRDriver
from scrapli.exceptions import ScrapliAuthenticationFailed, ScrapliConnectionError, ScrapliTimeout
import ollama

# Load the CSV data
df = pd.read_csv("sample.csv")

# Convert rows to DSPy Examples and aggregate into a dataset
dataset = [
    dspy.Example(question=row['question'], answer=row['answer']).with_inputs("question")
    for _, row in df.iterrows()
]

# Define the DSPy Dataset class
class HistoricalEventsDataset(Dataset):
    def __init__(self, file_path, train_size=0.8, train_seed=1):
        df = pd.read_csv(file_path)
        
        self.train_size = train_size
        self.train_seed = train_seed

        train_df = df.sample(frac=self.train_size, random_state=self.train_seed)
        test_df = df.drop(train_df.index)
        
        self._train = [
            dspy.Example(question=row['question'], answer=row['answer']).with_inputs("question")
            for _, row in train_df.iterrows()
        ]
        self._test = [
            dspy.Example(question=row['question'], answer=row['answer']).with_inputs("question")
            for _, row in test_df.iterrows()
        ]

    @property
    def train(self):
        return self._train
    
    @property
    def test(self):
        return self._test

# Load your dataset
historical_data = HistoricalEventsDataset("sample.csv")

def query_llama(question):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1",
        "prompt": question
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            response_text = response.text
            json_objects = response_text.strip().split('\n')
            full_response = ""
            for obj in json_objects:
                json_obj = json.loads(obj)
                full_response += json_obj.get('response', '')

            return full_response.strip()
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
            raise Exception("Failed to decode JSON response from LLaMA API")
    else:
        st.error(f"Error querying LLaMA: {response.status_code} {response.text}")
        raise Exception(f"Error querying LLaMA: {response.status_code} {response.text}")

def find_best_match(question, dataset, threshold=0.50):
    best_match = None
    highest_similarity = 0

    for example in dataset:
        similarity = SequenceMatcher(None, question, example.question).ratio()
        if similarity > highest_similarity and similarity >= threshold:
            highest_similarity = similarity
            best_match = example

    return best_match

llm = dspy.OllamaLocal(model="llama3.2:1b-instruct-fp16", temperature=0)
dspy.configure(lm=llm)

# Define the SSHTool class
class SSHTool:
    def __init__(self, name, hostname, username, password):
        self.name = name
        self.hostname = hostname
        self.username = username
        self.password = password
        self.input_variable = "command"
        self.desc = "Executes a command on a remote device via SSH"

    def execute(self, command):
        MY_DEVICE = {
            "host": self.hostname,
            "auth_username": self.username,
            "auth_password": self.password,
            "auth_strict_key": False,
            "timeout_socket": 10,
            "timeout_transport": 10,
            "timeout_ops": 10
        }

        try:
            with IOSXRDriver(**MY_DEVICE) as conn:
                response = conn.send_command(command)
                return response.result
        except ScrapliAuthenticationFailed:
            return "Authentication failed. Please check your username and password."
        except ScrapliConnectionError as e:
            return f"Connection error: {str(e)}"
        except ScrapliTimeout as e:
            return f"Timeout error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Initialize the ReAct module with the BasicQA signature and the custom SSH tool
ssh_tool = SSHTool(name="SSHCommandTool", hostname="131.226.217.150", username="admin", password="C1sco12345")
react_module = dspy.ReAct(BasicQA, tools=[ssh_tool])

def interpret_output_with_llm(output):
    prompt = f"The following output was received from a router command:\n{output}\n\n" \
             f"Provide a brief, human-readable summary of the router's status in one or two sentences."
    interpretation = llm(prompt)
    
    # Clean the output from unwanted prefixes
    if isinstance(interpretation, list):
        cleaned_interpretation = []
        for item in interpretation:
            if item.startswith("0:"):
                item = item.split("0:", 1)[1].strip()
            cleaned_interpretation.append(item)
        interpretation = " ".join(cleaned_interpretation).strip()
    else:
        if interpretation.startswith("0:"):
            interpretation = interpretation.split("0:", 1)[1].strip()
    
    return interpretation

st.title("AI-Driven Command Execution and Response System")

st.sidebar.header("Ask a Question")
user_question = st.sidebar.text_input("Enter a question:")

if user_question:
    st.write("Searching dataset for the best match...")
    best_match = find_best_match(user_question, historical_data.train)
    
    if best_match:
        st.write(f"Closest match found in dataset: {best_match.question}")
        command = best_match.answer
    else:
        st.write("No match found in dataset. Querying LLaMA...")
        command = query_llama(user_question)
    
    command_result = ssh_tool.execute(command)
    interpreted_result = interpret_output_with_llm(command_result)
    
    st.write("Response:")
    st.write(interpreted_result)
