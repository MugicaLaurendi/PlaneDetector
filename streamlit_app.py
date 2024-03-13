import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import requests

import numpy as np
import pandas as pd
import cv2, os, re
import matplotlib.image
import matplotlib.pyplot as plt

from Detector import *

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # image transformation

    model =  load_model('plane-model.h5')

    detector = Detector(image, model)

    image = detector.to_input(image)
    roi = detector.find_roi(image)
    rois, rois_locations = detector.normalise_roi(image, roi)
    predictions = detector.classification_on_roi(rois, model)
    image_predicted = detector.insert_roi_classed_on_image(image, predictions, rois_locations)
    detector.to_output(image_predicted)


    # end image transformation

    image_predicted = Image.open('detector.png')

    col2.write("Fixed Image :wrench:")
    col2.image(image_predicted)

    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download image_predicted", convert_image(image_predicted), "image_predicted.png", "image/png")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload)
#else:
#    fix_image("./zebra.jpg")
