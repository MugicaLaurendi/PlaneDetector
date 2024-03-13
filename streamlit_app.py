import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import requests


from requests_toolbelt.multipart.encoder import MultipartEncoder

backend = "http://127.0.0.1:8000/planedetector"


st.set_page_config(layout="wide", page_title="Plane Detector")

st.write("## Plane Detector")
st.write(
    ":plane: Try uploading a satellite image to detect planes. Full quality images can be downloaded from the sidebar."
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
    image = upload
    #image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # image transformation


    def process(image, server_url: str):

        m = MultipartEncoder(fields={"file": ("filename", image, "image/png")})

        r = requests.post(
            server_url, data=m, headers={"Content-Type": m.content_type}
        )

        return r


    segments = process(image, backend)
    image_predicted = Image.open(BytesIO(segments.content)).convert("RGB")

    # end image transformation

    #image_predicted = Image.open('detector.png')

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
#    fix_image("./not_plane.jpg")
