import streamlit as st
from PIL import Image
import torch
from ultralytics import YOLO
import numpy as np

# Force CPU for everything
torch.device("cpu")
model = YOLO("C:/Users/Harsh/Desktop/PD3/models/best.pt")
model.to("cpu")

# Streamlit UI
st.set_page_config(page_title="Airborne Threat Detection", layout="centered")
st.title("✈️ Airborne Threat Detection System")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Threats"):
        with st.spinner("Detecting..."):
            # Convert PIL image to numpy array
            image_np = np.array(image)

            # Run prediction (on CPU)
            results = model.predict(image_np, conf=0.3, device="cpu")

            # Get the annotated result image
            result_img = results[0].plot()

        st.image(result_img, caption="Detection Result", use_column_width=True)

        # Show detected labels
        boxes = results[0].boxes
        if boxes:
            labels = boxes.cls.tolist()
            class_map = model.names
            detected = [class_map[int(label)] for label in labels]
            st.success(f"Detected: {', '.join(set(detected))}")
        else:
            st.warning("No threats detected.")
