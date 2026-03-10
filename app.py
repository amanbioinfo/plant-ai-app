import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Gemini API key
API_KEY = "AIzaSyCrePeWTnPC7_XVh6PI55QKqOYwwo_NhgM"

client = genai.Client(api_key=API_KEY)

st.title("🌿 Plant AI Assistant")
st.write("Upload plant datasets or images and ask AI questions.")

# Upload dataset
dataset = st.file_uploader("Upload Plant Dataset (CSV)", type=["csv"])

if dataset:
    df = pd.read_csv(dataset)
    st.write("Dataset Preview")
    st.dataframe(df.head())

# Upload image
image_file = st.file_uploader("Upload Plant Image", type=["jpg","jpeg","png"])

image_bytes = None

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Plant Image")

    # Convert uploaded file to bytes
    image_bytes = image_file.getvalue()

# Ask AI
question = st.text_input("Ask AI about plant stress or dataset")

if st.button("Generate Answer") and question:

    try:

        if image_bytes:

            response = client.models.generate_content(
                model="gemini-1.5-flash",
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
                model="gemini-1.5-flash",
                contents=question
            )

        st.subheader("AI Response")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error occurred: {e}")