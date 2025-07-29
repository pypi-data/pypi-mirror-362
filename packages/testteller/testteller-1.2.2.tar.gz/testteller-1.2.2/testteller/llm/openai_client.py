"""
OpenAI API client implementation.
"""
import asyncio
import logging
import os
from typing import List

import openai
from pydantic import SecretStr

from testteller.config import settings
from testteller.constants import DEFAULT_OPENAI_GENERATION_MODEL, DEFAULT_OPENAI_EMBEDDING_MODEL
from testteller.utils.retry_helpers import api_retry_async, api_retry_sync

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for interacting with OpenAI's API."""

    def __init__(self):
        """Initialize the OpenAI client with API key from settings or environment."""
        self.api_key = self._get_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)
        self.async_client = openai.AsyncOpenAI(api_key=self.api_key)

        # Get model names from settings
        try:
            if settings and settings.llm:
                self.generation_model = settings.llm.__dict__.get(
                    'openai_generation_model', DEFAULT_OPENAI_GENERATION_MODEL)
                self.embedding_model = settings.llm.__dict__.get(
                    'openai_embedding_model', DEFAULT_OPENAI_EMBEDDING_MODEL)
            else:
                self.generation_model = DEFAULT_OPENAI_GENERATION_MODEL
                self.embedding_model = DEFAULT_OPENAI_EMBEDDING_MODEL
        except Exception as e:
            logger.warning(
                "Could not get model names from settings: %s. Using defaults.", e)
            self.generation_model = DEFAULT_OPENAI_GENERATION_MODEL
            self.embedding_model = DEFAULT_OPENAI_EMBEDDING_MODEL

        logger.info("Initialized OpenAI client with generation model '%s' and embedding model '%s'",
                    self.generation_model, self.embedding_model)

    def _get_api_key(self) -> str:
        """Get API key from settings or environment variables."""
        try:
            if settings and settings.api_keys:
                api_key = settings.api_keys.__dict__.get('openai_api_key')
                if api_key and isinstance(api_key, SecretStr):
                    return api_key.get_secret_value()
        except Exception as e:
            logger.debug("Could not get API key from settings: %s", e)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it in .env file as OPENAI_API_KEY "
                "or provide it through settings configuration."
            )
        return api_key

    @api_retry_async
    async def get_embedding_async(self, text: str) -> List[float]:
        """
        Get embeddings for text asynchronously.

        Args:
            text: Text to get embeddings for

        Returns:
            List of embedding values
        """
        if not text or not text.strip():
            logger.warning(
                "Empty text provided for embedding, returning None.")
            return None
        try:
            response = await self.async_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(
                "Error generating embedding for text: '%s...': %s", text[:50], e, exc_info=True)
            return None

    @api_retry_sync
    def get_embedding_sync(self, text: str) -> List[float]:
        """
        Get embeddings for text synchronously.

        Args:
            text: Text to get embeddings for

        Returns:
            List of embedding values
        """
        if not text or not text.strip():
            logger.warning(
                "Empty text provided for embedding, returning None.")
            return None
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(
                "Error generating embedding for text: '%s...': %s", text[:50], e, exc_info=True)
            return None

    @api_retry_sync
    def get_embeddings_sync(self, texts: list[str]) -> list[list[float] | None]:
        """
        Get embeddings for a list of texts synchronously in a single batch.

        Args:
            texts: List of texts to get embeddings for

        Returns:
            List of embedding lists, with None for failed texts.
        """
        if not texts:
            return []

        try:
            # Replace any empty strings with a single space to avoid API errors
            processed_texts = [text if text.strip() else " " for text in texts]

            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=processed_texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(
                "Error generating sync embeddings for a batch of %d texts: %s", len(texts), e, exc_info=True)
            # Return a list of Nones to indicate failure for all texts in the batch
            return [None] * len(texts)

    @api_retry_async
    async def generate_text_async(self, prompt: str) -> str:
        """
        Generate text using the OpenAI model asynchronously.

        Args:
            prompt: The input prompt for text generation

        Returns:
            Generated text response
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.generation_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Error generating text with OpenAI async: %s", e)
            raise

    @api_retry_sync
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the OpenAI model.

        Args:
            prompt: The input prompt for text generation

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.generation_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Error generating text with OpenAI: %s", e)
            raise
