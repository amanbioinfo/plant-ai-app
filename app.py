import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

API_KEY = "AIzaSyCrePeWTnPC7_XVh6PI55QKqOYwwo_NhgM"

client = genai.Client(api_key=API_KEY)

st.title("🌿 Plant AI Assistant")

# Upload dataset
dataset = st.file_uploader("Upload Plant Dataset (CSV)", type=["csv"])

if dataset:
    df = pd.read_csv(dataset)
    st.dataframe(df.head())

# Upload image
image_file = st.file_uploader("Upload Plant Image", type=["jpg","jpeg","png"])

image_bytes = None

if image_file:
    image = Image.open(image_file)
    st.image(image)
    image_bytes = image_file.getvalue()

question = st.text_input("Ask AI about plant stress")

if st.button("Generate Answer"):

    if question:

        if image_bytes:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {"text": question},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_bytes
                        }
                    }
                ]
            )

        else:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=question
            )

        st.write(response.text)