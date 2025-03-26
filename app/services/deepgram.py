import asyncio
import traceback
import openai
from app.core.config import settings
from app.core.logger import logger

# OpenAI API Key
openai.api_key = settings.openai_api_key

async def start_live_transcription(callback):
    """Start a live transcription connection using OpenAI's real-time API."""
    try:
        async def on_transcription(data):
            """Handle incoming transcription results."""
            try:
                if "text" in data:
                    text = data["text"]
                    if text.strip():
                        logger.info(f"Transcription received: {text}")
                        if callback:
                            await callback(text)
            except Exception as e:
                logger.error(f"Error handling transcript: {e}")

        async def stream_audio():
            """OpenAI's real-time streaming transcription using transcriptions.create()."""
            try:
                response = openai.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    language="en",  # Adjust as needed
                    response_format="text",  # Ensuring text output
                    stream=True  # Streaming format
                )

                logger.info("Live transcription started")

                async for result in response:
                    await on_transcription(result)

            except Exception as e:
                logger.error(f"Error during transcription: {e}")
                traceback.print_exc()

        asyncio.create_task(stream_audio())

    except Exception as e:
        logger.error(f"Error starting live transcription: {e}")
        traceback.print_exc()
        raise

async def send_audio(audio_data):
    """Send audio data to OpenAI's live transcription."""
    try:
        response = openai.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            language="en",
            response_format="text",
            audio=audio_data
        )
        logger.info(f"Audio sent for transcription: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending audio to OpenAI: {e}")
        raise

async def close():
    """Close the live transcription connection."""
    logger.info("Transcription session ended.")
