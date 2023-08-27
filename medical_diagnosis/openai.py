import os
import requests

# Set your OpenAI API key and base URL
openai_api_key = "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"
openai_api_base = "http://127.0.0.1:5000/v1/models"  # Update with the correct URL

def get_openai_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    payload = {
        "model": "text-ada-002",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(f"{openai_api_base}/chat_completions.create", json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Unable to get response from OpenAI"

if __name__ == '__main__':
    prompt = "hello?"  # Replace with your desired prompt
    response = get_openai_response(prompt)
    print("OpenAI Response:", response)
