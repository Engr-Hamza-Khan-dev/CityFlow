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
    st.subheader("Ask Your Question")
    
    st.markdown("")  # Spacing
    
    # Main question input
    st.markdown("**✍️ Your Question:**")
    
    # Get current value from session state
    current_question = st.session_state.get("user_question", "")
    
    question = st.text_area(
        label="question_input_label",
        value=current_question,
        height=120,
        placeholder="e.g., What permits do I need to open a restaurant?",
        key="question_textarea",
        label_visibility="collapsed"
    )
    
    # Store in session state whenever it changes
    st.session_state.user_question = question
    
    # Beautiful search button
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col1:
        search_clicked = st.button("🔍 Search", use_container_width=True, type="primary", key="search_btn")
    
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
    
    st.subheader("✅ Required Steps")
    
    for idx, item in enumerate(steps, 1):
        step_num = item.get("step", idx)
        requirement = item.get("requirement", "")
        department = item.get("department")
        cost = item.get("cost")
        timeline = item.get("timeline")
        source = item.get("source", "Unknown")
        
        # Beautiful step card with number badge
        with st.container():
            col1, col2 = st.columns([0.08, 0.92])
            
            with col1:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1f5ba8 0%, #2a6fbf 100%);
                        color: white;
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        font-size: 1.5rem;
                        box-shadow: 0 4px 12px rgba(31, 91, 168, 0.3);
                    ">
                        {step_num}
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{requirement}**")
            
            # Details in beautiful columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if department:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #e7f3ff 0%, #f0f7ff 100%);
                            padding: 0.8rem;
                            border-radius: 8px;
                            border-left: 4px solid #1f5ba8;
                        ">
                            <p style="margin: 0; color: #1f5ba8; font-weight: 600; font-size: 0.85rem;">🏢 DEPARTMENT</p>
                            <p style="margin: 0.5rem 0 0 0; color: #333; font-weight: 600;">{department}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if cost:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
                            padding: 0.8rem;
                            border-radius: 8px;
                            border-left: 4px solid #28a745;
                        ">
                            <p style="margin: 0; color: #28a745; font-weight: 600; font-size: 0.85rem;">💰 COST</p>
                            <p style="margin: 0.5rem 0 0 0; color: #333; font-weight: 600;">{cost}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                if timeline:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #fff9e6 0%, #fffbf0 100%);
                            padding: 0.8rem;
                            border-radius: 8px;
                            border-left: 4px solid #ff9800;
                        ">
                            <p style="margin: 0; color: #ff9800; font-weight: 600; font-size: 0.85rem;">⏱️ TIMELINE</p>
                            <p style="margin: 0.5rem 0 0 0; color: #333; font-weight: 600;">{timeline}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Source citation in a beautiful box
            st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #f5f9fd 0%, #f0f6fc 100%);
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                    border: 1px solid #dde8f0;
                ">
                    <p style="margin: 0; color: #1f5ba8; font-weight: 600; font-size: 0.9rem;">📚 SOURCE: <span style="color: #666;">{source}</span></p>
                </div>
            """, unsafe_allow_html=True)
            
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
