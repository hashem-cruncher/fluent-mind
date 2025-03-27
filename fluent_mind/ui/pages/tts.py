"""
صفحة تحويل النص إلى كلام
"""

import streamlit as st
from datetime import datetime
import os
from fluent_mind.core.tts_engine import text_to_speech
from fluent_mind.ui.components import render_tab_header

def render_tts_tab():
    """عرض تبويب تحويل النص إلى كلام"""
    render_tab_header(
        "تحويل النص إلى كلام",
        "حول النص العربي إلى كلام"
    )
    
    user_text = st.text_area(
        "النص المراد تحويله:",
        key="tts_text",
        height=150
    )
    
    if st.button("تحويل إلى صوت", use_container_width=True):
        if user_text:
            with st.spinner("جاري تحويل النص إلى صوت..."):
                audio_file, success = text_to_speech(user_text)
                if success:
                    st.audio(audio_file)
                    st.download_button(
                        "تحميل الملف الصوتي",
                        audio_file,
                        file_name=f"fluent_mind_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                    )
                    os.remove(audio_file)
                else:
                    st.error(f"حدث خطأ: {audio_file}")
        else:
            st.warning("يرجى إدخال نص للتحويل") 