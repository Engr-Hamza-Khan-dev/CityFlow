"""
CityFlow Streamlit Application

Chat-based interface for permit navigator.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from src.services.cityflow_service import get_service
from src.config import EXAMPLE_QUESTIONS

# Set page config
st.set_page_config(
    page_title="CityFlow",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chat-style UI CSS
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f5f7fa;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0f2f7 0%, #e8ecf3 100%);
        }
        
        /* Sidebar header */
        .sidebar-header {
            text-align: center;
            padding: 1.5rem 1rem;
            border-bottom: 1px solid #e0e6f0;
            margin-bottom: 2rem;
        }
        
        .sidebar-logo-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #1f5ba8;
        }
        
        .sidebar-subtitle {
            font-size: 0.75rem;
            color: #888;
            margin-top: 0.25rem;
        }
        
        /* Sidebar nav items */
        .nav-section {
            padding: 0 1rem;
            margin-bottom: 2rem;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
            color: #333;
            background: white;
            border: 1px solid transparent;
        }
        
        .nav-item:hover {
            background: rgba(31, 91, 168, 0.08);
            color: #1f5ba8;
            border-color: rgba(31, 91, 168, 0.2);
        }
        
        .nav-item.active {
            background: rgba(31, 91, 168, 0.12);
            color: #1f5ba8;
            border-color: #1f5ba8;
        }
        
        /* Main content */
        .main {
            background-color: #f5f7fa;
        }
        
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1400px;
        }
        
        /* Chat section */
        .chat-section {
            margin-right: 320px;
        }
        
        /* Chat header */
        .chat-header {
            margin-bottom: 1.5rem;
        }
        
        .chat-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1f5ba8;
            margin: 0 0 0.3rem 0;
        }
        
        .chat-subtitle {
            font-size: 0.95rem;
            color: #777;
            margin: 0;
        }
        
        /* Chat messages */
        .chat-messages {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-bottom: 2rem;
            min-height: 300px;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }
        
        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-messages::-webkit-scrollbar-track {
            background: #f0f0f0;
            border-radius: 3px;
        }
        
        .chat-messages::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 3px;
        }
        
        .message-container {
            display: flex;
            gap: 0.75rem;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message-container.user {
            justify-content: flex-end;
        }
        
        .message-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: 700;
            flex-shrink: 0;
        }
        
        .message-container.user .message-avatar {
            background: #e3e8f3;
            color: #1f5ba8;
        }
        
        .message-container.assistant .message-avatar {
            background: linear-gradient(135deg, #1f5ba8 0%, #2a6fbf 100%);
            color: white;
        }
        
        .message-content {
            max-width: 70%;
        }
        
        .message-bubble {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .message-container.user .message-bubble {
            background: linear-gradient(135deg, #1f5ba8 0%, #2a6fbf 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message-container.assistant .message-bubble {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        
        .message-time {
            font-size: 0.75rem;
            color: #999;
            margin-top: 0.25rem;
            text-align: right;
        }
        
        .message-container.user .message-time {
            text-align: right;
        }
        
        /* Example questions */
        .example-questions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin: 1.5rem 0;
        }
        
        .example-btn {
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: white;
            color: #333;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            text-align: center;
            transition: all 0.2s ease;
            line-height: 1.4;
        }
        
        .example-btn:hover {
            background: #f0f5fb;
            border-color: #1f5ba8;
            color: #1f5ba8;
        }
        
        /* Chat input */
        .chat-input-wrapper {
            display: flex;
            gap: 0.75rem;
            padding: 1rem;
            background: white;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            align-items: flex-end;
        }
        
        /* Right sidebar */
        .right-sidebar {
            position: fixed;
            right: 0;
            top: 60px;
            width: 300px;
            padding: 1.5rem;
            background: white;
            height: calc(100vh - 60px);
            overflow-y: auto;
            border-left: 1px solid #e0e0e0;
        }
        
        .sidebar-panel {
            margin-bottom: 1.5rem;
        }
        
        .panel-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #1f5ba8;
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .panel-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: #555;
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }
        
        .panel-item:last-child {
            margin-bottom: 0;
        }
        
        .check-mark {
            color: #17c65f;
            font-weight: 700;
        }
        
        .popular-item {
            padding: 0.75rem 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
            color: #333;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .popular-item:last-child {
            border-bottom: none;
        }
        
        .popular-item:hover {
            color: #1f5ba8;
        }
        
        .popular-item-arrow {
            color: #bbb;
            font-size: 1.2rem;
        }
        
        .important-panel {
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
            border: 1px solid #c8e6c9;
            border-radius: 8px;
            padding: 1rem;
        }
        
        .important-panel .panel-title {
            color: #2e7d32;
        }
        
        .important-panel .panel-item {
            color: #3d5a40;
        }
        
        /* Hackathon badge */
        .hackathon-badge {
            display: inline-block;
            background: linear-gradient(135deg, #17c65f 0%, #1ca85c 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .right-sidebar {
                display: none;
            }
            
            .chat-section {
                margin-right: 0;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""


def format_timestamp():
    """Get current time formatted."""
    return datetime.now().strftime("%I:%M %p")


def render_sidebar():
    """Render the left sidebar."""
    with st.sidebar:
        # Header
        st.markdown("""
            <div class="sidebar-header">
                <div class="sidebar-logo-icon">🏛️</div>
                <div class="sidebar-title">CityFlow</div>
                <div class="sidebar-subtitle">AI-Powered Permit Navigator</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
            <div class="nav-section">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Chat", use_container_width=True):
                st.session_state.current_page = "chat"
        
        with col2:
            if st.button("ℹ️ About", use_container_width=True):
                st.session_state.current_page = "about"
        
        with col3:
            if st.button("❓ Help", use_container_width=True):
                st.session_state.current_page = "help"
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Sidebar content
        st.markdown("""
            <div style="text-align: center; padding: 2rem 1rem; color: #666; font-size: 0.9rem; line-height: 1.6;">
                Understand government permits in plain English.
            </div>
        """, unsafe_allow_html=True)


