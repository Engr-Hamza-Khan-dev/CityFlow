"""Reusable UI components for CityFlow Streamlit app."""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_header():
    """Render the CityFlow header."""
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.markdown("### 🏛️")
    with col2:
        st.markdown("<h1>CityFlow</h1>", unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle">AI-Powered Permit Navigator</p>', unsafe_allow_html=True)
    st.markdown('<p class="description">Understand government permits in plain English.</p>', unsafe_allow_html=True)
    st.divider()


def render_question_input(example_questions: List[str]) -> Optional[str]:
    """Render the question input section and return the question or None."""
    
    st.markdown("")  # Spacing
    
    # Get current value from session state
    current_question = st.session_state.get("user_question", "")
    
    question = st.text_area(
        label="question_input_label",
        value=current_question,
        height=100,
        placeholder="Type your question here...",
        key="question_textarea",
        label_visibility="collapsed"
    )
    
    # Store in session state whenever it changes
    st.session_state.user_question = question
    
    # Beautiful search button
    col1, col2, col3 = st.columns([0.65, 0.25, 0.1])
    with col2:
        search_clicked = st.button("🔍 Send", use_container_width=True, type="primary", key="search_btn")
    
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
    st.info(summary)


def render_required_steps(steps: List[Dict[str, Any]]):
    """Render the required steps checklist with details from Member 2's agent."""
    if not steps:
        return
    
    for idx, item in enumerate(steps, 1):
        step_num = item.get("step", idx)
        requirement = item.get("requirement", "")
        department = item.get("department")
        cost = item.get("cost")
        timeline = item.get("timeline")
        source = item.get("source", "Unknown")
        
        # Beautiful step card
        st.markdown(f"""
            <div style="
                background: white;
                padding: 1.2rem;
                border-radius: 8px;
                border-left: 4px solid #2563eb;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            ">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="
                        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
                        color: white;
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        font-size: 1.2rem;
                        flex-shrink: 0;
                    ">
                        {step_num}
                    </div>
                    <p style="margin: 0; color: #1e293b; font-weight: 700; font-size: 1rem;">{requirement}</p>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.8rem; margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        if department:
            st.markdown(f"""
                    <div style="
                        background: #f0f9ff;
                        padding: 0.8rem;
                        border-radius: 6px;
                        border-left: 3px solid #2563eb;
                    ">
                        <p style="margin: 0; color: #2563eb; font-weight: 700; font-size: 0.75rem; text-transform: uppercase;">🏢 Dept</p>
                        <p style="margin: 0.5rem 0 0 0; color: #1e293b; font-weight: 600; font-size: 0.9rem;">{department}</p>
                    </div>
            """, unsafe_allow_html=True)
        
        if cost:
            st.markdown(f"""
                    <div style="
                        background: #f0fdf4;
                        padding: 0.8rem;
                        border-radius: 6px;
                        border-left: 3px solid #10b981;
                    ">
                        <p style="margin: 0; color: #10b981; font-weight: 700; font-size: 0.75rem; text-transform: uppercase;">💰 Cost</p>
                        <p style="margin: 0.5rem 0 0 0; color: #1e293b; font-weight: 600; font-size: 0.9rem;">{cost}</p>
                    </div>
            """, unsafe_allow_html=True)
        
        if timeline:
            st.markdown(f"""
                    <div style="
                        background: #fef3c7;
                        padding: 0.8rem;
                        border-radius: 6px;
                        border-left: 3px solid #f59e0b;
                    ">
                        <p style="margin: 0; color: #f59e0b; font-weight: 700; font-size: 0.75rem; text-transform: uppercase;">⏱️ Time</p>
                        <p style="margin: 0.5rem 0 0 0; color: #1e293b; font-weight: 600; font-size: 0.9rem;">{timeline}</p>
                    </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)


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
        st.warning(note)


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
    st.error(
        "⚠️ **Limited Information Available**\n\n"
        "I couldn't find enough reliable information in the available official sources "
        "to answer this confidently.\n\n"
        "**Please verify with the relevant government authority for accurate information.**"
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
