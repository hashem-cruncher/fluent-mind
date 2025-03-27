"""
أنماط CSS للتطبيق
"""

def get_base_styles() -> str:
    """الأنماط الأساسية للتطبيق"""
    return """
        /* استيراد الخطوط */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        
        /* أنماط عامة */
        * {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }
        
        /* أنماط العناوين */
        h1, h2, h3 {
            color: #FFFFFF;
            margin-bottom: 1rem;
        }
        
        /* أنماط النصوص */
        p {
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        /* أنماط الأزرار */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #45a049;
        }
        
        /* أنماط مناطق النص */
        .stTextArea > div > div > textarea {
            background-color: #2b2b2b;
            color: #FFFFFF;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 0.5rem;
        }
        
        /* أنماط التبويبات */
        .stTabs {
            background-color: #1e1e1e;
            border-radius: 4px;
            padding: 1rem;
        }
    """

def get_theme_styles(theme: str) -> dict:
    """أنماط السمات المختلفة"""
    themes = {
        'light': {
            'background': '#FFFFFF',
            'text': '#000000',
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'accent': '#FF9800'
        },
        'dark': {
            'background': '#1e1e1e',
            'text': '#FFFFFF',
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'accent': '#FF9800'
        },
        'high_contrast': {
            'background': '#000000',
            'text': '#FFFFFF',
            'primary': '#00FF00',
            'secondary': '#00FFFF',
            'accent': '#FFFF00'
        }
    }
    return themes.get(theme, themes['dark']) 