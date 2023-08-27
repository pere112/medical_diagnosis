import streamlit as st
import openai
import llama_api_server
import streamlit_chat
import sklearn
from streamlit_chat import message
from llama_api_server import LlamaAPI  # Replace with actual import from llama-api-server
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import './server'


# Set up LlamaAPI instance (replace with actual API initialization)
llama_api = LlamaAPI()

# Load and preprocess data (replace with actual data loading logic)
data = pd.read_csv('/kaggle/input/medical-datacsv/test-case/subject-info.csv')
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

# Model training (replace with actual model training logic)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

def main():
    st.title("Llama2 Medical Diagnosis Assistant")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]

    # Load CSV data
    csv_data = pd.read_csv('/kaggle/input/medical-datacsv/test-case/subject-info.csv')  # Replace with actual CSV file path

    st.write("CSV Data:")
    st.dataframe(csv_data)

    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])

        user_prompt = a.selectbox(
            label="Select a prompt:",
            options=csv_data.columns,
        )

        b.form_submit_button("Send", use_container_width=True)

    for msg in st.session_state.messages:
        message(msg["content"], is_user=msg["role"] == "user")

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Call LlamaAPI for response
        response = llama_api.get_response(user_prompt)  # Use the appropriate method from llama-api-server

        st.session_state.messages.append({"role": "assistant", "content": response})
        message(response)

        # Use medical diagnosis model
        user_input_df = pd.DataFrame([user_prompt])  # Replace with appropriate features
        prediction = model.predict(user_input_df)
        st.write("Medical Diagnosis Prediction:", prediction[0])

    if len(st.session_state.messages) > 1:
        st.button('Clear Chat', on_click=clear_chat)

if __name__ == '__main__':
    main()

