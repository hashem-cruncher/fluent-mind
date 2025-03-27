import streamlit as st
from gtts import gTTS
import os
import re
import arabic_reshaper
from bidi.algorithm import get_display
import pyarabic.araby as araby
from pyarabic.normalize import normalize_hamza, normalize_lamalef
from typing import List, Tuple
import pyttsx3
import json
import time
from datetime import datetime
import threading
from queue import Queue
import pygame

# ثوابت التطبيق
COLORS = {
    'default': [
        "#FF6B6B",  # أحمر فاتح
        "#4ECDC4",  # تركواز
        "#45B7D1",  # أزرق فاتح
        "#96CEB4",  # أخضر فاتح
        "#FFEEAD",  # أصفر فاتح
        "#D4A5A5",  # وردي فاتح
        "#9B59B6",  # بنفسجي
        "#3498DB"   # أزرق
    ],
    'warm': [
        "#FF6B6B", "#FFB347", "#FF7F50", "#FFA07A",
        "#FFD700", "#F4A460", "#DEB887", "#D2691E"
    ],
    'cool': [
        "#4ECDC4", "#45B7D1", "#87CEEB", "#96CEB4",
        "#98FB98", "#87CEFA", "#B0E0E6", "#ADD8E6"
    ],
    'contrast': [
        "#FF0000", "#00FF00", "#0000FF", "#FFFF00",
        "#FF00FF", "#00FFFF", "#FFFFFF", "#000000"
    ]
}

# معالجة النص العربي
def normalize_arabic_text(text: str) -> str:
    """تطبيع النص العربي وتوحيد أشكال الحروف"""
    text = araby.strip_tatweel(text)
    text = normalize_hamza(text)
    text = normalize_lamalef(text)
    text = re.sub('[ةه]', 'ه', text)
    text = araby.reduce_tashkeel(text)
    return text

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
    
    # استخدام الألوان المناسبة حسب النمط المحدد
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

# محرك تحويل النص إلى كلام
class ArabicTTSEngine:
    def __init__(self):
        self.offline_engine = pyttsx3.init()
        self.offline_engine.setProperty('rate', 150)
        self.offline_engine.setProperty('volume', 1.0)
        pygame.mixer.init()
        
        self.voice_options = {
            'online': {
                'male': {'lang': 'ar', 'tld': 'com.sa'},
                'female': {'lang': 'ar', 'tld': 'com.eg'}
            },
            'offline': {
                'voices': self.offline_engine.getProperty('voices')
            }
        }
        
        self.arabic_punctuation = '،؛؟.!۔'
    
    def preprocess_text(self, text: str) -> Tuple[str, List[str]]:
        text = normalize_arabic_text(text)
        difficult_words = self.identify_difficult_words(text)
        text = self.add_pause_markers(text)
        return text, difficult_words
    
    def identify_difficult_words(self, text: str) -> List[str]:
        words = text.split()
        difficult_words = []
        similar_letters = {
            'ح': 'جخ', 'د': 'ذ', 'ر': 'ز', 'س': 'ش',
            'ص': 'ض', 'ط': 'ظ', 'ع': 'غ'
        }
        
        for word in words:
            if len(word) > 6:
                difficult_words.append(word)
                continue
            
            for char in word:
                if char in similar_letters and any(similar in word for similar in similar_letters[char]):
                    difficult_words.append(word)
                    break
        
        return difficult_words
    
    def add_pause_markers(self, text: str) -> str:
        for punct in self.arabic_punctuation:
            text = text.replace(punct, punct + ' <pause> ')
        return text
    
    def speak_online(self, text: str, voice_type: str = 'male', speed: float = 1.0) -> str:
        try:
            voice_params = self.voice_options['online'][voice_type]
            tts = gTTS(text=text, lang=voice_params['lang'], 
                      tld=voice_params['tld'], slow=(speed < 1.0))
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            audio_file = f"speech_{timestamp}.mp3"
            tts.save(audio_file)
            return audio_file
        except Exception as e:
            st.error(f"خطأ في تحويل النص إلى كلام: {str(e)}")
            return None
    
    def speak_offline(self, text: str, voice_idx: int = 0, 
                     speed: float = 1.0, pitch: float = 1.0) -> str:
        try:
            self.offline_engine.setProperty('rate', int(150 * speed))
            self.offline_engine.setProperty('voice', 
                self.voice_options['offline']['voices'][voice_idx].id)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            audio_file = f"speech_offline_{timestamp}.wav"
            
            self.offline_engine.save_to_file(text, audio_file)
            self.offline_engine.runAndWait()
            return audio_file
        except Exception as e:
            st.error(f"خطأ في تحويل النص إلى كلام محلياً: {str(e)}")
            return None

