"""gTTS helper — converts AI response text to MP3 audio bytes for Streamlit."""

import io
from gtts import gTTS


LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh",
}


def text_to_audio_bytes(text: str, language_name: str = "English") -> bytes | None:
    """Convert text to MP3 audio bytes using gTTS.

    Returns raw MP3 bytes that can be passed to st.audio(), or None on failure.
    """
    lang_code = LANG_CODES.get(language_name, "en")
    try:
        tts = gTTS(text=text[:3000], lang=lang_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None
