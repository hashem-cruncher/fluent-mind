"""
تقسيم النص إلى مقاطع
"""

from typing import List
import streamlit as st
from fluent_mind.config.constants import COLORS
from fluent_mind.core.text_processor import normalize_arabic_text

def identify_syllable_pattern(word: str) -> List[str]:
    """تقسيم الكلمة إلى مقاطع"""
    syllables = []
    current_syllable = ""
    long_vowels = "اوي"
    syllable_endings = "ةهً" + long_vowels
    
    for i, char in enumerate(word):
        current_syllable += char
        if (char in long_vowels or 
            i == len(word) - 1 or 
            char in syllable_endings or 
            len(current_syllable) >= 3):
            if current_syllable.strip():
                syllables.append(current_syllable)
            current_syllable = ""
            continue
    
    if current_syllable.strip():
        syllables.append(current_syllable)
    
    return syllables

def format_word(word: str, color: str, is_short: bool = False) -> str:
    """تنسيق كلمة واحدة"""
    base_style = f"""
        display: inline-block;
        color: {color};
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        margin: 0 5px;
        font-size: 24px;
    """
    
    if is_short:
        return f'<span style="{base_style}">{word}</span>'
    
    syllables = identify_syllable_pattern(word)
    formatted_syllables = [
        f'<span style="color:{color};font-weight:bold;text-shadow:1px 1px 2px rgba(0,0,0,0.2);">{syllable}</span>'
        for syllable in syllables
    ]
    
    separator = f'<span style="color:{color};font-weight:normal;margin:0 1px;">-</span>'
    word_with_syllables = separator.join(formatted_syllables)
    
    return f'<span style="{base_style}">{word_with_syllables}</span>'

def split_into_syllables(text: str) -> str:
    """تقسيم النص العربي إلى مقاطع مع تنسيق"""
    normalized_text = normalize_arabic_text(text)
    words = normalized_text.split()
    result = []
    
    colors = COLORS[st.session_state.get('color_theme', 'default')]
    
    for word_idx, word in enumerate(words):
        color = colors[word_idx % len(colors)]
        is_short = len(word) <= 3
        result.append(format_word(word, color, is_short))
    
    bg_color = "#000000" if st.session_state.get('high_contrast', False) else "#111111"
    ui_scale = st.session_state.get('ui_scale', 1.0)
    reduce_motion = st.session_state.get('reduce_motion', True)
    
    return f'''
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 10px;
            line-height: 2.5;
            direction: rtl;
            text-align: right;
            transform: scale({ui_scale});
            transform-origin: top right;
            {'transition: none;' if reduce_motion else ''}
        ">
            {' '.join(result)}
        </div>
    ''' 