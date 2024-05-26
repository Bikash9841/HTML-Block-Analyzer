
'''
I have tested the LLM on google colab environment only as I am unable to provide the
hardware resources necessary to load and test the model on my local machine.

The link to the colab notebook is provided in the report.

I have only setup the API that can receive the html block as input and provides the output in the
same format as provided by the LLM on my local machine.
Although, I have also integrated the code to run LLM here in the local machine but is
commented.
'''


import threading
import uvicorn
import streamlit as st
from api import app
import requests
import subprocess


def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def start_fastapi():
    # Check if the server is already running by looking for the port
    try:
        subprocess.check_call(["lsof", "-i", ":8000"])
        print("FastAPI server is already running.")
    except subprocess.CalledProcessError:
        print("Starting FastAPI server...")
        fastapi_thread = threading.Thread(target=run_fastapi)
        fastapi_thread.daemon = True
        fastapi_thread.start()


# Streamlit app


def main():
    st.title("HTML Block Analyzer")
    # Text area for HTML input
    html_input = st.text_area("Enter the HTML block:", height=300)

    # Button to process the input
    if st.button("Analyze"):
        # Store the HTML block as a string
        data = {
            "html_content": f'''{html_input}'''
        }
        response = requests.post(
            "http://127.0.0.1:8000/process-html/", json=data)

        st.success("Process Complete")
        st.write(response.json())


if __name__ == "__main__":

    # Start FastAPI in a separate thread
    start_fastapi()

    # Start Streamlit
    main()
