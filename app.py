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