def render_right_sidebar():
    """Render the right sidebar with tips and popular questions."""
    right_sidebar_html = """
    <div class="right-sidebar">
        <!-- Quick Tips -->
        <div class="sidebar-panel">
            <div class="panel-title">⚡ Quick Tips</div>
            <div class="panel-item">
                <span class="check-mark">✓</span>
                <span>Be as specific as you can</span>
            </div>
            <div class="panel-item">
                <span class="check-mark">✓</span>
                <span>Use plain, natural language</span>
            </div>
            <div class="panel-item">
                <span class="check-mark">✓</span>
                <span>You can ask follow-up questions</span>
            </div>
            <div class="panel-item">
                <span class="check-mark">✓</span>
                <span>We'll show you official sources</span>
            </div>
        </div>
        
        <!-- Popular Questions -->
        <div class="sidebar-panel">
            <div class="panel-title">🔥 Popular Questions</div>
            <div class="popular-item">
                <span>Restaurant permits?</span>
                <span class="popular-item-arrow">→</span>
            </div>
            <div class="popular-item">
                <span>Home business permit?</span>
                <span class="popular-item-arrow">→</span>
            </div>
            <div class="popular-item">
                <span>Building requirements?</span>
                <span class="popular-item-arrow">→</span>
            </div>
            <div class="popular-item">
                <span>Permit timeline?</span>
                <span class="popular-item-arrow">→</span>
            </div>
        </div>
        
        <!-- Important -->
        <div class="sidebar-panel important-panel">
            <div class="panel-title">🛡️ Important</div>
            <div class="panel-item">
                CityFlow provides guidance based on available official sources. Requirements may change, so verify important information with the relevant authority.
            </div>
        </div>
    </div>
    """
    st.markdown(right_sidebar_html, unsafe_allow_html=True)


