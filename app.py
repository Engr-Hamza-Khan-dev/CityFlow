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
        /* Main background - clean white/light gray */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Remove padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1000px;
        }
        
        /* Header styling */
        h1 {
            color: #1f3a93 !important;
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        h2 {
            color: #1f3a93 !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            color: #2a5298 !important;
            font-weight: 600 !important;
        }
        
        /* Subtitle styling */
        .subtitle {
            color: #2a5298;
            font-size: 1.3rem;
            font-weight: 500;
            margin: 0.5rem 0;
        }
        
        .description {
            color: #555;
            font-size: 1rem;
            margin: 0.5rem 0 1.5rem 0;
        }
        
        /* Text areas and inputs */
        .stTextArea textarea {
            border: 2px solid #e0e0e0 !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
        }
        
        .stTextArea textarea:focus {
            border: 2px solid #1f3a93 !important;
            box-shadow: 0 0 0 3px rgba(31, 58, 147, 0.1) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #1f3a93 0%, #2a5298 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(31, 58, 147, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(31, 58, 147, 0.3) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: #e7f3ff !important;
            border-left: 4px solid #1f3a93 !important;
            border-radius: 4px !important;
            padding: 1rem !important;
            color: #1f3a93 !important;
        }
        
        /* Warning boxes */
        .stWarning {
            background-color: #fff3cd !important;
            border-left: 4px solid #ffc107 !important;
            border-radius: 4px !important;
            padding: 1rem !important;
            color: #856404 !important;
        }
        
        /* Error boxes */
        .stError {
            background-color: #f8d7da !important;
            border-left: 4px solid #dc3545 !important;
            border-radius: 4px !important;
            padding: 1rem !important;
            color: #721c24 !important;
        }
        
        /* Success boxes */
        .stSuccess {
            background-color: #d4edda !important;
            border-left: 4px solid #28a745 !important;
            border-radius: 4px !important;
            padding: 1rem !important;
            color: #155724 !important;
        }
        
        /* Cards/containers */
        .stContainer {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            margin: 1rem 0;
        }
        
        /* Dividers */
        hr {
            margin: 2rem 0 !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f0f2f6 !important;
            border-radius: 6px !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #e8eaef !important;
        }
        
        /* Text styling */
        p {
            color: #333;
            line-height: 1.6;
        }
        
        /* Caption text */
        .stCaption {
            color: #666 !important;
            font-size: 0.9rem !important;
        }
        
        /* Remove default margins */
        body {
            margin: 0;
            padding: 0;
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
