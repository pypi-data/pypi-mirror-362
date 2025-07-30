import re
import asyncio


# Helper function to handle streaming response and chunking
async def stream_sentences(streaming_response, punctuation_marks=None, clean_text=True):
    """
    Streams OpenAI or Google Gemini response and yields complete sentences as strings.

    Args:
        streaming_response: The streaming response from OpenAI or Google Gemini
        punctuation_marks: Optional set of punctuation marks to use for sentence boundaries
                          Defaults to ['.', '!', '?', '\n']
        clean_text: Whether to clean markdown and special characters for speech
                   Defaults to True

    Yields:
        str: Complete sentences as they are formed
    """
    sentence_buffer = ""

    # Check if this is an async iterator (OpenAI) or sync iterator (Gemini)
    if hasattr(streaming_response, "__aiter__"):
        # OpenAI async streaming
        async for chunk in streaming_response:
            tool_calls = _extract_tool_calls_from_chunk(chunk)
            if tool_calls:
                yield {"tool_calls": tool_calls}

            content = _extract_content_from_chunk(chunk)
            sentence_buffer, complete_sentence = _update_sentence_buffer(
                content,
                sentence_buffer,
                punctuation_marks,
                clean_text,
            )

            if complete_sentence:
                yield {"content": complete_sentence}
    else:
        # Gemini sync streaming - wrap in async to prevent blocking
        for chunk in streaming_response:
            content = _extract_content_from_chunk(chunk)
            sentence_buffer, complete_sentence = _update_sentence_buffer(
                content,
                sentence_buffer,
                punctuation_marks,
                clean_text,
            )

            if complete_sentence:
                yield {"content": complete_sentence}

            # Yield control to prevent blocking the event loop
            await asyncio.sleep(0)

    # Handle any remaining text in buffer
    if sentence_buffer.strip():
        if clean_text:
            sentence_buffer = _clean_text_for_speech(sentence_buffer)

        if sentence_buffer:
            yield {"content": sentence_buffer}


def _extract_tool_calls_from_chunk(chunk):
    if hasattr(chunk, "choices") and chunk.choices:
        if hasattr(chunk.choices[0], "delta") and hasattr(
            chunk.choices[0].delta, "tool_calls"
        ):
            return chunk.choices[0].delta.tool_calls or ""
    return ""


def _extract_content_from_chunk(chunk):
    """
    Extract content from streaming chunk, supporting OpenAI and Direct Gemini API formats only.

    Args:
        chunk: The streaming chunk from either OpenAI or Google Gemini (direct API)

    Returns:
        str: The content text from the chunk, or empty string if no content
    """
    # OpenAI format: chunk.choices[0].delta.content
    if hasattr(chunk, "choices") and chunk.choices:
        if hasattr(chunk.choices[0], "delta") and hasattr(
            chunk.choices[0].delta, "content"
        ):
            return chunk.choices[0].delta.content or ""

    # Google Gemini Direct API format: chunk.text
    if hasattr(chunk, "text"):
        return chunk.text or ""

    return ""


def _update_sentence_buffer(
    content, sentence_buffer, punctuation_marks=None, clean_text=True
):
    if punctuation_marks is None:
        punctuation_marks = [".", "!", "?", "\n"]

    if content:
        sentence_buffer += content

        # Check if we have a complete sentence (ends with punctuation)
        if any(punct in sentence_buffer for punct in punctuation_marks):
            # Find the last sentence boundary
            last_sentence_end = max(
                (sentence_buffer.rfind(punct) for punct in punctuation_marks),
                default=-1,
            )

            if last_sentence_end != -1:
                # Extract complete sentence
                complete_sentence = sentence_buffer[: last_sentence_end + 1]

                # Keep remaining text in buffer
                sentence_buffer = sentence_buffer[last_sentence_end + 1 :]

                # Clean and yield complete sentence
                if clean_text:
                    complete_sentence = _clean_text_for_speech(complete_sentence)

                if complete_sentence:
                    return sentence_buffer, complete_sentence

    return sentence_buffer, None


def _clean_text_for_speech(text):
    """
    Clean text for better speech synthesis by removing/replacing problematic characters,
    and ensure the sentence contains at least one alphanumeric character.

    Args:
        text: The text to clean

    Returns:
        str: Cleaned text suitable for speech synthesis, or empty string if no alphanumeric chars
    """
    if not text:
        return text

    # Remove markdown formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold** -> bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # *italic* -> italic
    text = re.sub(r"__(.*?)__", r"\1", text)  # __bold__ -> bold
    text = re.sub(r"_(.*?)_", r"\1", text)  # _italic_ -> italic
    text = re.sub(r"~~(.*?)~~", r"\1", text)  # ~~strikethrough~~ -> strikethrough
    text = re.sub(r"`(.*?)`", r"\1", text)  # `code` -> code

    # Remove markdown headers
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)  # # Header -> Header

    # Replace common symbols with spoken equivalents
    replacements = {
        "#": "hashtag ",
        "@": "at ",
        "&": "and ",
        "%": "percent ",
        "$": "dollar ",
        "+": "plus ",
        "=": "equals ",
        "<": "less than ",
        ">": "greater than ",
        "|": "pipe ",
        "\\": "backslash ",
        "/": "slash ",
        "^": "caret ",
        "~": "tilde ",
    }

    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)

    # Remove brackets and their content (often contains technical info)
    text = re.sub(r"\[.*?\]", "", text)  # [link text] ->
    text = re.sub(r"\{.*?\}", "", text)  # {code} ->

    # Clean up URLs (replace with "link")
    text = re.sub(r"https?://\S+", "link", text)
    text = re.sub(r"www\.\S+", "link", text)

    # Clean up email addresses
    text = re.sub(r"\S+@\S+\.\S+", "email address", text)

    # Clean up multiple spaces and newlines
    text = re.sub(r"\s+", " ", text)  # Multiple spaces -> single space
    text = re.sub(r"\n+", ". ", text)  # Multiple newlines -> period space

    # Remove leading/trailing whitespace
    text = text.strip()

    # Ensure the sentence contains at least one alphanumeric character
    if not re.search(r"[A-Za-z0-9]", text):
        return ""

    return text
