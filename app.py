"""
CityFlow Streamlit Application

Main entry point for the CityFlow permit navigator.
"""

import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from src.ui import components
from src.services.cityflow_service import get_service
from src.config import (
    EXAMPLE_QUESTIONS,
    DISCLAIMER,
    FALLBACK_MESSAGE,
)

# Set page config FIRST before any other st commands
st.set_page_config(
    page_title="CityFlow",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
        /* Overall styling */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Main background - beautiful light gradient */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #f0f4f8 100%);
        }
        
        /* Container padding and max width */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 1100px !important;
        }
        
        /* Header styling */
        h1 {
            color: #0f3a7d !important;
            font-weight: 800 !important;
            font-size: 3rem !important;
            margin-bottom: 0.3rem !important;
            text-shadow: 0 2px 4px rgba(15, 58, 125, 0.1) !important;
            letter-spacing: -1px !important;
        }
        
        h2 {
            color: #1f5ba8 !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
            margin-top: 1rem !important;
            margin-bottom: 0.8rem !important;
            border-bottom: 3px solid #1f5ba8 !important;
            padding-bottom: 0.5rem !important;
        }
        
        h3 {
            color: #2a6fbf !important;
            font-weight: 600 !important;
            font-size: 1.3rem !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Subtitle and description */
        .subtitle {
            color: #2a6fbf !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 0.5rem 0 0.3rem 0 !important;
            letter-spacing: 0.3px !important;
        }
        
        .description {
            color: #666 !important;
            font-size: 1.1rem !important;
            margin: 0.5rem 0 2rem 0 !important;
            line-height: 1.6 !important;
        }
        
        /* Text areas */
        .stTextArea label {
            display: none !important;
        }
        
        .stTextArea {
            width: 100% !important;
        }
        
        .stTextArea textarea {
            border: 2px solid #dde8f0 !important;
            border-radius: 12px !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            background-color: #fafbfc !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            transition: all 0.3s ease !important;
            color: #333 !important;
            font-weight: 500 !important;
        }
        
        .stTextArea textarea:focus {
            border: 2px solid #1f5ba8 !important;
            box-shadow: 0 0 0 4px rgba(31, 91, 168, 0.15) !important;
            background-color: #ffffff !important;
        }
        
        .stTextArea textarea::placeholder {
            color: #999 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #1f5ba8 0%, #2a6fbf 50%, #1f5ba8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(31, 91, 168, 0.25) !important;
            letter-spacing: 0.3px !important;
            text-transform: uppercase !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 20px rgba(31, 91, 168, 0.4) !important;
            background: linear-gradient(135deg, #2a6fbf 0%, #3476d0 50%, #2a6fbf 100%) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(31, 91, 168, 0.3) !important;
        }
        
        /* Info boxes */
        .stInfo {
            background: linear-gradient(135deg, #e7f3ff 0%, #f0f7ff 100%) !important;
            border-left: 5px solid #1f5ba8 !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            color: #1f5ba8 !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 8px rgba(31, 91, 168, 0.1) !important;
        }
        
        /* Warning boxes */
        .stWarning {
            background: linear-gradient(135deg, #fff9e6 0%, #fffbf0 100%) !important;
            border-left: 5px solid #ff9800 !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            color: #e65100 !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 8px rgba(255, 152, 0, 0.1) !important;
        }
        
        /* Error boxes */
        .stError {
            background: linear-gradient(135deg, #ffebee 0%, #fff5f5 100%) !important;
            border-left: 5px solid #dc3545 !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            color: #b71c1c !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 8px rgba(220, 53, 69, 0.1) !important;
        }
        
        /* Success boxes */
        .stSuccess {
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%) !important;
            border-left: 5px solid #28a745 !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            color: #1b5e20 !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1) !important;
        }
        
        /* Dividers */
        hr {
            margin: 1.5rem 0 !important;
            border: none !important;
            height: 2px !important;
            background: linear-gradient(90deg, transparent, #dde8f0, transparent) !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f5f9fd 0%, #f0f6fc 100%) !important;
            border-radius: 10px !important;
            border: 1px solid #dde8f0 !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #eef5fb 0%, #e8f2fa 100%) !important;
            border-color: #1f5ba8 !important;
            box-shadow: 0 2px 8px rgba(31, 91, 168, 0.1) !important;
        }
        
        /* Text styling */
        p {
            color: #333 !important;
            line-height: 1.8 !important;
            font-size: 1rem !important;
        }
        
        /* Caption text */
        .stCaption {
            color: #888 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }
        
        /* Markdown bold text */
        strong {
            color: #1f5ba8 !important;
            font-weight: 700 !important;
        }
        
        /* Links */
        a {
            color: #1f5ba8 !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
            border-bottom: 2px solid transparent !important;
        }
        
        a:hover {
            color: #2a6fbf !important;
            border-bottom-color: #2a6fbf !important;
        }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    if "processing" not in st.session_state:
        st.session_state.processing = False


def main():
    """Main Streamlit application."""
    # Initialize
    initialize_session_state()
    components.render_header()

    # Get service
    try:
        service = get_service()
    except Exception as e:
        components.render_error(
            f"Failed to initialize service: {str(e)}. "
            "Make sure the RAG index is built: `python scripts/build_faiss_index.py`"
        )
        return

    # Question input section
    st.divider()
    question = components.render_question_input(EXAMPLE_QUESTIONS)

    # Process question if submitted
    if question:
        st.session_state.processing = True
        
        with st.spinner("Processing your question..."):
            try:
                response = service.process_question(question)
                st.session_state.last_response = response
            except Exception as e:
                components.render_error(f"Error processing question: {str(e)}")
                st.session_state.processing = False
                return

        st.session_state.processing = False
    
    # Display results if available
    if st.session_state.last_response:
        st.divider()
        render_response(st.session_state.last_response)


def render_response(response):
    """Render the CityFlow response with Agent-generated checklist."""
    
    # Fallback state
    if response.is_fallback:
        components.render_fallback()
        if response.notes:
            st.subheader("📝 Notes")
            for note in response.notes:
                st.info(note)
        return
    
    # Summary
    if response.summary:
        components.render_permit_summary(response.summary)
    
    # Required steps (from Agent's checklist)
    if response.steps:
        components.render_required_steps(response.steps)
    
    # Edge case notes (from Agent)
    if response.notes:
        components.render_edge_cases(response.notes)


if __name__ == "__main__":
    main()
