import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Gemini API key
API_KEY = "AIzaSyCrePeWTnPC7_XVh6PI55QKqOYwwo_NhgM"

# Initialize client
client = genai.Client(api_key=API_KEY)

st.title("🌿 Plant AI Assistant")
st.write("Upload plant datasets or images and ask AI questions.")

# Upload dataset
dataset = st.file_uploader("Upload Plant Dataset (CSV)", type=["csv"])

if dataset:
    df = pd.read_csv(dataset)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# Upload image
image_file = st.file_uploader("Upload Plant Image", type=["jpg", "jpeg", "png"])

image_bytes = None

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Plant Image")
    image_bytes = image_file.getvalue()

# Ask question
question = st.text_input("Ask AI about plant stress")

if st.button("Generate Answer"):

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    try:

        if image_bytes:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": question},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_bytes
                                }
                            }
                        ],
                    }
                ],
                config={"temperature": 0.3}
            )

        else:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": question}]
                    }
                ],
                config={"temperature": 0.3}
            )

        st.subheader("AI Response")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error occurred: {e}")