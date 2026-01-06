import streamlit as st
import os
from markitdown import MarkItDown
import requests

# Page Configuration
st.set_page_config(page_title="DesignSpark | Universal Doc Converter", page_icon="⚡")

def main():
    st.title("⚡ Universal File-to-Text Converter")
    st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown for LLMs or documentation.")

    # Initialize MarkItDown with custom request settings for resilience
    # Note: MarkItDown uses requests internally for URL-based conversions
    session = requests.Session()
    session.headers.update({"User-Agent": "DesignSpark-Internal-Tool/1.0"})
    
    # markitdown currently handles local files primarily; we wrap the tool logic
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
                # Save uploaded file to a temporary location to process
                with open(file_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # [1] The Engine: Process file
                with st.spinner(f"Processing {file_name}..."):
                    # We set a timeout logic context if it were a URL, 
                    # for local files markitdown is near-instant.
                    result = mid.convert(file_name)
                    md_content = result.text_content

                # [2] Interface: Instant Preview
                st.subheader(f"📄 Preview: {file_name}")
                st.text_area(
                    label="Converted Content",
                    value=md_content,
                    height=300,
                    key=f"preview_{file_name}"
                )

                # [2] Interface: Download Options
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Download as Markdown (.md)",
                        data=md_content,
                        file_name=f"{base_name}_converted.md",
                        mime="text/markdown",
                        key=f"md_{file_name}"
                    )
                
                with col2:
                    st.download_button(
                        label="📥 Download as Text (.txt)",
                        data=md_content,
                        file_name=f"{base_name}_converted.txt",
                        mime="text/plain",
                        key=f"txt_{file_name}"
                    )
                
                # Cleanup temp file
                os.remove(file_name)
                st.divider()

            except Exception as e:
                # [3] Resilience: Error Handling
                st.error(f"⚠️ Could not read {file_name}. Please check the format.")
                # Log the specific error to console for debugging
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    main()
