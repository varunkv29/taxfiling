# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:23:14 2023

@author: varun
"""
import requests
import os
import json
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title="File Taxes", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#--LOAD ASSETS--
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")   
    
#Header Section ------
with st.container():
    st.subheader("File your 2022 taxes")
    st.title("Speed Tax")
    st.write("Easy way to file your taxes")
    st.write("Upload your W-2 form here")

#---Content --> How does website work---
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("How does it work")
        st.write("##")
        st.write(""" Easy way to fill your taxes
                  Just upload your W-2 form and confirm your dertails and tax refunds.
                  And pay to download your 1040 forms and follow the instructions to mail them to IRS""")
        st.write("[Youtube Channel >](https://www.youtube.com/watch?v=xuQF3xqInSw)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

if st.checkbox( "I have more than W2 form to file taxes"):
    st.warning("Sorry, you do not qualify to file taxes through Speed Tax. We only process W2 tax returns with standard deductions")

"""----------------------------------------------------------------------------
Upload W2 and extract Data
----------------------------------------------------------------------------""" 
# Make sure to first install the SDK using 'pip install butler-sdk'
from butler import Client

# Specify variables for use in script below
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHw2M2Q0NTY4NWE4OTU3ZDM0MzgzNDcxZDciLCJlbWFpbCI6InZhcnVua3YyOTA4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpYXQiOjE2NzQ4NjAyNzM0ODR9.4pzHJ7C3VB6zhZ6pqM9f032xI00sHLaqZG5dmXre7eU'
queue_id = 'b559a27f-d61c-4fdd-995b-e96dc41ff1b5'

#--upload file--
st.title("Upload W2 file")
uploaded_file = st.file_uploader("Choose a file", type=["pdf","png","jpeg", "jpg"])
folder_name = "uploads"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
file_name = "W2_upload.pdf"
file_path = os.path.join(folder_name, file_name)

if uploaded_file is not None:
    uploaded_file.seek(0)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.write("W2 uploaded successfully")

# Specify the path to the file you would like to process
    with st.spinner("Processing your W2 form"):    
        response = Client(api_key).extract_document(queue_id, file_path)
        data = response.to_dict()
#---W2 details extracted---
        with st.container():
            st.success("Verify if your details are correct")           
            for form_field in data["formFields"]:
                st.text_input(form_field["fieldName"], form_field["value"])  
        if st.button("Save"):
            with open("uploads/user_tax_info.txt","w") as file:
                file.write(json.loads(data))
            st.success("Saved successfully")
else:
    st.warning("Please upload your W2 form")
