"""
محرك تحويل النص إلى كلام
"""

from typing import Tuple, List
from gtts import gTTS
from datetime import datetime
import os
from fluent_mind.core.text_processor import normalize_arabic_text, identify_difficult_words

def preprocess_text(text: str) -> Tuple[str, List[str]]:
    """معالجة النص قبل التحويل إلى كلام"""
    text = normalize_arabic_text(text)
    difficult_words = identify_difficult_words(text)
    text = add_pause_markers(text)
    return text, difficult_words

def add_pause_markers(text: str) -> str:
    """إضافة علامات التوقف للنص"""
    arabic_punctuation = '،؛؟.!۔'
    for punct in arabic_punctuation:
        text = text.replace(punct, punct + ' <pause> ')
    return text

def text_to_speech(text: str) -> Tuple[str, bool]:
    """الدالة الرئيسية لتحويل النص إلى كلام"""
    try:
        processed_text, _ = preprocess_text(text)
        
        tts = gTTS(
            text=processed_text,
            lang='ar'
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = f"speech_{timestamp}.mp3"
        tts.save(audio_file)
        
        return audio_file, True
    except Exception as e:
        return str(e), False 