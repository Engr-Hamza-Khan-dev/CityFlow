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

# Professional CSS - Matching design image
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Main background - light lavender blue */
        .main {
            background: linear-gradient(180deg, #f0f4ff 0%, #e8f0ff 100%);
        }
        
        /* Container */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 900px !important;
        }
        
        /* Headers - Professional styling */
        h1 {
            color: #1e3a8a !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.2rem !important;
        }
        
        h2 {
            color: #2563eb !important;
            font-weight: 700 !important;
            font-size: 1.4rem !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            color: #2563eb !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            margin-top: 1rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Subtitle */
        .subtitle {
            color: #64748b !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            margin: 0.2rem 0 0 0 !important;
        }
        
        .description {
            color: #666 !important;
            font-size: 0.95rem !important;
            margin: 0.3rem 0 0 0 !important;
            line-height: 1.6 !important;
        }
        
        /* Connection status badge */
        .connection-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: #e0f2fe;
            color: #0369a1;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .connection-dot {
            width: 8px;
            height: 8px;
            background: #06b6d4;
            border-radius: 50%;
            display: inline-block;
        }
        
        /* Text areas */
        .stTextArea label {
            display: none !important;
        }
        
        .stTextArea textarea {
            border: 2px solid #cbd5e1 !important;
            border-radius: 10px !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            background-color: white !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            transition: all 0.3s ease !important;
            color: #1e293b !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }
        
        .stTextArea textarea:focus {
            border: 2px solid #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), 0 1px 3px rgba(0, 0, 0, 0.1) !important;
            background-color: #fafbff !important;
        }
        
        .stTextArea textarea::placeholder {
            color: #a0aec0 !important;
        }
        
        /* Buttons - Primary blue */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.7rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        }
        
        /* Info boxes - Light blue */
        .stInfo {
            background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%) !important;
            border-left: 4px solid #2563eb !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
            color: #1e40af !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 3px rgba(37, 99, 235, 0.1) !important;
            margin: 1rem 0 !important;
        }
        
        /* Warning boxes - Yellow */
        .stWarning {
            background: linear-gradient(135deg, #fef3c7 0%, #fef9e7 100%) !important;
            border-left: 4px solid #f59e0b !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
            color: #d97706 !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 3px rgba(245, 158, 11, 0.1) !important;
            margin: 1rem 0 !important;
        }
        
        /* Error boxes - Red */
        .stError {
            background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%) !important;
            border-left: 4px solid #ef4444 !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
            color: #991b1b !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 3px rgba(239, 68, 68, 0.1) !important;
            margin: 1rem 0 !important;
        }
        
        /* Dividers */
        hr {
            margin: 1.5rem 0 !important;
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
        }
        
        /* Text styling */
        p {
            color: #475569 !important;
            line-height: 1.7 !important;
            font-size: 0.95rem !important;
        }
        
        strong {
            color: #1e3a8a !important;
            font-weight: 700 !important;
        }
        
        /* Links */
        a {
            color: #2563eb !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
            font-weight: 600 !important;
        }
        
        a:hover {
            color: #1d4ed8 !important;
            text-decoration: underline !important;
        }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    if "last_response" not in st.session_state:
        st.session_state.last_response = None


