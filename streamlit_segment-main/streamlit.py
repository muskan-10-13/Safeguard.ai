import cv2
import streamlit as st
from video_input import frames
import matplotlib.pyplot as plt
import requests
from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)



url = 'http://ec2-43-204-130-153.ap-south-1.compute.amazonaws.com:5000/data'

st.header("Flood intensity")
with st.form(key="form1"):
    st.subheader("Upload a real time flood scenario")
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
    if uploaded_file is not None:
        with open("my_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
    col1, col2 = st.columns(2)
    latitude=col1.text_input("Enter a Latitude")
    longitude=col2.text_input("Enter a Longitude")
    submit_button = st.form_submit_button(label="Submit")
if submit_button:    
    image,intensity = frames("my_video.mp4")
    filename = 'frame.jpg'
    cv2.imwrite(filename, image)
    st.write(intensity)
    st.image(filename)
    if intensity>0.30:
        str1 = str(intensity)
        payload = {
        "intensity": str1,
        "latitude": latitude,
        "longitude": longitude
        }
        
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("POST request successful!")
            message = client.messages.create(
                    body='flood detected',
                      from_='+15417038090',
            to='+918189005612')

        else:
            st.error("Error sending POST request.")
            st.write(response.status_code)
            st.write(response.reason)

        

       
        
    print(intensity)