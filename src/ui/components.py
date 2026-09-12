"""Reusable UI components for CityFlow Streamlit app."""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_header():
    """Render the CityFlow header."""
    st.set_page_config(
        page_title="CityFlow",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.write("🏛️")
    with col2:
        st.title("CityFlow")
    
    st.markdown("### AI-Powered Permit Navigator")
    st.markdown("Understand government permits in plain English.")
    st.divider()


def render_question_input(example_questions: List[str]) -> Optional[str]:
    """Render the question input section and return the question or None."""
    st.subheader("Ask Your Question")
    
    # Quick example buttons
    st.markdown("**Example questions:**")
    cols = st.columns(len(example_questions))
    for i, example in enumerate(example_questions):
        with cols[i % len(cols)]:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state.user_question = example
    
    # Main question input
    question = st.text_area(
        "What would you like to know about permits?",
        value=st.session_state.get("user_question", ""),
        height=100,
        placeholder="e.g., What permits do I need to open a restaurant?",
        key="question_input",
    )
    
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        search_clicked = st.button("🔍 Search", use_container_width=True, type="primary")
    
    if search_clicked and question.strip():
        return question.strip()
    
    return None


def render_loading_state():
    """Render loading animation."""
    with st.spinner("Processing your question..."):
        st.info(
            "🔄 Analyzing your request...\n\n"
            "📚 Searching official documents...\n\n"
            "📋 Preparing your permit information..."
        )


def render_permit_summary(summary: str):
    """Render the permit summary section."""
    st.subheader("📋 Permit Summary")
    st.markdown(summary)


def render_required_steps(steps: List[Dict[str, Any]]):
    """Render the required steps checklist with details from Member 2's agent."""
    if not steps:
        return
    
    st.subheader("✅ Required Steps")
    
    for item in steps:
        step_num = item.get("step", "")
        requirement = item.get("requirement", "")
        department = item.get("department")
        cost = item.get("cost")
        timeline = item.get("timeline")
        source = item.get("source", "Unknown")
        
        # Main requirement with step number
        st.markdown(f"**Step {step_num}.** {requirement}")
        
        # Details in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if department:
                st.caption(f"🏢 {department}")
        
        with col2:
            if cost:
                st.caption(f"💰 {cost}")
        
        with col3:
            if timeline:
                st.caption(f"⏱️ {timeline}")
        
        # Source citation
        st.caption(f"📚 Source: *{source}*")
        st.divider()


def render_required_documents(documents: List[str]):
    """Render the required documents section."""
    if not documents:
        return
    
    st.subheader("📄 Required Documents")
    for doc in documents:
        st.markdown(f"• {doc}")


def render_edge_cases(notes: List[str]):
    """Render edge case notes from the agent."""
    if not notes:
        return
    
    st.subheader("⚠️ Important Notes")
    for note in notes:
        st.info(note)


def render_permit_details(
    department: Optional[str] = None,
    cost: Optional[str] = None,
    processing_time: Optional[str] = None,
    edge_cases: Optional[List[str]] = None,
):
    """Render permit details in a compact layout (deprecated - use individual sections)."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏢 Department")
        if department:
            st.write(department)
        else:
            st.write("*Not available in sources*")
    
    with col2:
        st.subheader("💰 Estimated Cost")
        if cost:
            st.write(cost)
        else:
            st.write("*Not available in sources*")
    
    with col3:
        st.subheader("⏱️ Processing Time")
        if processing_time:
            st.write(processing_time)
        else:
            st.write("*Not available in sources*")
    
    # Edge cases section
    if edge_cases and len(edge_cases) > 0:
        st.subheader("⚠️ Special Conditions / Edge Cases")
        for case in edge_cases:
            st.markdown(f"• {case}")


def render_sources(sources: List[Dict[str, Any]]):
    """Render the official sources section (deprecated - sources now embedded in checklist)."""
    if not sources:
        return
    
    st.subheader("📚 Official Sources")
    st.markdown("*References used to provide this information:*")
    
    for i, source in enumerate(sources, start=1):
        with st.expander(f"Source {i}: {source.get('source', 'Unknown')}"):
            if source.get("text"):
                st.markdown(source["text"])
            if source.get("metadata"):
                st.caption(f"**Evidence ID:** `{source['metadata'].get('evidence_id', 'N/A')}`")


def render_fallback():
    """Render fallback when confidence is low."""
    st.warning(
        "⚠️ **Limited Information Available**\n\n"
        "I couldn't find enough reliable information in the available official sources "
        "to answer this confidently.\n\n"
        "Please verify with the relevant government authority for accurate information."
    )


def render_error(error_message: str):
    """Render error message."""
    st.error(f"❌ **Error:** {error_message}")


def render_empty_state():
    """Render empty state on first load."""
    st.info("💡 Ask a permit-related question to get started.")


def render_disclaimer():
    """Render the disclaimer footer."""
    st.divider()
    st.caption(
        "📌 **Disclaimer:** CityFlow provides guidance based on available official sources. "
        "Requirements may change, so verify important information with the relevant authority."
    )
