"""
Advanced UI Components for CogniVerse

This module demonstrates sophisticated UI/UX design principles that create engaging,
professional user experiences. The patterns here show how to:

1. Component-Based Architecture: Reusable UI elements that maintain consistency
2. Responsive Design: Interfaces that work well across different screen sizes
3. Progressive Enhancement: Graceful degradation when features aren't available
4. Accessibility: Ensuring the app works for users with different abilities
5. Visual Hierarchy: Guiding user attention through thoughtful design

Think of this module as your design system - a collection of carefully crafted
components that work together to create a cohesive, delightful user experience.
Just like how a symphony orchestra has different instruments that combine to create
beautiful music, these UI components combine to create a beautiful application.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import json
import base64
from pathlib import Path

from config.settings import AppConfig

class UIComponents:
    """
    A comprehensive collection of advanced UI components for CogniVerse.
    
    This class demonstrates the Component pattern - we create reusable UI elements
    that can be easily combined and customized. Each method represents a different
    type of interface element, designed with both functionality and aesthetics in mind.
    """
    
    def __init__(self):
        self.config = AppConfig()
        self.theme_colors = self.config.get_theme_colors(
            st.session_state.get('theme', 'dark')
        )
    
    def load_custom_css(self):
        """
        Load custom CSS styling for the application.
        
        Custom CSS allows us to create unique, branded experiences that go beyond
        Streamlit's default styling. This demonstrates how to inject professional
        design elements while maintaining compatibility with the underlying framework.
        """
        css = self._generate_custom_css()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    def _generate_custom_css(self) -> str:
        """
        Generate dynamic CSS based on current theme and configuration.
        
        Dynamic CSS generation allows us to create theme-aware interfaces that
        adapt to user preferences. This approach ensures consistency while
        providing flexibility for customization.
        """
        colors = self.theme_colors
        
        return f"""
        /* Global Styling */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 95%;
        }}
        
        /* Welcome Screen Styling */
        .welcome-container {{
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, {colors['primary']}20, {colors['secondary']}20);
            border-radius: 15px;
            margin: 2rem 0;
            border: 1px solid {colors['primary']}40;
        }}
        
        .welcome-title {{
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .welcome-subtitle {{
            font-size: 1.3rem;
            color: {colors['text']}dd;
            margin-bottom: 2rem;
            font-weight: 300;
        }}
        
        /* Message Styling */
        .message-container {{
            margin: 1rem 0;
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid;
            animation: slideIn 0.3s ease-out;
        }}
        
        .user-message {{
            background: {colors['primary']}15;
            border-left-color: {colors['primary']};
            margin-left: 2rem;
        }}
        
        .assistant-message {{
            background: {colors['surface']};
            border-left-color: {colors['secondary']};
            margin-right: 2rem;
        }}
        
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        .message-content {{
            line-height: 1.6;
            word-wrap: break-word;
        }}
        
        .message-timestamp {{
            font-size: 0.8rem;
            opacity: 0.6;
        }}
        
        .model-badge {{
            background: {colors['accent']};
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
        }}
        
        /* Stats and Metrics */
        .metric-card {{
            background: {colors['surface']};
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid {colors['primary']}30;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {colors['primary']};
            display: block;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: {colors['text']}cc;
            margin-top: 0.5rem;
        }}
        
        /* File Upload Areas */
        .upload-area {{
            border: 2px dashed {colors['primary']}60;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            background: {colors['primary']}08;
            transition: all 0.3s ease;
        }}
        
        .upload-area:hover {{
            border-color: {colors['primary']};
            background: {colors['primary']}15;
        }}
        
        /* Progress and Status Indicators */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .status-success {{
            background: #10B98150;
            color: #059669;
        }}
        
        .status-warning {{
            background: #F59E0B50;
            color: #D97706;
        }}
        
        .status-error {{
            background: #EF444450;
            color: #DC2626;
        }}
        
        .status-info {{
            background: {colors['primary']}50;
            color: {colors['primary']};
        }}
        
        /* Animations */
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.7;
            }}
        }}
        
        .typing-indicator {{
            animation: pulse 2s infinite;
        }}
        
        /* Button Enhancements */
        .stButton > button {{
            border-radius: 8px;
            border: none;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        /* Sidebar Enhancements */
        .sidebar-section {{
            background: {colors['surface']};
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid {colors['primary']}20;
        }}
        
        .sidebar-title {{
            font-weight: 600;
            color: {colors['primary']};
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Code blocks */
        .stCode {{
            border-radius: 8px;
            border: 1px solid {colors['primary']}30;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .welcome-title {{
                font-size: 2.5rem;
            }}
            
            .message-container {{
                margin-left: 0;
                margin-right: 0;
            }}
            
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
        }}
        """
    
    def render_message(self, message: Dict[str, Any]):
        """
        Render a single chat message with sophisticated styling and metadata.
        
        This method demonstrates how to create rich, informative message displays
        that provide context and visual hierarchy. Each message becomes a small
        interface element that tells a story about the conversation flow.
        """
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        timestamp = message.get('timestamp')
        model_used = message.get('model_used')
        
        # Choose styling and layout based on message role
        if role == 'user':
            icon = "👤"
            role_display = "You"
            # Use Streamlit's built-in chat message for user
            with st.chat_message("user"):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(content)
                with col2:
                    time_str = self._format_timestamp(timestamp)
                    st.caption(time_str)
        else:
            icon = "🤖"
            role_display = "AI Assistant"
            # Use Streamlit's built-in chat message for assistant
            with st.chat_message("assistant"):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(content)
                with col2:
                    time_str = self._format_timestamp(timestamp)
                    if model_used:
                        st.caption(f"{model_used.split('-')[0]}")
                    st.caption(time_str)
    
    def _format_timestamp(self, timestamp):
        """Format timestamp for display."""
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                timestamp = datetime.now()
        elif not isinstance(timestamp, datetime):
            timestamp = datetime.now()
        
        return timestamp.strftime("%H:%M")
    
    def _format_message_content(self, content: str) -> str:
        """
        Format message content with syntax highlighting and special formatting.
        
        This method demonstrates content processing that enhances readability.
        We look for patterns in the text and apply appropriate formatting to
        make code, lists, and other structured content more visually appealing.
        """
        # Convert newlines to HTML breaks
        content = content.replace('\n', '<br>')
        
        # Simple code block detection and formatting
        import re
        
        # Format code blocks (```code```)
        code_block_pattern = r'```(.*?)```'
        content = re.sub(
            code_block_pattern,
            r'<div style="background: #1e1e1e; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0; overflow-x: auto;"><code style="color: #f8f8f2;">\1</code></div>',
            content,
            flags=re.DOTALL
        )
        
        # Format inline code (`code`)
        inline_code_pattern = r'`([^`]+)`'
        content = re.sub(
            inline_code_pattern,
            r'<code style="background: #f1f5f9; padding: 0.2rem 0.4rem; border-radius: 3px; font-family: monospace;">\1</code>',
            content
        )
        
        # Format bold text (**text**)
        bold_pattern = r'\*\*(.*?)\*\*'
        content = re.sub(bold_pattern, r'<strong>\1</strong>', content)
        
        # Format italic text (*text*)
        italic_pattern = r'\*(.*?)\*'
        content = re.sub(italic_pattern, r'<em>\1</em>', content)
        
        return content
    
    def create_metric_card(self, title: str, value: Union[str, int, float], 
                          subtitle: Optional[str] = None, 
                          delta: Optional[str] = None) -> str:
        """
        Create an enhanced metric card with visual appeal and optional delta indicators.
        
        Metric cards are essential for dashboards and analytics views. This implementation
        creates visually striking cards that draw attention to important numbers while
        providing context through subtitles and trend indicators.
        """
        delta_html = ""
        if delta:
            delta_color = "#10B981" if delta.startswith("+") else "#EF4444"
            delta_html = f'<div style="color: {delta_color}; font-size: 0.8rem; margin-top: 0.3rem;">{delta}</div>'
        
        subtitle_html = ""
        if subtitle:
            subtitle_html = f'<div class="metric-label">{subtitle}</div>'
        
        return f"""
        <div class="metric-card">
            <span class="metric-value">{value}</span>
            <div class="metric-label">{title}</div>
            {subtitle_html}
            {delta_html}
        </div>
        """
    
    def create_status_indicator(self, status: str, message: str) -> str:
        """
        Create status indicators for various application states.
        
        Status indicators provide immediate visual feedback about system state,
        operation results, or user actions. They're crucial for user experience
        because they communicate what's happening without requiring users to guess.
        """
        status_classes = {
            'success': 'status-success',
            'warning': 'status-warning', 
            'error': 'status-error',
            'info': 'status-info'
        }
        
        status_icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        }
        
        css_class = status_classes.get(status, 'status-info')
        icon = status_icons.get(status, 'ℹ️')
        
        return f"""
        <div class="status-indicator {css_class}">
            <span>{icon}</span>
            <span>{message}</span>
        </div>
        """
    
    def create_progress_bar(self, progress: float, label: str = "", 
                           show_percentage: bool = True) -> str:
        """
        Create an animated progress bar for long-running operations.
        
        Progress bars are essential for operations that take time - they reassure
        users that something is happening and provide estimates for completion.
        This implementation includes smooth animations and customizable styling.
        """
        percentage = min(100, max(0, progress * 100))
        colors = self.theme_colors
        
        percentage_text = f" ({percentage:.0f}%)" if show_percentage else ""
        
        return f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <span style="font-size: 0.9rem; color: {colors['text']};">{label}</span>
                <span style="font-size: 0.8rem; color: {colors['text']}cc;">{percentage:.0f}%</span>
            </div>
            <div style="background: {colors['surface']}; border-radius: 10px; height: 8px; overflow: hidden;">
                <div style="
                    background: linear-gradient(90deg, {colors['primary']}, {colors['secondary']});
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """
    
    def create_file_preview_card(self, file_info: Dict[str, Any]) -> str:
        """
        Create a preview card for uploaded files.
        
        File preview cards help users understand what files they've uploaded and
        provide quick access to file information. This visual representation makes
        file management more intuitive and user-friendly.
        """
        name = file_info.get('name', 'Unknown file')
        file_type = file_info.get('type', 'unknown')
        size = file_info.get('size', 0)
        timestamp = file_info.get('timestamp', datetime.now())
        
        # Choose icon based on file type
        if file_type.startswith('image/'):
            icon = "🖼️"
        elif file_type == 'application/pdf':
            icon = "📄"
        elif 'text' in file_type:
            icon = "📝"
        elif 'csv' in file_type:
            icon = "📊"
        else:
            icon = "📎"
        
        # Format file size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        
        # Format timestamp
        time_str = timestamp.strftime("%H:%M") if isinstance(timestamp, datetime) else "Recently"
        
        colors = self.theme_colors
        
        return f"""
        <div style="
            background: {colors['surface']};
            border: 1px solid {colors['primary']}30;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.2s ease;
        " onmouseover="this.style.borderColor='{colors['primary']}'" 
           onmouseout="this.style.borderColor='{colors['primary']}30'">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 500; color: {colors['text']};">{name}</div>
                <div style="font-size: 0.8rem; color: {colors['text']}cc; margin-top: 0.2rem;">
                    {size_str} • {time_str}
                </div>
            </div>
        </div>
        """
    
    def create_conversation_card(self, conversation_summary: Dict[str, Any], 
                               is_active: bool = False) -> str:
        """
        Create a conversation card for the conversation list.
        
        Conversation cards provide an overview of chat history and help users
        navigate between different conversation threads. The design emphasizes
        important information while maintaining visual consistency.
        """
        title = conversation_summary.get('title', 'Untitled Conversation')
        message_count = conversation_summary.get('total_messages', 0)
        updated_at = conversation_summary.get('updated_at', datetime.now())
        models_used = conversation_summary.get('models_used', [])
        is_favorite = conversation_summary.get('is_favorite', False)
        
        # Format update time
        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            except:
                updated_at = datetime.now()
        
        time_diff = datetime.now() - updated_at
        if time_diff.days > 0:
            time_str = f"{time_diff.days}d ago"
        elif time_diff.seconds > 3600:
            time_str = f"{time_diff.seconds // 3600}h ago"
        elif time_diff.seconds > 60:
            time_str = f"{time_diff.seconds // 60}m ago"
        else:
            time_str = "Just now"
        
        colors = self.theme_colors
        
        # Active state styling
        active_style = ""
        if is_active:
            active_style = f"border-left: 4px solid {colors['primary']}; background: {colors['primary']}10;"
        
        # Favorite indicator
        favorite_icon = "⭐" if is_favorite else ""
        
        # Model badges
        model_badges = ""
        if models_used:
            model_badges = " ".join([
                f'<span style="background: {colors["accent"]}; color: white; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.7rem;">{model}</span>'
                for model in models_used[:2]  # Show first 2 models
            ])
        
        return f"""
        <div style="
            background: {colors['surface']};
            border: 1px solid {colors['primary']}20;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.2s ease;
            {active_style}
        " onmouseover="this.style.borderColor='{colors['primary']}'" 
           onmouseout="this.style.borderColor='{colors['primary']}20'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                <div style="font-weight: 500; color: {colors['text']}; flex: 1;">{title} {favorite_icon}</div>
                <div style="font-size: 0.8rem; color: {colors['text']}cc;">{time_str}</div>
            </div>
            <div style="font-size: 0.8rem; color: {colors['text']}cc; margin-bottom: 0.5rem;">
                {message_count} messages
            </div>
            <div>{model_badges}</div>
        </div>
        """
    
    def show_typing_indicator(self):
        """
        Display a typing indicator while the AI is generating a response.
        
        Typing indicators provide immediate feedback that the system is working
        on a response. This reduces perceived wait time and improves the
        conversational feel of the interface.
        """
        st.markdown("""
        <div class="message-container assistant-message typing-indicator">
            <div class="message-header">
                <span><strong>🤖 AI Assistant</strong></span>
            </div>
            <div class="message-content">
                <em>Thinking...</em> 💭
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def create_feature_showcase(self, features: List[Dict[str, str]]):
        """
        Create a feature showcase grid for the welcome screen.
        
        Feature showcases help new users understand what the application can do.
        This implementation creates an engaging grid layout that highlights
        key capabilities while maintaining visual appeal.
        """
        colors = self.theme_colors
        
        # Create feature cards in a responsive grid
        cols = st.columns(len(features))
        
        for i, feature in enumerate(features):
            with cols[i]:
                icon = feature.get('icon', '⚡')
                title = feature.get('title', 'Feature')
                description = feature.get('description', 'Description')
                
                st.markdown(f"""
                <div style="
                    background: {colors['surface']};
                    border: 1px solid {colors['primary']}30;
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    height: 200px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    transition: all 0.3s ease;
                " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.15)'"
                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                    <div style="font-weight: 600; color: {colors['primary']}; margin-bottom: 0.5rem;">{title}</div>
                    <div style="font-size: 0.9rem; color: {colors['text']}cc; line-height: 1.4;">{description}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def create_toast_notification(self, message: str, notification_type: str = "info", 
                                duration: int = 3000):
        """
        Create toast notifications for user feedback.
        
        Toast notifications provide non-intrusive feedback about user actions.
        They appear temporarily and disappear automatically, making them perfect
        for confirmations, warnings, and status updates.
        """
        colors = {
            'success': '#10B981',
            'error': '#EF4444',
            'warning': '#F59E0B',
            'info': self.theme_colors['primary']
        }
        
        color = colors.get(notification_type, colors['info'])
        
        # Use Streamlit's built-in notification system
        if notification_type == 'success':
            st.success(message)
        elif notification_type == 'error':
            st.error(message)
        elif notification_type == 'warning':
            st.warning(message)
        else:
            st.info(message)
    
    def create_empty_state(self, title: str, description: str, 
                          action_text: Optional[str] = None, 
                          icon: str = "📭"):
        """
        Create empty state displays for when there's no content.
        
        Empty states guide users when there's no data to display. Instead of
        showing blank screens, we provide helpful information and clear next steps.
        This improves user experience by reducing confusion and providing direction.
        """
        colors = self.theme_colors
        
        empty_state_html = f"""
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            color: {colors['text']}cc;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.6;">{icon}</div>
            <h3 style="color: {colors['text']}; margin-bottom: 1rem;">{title}</h3>
            <p style="font-size: 1.1rem; margin-bottom: 2rem; max-width: 400px; margin-left: auto; margin-right: auto;">
                {description}
            </p>
        </div>
        """
        
        st.markdown(empty_state_html, unsafe_allow_html=True)
        
        if action_text:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                return st.button(action_text, type="primary", use_container_width=True)
        
        return False