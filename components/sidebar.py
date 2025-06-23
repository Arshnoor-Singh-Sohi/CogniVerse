"""
Intelligent Sidebar Interface for CogniVerse

This module demonstrates advanced sidebar design that transforms a simple navigation
area into an intelligent command center. The patterns here show how to:

1. Progressive Disclosure: Revealing functionality as users need it
2. Contextual Controls: Showing relevant options based on current state
3. Efficient Navigation: Quick access to frequently used features
4. Settings Management: Organized, discoverable configuration options
5. Status Awareness: Real-time feedback about system state

Think of this sidebar as the cockpit of an advanced aircraft - everything the pilot
needs is within easy reach, organized logically, and provides clear feedback about
the system's current state. Just as a pilot can focus on flying while the instruments
provide crucial information, users can focus on their conversations while the sidebar
handles the technical details.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

from config.settings import AppConfig
from utils.chat_manager import ChatManager

class Sidebar:
    """
    An intelligent sidebar that adapts to user needs and application state.
    
    This class demonstrates the Adaptive Interface pattern - the sidebar changes
    its appearance and available options based on what the user is doing and
    what features are relevant to their current context.
    """
    
    def __init__(self):
        self.config = AppConfig()
        self.chat_manager = ChatManager()
    
    def render(self):
        """
        Render the complete sidebar interface.
        
        This method orchestrates the entire sidebar, organizing different sections
        in a logical hierarchy. The order and content adapt based on user state
        and application context.
        """
        with st.sidebar:
            # App header and branding
            self._render_header()
            
            # Main navigation
            self._render_navigation()
            
            # Quick actions
            self._render_quick_actions()
            
            # Conversation management
            self._render_conversation_management()
            
            # File upload area
            self._render_file_upload()
            
            # Model and AI settings
            self._render_ai_settings()
            
            # Application settings
            self._render_app_settings()
            
            # Usage statistics
            self._render_usage_stats()
            
            # Help and information
            self._render_help_section()
    
    def _render_header(self):
        """
        Render the application header with branding and status.
        
        The header establishes identity and provides immediate context about
        the application state. It's the first thing users see, so it needs
        to be both welcoming and informative.
        """
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(135deg, #1E88E5, #FFC107); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🧠 CogniVerse
            </h1>
            <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; opacity: 0.7;">
                AI Conversation Universe
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # System status indicator
        self._render_system_status()
    
    def _render_system_status(self):
        """
        Display current system status and connectivity.
        
        System status indicators provide immediate feedback about the health
        of various system components. This builds user confidence and helps
        troubleshoot issues quickly.
        """
        # Check API connectivity (simplified)
        api_status = "🟢 Connected" if self.config.google_api_key else "🔴 No API Key"
        
        # Count active conversations
        conversation_count = len(st.session_state.get('conversations', {}))
        
        # Use colors that work in both light and dark mode
        st.markdown(f"""
        <div style="
            background: rgba(100, 116, 139, 0.1); 
            border: 1px solid rgba(100, 116, 139, 0.2);
            padding: 0.8rem; 
            border-radius: 8px; 
            margin-bottom: 1rem; 
            font-size: 0.85rem;
            color: var(--text-color);
        ">
            <div style="margin-bottom: 0.3rem; font-weight: 500;">🔌 API: {api_status}</div>
            <div style="margin-bottom: 0.3rem; font-weight: 500;">💬 Conversations: {conversation_count}</div>
            <div style="font-weight: 500;">🕐 Session: {self._get_session_duration()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _get_session_duration(self) -> str:
        """Calculate and format session duration."""
        if 'session_start_time' not in st.session_state:
            st.session_state.session_start_time = datetime.now()
        
        duration = datetime.now() - st.session_state.session_start_time
        
        if duration.seconds < 60:
            return f"{duration.seconds}s"
        elif duration.seconds < 3600:
            return f"{duration.seconds // 60}m"
        else:
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def _render_navigation(self):
        """
        Render the main navigation interface.
        
        Navigation should be intuitive and provide clear feedback about the
        current location. This implementation uses both visual and functional
        cues to guide user interaction.
        """
        st.markdown("### 🧭 Navigation")
        
        # Mode selection with visual feedback
        modes = {
            'chat': {'label': '💬 Chat', 'description': 'AI Conversations'},
            'document': {'label': '📄 Documents', 'description': 'File Analysis'},
            'image': {'label': '🖼️ Images', 'description': 'Visual AI'},
            'analytics': {'label': '📊 Analytics', 'description': 'Usage Insights'}
        }
        
        current_mode = st.session_state.get('current_mode', 'chat')
        
        for mode_key, mode_info in modes.items():
            # Create a button-like selectbox alternative
            is_selected = current_mode == mode_key
            button_style = "primary" if is_selected else "secondary"
            
            if st.button(
                mode_info['label'], 
                key=f"nav_{mode_key}",
                help=mode_info['description'],
                type=button_style if is_selected else "secondary",
                use_container_width=True
            ):
                st.session_state.current_mode = mode_key
                st.rerun()
        
        st.markdown("---")
    
    def _render_quick_actions(self):
        """
        Render quick action buttons for common tasks.
        
        Quick actions reduce the number of steps needed for frequent operations.
        This section demonstrates how to identify and optimize common user workflows.
        """
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🆕 New Chat", use_container_width=True, help="Start a fresh conversation"):
                self.chat_manager.create_new_conversation()
                st.rerun()
        
        with col2:
            if st.button("📤 Export", use_container_width=True, help="Export current conversation"):
                self._handle_export_action()
        
        # Advanced quick actions
        with st.expander("🔧 More Actions"):
            if st.button("🧹 Clear History", use_container_width=True):
                if st.session_state.get('confirm_clear'):
                    # Clear conversations
                    st.session_state.conversations = {}
                    st.session_state.current_conversation_id = None
                    st.session_state.confirm_clear = False
                    st.success("History cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm clearing all conversation history")
            
            if st.button("💾 Save Session", use_container_width=True):
                self._save_session_data()
            
            if st.button("🔄 Reset App", use_container_width=True):
                self._reset_application_state()
        
        st.markdown("---")
    
    def _handle_export_action(self):
        """
        Handle conversation export with format selection.
        
        This demonstrates how to provide users with meaningful choices while
        maintaining simplicity. Export functionality needs to be both powerful
        and accessible.
        """
        try:
            current_conversation = self.chat_manager.get_current_conversation()
            if not current_conversation:
                st.warning("No conversation to export")
                return
            
            # Simple export to JSON (in a real app, you'd provide format choices)
            export_data = self.chat_manager.export_conversation(format='json')
            
            # Create download link
            st.download_button(
                label="📥 Download JSON",
                data=export_data,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Export failed: {str(e)}")
    
    def _render_conversation_management(self):
        """
        Render conversation history and management interface.
        
        Conversation management is crucial for users who have multiple ongoing
        discussions. This interface provides overview, navigation, and organization
        tools in a compact, efficient format.
        """
        st.markdown("### 💬 Conversations")
        
        conversations = st.session_state.get('conversations', {})
        current_id = st.session_state.get('current_conversation_id')
        
        if not conversations:
            st.info("No conversations yet. Start chatting to create your first conversation!")
            return
        
        # Sort conversations by update time
        sorted_conversations = sorted(
            conversations.items(),
            key=lambda x: x[1].get('updated_at', ''),
            reverse=True
        )
        
        # Show recent conversations
        st.markdown("#### Recent Chats")
        
        for conv_id, conv_data in sorted_conversations[:5]:  # Show 5 most recent
            if isinstance(conv_data, dict):
                title = conv_data.get('title', 'Untitled')
                message_count = len(conv_data.get('messages', []))
                is_current = conv_id == current_id
            else:
                title = getattr(conv_data, 'title', 'Untitled')
                message_count = len(getattr(conv_data, 'messages', []))
                is_current = conv_id == current_id
            
            # Truncate title if too long
            display_title = title[:25] + "..." if len(title) > 25 else title
            
            button_type = "primary" if is_current else "secondary"
            
            if st.button(
                f"{'🔸' if is_current else '💬'} {display_title}",
                key=f"conv_{conv_id}",
                help=f"{message_count} messages",
                use_container_width=True
            ):
                st.session_state.current_conversation_id = conv_id
                st.rerun()
        
        # Show more conversations in expander
        if len(conversations) > 5:
            with st.expander(f"📁 All Conversations ({len(conversations)})"):
                for conv_id, conv_data in sorted_conversations[5:]:
                    if isinstance(conv_data, dict):
                        title = conv_data.get('title', 'Untitled')
                    else:
                        title = getattr(conv_data, 'title', 'Untitled')
                    
                    if st.button(title, key=f"all_conv_{conv_id}", use_container_width=True):
                        st.session_state.current_conversation_id = conv_id
                        st.rerun()
        
        st.markdown("---")
    
    def _render_file_upload(self):
        """
        Render file upload interface with drag-and-drop support.
        
        File upload is a critical feature that needs to be both prominent and
        user-friendly. This implementation provides clear feedback and supports
        multiple file types with intelligent processing.
        """
        st.markdown("### 📁 File Upload")
        
        # Show supported formats
        with st.expander("📋 Supported Formats"):
            formats = {
                "Text": "txt, md, csv, json, py, js",
                "Documents": "pdf, docx",
                "Images": "jpg, png, gif, bmp",
                "Data": "csv, json"
            }
            
            for category, extensions in formats.items():
                st.markdown(f"**{category}:** {extensions}")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Drop files here or click to browse",
            accept_multiple_files=True,
            type=self.config.ui.supported_file_types,
            help=f"Maximum file size: {self.config.ui.max_file_size_mb}MB"
        )
        
        # Display uploaded files
        if uploaded_files:
            st.markdown("#### 📎 Current Files")
            for file in uploaded_files:
                file_size = len(file.read())
                file.seek(0)  # Reset file pointer
                
                size_mb = file_size / (1024 * 1024)
                st.markdown(f"📄 **{file.name}** ({size_mb:.1f}MB)")
        
        # Show recent uploads from session
        recent_files = st.session_state.get('uploaded_files', [])
        if recent_files:
            with st.expander("🕐 Recent Uploads"):
                for file_info in recent_files[-3:]:  # Show last 3
                    name = file_info.get('name', 'Unknown')
                    st.markdown(f"📎 {name}")
        
        st.markdown("---")
    
    def _render_ai_settings(self):
        """
        Render AI model and generation settings.
        
        AI settings allow users to customize the behavior of the AI assistant.
        This interface balances advanced control with simplicity, providing
        sensible defaults while allowing for expert-level customization.
        """
        st.markdown("### 🤖 AI Settings")
        
        # Model selection
        available_models = list(self.config.models.keys())
        current_model = st.session_state.user_preferences.get('model', available_models[0])
        
        selected_model = st.selectbox(
            "Model",
            available_models,
            index=available_models.index(current_model) if current_model in available_models else 0,
            help="Choose which AI model to use for responses"
        )
        
        # Update preferences
        st.session_state.user_preferences['model'] = selected_model
        
        # Model information
        model_config = self.config.get_model_config(selected_model)
        if model_config:
            with st.expander("ℹ️ Model Info"):
                st.markdown(f"**Name:** {model_config.display_name}")
                st.markdown(f"**Description:** {model_config.description}")
                st.markdown(f"**Max Tokens:** {model_config.max_tokens:,}")
                st.markdown(f"**Vision Support:** {'✅' if model_config.supports_vision else '❌'}")
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            # Temperature
            temperature = st.slider(
                "Creativity (Temperature)",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.user_preferences.get('temperature', 0.7),
                step=0.1,
                help="Higher values make responses more creative but less predictable"
            )
            st.session_state.user_preferences['temperature'] = temperature
            
            # Max tokens
            max_tokens = st.number_input(
                "Max Response Length",
                min_value=100,
                max_value=model_config.max_tokens if model_config else 2048,
                value=st.session_state.user_preferences.get('max_tokens', 2048),
                step=100,
                help="Maximum length of AI responses"
            )
            st.session_state.user_preferences['max_tokens'] = max_tokens
        
        st.markdown("---")
    
    def _render_app_settings(self):
        """
        Render application-wide settings and preferences.
        
        Application settings control the overall user experience. This section
        demonstrates how to organize settings logically and provide immediate
        feedback when changes are made.
        """
        st.markdown("### ⚙️ App Settings")
        
        # Theme selection
        current_theme = st.session_state.get('theme', 'dark')
        theme = st.selectbox(
            "Theme",
            options=['dark', 'light'],
            index=0 if current_theme == 'dark' else 1,
            help="Choose your preferred color theme"
        )
        
        if theme != current_theme:
            st.session_state.theme = theme
            st.rerun()  # Refresh to apply theme changes
        
        # Display preferences
        with st.expander("🖥️ Display Options"):
            show_timestamps = st.checkbox(
                "Show message timestamps",
                value=st.session_state.user_preferences.get('show_timestamps', True)
            )
            st.session_state.user_preferences['show_timestamps'] = show_timestamps
            
            auto_save = st.checkbox(
                "Auto-save conversations",
                value=st.session_state.user_preferences.get('auto_save', True)
            )
            st.session_state.user_preferences['auto_save'] = auto_save
        
        # Data management
        with st.expander("💾 Data Management"):
            st.markdown("**Storage Usage**")
            
            # Calculate storage usage
            conversations = st.session_state.get('conversations', {})
            total_messages = sum(
                len(conv.get('messages', [])) if isinstance(conv, dict) 
                else len(getattr(conv, 'messages', []))
                for conv in conversations.values()
            )
            
            st.metric("Total Messages", total_messages)
            st.metric("Conversations", len(conversations))
            
            if st.button("🗑️ Clean Old Data", use_container_width=True):
                cleaned = self.chat_manager.cleanup_old_conversations(days_old=30)
                if cleaned > 0:
                    st.success(f"Cleaned {cleaned} old conversations")
                else:
                    st.info("No old conversations to clean")
        
        st.markdown("---")
    
    def _render_usage_stats(self):
        """
        Render usage statistics and analytics.
        
        Usage statistics help users understand their interaction patterns and
        provide insights into how they're using the application. This can inform
        both user behavior and product development decisions.
        """
        st.markdown("### 📊 Usage Stats")
        
        try:
            stats = self.chat_manager.get_conversation_stats()
            
            if stats['total_conversations'] > 0:
                # Key metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Conversations", stats['total_conversations'])
                    st.metric("Messages", stats['total_messages'])
                
                with col2:
                    avg_messages = stats.get('average_messages_per_conversation', 0)
                    st.metric("Avg Messages", f"{avg_messages:.1f}")
                    
                    # Most used model
                    most_used_models = stats.get('most_used_models', {})
                    if most_used_models:
                        top_model = list(most_used_models.keys())[0]
                        st.metric("Top Model", top_model.split('-')[0])  # Shortened name
                
                # Detailed stats in expander
                with st.expander("📈 Detailed Analytics"):
                    if most_used_models:
                        st.markdown("**Model Usage:**")
                        for model, count in list(most_used_models.items())[:3]:
                            st.markdown(f"- {model}: {count} times")
                    
                    activity = stats.get('conversation_activity', {})
                    if activity:
                        st.markdown("**Recent Activity:**")
                        for date, count in list(activity.items())[-5:]:
                            st.markdown(f"- {date}: {count} conversations")
            else:
                st.info("Start chatting to see your usage statistics!")
                
        except Exception as e:
            st.error(f"Error loading stats: {str(e)}")
        
        st.markdown("---")
    
    def _render_help_section(self):
        """
        Render help and information section.
        
        Help sections are often overlooked but are crucial for user adoption
        and satisfaction. This implementation provides contextual help,
        shortcuts, and troubleshooting information in an accessible format.
        """
        st.markdown("### ❓ Help & Info")
        
        with st.expander("🚀 Quick Tips"):
            tips = [
                "💡 Use different models for different tasks",
                "📁 Upload files to analyze documents",
                "🔄 Create multiple conversations to organize topics",
                "⚙️ Adjust temperature for creative vs. factual responses",
                "📤 Export conversations to save important discussions"
            ]
            
            for tip in tips:
                st.markdown(f"- {tip}")
        
        with st.expander("⌨️ Keyboard Shortcuts"):
            shortcuts = {
                "Ctrl + Enter": "Send message",
                "Ctrl + N": "New conversation",
                "Ctrl + /": "Toggle sidebar",
                "Ctrl + ,": "Open settings"
            }
            
            for shortcut, description in shortcuts.items():
                st.markdown(f"**{shortcut}**: {description}")
        
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **Common Issues:**
            
            - **No API response**: Check your internet connection and API key
            - **File upload fails**: Ensure file size is under the limit
            - **Slow responses**: Try using a faster model like Flash
            - **Memory issues**: Clear old conversations to free up space
            
            **Need more help?** Check the documentation or contact support.
            """)
        
        # App version and info
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; font-size: 0.8rem; opacity: 0.6;">
            CogniVerse v{self.config.app_version}<br>
            Made with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)
    
    def _save_session_data(self):
        """
        Save current session data for persistence.
        
        Session saving allows users to preserve their work across browser sessions.
        This demonstrates how to implement data persistence in web applications.
        """
        try:
            session_data = {
                'conversations': st.session_state.get('conversations', {}),
                'preferences': st.session_state.get('user_preferences', {}),
                'theme': st.session_state.get('theme', 'dark'),
                'saved_at': datetime.now().isoformat()
            }
            
            # In a real app, this would save to a database or file
            # For demo purposes, we'll just show a success message
            st.success("Session data saved successfully!")
            
        except Exception as e:
            st.error(f"Failed to save session: {str(e)}")
    
    def _reset_application_state(self):
        """
        Reset the application to its initial state.
        
        Reset functionality provides users with a clean slate when needed.
        This is particularly useful for testing, troubleshooting, or starting fresh.
        """
        if st.session_state.get('confirm_reset'):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key != 'confirm_reset':
                    del st.session_state[key]
            
            st.success("Application reset successfully!")
            st.rerun()
        else:
            st.session_state.confirm_reset = True
            st.warning("⚠️ This will clear all data. Click again to confirm.")