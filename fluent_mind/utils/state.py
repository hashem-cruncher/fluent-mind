"""
إدارة حالة التطبيق
"""

import streamlit as st
from fluent_mind.config.constants import DEFAULT_SETTINGS

def initialize_session_state():
    """تهيئة متغيرات الحالة للتطبيق"""
    for key, value in DEFAULT_SETTINGS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_state(key: str, default=None):
    """الحصول على قيمة من حالة التطبيق"""
    return st.session_state.get(key, default)

def set_state(key: str, value):
    """تعيين قيمة في حالة التطبيق"""
    st.session_state[key] = value 