"""Streaming support for io Intelligence API."""

import json
from typing import Any, Dict, Iterator, Optional

import requests
from langchain_core.messages import AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk

from .exceptions import IOIntelligenceError, classify_api_error


class IOIntelligenceStreamer:
    """Handles streaming responses from io Intelligence API."""

    def __init__(self, api_key: str, api_url: str, timeout: int = 30):
        self.api_key = api_key
        self.api_url = api_url
        self.timeout = timeout

    def stream_chat_completion(self, data: Dict[str, Any]) -> Iterator[ChatGenerationChunk]:
        """Stream chat completion responses.

        Args:
            data: Request data dictionary

        Yields:
            ChatGenerationChunk objects for each token/chunk
        """
        # Enable streaming in request
        stream_data = data.copy()
        stream_data["stream"] = True

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        try:
            with requests.post(
                self.api_url, headers=headers, json=stream_data, stream=True, timeout=self.timeout
            ) as response:
                if not response.ok:
                    error = classify_api_error(response.status_code, response.text)
                    raise error

                # Process Server-Sent Events
                for chunk in self._parse_sse_stream(response):
                    if chunk:
                        yield chunk

        except requests.exceptions.RequestException as e:
            raise IOIntelligenceError(f"Streaming request failed: {str(e)}")

    def _parse_sse_stream(self, response) -> Iterator[ChatGenerationChunk]:
        """Parse Server-Sent Events stream.

        Args:
            response: Streaming HTTP response

        Yields:
            ChatGenerationChunk objects
        """
        for line in response.iter_lines(decode_unicode=True):
            if line is None:
                continue

            # SSE format: "data: {json}" or "data: [DONE]"
            if line.startswith("data: "):
                data_part = line[6:]  # Remove "data: " prefix

                # End of stream marker
                if data_part.strip() == "[DONE]":
                    break

                try:
                    chunk_data = json.loads(data_part)
                    chunk = self._create_chat_chunk(chunk_data)
                    if chunk:
                        yield chunk

                except json.JSONDecodeError:
                    # Skip malformed JSON
                    continue
                except Exception as e:
                    # Log error but continue streaming
                    print(f"Warning: Error processing chunk: {e}")
                    continue

    def _create_chat_chunk(self, chunk_data: Dict[str, Any]) -> Optional[ChatGenerationChunk]:
        """Create ChatGenerationChunk from API chunk data.

        Args:
            chunk_data: Raw chunk data from API

        Returns:
            ChatGenerationChunk or None if invalid
        """
        try:
            choices = chunk_data.get("choices", [])
            if not choices:
                return None

            choice = choices[0]
            delta = choice.get("delta", {})

            # Extract content from delta
            content = delta.get("content", "")
            finish_reason = choice.get("finish_reason")

            # Create message chunk
            message_chunk = AIMessageChunk(content=content)

            # Create generation chunk
            generation_chunk = ChatGenerationChunk(
                message=message_chunk,
                generation_info={
                    "finish_reason": finish_reason,
                    "model": chunk_data.get("model"),
                    "chunk_id": chunk_data.get("id"),
                },
            )

            return generation_chunk

        except (KeyError, TypeError):
            return None


def stream_text_from_chunks(chunks: Iterator[ChatGenerationChunk]) -> Iterator[str]:
    """Extract text content from streaming chunks.

    Args:
        chunks: Iterator of ChatGenerationChunk objects

    Yields:
        String content from each chunk
    """
    for chunk in chunks:
        if chunk.message and chunk.message.content:
            yield chunk.message.content


def accumulate_stream(chunks: Iterator[ChatGenerationChunk]) -> str:
    """Accumulate all streaming chunks into final text.

    Args:
        chunks: Iterator of ChatGenerationChunk objects

    Returns:
        Complete accumulated text
    """
    accumulated = []
    for chunk in chunks:
        if chunk.message and chunk.message.content:
            accumulated.append(chunk.message.content)

    return "".join(accumulated)
