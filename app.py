import streamlit as st
import tempfile
import os
import sys
from document_processor import parse_document, chunk_text
from utils import format_eligibility_criteria, format_verdict, get_app_info
from report_generator import generate_report

# Run the Streamlit app with: streamlit run app.py
import os
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

from analyzer import (
    summarize_rfp,
    extract_eligibility_criteria,
    evaluate_company_eligibility,
    determine_verdict
)

# Set page configuration
st.set_page_config(
    page_title="RFP Eligibility Analyzer",
    page_icon="📝",
    layout="wide"
)

# Initialize model and tokenizer
from model_manager import load_model, load_tokenizer

if 'model' not in st.session_state:
    with st.spinner("Loading model..."):
        model_name = "facebook/opt-125m"  # Using smaller, open-source model
        st.session_state.model = load_model(model_name)
        st.session_state.tokenizer = load_tokenizer(model_name)
        st.session_state.model_loaded = True

# Initialize session state variables if they don't exist
if 'rfp_text' not in st.session_state:
    st.session_state.rfp_text = None
if 'company_text' not in st.session_state:
    st.session_state.company_text = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'criteria' not in st.session_state:
    st.session_state.criteria = None
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None
if 'verdict' not in st.session_state:
    st.session_state.verdict = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None
if 'report_html' not in st.session_state:
    st.session_state.report_html = None

# App title and introduction
st.title("RFP Eligibility Analyzer")
st.markdown("""
This tool helps you analyze Request for Proposals (RFPs) to determine if your company is eligible to bid.
Upload your RFP document and company profile to get started. All processing is done locally on your machine,
ensuring complete privacy of your sensitive documents.
""")

# Sidebar with information
with st.sidebar:
    st.header("Application Information")
    
    st.markdown("""
    ### RFP Analyzer
    
    This application helps you determine if your company is eligible to respond to a Request for Proposal (RFP).
    
    #### How it works:
    1. Upload your RFP document
    2. Upload your company profile
    3. Click "Analyze Documents"
    4. Review results in the Analysis tab
    5. Download a detailed report
    
    #### Supported file formats:
    - PDF (.pdf)
    - Word (.docx)
    - Text (.txt)
    """)
    
    # Display app info
    st.code(get_app_info(), language=None)
    
    # Set model as loaded for demo purposes
    st.session_state.model_loaded = True

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["Document Upload", "Analysis", "Report"])

with tab1:
    st.header("Upload Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload RFP Document")
        rfp_file = st.file_uploader("Choose an RFP document", type=['pdf', 'docx', 'txt'], key="rfp_upload")
        
        if rfp_file:
            with st.spinner("Processing RFP document..."):
                # Save uploaded file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{rfp_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(rfp_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Parse the document
                    rfp_text = parse_document(tmp_path)
                    st.session_state.rfp_text = rfp_text
                    st.success(f"✅ RFP document processed: {len(rfp_text)} characters")
                    
                    # Show sample of the text
                    with st.expander("Preview RFP Text"):
                        st.text(rfp_text[:1000] + "..." if len(rfp_text) > 1000 else rfp_text)
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                
                # Clean up the temporary file
                os.unlink(tmp_path)
    
    with col2:
        st.subheader("Upload Company Profile")
        company_file = st.file_uploader("Choose a company profile document", type=['pdf', 'docx', 'txt'], key="company_upload")
        
        if company_file:
            with st.spinner("Processing company profile..."):
                # Save uploaded file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{company_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(company_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Parse the document
                    company_text = parse_document(tmp_path)
                    st.session_state.company_text = company_text
                    st.success(f"✅ Company profile processed: {len(company_text)} characters")
                    
                    # Show sample of the text
                    with st.expander("Preview Company Profile Text"):
                        st.text(company_text[:1000] + "..." if len(company_text) > 1000 else company_text)
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                
                # Clean up the temporary file
                os.unlink(tmp_path)
    
    # Analyze button
    if st.button("Analyze Documents", disabled=not (st.session_state.model_loaded and st.session_state.rfp_text and st.session_state.company_text)):
        with st.spinner("Analyzing documents... This may take several minutes."):
            try:
                # Use simple string chunks for the mock functions
                rfp_chunks = [st.session_state.rfp_text] if st.session_state.rfp_text else []
                company_chunks = [st.session_state.company_text] if st.session_state.company_text else []
                
                # Analysis steps using real functions
                # 1. Summarize RFP
                st.session_state.summary = summarize_rfp(
                    st.session_state.model,
                    st.session_state.tokenizer,
                    rfp_chunks
                )
                
                # 2. Extract eligibility criteria
                st.session_state.criteria = extract_eligibility_criteria(
                    st.session_state.model,
                    st.session_state.tokenizer,
                    rfp_chunks
                )
                
                # 3. Evaluate company against criteria
                st.session_state.evaluation = evaluate_company_eligibility(
                    st.session_state.model,
                    st.session_state.tokenizer,
                    st.session_state.criteria,
                    company_chunks
                )
                
                # 4. Determine final verdict
                st.session_state.verdict = determine_verdict(
                    st.session_state.model,
                    st.session_state.tokenizer,
                    st.session_state.criteria,
                    st.session_state.evaluation
                )
                
                # 5. Generate report HTML
                st.session_state.report_html = generate_report(
                    st.session_state.summary,
                    st.session_state.criteria,
                    st.session_state.evaluation,
                    st.session_state.verdict
                )
                
                st.success("✅ Analysis complete! Switch to the Analysis tab to view results.")
                
                # Auto-switch to Analysis tab
                st.info("Please click on the 'Analysis' tab to view the results.")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

with tab2:
    st.header("RFP Analysis Results")
    
    if st.session_state.summary:
        st.subheader("RFP Summary")
        st.write(st.session_state.summary)
        
        st.subheader("Eligibility Criteria")
        criteria_formatted = format_eligibility_criteria(st.session_state.criteria)
        st.markdown(criteria_formatted, unsafe_allow_html=True)
        
        st.subheader("Company Evaluation")
        st.write(st.session_state.evaluation)
        
        st.subheader("Final Verdict")
        verdict_html = format_verdict(st.session_state.verdict)
        st.markdown(verdict_html, unsafe_allow_html=True)
    else:
        st.info("No analysis results yet. Please upload and analyze documents first.")

with tab3:
    st.header("Eligibility Report")
    
    if st.session_state.report_html:
        st.download_button(
            label="Download Report as HTML",
            data=st.session_state.report_html,
            file_name="rfp_eligibility_report.html",
            mime="text/html"
        )
        
        st.subheader("Report Preview")
        st.components.v1.html(st.session_state.report_html, height=600, scrolling=True)
    else:
        st.info("No report generated yet. Please complete the analysis first.")

# Footer
st.markdown("---")
st.markdown("""
**Privacy Notice**: All processing is done locally on your device. No data is sent to external servers.
""")
