import logging

from typing import Dict, List

import openai

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ..settings import SUPPORTAL_SETTINGS

logger = logging.getLogger("django_supportal")


class AIService:
    def __init__(self):
        openai.api_key = SUPPORTAL_SETTINGS["OPENAI_API_KEY"]
        self.model = SUPPORTAL_SETTINGS["OPENAI_MODEL"]
        self.embedding_model = SUPPORTAL_SETTINGS["OPENAI_EMBEDDING_MODEL"]
        self.max_tokens = SUPPORTAL_SETTINGS["MAX_TOKENS"]
        self.temperature = SUPPORTAL_SETTINGS["TEMPERATURE"]

    async def generate_response(
        self, messages: List[Dict[str, str]], context: str = ""
    ) -> str:
        """generate ai response using openai chat completion"""
        try:
            system_prompt = self._create_system_prompt(context)

            full_messages = [{"role": "system", "content": system_prompt}] + messages

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=full_messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"error generating ai response: {str(e)}")
            return _(
                "Sorry, I'm having trouble processing your request right now. please try again"
            )

    def generate_embedding(self, text: str) -> List[float]:
        """generate embedding for text using openai embeddings"""
        try:
            response = openai.Embedding.create(model=self.embedding_model, input=text)
            return response["data"][0]["embedding"]
        except Exception as e:
            logger.error(f"error generating embedding: {str(e)}")
            return []

    def _create_system_prompt(self, context: str) -> str:
        """create system prompt with context"""
        base_prompt = f"""you are a helpful customer support assistant. you have access to business documents and information.
        use the provided context to answer questions accurately and helpfully.
        if you don't know the answer based on the context, say so politely.
        keep responses concise and professional. Also response must be on this language: {settings.LANGUAGE_CODE}."""

        if context:
            return f"{base_prompt}\n\ncontext information:\n{context}"

        return base_prompt

    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
