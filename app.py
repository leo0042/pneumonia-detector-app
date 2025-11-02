import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

@st.cache_resource
def load_my_model():
    model = load_model('pneumonia_model.keras')
    return model

model = load_my_model()

st.title('Pneumonia Detection from Chest X-Ray Images')
st.write("Upload a chest X-ray image and the model will predict if it's 'NORMAL' or 'PNEUMONIA'.")

uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded X-ray Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    image = image.resize((128, 128), Image.LANCZOS)
    image = image.convert('RGB')

    img_array = np.array(image)

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    score = prediction[0][0]


    # Display the result
    if score > 0.5:
        st.error(f"**Prediction: PNEUMONIA** (Confidence: {score * 100:.2f}%)")
    else:
        st.success(f"**Prediction: NORMAL** (Confidence: {(1 - score) * 100:.2f}%)")
