import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# read API key securely
genai.configure(api_key=st.secrets["AIzaSyCrePeWTnPC7_XVh6PI55QKqOYwwo_NhgM"])

model = genai.GenerativeModel("gemini-pro")

st.title("🌿 Plant AI Assistant")

st.write("Upload plant datasets or images and ask AI questions.")

# upload dataset
dataset = st.file_uploader("Upload Plant Dataset (CSV)", type=["csv"])

if dataset:
    df = pd.read_csv(dataset)
    st.write("Dataset Preview")
    st.dataframe(df.head())

# upload image
image_file = st.file_uploader("Upload Plant Image", type=["jpg","png"])

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Plant Image")

# ask AI
question = st.text_input("Ask AI about plant stress or dataset")

if st.button("Generate Answer"):

    prompt = f"""
    You are a plant scientist AI.
    Answer this question clearly:

    {question}
    """

    response = model.generate_content(prompt)

    st.subheader("AI Response")
    st.write(response.text)