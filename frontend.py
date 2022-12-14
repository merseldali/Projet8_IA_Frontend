import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from PIL import Image
import io

st.title('DeepLabV3 image segmentation')

# fastapi endpoint
url = 'https://p8ai-api.herokuapp.com'
endpoint = '/segmentation'

st.write('''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in Keras.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation.''') # description and instructions

image = st.file_uploader('insert image')  # image upload widget


def process(image, server_url: str):

    m = MultipartEncoder(
        fields={'file': ('filename', image, 'image/png')}
        )

    r = requests.post(server_url,
                      data=m,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)

    return r


if st.button('Get segmentation map'):

    if image == None:
        st.write("Insert an image!")  # handle case with no image
    else:
        segments = process(image, url+endpoint)
        segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
        
        img = Image.open(io.BytesIO(image.read()))
        img = img.convert('RGB')
        img = img.resize((1024,1024), Image.NEAREST)

        st.image([img, segmented_image], width=300)  # output dyptich
