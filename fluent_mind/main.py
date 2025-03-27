"""
التطبيق الرئيسي
"""

import streamlit as st
from fluent_mind.config.settings import STREAMLIT_CONFIG
from fluent_mind.ui.components import render_header, render_sidebar
from fluent_mind.ui.pages.syllables import render_syllable_tab
from fluent_mind.ui.pages.tts import render_tts_tab
from fluent_mind.ui.pages.reader import render_enhanced_reading_tab
from fluent_mind.utils.state import initialize_session_state
from fluent_mind.ui.styles import get_base_styles

def main():
    """الدالة الرئيسية للتطبيق"""
    # تهيئة حالة التطبيق
    initialize_session_state()
    
    # تكوين الصفحة
    st.set_page_config(**STREAMLIT_CONFIG)
    
    # تطبيق الأنماط الأساسية
    css = get_base_styles()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    
    # عرض رأس الصفحة والشريط الجانبي
    render_header()
    render_sidebar()
    
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

if __name__ == "__main__":
    main() 