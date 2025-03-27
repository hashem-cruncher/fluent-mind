"""
مكونات واجهة المستخدم المشتركة
"""

import streamlit as st
from fluent_mind.config.constants import COLORS, FONTS, DEFAULT_SETTINGS

def render_header():
    """عرض رأس الصفحة"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("assets/images/logo.png", width=100)
    with col2:
        st.title("Fluent Mind 🧠")

def render_sidebar():
    """عرض الشريط الجانبي مع الإعدادات"""
    with st.sidebar:
        st.header("الإعدادات العامة")
        
        st.subheader("إمكانية الوصول")
        st.session_state.ui_scale = st.slider(
            "حجم عناصر الواجهة",
            min_value=0.8,
            max_value=1.5,
            value=st.session_state.get('ui_scale', DEFAULT_SETTINGS['ui_scale']),
            step=0.1
        )
        
        st.session_state.reduce_motion = st.checkbox(
            "تقليل الحركة",
            value=st.session_state.get('reduce_motion', DEFAULT_SETTINGS['reduce_motion'])
        )
        
        st.session_state.high_contrast = st.checkbox(
            "تباين عالي",
            value=st.session_state.get('high_contrast', DEFAULT_SETTINGS['high_contrast'])
        )
        
        st.subheader("تخصيص الألوان")
        st.session_state.color_theme = st.selectbox(
            "نمط الألوان",
            options=list(COLORS.keys()),
            format_func=lambda x: {
                'default': "الوضع الافتراضي",
                'warm': "ألوان دافئة",
                'cool': "ألوان باردة",
                'contrast': "ألوان متباينة"
            }[x],
            index=list(COLORS.keys()).index(
                st.session_state.get('color_theme', DEFAULT_SETTINGS['color_theme'])
            )
        )

def render_tab_header(title: str, description: str):
    """عرض رأس التبويب"""
    st.markdown(f"""
        <div class="tab-content">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True) 