def text_to_speech(text: str, voice_settings: dict) -> Tuple[str, bool]:
    """تحويل النص إلى صوت مع دعم الخيارات المتقدمة"""
    tts_engine = ArabicTTSEngine()
    processed_text, difficult_words = tts_engine.preprocess_text(text)
    
    try:
        if voice_settings.get('use_offline', False):
            audio_file = tts_engine.speak_offline(
                processed_text,
                voice_idx=voice_settings.get('voice_idx', 0),
                speed=voice_settings.get('speed', 1.0),
                pitch=voice_settings.get('pitch', 1.0)
            )
        else:
            audio_file = tts_engine.speak_online(
                processed_text,
                voice_type=voice_settings.get('voice_type', 'male'),
                speed=voice_settings.get('speed', 1.0)
            )
        
        if audio_file:
            return audio_file, True
        return "فشل في إنشاء الملف الصوتي", False
    except Exception as e:
        return str(e), False

# تهيئة حالة التطبيق
def initialize_session_state():
    """تهيئة متغيرات الحالة للتطبيق"""
    if 'color_theme' not in st.session_state:
        st.session_state.color_theme = 'default'
    if 'ui_scale' not in st.session_state:
        st.session_state.ui_scale = 1.0
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    if 'reduce_motion' not in st.session_state:
        st.session_state.reduce_motion = True

# تكوين الصفحة
def setup_page():
    """إعداد تكوين الصفحة الرئيسية"""
    st.set_page_config(
        page_title="Fluent Mind - دعم ذوي عسر القراءة",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.example.com/help',
            'Report a bug': "https://www.example.com/bug",
            'About': "تطبيق Fluent Mind لدعم ذوي عسر القراءة"
        }
    )

# الشريط الجانبي
def render_sidebar():
    """عرض الشريط الجانبي مع الإعدادات"""
    with st.sidebar:
        st.header("الإعدادات العامة")
        
        st.subheader("إمكانية الوصول")
        st.session_state.ui_scale = st.slider(
            "حجم عناصر الواجهة",
            min_value=0.8,
            max_value=1.5,
            value=st.session_state.ui_scale,
            step=0.1
        )
        
        st.session_state.reduce_motion = st.checkbox(
            "تقليل الحركة",
            value=st.session_state.reduce_motion
        )
        
        st.session_state.high_contrast = st.checkbox(
            "تباين عالي",
            value=st.session_state.high_contrast
        )
        
        st.subheader("تخصيص الألوان")
        st.session_state.color_theme = st.selectbox(
            "نمط الألوان",
            options=['default', 'warm', 'cool', 'contrast'],
            format_func=lambda x: {
                'default': "الوضع الافتراضي",
                'warm': "ألوان دافئة",
                'cool': "ألوان باردة",
                'contrast': "ألوان متباينة"
            }[x]
        )

# الواجهة الرئيسية
def main():
    """الدالة الرئيسية للتطبيق"""
    initialize_session_state()
    setup_page()
    render_sidebar()
    
    # شريط التنقل العلوي
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("logo.png", width=100)
    with col2:
        st.title("Fluent Mind 🧠")
    
    # التبويبات الرئيسية
    tab1, tab2, tab3 = st.tabs([
        "تقسيم النص إلى مقاطع",
        "تحويل النص إلى كلام",
        "قراءة معززة"
    ])
    
    with tab1:
        render_syllable_tab()
    
    with tab2:
        render_tts_tab()
    
    with tab3:
        render_enhanced_reading_tab()

