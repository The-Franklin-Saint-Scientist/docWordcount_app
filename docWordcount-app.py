import streamlit as st
import docx
import PyPDF2
import time
import logging

# Configure logging to output to terminal with a time stamp.
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# displays name of webapp
st.title("ESSAY WORD COUNT VALIDATOR!")
st.write("Upload your essay docx, to extract its text and count the words.")
st.subheader("Words should be between 250 and 3000.")

# Function to read the uploaded file
def read_file(uploaded_file):
    text = ""
    if uploaded_file.type == "text/plain":
        # For text files, reads as bytes and converts to text
        text = uploaded_file.getvalue().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # For DOCX files, extract text using the docx library
        document = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in document.paragraphs])
    elif uploaded_file.type == "application/pdf":
        # For PDF files, extract text using PyPDF2 library
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    else:
        st.error("File is not supported!")
        logging.error("Unsupported file type: %s", uploaded_file.type)
    return text

# File uploader widget to upload a document file
uploaded_file = st.file_uploader("Upload a file", type=["txt", "docx", "pdf"])

if uploaded_file is not None:
    logging.info("User uploaded file with type: %s", uploaded_file.type)
    if st.button("Submit"):
        logging.info("Submit button clicked")
        # Simulate a progress bar for file upload and processing
        with st.spinner("Processing your document..."):
            progress = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.02)  # Adjust sleep time as needed for the simulation
                progress.progress(percent_complete + 1)
        text = read_file(uploaded_file)
        words = text.split()
        word_count = len(words)
        logging.info("Extracted word count: %d", word_count)
        
        # Word count conditional validation and handling with colored messages
        if word_count < 250:
            st.markdown("<span style='color:red;'>Submission is not allowed due to insufficient words.</span>", unsafe_allow_html=True)
            logging.info("Submission rejected: insufficient words (word_count=%d).", word_count)
        elif word_count > 3000:
            st.markdown("<span style='color:red;'>Document exceeds word limit.</span>", unsafe_allow_html=True)
            logging.info("Submission rejected: document exceeds word limit (word_count=%d).", word_count)
        else:
            st.markdown("<span style='color:green;'>Document accepted and submitted successfully.</span>", unsafe_allow_html=True)
            st.subheader("Word Count")
            st.write(f"Total words: {word_count}")
            logging.info("Submission accepted: Document processed successfully (word_count=%d).", word_count)
