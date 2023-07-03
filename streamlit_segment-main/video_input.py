import cv2
import numpy as np
import streamlit as st
from model import model

def frames(file):
    cap = cv2.VideoCapture(file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        image,intensity = model(frame,0.2)
        if image:
            

            cap.release()
            cv2.destroyAllWindows()
            return frame,intensity
            break