def render_syllable_tab():
    """عرض تبويب تقسيم النص إلى مقاطع"""
    st.markdown("""
        <div class="tab-content">
            <h2>أدخل النص ليتم تقسيمه إلى مقاطع</h2>
            <p>هذه الأداة تساعدك في تقسيم النص العربي إلى مقاطع سهلة القراءة</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_text = st.text_area(
        "النص الأصلي:",
        key="syllable_text",
        height=150,
        help="اكتب أو الصق النص العربي هنا"
    )
    
    if st.button("تقسيم النص", use_container_width=True):
        if user_text:
            with st.spinner("جاري تقسيم النص..."):
                result = split_into_syllables(user_text)
                st.markdown(result, unsafe_allow_html=True)
        else:
            st.warning("يرجى إدخال نص للتقسيم")

def render_tts_tab():
    """عرض تبويب تحويل النص إلى كلام"""
    st.markdown("""
        <div class="tab-content">
            <h2>تحويل النص إلى كلام مع خيارات متقدمة</h2>
            <p>حول النص العربي إلى كلام مع إمكانية التحكم في الصوت والسرعة</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_text = st.text_area(
        "النص المراد تحويله:",
        key="tts_text",
        height=150
    )
    
    with st.expander("إعدادات الصوت", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            use_offline = st.checkbox("استخدام المحرك المحلي")
            voice_type = st.selectbox(
                "نوع الصوت",
                ["ذكر", "أنثى"] if not use_offline else ["صوت 1", "صوت 2"]
            )
        
        with col2:
            speed = st.slider("سرعة النطق", 0.5, 2.0, 1.0, 0.1)
            if use_offline:
                pitch = st.slider("درجة الصوت", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("تحويل إلى صوت", use_container_width=True):
        if user_text:
            with st.spinner("جاري تحويل النص إلى صوت..."):
                voice_settings = {
                    'use_offline': use_offline,
                    'voice_type': 'male' if voice_type == "ذكر" else 'female',
                    'voice_idx': int(voice_type.split()[-1]) - 1 if use_offline else 0,
                    'speed': speed,
                    'pitch': pitch if use_offline else 1.0
                }
                
                audio_file, success = text_to_speech(user_text, voice_settings)
                if success:
                    st.audio(audio_file)
                    st.download_button(
                        "تحميل الملف الصوتي",
                        audio_file,
                        file_name=f"fluent_mind_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{'mp3' if not use_offline else 'wav'}"
                    )
                    os.remove(audio_file)
                else:
                    st.error(f"حدث خطأ: {audio_file}")
        else:
            st.warning("يرجى إدخال نص للتحويل")

def render_enhanced_reading_tab():
    """عرض تبويب القراءة المعززة"""
    st.markdown("""
        <div class="tab-content">
            <h2>القراءة المعززة للنصوص</h2>
            <p>أدوات متقدمة لتحسين تجربة القراءة وفهم النص</p>
        </div>
    """, unsafe_allow_html=True)
    
    # إعدادات العرض
    with st.expander("إعدادات العرض", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            font = st.selectbox(
                "نوع الخط",
                ["OpenDyslexic", "Tajawal", "Arial"]
            )
            font_size = st.slider("حجم الخط", 16, 42, 24)
        with col2:
            line_spacing = st.slider("المسافة بين السطور", 1.0, 3.0, 1.8)
            word_spacing = st.slider("المسافة بين الكلمات", 0, 20, 4)
    
    user_text = st.text_area(
        "النص للقراءة المعززة:",
        key="enhanced_text",
        height=150
    )
    
    if st.button("تطبيق التنسيق", use_container_width=True):
        if user_text:
            st.markdown(f"""
                <div style="
                    font-family: {font};
                    font-size: {font_size}px;
                    line-height: {line_spacing};
                    word-spacing: {word_spacing}px;
                    background-color: {'#000000' if st.session_state.high_contrast else '#111111'};
                    color: #FFFFFF;
                    padding: 20px;
                    border-radius: 10px;
                    direction: rtl;
                    text-align: right;
                ">
                    {user_text}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("يرجى إدخال نص للقراءة المعززة")

if __name__ == "__main__":
    main()