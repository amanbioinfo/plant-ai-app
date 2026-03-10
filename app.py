import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# API key
API_KEY = "AIzaSyCrePeWTnPC7_XVh6PI55QKqOYwwo_NhgM"

client = genai.Client(api_key=API_KEY)

st.title("🌿 Plant AI Assistant")

st.write("Upload plant datasets or images and ask AI questions.")

# upload dataset
dataset = st.file_uploader("Upload Plant Dataset (CSV)", type=["csv"])

if dataset:
    df = pd.read_csv(dataset)
    st.write("Dataset Preview")
    st.dataframe(df.head())

# upload image
image_file = st.file_uploader("Upload Plant Image", type=["jpg","png","jpeg"])

image = None

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Plant Image")

# ask AI
question = st.text_input("Ask AI about plant stress or dataset")

if st.button("Generate Answer"):

    if question:

        if image:

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[question, image]
            )

        else:

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=question
            )

        st.subheader("AI Response")
        st.write(response.text)