def render_header_with_badge():
    """Render the CityFlow header with connection badge."""
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    
    with col1:
        st.markdown("<div style='font-size: 3rem; text-align: center;'>🏛️</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div>
                <h1 style="color: #1e40af; margin: 0; font-size: 3rem; font-weight: 900;">CityFlow</h1>
                <p style="color: #64748b; margin: 0.3rem 0 0 0; font-size: 0.95rem;">AI-Powered Permit Navigator</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="text-align: right; padding-top: 0.8rem;">
                <span class="connection-badge">
                    <span class="connection-dot"></span> Connected
                </span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<p class="description">Ask any question about government permits and get clear, step-by-step guidance based on official sources.</p>', unsafe_allow_html=True)
    st.divider()


def main():
    """Main Streamlit application."""
    # Initialize
    initialize_session_state()
    render_header_with_badge()

    # Get service
    try:
        service = get_service()
    except Exception as e:
        components.render_error(
            f"Failed to initialize service: {str(e)}. "
            "Make sure the RAG index is built: `python scripts/build_faiss_index.py`"
        )
        return

    # If no response yet, show welcome message
    if not st.session_state.last_response:
        render_welcome_message()
    else:
        # Display results if available
        render_response(st.session_state.last_response)
    
    st.divider()
    
    # Question input section at bottom (always visible)
    question = components.render_question_input(EXAMPLE_QUESTIONS)

    # Process question if submitted
    if question:
        with st.spinner("Processing your question..."):
            try:
                response = service.process_question(question)
                st.session_state.last_response = response
                st.rerun()  # Refresh to show results above
            except Exception as e:
                components.render_error(f"Error processing question: {str(e)}")
                return


def render_welcome_message():
    """Render welcome message when no question has been asked yet."""
    st.markdown("""
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            margin: 2rem 0;
        ">
            <p style="color: #2563eb; font-size: 1.1rem; font-weight: 700; margin: 0;">
                ✨ Welcome to CityFlow!
            </p>
            <p style="color: #475569; font-size: 1rem; margin: 1rem 0 0 0; line-height: 1.6;">
                Ask any question about government permits and get clear, step-by-step guidance 
                based on official sources.
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_response(response):
    """Render the CityFlow response with organized sections matching design."""
    
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
        st.markdown("""
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid #2563eb;
                margin-bottom: 1.5rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            ">
                <p style="margin: 0; color: #2563eb; font-weight: 700; font-size: 0.9rem; text-transform: uppercase;">📌 Permit Summary</p>
                <p style="margin: 1rem 0 0 0; color: #1e293b; font-weight: 500; line-height: 1.6;">{}</p>
            </div>
        """.format(response.summary), unsafe_allow_html=True)
    
    # Required steps (from Agent's checklist)
    if response.steps:
        st.markdown("<h3 style='color: #2563eb; margin-top: 2rem;'>✅ Required Steps</h3>", unsafe_allow_html=True)
        components.render_required_steps(response.steps)
    
    # Department, Cost, Processing Time in a row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="
                background: white;
                padding: 1.2rem;
                border-radius: 8px;
                border-left: 4px solid #2563eb;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
                text-align: center;
            ">
                <p style="margin: 0; color: #2563eb; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">🏢 Department/Authority</p>
                <p style="margin: 0.8rem 0 0 0; color: #1e293b; font-weight: 600;">Local Government / Health Department</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="
                background: white;
                padding: 1.2rem;
                border-radius: 8px;
                border-left: 4px solid #10b981;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
                text-align: center;
            ">
                <p style="margin: 0; color: #10b981; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">💰 Estimated Cost</p>
                <p style="margin: 0.8rem 0 0 0; color: #1e293b; font-weight: 600;">Not available in current sources</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="
                background: white;
                padding: 1.2rem;
                border-radius: 8px;
                border-left: 4px solid #f59e0b;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
                text-align: center;
            ">
                <p style="margin: 0; color: #f59e0b; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">⏱️ Processing Time</p>
                <p style="margin: 0.8rem 0 0 0; color: #1e293b; font-weight: 600;">Not available in current sources</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    # Edge case notes (from Agent)
    if response.notes:
        st.markdown("<h3 style='color: #2563eb; margin-top: 2rem;'>⚠️ Special Conditions / Edge Cases</h3>", unsafe_allow_html=True)
        for note in response.notes:
            st.warning(note)
    
    # Sources section
    st.markdown("<h3 style='color: #2563eb; margin-top: 2rem;'>📚 Official Sources</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #8b5cf6;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        ">
            <ul style="margin: 0; padding-left: 1.5rem; color: #1e293b;">
                <li style="margin: 0.5rem 0;"><strong>City of Lahore</strong> - <a href="#" style="color: #2563eb; text-decoration: none; font-weight: 600;">Restaurant Business License 🔗</a></li>
                <li style="margin: 0.5rem 0;"><strong>Punjab Food Authority</strong> - <a href="#" style="color: #2563eb; text-decoration: none; font-weight: 600;">Food Business Registration 🔗</a></li>
                <li style="margin: 0.5rem 0;"><strong>Local Government Zoning</strong> - <a href="#" style="color: #2563eb; text-decoration: none; font-weight: 600;">Zoning Regulations 🔗</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("")  # Spacing
    st.markdown("""
        <div style="
            background: #f0f4ff;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #94a3b8;
            margin-top: 1.5rem;
        ">
            <p style="margin: 0; color: #475569; font-size: 0.9rem; font-weight: 500;">
                ℹ️ CityFlow provides guidance based on the available official sources. 
                Requirements may change, so verify important information with the relevant authority.
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
