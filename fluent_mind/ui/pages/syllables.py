"""
صفحة تقسيم النص إلى مقاطع
"""

import streamlit as st
from fluent_mind.core.syllable_splitter import split_into_syllables
from fluent_mind.ui.components import render_tab_header

def render_syllable_tab():
    """عرض تبويب تقسيم النص إلى مقاطع"""
    render_tab_header(
        "تقسيم النص إلى مقاطع",
        "هذه الأداة تساعدك في تقسيم النص العربي إلى مقاطع سهلة القراءة"
    )
    
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