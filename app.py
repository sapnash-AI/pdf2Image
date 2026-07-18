import io
import os
import zipfile
import streamlit as st
from pdf2image import convert_from_bytes

# Set up page config
st.set_page_config(page_title="PWS-App-PDF to JPEG Converter", page_icon="📄", layout="centered")

st.title("📄 PDF to JPEG Converter")
st.write("Upload a multi-page PDF, convert all pages to JPEGs, and download them together in a single ZIP folder.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Read the file bytes
    file_bytes = uploaded_file.read()
    
    st.info("Converting PDF pages to images... This might take a moment for large files.")
    
    try:
        # Convert PDF bytes directly to a list of PIL Images
        # You can adjust 'dpi' for higher/lower quality (200 is a good baseline balance)
        images = convert_from_bytes(file_bytes, dpi=200)
        
        num_pages = len(images)
        st.success(f"Successfully converted {num_pages} page(s)!")
        
        # Create an in-memory byte stream to hold the ZIP archive
        zip_buffer = io.BytesIO()
        
        # Write images into the zip archive
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Extract base filename without extension
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            for i, image in enumerate(images):
                # Save individual PIL image to an in-memory byte stream as JPEG
                img_buffer = io.BytesIO()
                image.save(img_buffer, format="JPEG", quality=90)
                img_buffer.seek(0)
                
                # Name each image sequentially inside the ZIP
                img_filename = f"{base_name}_page_{i+1}.jpg"
                zip_file.writestr(img_filename, img_buffer.getvalue())
        
        # Rewind the zip buffer pointer to the beginning so it can be read completely
        zip_buffer.seek(0)
        
        # Generate clean download file name
        download_filename = f"{base_name}_images.zip"
        
        # Visual separator before the download button
        st.divider()
        
        # Centered download button
        st.download_button(
            label="📥 Download All Images (ZIP)",
            data=zip_buffer,
            file_name=download_filename,
            mime="application/zip",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        st.warning("Make sure 'poppler' is installed on your system and added to your system path environment.")
