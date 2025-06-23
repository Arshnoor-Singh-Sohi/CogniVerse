import streamlit as st
import os
from datetime import datetime
import json
import uuid
from pathlib import Path

# Import our custom modules
from config.settings import AppConfig
from utils.gemini_client import GeminiClient
from utils.chat_manager import ChatManager
from utils.file_processor import FileProcessor
from components.ui_components import UIComponents
from components.sidebar import Sidebar

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="CogniVerse - AI Conversation Universe",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/cogniverse',
        'Report a bug': "https://github.com/yourusername/cogniverse/issues",
        'About': "# CogniVerse\nYour Complete AI Conversation Universe!"
    }
)

class CogniVerse:
    """
    Main application class that orchestrates the entire CogniVerse experience.
    This design pattern helps us maintain clean separation of concerns and 
    makes the application more maintainable as it grows.
    """
    
    def __init__(self):
        self.config = AppConfig()
        self.gemini_client = GeminiClient()
        self.chat_manager = ChatManager()
        self.file_processor = FileProcessor()
        self.ui = UIComponents()
        self.sidebar = Sidebar()
        
        # Initialize session state variables
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize all session state variables with default values."""
        defaults = {
            'current_conversation_id': str(uuid.uuid4()),
            'conversations': {},
            'current_mode': 'chat',
            'theme': 'dark',
            'show_welcome': True,
            'uploaded_files': [],
            'user_preferences': {
                'model': 'gemini-2.0-flash-exp',
                'temperature': 0.7,
                'max_tokens': 2048,
                'show_timestamps': True,
                'auto_save': True
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def run(self):
        """Main application entry point that orchestrates the entire user experience."""
        
        # Load custom CSS for enhanced styling
        self.ui.load_custom_css()
        
        # Render sidebar with all controls and settings
        self.sidebar.render()
        
        # Show welcome screen for first-time users
        if st.session_state.show_welcome:
            self._show_welcome_screen()
            return
        
        # Main content area based on selected mode
        self._render_main_content()
    
    def _show_welcome_screen(self):
        """Create an engaging welcome experience that introduces users to CogniVerse capabilities."""
        
        st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">🧠 Welcome to CogniVerse</h1>
            <p class="welcome-subtitle">Your Complete AI Conversation Universe</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 💬 Smart Conversations
            Engage with advanced AI powered by Google's latest Gemini models. 
            Get intelligent responses, creative writing, and problem-solving assistance.
            """)
        
        with col2:
            st.markdown("""
            ### 📄 Document Analysis
            Upload PDFs, Word documents, or text files for AI-powered analysis.
            Ask questions about your documents and get instant insights.
            """)
        
        with col3:
            st.markdown("""
            ### 🖼️ Visual Intelligence
            Analyze images, create visualizations, and work with multimedia content.
            Perfect for creative projects and data analysis.
            """)
        
        # Getting started section
        st.markdown("---")
        st.markdown("### 🚀 Getting Started")
        
        if st.button("Start Your First Conversation", type="primary", use_container_width=True):
            st.session_state.show_welcome = False
            st.rerun()
        
        # Quick tips
        with st.expander("💡 Quick Tips"):
            st.markdown("""
            - Use the sidebar to switch between different AI models
            - Upload files using the file uploader for document analysis
            - Create multiple conversation threads to organize your chats
            - Export your conversations for future reference
            - Customize the interface theme in settings
            """)
    
    def _render_main_content(self):
        """Render the main content area based on the selected mode."""
        
        mode = st.session_state.current_mode
        
        if mode == 'chat':
            self._render_chat_interface()
        elif mode == 'document':
            self._render_document_analysis()
        elif mode == 'image':
            self._render_image_analysis()
        elif mode == 'analytics':
            self._render_analytics_dashboard()
    
    def _render_chat_interface(self):
        """Render the enhanced chat interface with advanced features."""
        
        # Chat header with conversation management
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown("### 💬 AI Conversation")
        
        with col2:
            if st.button("🆕 New Chat", help="Start a new conversation"):
                self.chat_manager.create_new_conversation()
                st.rerun()
        
        with col3:
            if st.button("💾 Export", help="Export current conversation"):
                self.chat_manager.export_conversation()
        
        # Display conversation history
        self._display_chat_history()
        
        # Input area with enhanced features
        self._render_chat_input()
    
    def _display_chat_history(self):
        """Display the conversation history with enhanced formatting."""
        
        # Get current conversation
        current_conversation = self.chat_manager.get_current_conversation()
        
        if not current_conversation or not current_conversation.messages:
            st.info("👋 Start a conversation by typing a message below!")
            return
        
        # Create a container for scrollable chat history
        chat_container = st.container()
        
        with chat_container:
            # Convert conversation messages to the format expected by UI
            for message in current_conversation.messages:
                message_data = {
                    'id': message.id,
                    'content': message.content,
                    'role': message.role,
                    'timestamp': message.timestamp,
                    'model_used': message.model_used,
                    'metadata': message.metadata
                }
                self.ui.render_message(message_data)
    
    def _render_chat_input(self):
        """Render the enhanced chat input area with multiple input options."""
        
        # Create tabs for different input methods
        input_tab1, input_tab2, input_tab3 = st.tabs(["💬 Text", "🎤 Voice", "📁 File"])
        
        with input_tab1:
            # Model selection outside form
            model_options = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"]
            selected_model = st.selectbox(
                "Model:",
                model_options,
                index=0,
                key="selected_model"
            )
            
            # Use form for automatic input clearing
            with st.form("chat_form", clear_on_submit=True):
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    user_input = st.text_area(
                        "Type your message here...",
                        height=100,
                        placeholder="Ask me anything! I can help with questions, writing, coding, analysis, and more..."
                    )
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                    send_button = st.form_submit_button("🚀 Send", type="primary", use_container_width=True)
                
                # Process input when form is submitted
                if send_button and user_input.strip():
                    self._process_user_input(user_input, selected_model)
        
        with input_tab2:
            st.info("🎤 Voice input feature coming soon!")
            st.markdown("This will allow you to speak your questions directly.")
        
        with input_tab3:
            uploaded_file = st.file_uploader(
                "Upload a file to analyze",
                type=['txt', 'pdf', 'docx', 'csv', 'json', 'png', 'jpg', 'jpeg'],
                help="Upload documents, images, or data files for AI analysis"
            )
            
            if uploaded_file:
                self._handle_file_upload(uploaded_file)
    
    def _handle_file_upload(self, uploaded_file):
        """Handle file uploads and prepare them for analysis."""
        
        try:
            # Process the uploaded file
            file_content = self.file_processor.process_file(uploaded_file)
            
            # Add to session state
            st.session_state.uploaded_files.append({
                'name': uploaded_file.name,
                'content': file_content,
                'type': uploaded_file.type,
                'timestamp': datetime.now()
            })
            
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            st.info("💡 You can now ask questions about this file in your conversation.")
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    
    def _process_user_input(self, user_input, model):
        """Process user input and generate AI response."""
        
        try:
            # Show typing indicator
            with st.spinner("🤔 Thinking..."):
                
                # Prepare context with uploaded files if any
                context = self._prepare_context()
                
                # Generate response using the selected model
                response = self.gemini_client.generate_response(
                    user_input, 
                    model=model,
                    context=context
                )
                
                # Save the conversation
                self.chat_manager.add_message(user_input, response, model)
                
                # Refresh to show new message
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
    
    def _prepare_context(self):
        """Prepare context from uploaded files and conversation history."""
        
        context = {
            'uploaded_files': st.session_state.uploaded_files,
            'conversation_history': self.chat_manager.get_recent_history(),
            'user_preferences': st.session_state.user_preferences
        }
        
        return context
    
    def _render_document_analysis(self):
        """Render the document analysis interface."""
        
        st.markdown("### 📄 Document Analysis")
        st.markdown("Upload documents and ask questions about their content.")
        
        # File upload area
        uploaded_files = st.file_uploader(
            "Choose files to analyze",
            type=['pdf', 'txt', 'docx', 'csv'],
            accept_multiple_files=True,
            help="Upload documents for AI-powered analysis"
        )
        
        if uploaded_files:
            # Display uploaded files
            st.markdown("#### 📂 Uploaded Files:")
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}"):
                    # Process and display file summary
                    content = self.file_processor.process_file(file)
                    st.text_area("File content preview:", content[:500] + "...", height=100)
            
            # Question input for document analysis
            question = st.text_input("Ask a question about your documents:")
            
            if st.button("🔍 Analyze") and question:
                self._analyze_documents(uploaded_files, question)
    
    def _render_image_analysis(self):
        """Render the image analysis interface."""
        
        st.markdown("### 🖼️ Image Analysis")
        st.markdown("Upload images for AI-powered visual analysis.")
        
        uploaded_image = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload an image for AI analysis"
        )
        
        if uploaded_image:
            # Display the image
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Analysis options
            analysis_type = st.selectbox(
                "Choose analysis type:",
                ["Describe the image", "Extract text (OCR)", "Identify objects", "Custom question"]
            )
            
            if analysis_type == "Custom question":
                custom_question = st.text_input("What would you like to know about this image?")
            
            if st.button("🔍 Analyze Image"):
                self._analyze_image(uploaded_image, analysis_type)
    
    def _render_analytics_dashboard(self):
        """Render the analytics dashboard."""
        
        st.markdown("### 📊 Analytics Dashboard")
        
        # Get conversation statistics
        stats = self.chat_manager.get_conversation_stats()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Conversations", stats.get('total_conversations', 0))
        
        with col2:
            st.metric("Total Messages", stats.get('total_messages', 0))
        
        with col3:
            st.metric("Files Analyzed", len(st.session_state.uploaded_files))
        
        with col4:
            st.metric("Active Session", "1")
        
        # Conversation timeline
        st.markdown("#### 📈 Conversation Activity")
        # Here you would add charts showing usage patterns
        st.info("📊 Advanced analytics features coming soon!")

# Application entry point
if __name__ == "__main__":
    app = CogniVerse()
    app.run()