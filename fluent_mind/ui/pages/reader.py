"""
صفحة القراءة المعززة
"""

import streamlit as st
from fluent_mind.config.constants import FONTS
from fluent_mind.ui.components import render_tab_header

def render_enhanced_reading_tab():
    """عرض تبويب القراءة المعززة"""
    render_tab_header(
        "القراءة المعززة للنصوص",
        "أدوات متقدمة لتحسين تجربة القراءة وفهم النص"
    )
    
    # إعدادات العرض
    with st.expander("إعدادات العرض", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            font = st.selectbox(
                "نوع الخط",
                list(FONTS.values())
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
                    background-color: {'#000000' if st.session_state.get('high_contrast', False) else '#111111'};
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