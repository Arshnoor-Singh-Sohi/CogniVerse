"""
Conversation Management System

This module demonstrates several advanced software engineering concepts that are crucial
for building robust, user-friendly applications:

1. State Management: How to track and persist conversation data across sessions
2. Data Persistence: Storing conversations so users don't lose their chat history
3. Memory Management: Efficiently handling large conversation histories
4. Search and Retrieval: Finding specific conversations or messages quickly
5. Import/Export: Allowing users to backup and share their conversations

Think of this class as a librarian for your conversations - it knows where everything
is stored, can find what you're looking for quickly, and keeps everything organized.
"""

import json
import uuid
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging
import csv
import io

from config.settings import AppConfig

logger = logging.getLogger(__name__)

class ConversationMessage:
    """
    Represents a single message in a conversation.
    
    Using a class for messages might seem like overkill for simple text, but it provides
    several benefits:
    - Type safety: We know exactly what properties a message has
    - Extensibility: Easy to add new features like reactions, formatting, or metadata
    - Validation: We can ensure messages are properly formed
    - Serialization: Easy conversion to/from JSON for storage
    """
    
    def __init__(
        self, 
        content: str, 
        role: str, 
        timestamp: Optional[datetime] = None,
        model_used: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        self.id = str(uuid.uuid4())  # Unique identifier for each message
        self.content = content
        self.role = role  # 'user' or 'assistant'
        self.timestamp = timestamp or datetime.now()
        self.model_used = model_used  # Which AI model generated this response
        self.metadata = metadata or {}  # Additional data like file attachments, ratings, etc.
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary for JSON serialization.
        
        This method demonstrates the concept of serialization - converting complex
        objects into simple data structures that can be easily stored or transmitted.
        """
        return {
            'id': self.id,
            'content': self.content,
            'role': self.role,
            'timestamp': self.timestamp.isoformat(),
            'model_used': self.model_used,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationMessage':
        """
        Create a message object from a dictionary.
        
        This is the reverse of to_dict() - deserializing data back into objects.
        The @classmethod decorator makes this a factory method that creates instances.
        """
        message = cls(
            content=data['content'],
            role=data['role'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            model_used=data.get('model_used'),
            metadata=data.get('metadata', {})
        )
        message.id = data['id']  # Preserve the original ID
        return message

class Conversation:
    """
    Represents a complete conversation thread.
    
    A conversation is more than just a list of messages - it has its own identity,
    metadata, and behavior. This class encapsulates all conversation-related logic
    in one place, making the code more organized and maintainable.
    """
    
    def __init__(
        self, 
        title: str = "New Conversation", 
        conversation_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = conversation_id or str(uuid.uuid4())
        self.title = title
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()
        self.messages: List[ConversationMessage] = []
        self.metadata = {
            'total_messages': 0,
            'models_used': set(),
            'tags': [],
            'is_favorite': False
        }
    
    def add_message(self, content: str, role: str, model_used: Optional[str] = None) -> ConversationMessage:
        """
        Add a new message to the conversation.
        
        This method demonstrates encapsulation - the conversation manages its own
        internal state and ensures consistency. Notice how we update multiple
        pieces of related data together.
        """
        message = ConversationMessage(
            content=content,
            role=role,
            model_used=model_used
        )
        
        self.messages.append(message)
        self.updated_at = datetime.now()
        self.metadata['total_messages'] = len(self.messages)
        
        # Track which models have been used in this conversation
        if model_used:
            self.metadata['models_used'].add(model_used)
        
        # Auto-generate title from first user message if still default
        if self.title == "New Conversation" and role == 'user' and len(self.messages) == 1:
            self.title = self._generate_title_from_content(content)
        
        return message
    
    def _generate_title_from_content(self, content: str) -> str:
        """
        Generate a conversation title from the first message.
        
        This is a nice user experience touch - instead of having generic titles,
        we create meaningful ones based on what the user is actually discussing.
        """
        # Take first 50 characters and clean up
        title = content.strip()[:50]
        if len(content) > 50:
            title += "..."
        
        # Remove newlines and excessive whitespace
        title = " ".join(title.split())
        
        return title or "New Conversation"
    
    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """Get the most recent messages from the conversation."""
        return self.messages[-count:] if self.messages else []
    
    def search_messages(self, query: str) -> List[ConversationMessage]:
        """
        Search for messages containing specific text.
        
        This enables users to find specific information within long conversations.
        In a production system, you might use more sophisticated search techniques
        like fuzzy matching or semantic search.
        """
        query_lower = query.lower()
        return [
            message for message in self.messages
            if query_lower in message.content.lower()
        ]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of conversation statistics.
        
        This provides users with insights about their conversation patterns
        and helps them understand their usage of the application.
        """
        user_messages = [m for m in self.messages if m.role == 'user']
        assistant_messages = [m for m in self.messages if m.role == 'assistant']
        
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'total_messages': len(self.messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'models_used': list(self.metadata['models_used']),
            'duration': self.updated_at - self.created_at,
            'is_favorite': self.metadata.get('is_favorite', False)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary for storage."""
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': [message.to_dict() for message in self.messages],
            'metadata': {
                **self.metadata,
                'models_used': list(self.metadata['models_used'])  # Convert set to list for JSON
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create conversation from dictionary."""
        conversation = cls(
            title=data['title'],
            conversation_id=data['id'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        conversation.updated_at = datetime.fromisoformat(data['updated_at'])
        
        # Restore messages
        for message_data in data.get('messages', []):
            message = ConversationMessage.from_dict(message_data)
            conversation.messages.append(message)
        
        # Restore metadata
        conversation.metadata = data.get('metadata', {})
        if 'models_used' in conversation.metadata:
            conversation.metadata['models_used'] = set(conversation.metadata['models_used'])
        
        return conversation

class ChatManager:
    """
    The central hub for managing all conversation-related operations.
    
    This class demonstrates the Manager pattern - it coordinates between different
    components and provides a clean interface for conversation operations. Think of
    it as the conductor of an orchestra, making sure all the conversation pieces
    work together harmoniously.
    """
    
    def __init__(self):
        self.config = AppConfig()
        self.conversations: Dict[str, Conversation] = {}
        
        # Initialize from session state if available
        self._load_from_session_state()
        
        logger.info("ChatManager initialized")
    
    def _load_from_session_state(self):
        """
        Load conversations from Streamlit's session state.
        
        Session state is Streamlit's way of maintaining data between page refreshes.
        It's like the application's short-term memory - it remembers things during
        a user's session but forgets them when they close the browser.
        """
        if 'conversations' in st.session_state:
            # Convert stored dictionaries back to Conversation objects
            for conv_id, conv_data in st.session_state.conversations.items():
                if isinstance(conv_data, dict):
                    self.conversations[conv_id] = Conversation.from_dict(conv_data)
                else:
                    # Already a Conversation object
                    self.conversations[conv_id] = conv_data
    
    def _save_to_session_state(self):
        """
        Save conversations to session state.
        
        This ensures that conversations persist as users navigate through the app.
        We convert our Conversation objects to dictionaries because session state
        works best with simple data types.
        """
        st.session_state.conversations = {
            conv_id: conv.to_dict() for conv_id, conv in self.conversations.items()
        }
    
    def create_new_conversation(self, title: str = "New Conversation") -> str:
        """
        Create a new conversation and make it the active one.
        
        This method demonstrates how to properly initialize new objects while
        maintaining consistency across the application state.
        """
        conversation = Conversation(title=title)
        self.conversations[conversation.id] = conversation
        
        # Update session state
        st.session_state.current_conversation_id = conversation.id
        self._save_to_session_state()
        
        logger.info(f"Created new conversation: {conversation.id}")
        return conversation.id
    
    def get_current_conversation(self) -> Optional[Conversation]:
        """
        Get the currently active conversation.
        
        This method handles the common case where we need to work with whatever
        conversation the user is currently viewing. It includes error handling
        for edge cases and ensures a conversation always exists.
        """
        current_id = st.session_state.get('current_conversation_id')
        
        # If no current conversation ID, create a new one
        if not current_id:
            current_id = self.create_new_conversation()
            return self.conversations.get(current_id)
        
        # Check if the conversation exists in our memory
        if current_id in self.conversations:
            return self.conversations[current_id]
        
        # If conversation ID exists but conversation is missing, create new one
        logger.warning(f"Conversation {current_id} not found, creating new one")
        current_id = self.create_new_conversation()
        return self.conversations.get(current_id)
    
    def add_message(self, user_input: str, ai_response: str, model_used: str) -> bool:
        """
        Add a user-AI exchange to the current conversation.
        
        This method demonstrates transaction-like behavior - we add both messages
        together to maintain conversation integrity. In a database system, this
        might be wrapped in a transaction.
        """
        try:
            conversation = self.get_current_conversation()
            if not conversation:
                logger.error("No current conversation available")
                return False
            
            # Add both messages in order
            conversation.add_message(user_input, 'user')
            conversation.add_message(ai_response, 'assistant', model_used)
            
            # Persist the changes
            self._save_to_session_state()
            
            logger.info(f"Added message exchange to conversation {conversation.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return False
    
    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the message history for a conversation.
        
        This method converts our internal message objects into a format that's
        easy for UI components to work with. This separation between internal
        data structures and UI data is a key principle in clean architecture.
        """
        if not conversation_id:
            conversation = self.get_current_conversation()
        else:
            conversation = self.conversations.get(conversation_id)
        
        if not conversation:
            return []
        
        # Convert messages to a format suitable for UI display
        history = []
        for message in conversation.messages:
            history.append({
                'id': message.id,
                'content': message.content,
                'role': message.role,
                'timestamp': message.timestamp,
                'model_used': message.model_used,
                'metadata': message.metadata
            })
        
        return history
    
    def get_recent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent message history for context purposes."""
        full_history = self.get_conversation_history()
        return full_history[-limit:] if full_history else []
    
    def search_conversations(self, query: str) -> List[Dict[str, Any]]:
        """
        Search across all conversations for specific content.
        
        This provides a powerful way for users to find information across
        their entire conversation history. The results include context about
        which conversation contained the matching content.
        """
        results = []
        
        for conversation in self.conversations.values():
            matching_messages = conversation.search_messages(query)
            if matching_messages:
                results.append({
                    'conversation_id': conversation.id,
                    'conversation_title': conversation.title,
                    'matching_messages': len(matching_messages),
                    'messages': [msg.to_dict() for msg in matching_messages[:3]]  # Show top 3 matches
                })
        
        # Sort by number of matches (most relevant first)
        results.sort(key=lambda x: x['matching_messages'], reverse=True)
        return results
    
    def export_conversation(self, conversation_id: Optional[str] = None, format: str = 'json') -> bytes:
        """
        Export a conversation in various formats.
        
        This feature demonstrates how to make data portable - users can backup
        their conversations or share them with others. Different formats serve
        different purposes: JSON for programmatic use, CSV for spreadsheets, etc.
        """
        conversation = self.conversations.get(conversation_id) if conversation_id else self.get_current_conversation()
        
        if not conversation:
            raise ValueError("No conversation to export")
        
        if format.lower() == 'json':
            return self._export_as_json(conversation)
        elif format.lower() == 'csv':
            return self._export_as_csv(conversation)
        elif format.lower() == 'txt':
            return self._export_as_text(conversation)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_as_json(self, conversation: Conversation) -> bytes:
        """Export conversation as JSON with full metadata."""
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'application': 'CogniVerse',
                'version': self.config.app_version
            },
            'conversation': conversation.to_dict()
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False).encode('utf-8')
    
    def _export_as_csv(self, conversation: Conversation) -> bytes:
        """Export conversation as CSV for spreadsheet analysis."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Timestamp', 'Role', 'Content', 'Model Used'])
        
        # Write messages
        for message in conversation.messages:
            writer.writerow([
                message.timestamp.isoformat(),
                message.role,
                message.content.replace('\n', ' '),  # Replace newlines for CSV compatibility
                message.model_used or 'N/A'
            ])
        
        return output.getvalue().encode('utf-8')
    
    def _export_as_text(self, conversation: Conversation) -> bytes:
        """Export conversation as readable text format."""
        lines = [
            f"Conversation: {conversation.title}",
            f"Created: {conversation.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Messages: {len(conversation.messages)}",
            "=" * 50,
            ""
        ]
        
        for message in conversation.messages:
            timestamp = message.timestamp.strftime('%H:%M:%S')
            role = "You" if message.role == 'user' else "AI"
            lines.append(f"[{timestamp}] {role}: {message.content}")
            lines.append("")
        
        return '\n'.join(lines).encode('utf-8')
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Generate comprehensive statistics about all conversations.
        
        This provides insights that help users understand their usage patterns
        and helps developers understand how the application is being used.
        """
        if not self.conversations:
            return {
                'total_conversations': 0,
                'total_messages': 0,
                'average_messages_per_conversation': 0,
                'most_used_models': {},
                'conversation_activity': {}
            }
        
        total_messages = sum(len(conv.messages) for conv in self.conversations.values())
        
        # Count model usage
        model_usage = {}
        for conversation in self.conversations.values():
            for model in conversation.metadata.get('models_used', []):
                model_usage[model] = model_usage.get(model, 0) + 1
        
        # Activity by date
        activity_by_date = {}
        for conversation in self.conversations.values():
            date_key = conversation.created_at.date().isoformat()
            activity_by_date[date_key] = activity_by_date.get(date_key, 0) + 1
        
        return {
            'total_conversations': len(self.conversations),
            'total_messages': total_messages,
            'average_messages_per_conversation': total_messages / len(self.conversations),
            'most_used_models': dict(sorted(model_usage.items(), key=lambda x: x[1], reverse=True)),
            'conversation_activity': activity_by_date,
            'oldest_conversation': min(conv.created_at for conv in self.conversations.values()),
            'newest_conversation': max(conv.created_at for conv in self.conversations.values())
        }
    
    def cleanup_old_conversations(self, days_old: int = 30):
        """
        Remove conversations older than specified days.
        
        This helps manage storage and keeps the application responsive by
        removing very old data that users might not need anymore.
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        conversations_to_remove = []
        
        for conv_id, conversation in self.conversations.items():
            if conversation.updated_at < cutoff_date and not conversation.metadata.get('is_favorite'):
                conversations_to_remove.append(conv_id)
        
        for conv_id in conversations_to_remove:
            del self.conversations[conv_id]
            logger.info(f"Removed old conversation: {conv_id}")
        
        self._save_to_session_state()
        return len(conversations_to_remove)