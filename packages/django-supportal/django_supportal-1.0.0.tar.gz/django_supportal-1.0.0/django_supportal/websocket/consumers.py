import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import Business, ChatMessage, ChatSession
from ..services.ai_service import AIService
from ..services.vector_service import VectorService

logger = logging.getLogger("django_supportal")


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.business_id = None
        self.session_id = None
        self.room_group_name = None
        self.ai_service = AIService()
        self.vector_service = VectorService()

    async def connect(self):
        self.business_id = self.scope["url_route"]["kwargs"]["business_id"]
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room_group_name = f"chat_{self.business_id}_{self.session_id}"

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # create or get chat session
        await self.get_or_create_chat_session()

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            message_type = text_data_json.get("type", "user")

            if message_type == "user":
                await self.handle_user_message(message)
            elif message_type == "system":
                await self.handle_system_message(message)

        except Exception as e:
            logger.error(f"error in websocket receive: {str(e)}")
            await self.send(
                text_data=json.dumps({"error": _("Failed to process message")})
            )

    async def handle_user_message(self, message):
        """handle user message and generate ai response"""
        try:
            # save user message
            await self.save_message("user", message)

            # send user message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": "user",
                },
            )

            # get relevant context using rag
            context = await self.get_context_for_query(message)

            # get conversation history
            messages = await self.get_conversation_history()

            # generate ai response
            ai_response = await self.ai_service.generate_response(messages, context)

            # save ai response
            await self.save_message("assistant", ai_response)

            # send ai response to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": ai_response,
                    "sender": "assistant",
                },
            )

        except Exception as e:
            logger.error(f"error handling user message: {str(e)}")
            await self.send_error_message(
                _("sorry, I encountered an error processing your message")
            )

    async def handle_system_message(self, message):
        """handle system messages"""
        await self.save_message("system", message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": "system",
            },
        )

    async def chat_message(self, event):
        """receive message from room group"""
        message = event["message"]
        sender = event["sender"]

        # send message to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                    "timestamp": str(timezone.now()),
                }
            )
        )

    async def send_error_message(self, error_message):
        """send error message to client"""
        await self.send(
            text_data=json.dumps(
                {
                    "error": error_message,
                    "sender": "system",
                }
            )
        )

    @database_sync_to_async
    def get_or_create_chat_session(self):
        """get or create chat session"""

        try:
            business = Business.objects.get(id=self.business_id)
            session, created = ChatSession.objects.get_or_create(
                business=business,
                session_id=self.session_id,
                defaults={"is_active": True},
            )
            return session
        except Business.DoesNotExist:
            logger.error(f"business {self.business_id} not found")
            return None

    @database_sync_to_async
    def save_message(self, message_type, content):
        """save message to database"""

        try:
            session = ChatSession.objects.get(
                business_id=self.business_id, session_id=self.session_id
            )

            ChatMessage.objects.create(
                session=session, message_type=message_type, content=content
            )
        except ChatSession.DoesNotExist:
            logger.error(f"chat session not found: {self.session_id}")

    @database_sync_to_async
    def get_conversation_history(self):
        """get recent conversation history"""

        try:
            session = ChatSession.objects.get(
                business_id=self.business_id, session_id=self.session_id
            )

            messages = ChatMessage.objects.filter(session=session).order_by(
                "-created_at"
            )[:10]

            conversation = []
            for msg in reversed(messages):
                if msg.message_type in ["user", "assistant"]:
                    conversation.append(
                        {"role": msg.message_type, "content": msg.content}
                    )

            return conversation
        except ChatSession.DoesNotExist:
            return []

    async def get_context_for_query(self, query):
        """get relevant context using rag"""
        try:
            # generate query embedding
            query_embedding = self.ai_service.generate_embedding(query)

            if not query_embedding:
                return ""

            # search for similar chunks
            similar_chunks = self.vector_service.search_similar_chunks(
                self.business_id, query_embedding
            )

            # combine chunks into context
            context = self.vector_service.get_context_from_chunks(similar_chunks)

            return context

        except Exception as e:
            logger.error(f"error getting context for query: {str(e)}")
            return ""