def render_chat_area():
    """Render the main chat area."""
    st.markdown("""
        <div class="chat-header">
            <div class="chat-title">Ask About Your Permit</div>
            <div class="chat-subtitle">Type your question in plain English and I'll help you find the right permits, requirements and next steps.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Chat messages area
    if st.session_state.messages:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="message-container user">
                        <div class="message-content">
                            <div class="message-bubble">{message["content"]}</div>
                            <div class="message-time">{message.get("timestamp", "")}</div>
                        </div>
                        <div class="message-avatar">👤</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="message-container assistant">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            <div class="message-bubble">{message["content"]}</div>
                            <div class="message-time">{message.get("timestamp", "")}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show example questions if no messages
        st.markdown("""
            <div style="text-align: center; padding: 2rem 1rem; color: #999;">
                <div style="font-size: 0.95rem; margin-bottom: 1.5rem;">Try asking:</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("I want to open a restaurant. What permits do I need?", use_container_width=True, key="ex1"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "I want to open a restaurant. What permits do I need?",
                    "timestamp": format_timestamp()
                })
                st.rerun()
        
        with col2:
            if st.button("How do I get a home business permit?", use_container_width=True, key="ex2"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "How do I get a home business permit?",
                    "timestamp": format_timestamp()
                })
                st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("What are the requirements for a building permit?", use_container_width=True, key="ex3"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What are the requirements for a building permit?",
                    "timestamp": format_timestamp()
                })
                st.rerun()
        
        with col2:
            if st.button("How long does it take to get a permit?", use_container_width=True, key="ex4"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "How long does it take to get a permit?",
                    "timestamp": format_timestamp()
                })
                st.rerun()


def render_input_area():
    """Render the chat input area."""
    col1, col2, col3 = st.columns([0.85, 0.05, 0.1])
    
    with col1:
        question = st.text_input(
            "Type your question here...",
            key="chat_input",
            placeholder="Type your question here...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("")  # Spacing
    
    with col3:
        send_clicked = st.button("Send", use_container_width=True, type="primary")
    
    return question if send_clicked and question.strip() else None


def process_question(question: str):
    """Process the user's question and get response from backend."""
    try:
        service = get_service()
        
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": question,
            "timestamp": format_timestamp()
        })
        
        # Get response from service
        response = service.process_question(question)
        
        # Format response for display
        if response.is_fallback:
            answer_text = f"⚠️ {response.summary}"
            if response.notes:
                answer_text += "\n\n" + "\n".join(response.notes)
        else:
            answer_text = response.summary
            
            if response.steps:
                answer_text += "\n\n**Required Steps:**"
                for i, step in enumerate(response.steps, 1):
                    requirement = step.get("requirement", "")
                    department = step.get("department", "")
                    cost = step.get("cost", "")
                    timeline = step.get("timeline", "")
                    
                    answer_text += f"\n{i}. {requirement}"
                    if department:
                        answer_text += f"\n   • Department: {department}"
                    if cost:
                        answer_text += f"\n   • Cost: {cost}"
                    if timeline:
                        answer_text += f"\n   • Timeline: {timeline}"
            
            if response.notes:
                answer_text += "\n\n**Important Notes:**"
                for note in response.notes:
                    answer_text += f"\n• {note}"
        
        # Add assistant response to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "timestamp": format_timestamp()
        })
        
    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message,
            "timestamp": format_timestamp()
        })


def main():
    """Main application."""
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    col_main, col_right = st.columns([1, 0], gap="large")
    
    with col_main:
        render_chat_area()
        
        # Input area
        question = render_input_area()
        
        if question:
            process_question(question)
            st.rerun()
    
    # Right sidebar (overlay)
    render_right_sidebar()


if __name__ == "__main__":
    main()
