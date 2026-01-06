import streamlit as st
import os
from markitdown import MarkItDown
import requests

# Page Configuration
st.set_page_config(page_title="DesignSpark | Universal Doc Converter", page_icon="⚡")

def get_file_size(file_path):
    """Returns file size in MB."""
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    return 0

def main():
    st.title("⚡ Universal File-to-Text Converter")
    st.markdown("Convert Office docs and PDFs into clean Markdown. Compare efficiency in the analytics tab.")

    # Initialize Engine
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
                        # FIXED: Ensured f-strings are correctly closed
                        st.download_button(
                            label="📥 Download .md", 
                            data=md_content, 
                            file_name=f"{base_name}_converted.md", 
                            mime="text/markdown", 
                            key=f"md_btn_{file_name}"
                        )
                    with col2:
                        st.download_button(
                            label="📥 Download .txt", 
                            data=md_content, 
                            file_name=f"{base_name}_converted.txt", 
                            mime="text/plain", 
                            key=f"txt_btn_{file_name}"
                        )

                with tab2:
                    st.write("### Efficiency Analytics")
                    data = {
                        "Version": ["Original File", "Converted Text"],
                        "Size (MB)": [f"{orig_size:.2f} MB", f"{conv_size:.2f} MB"]
                    }
                    st.table(data)
                    
                    if reduction > 0:
                        st.success(f"✨ **Efficiency Gain:** Text version is **{reduction:.1f}% smaller** than the original.")
                    else:
                        st.info("The converted version is roughly the same size as the original.")

                # Cleanup
                if os.path.exists(file_name):
                    os.remove(file_name)
                if os.path.exists(temp_md_name):
                    os.remove(temp_md_name)
                st.divider()

            except Exception as e:
                st.error(f"⚠️ Could not read {file_name}. Please check the format.")
                # Ensure local cleanup on error
                if os.path.exists(file_name): 
                    os.remove(file_name)

if __name__ == "__main__":
    main()
