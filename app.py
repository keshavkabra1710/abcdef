import streamlit as st
import os
from markitdown import MarkItDown
import requests

# Page Configuration
st.set_page_config(page_title="DesignSpark | Universal Doc Converter", page_icon="⚡")

def get_file_size(file_path):
    """Returns file size in MB."""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def main():
    st.title("⚡ Universal File-to-Text Converter")
    st.markdown("Convert Office docs and PDFs into clean Markdown. Compare efficiency in the analytics tab.")

    mid = MarkItDown()

    # [2] Interface: Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            base_name = os.path.splitext(file_name)[0]
            
            try:
                # Save uploaded file to get accurate original size
                with open(file_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                orig_size = get_file_size(file_name)

                with st.spinner(f"Processing {file_name}..."):
                    result = mid.convert(file_name)
                    md_content = result.text_content
                
                # Create temporary converted file to calculate size
                temp_md_name = f"{base_name}_temp.md"
                with open(temp_md_name, "w", encoding="utf-8") as f:
                    f.write(md_content)
                
                conv_size = get_file_size(temp_md_name)
                
                # Calculate percentage reduction
                reduction = ((orig_size - conv_size) / orig_size) * 100 if orig_size > 0 else 0

                # UI Layout with Tabs
                st.subheader(f"📄 File: {file_name}")
                tab1, tab2 = st.tabs(["🔍 Instant Preview", "📊 File Size Comparison"])

                with tab1:
                    st.text_area(
                        label="Converted Content",
                        value=md_content,
                        height=300,
                        key=f"preview_{file_name}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button("📥 Download .md", md_content, f"{base_name}_converted.md", "text/markdown", key=f"md_{
