"""
ثوابت التطبيق
"""

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

FONTS = {
    'primary': 'Tajawal',
    'dyslexic': 'OpenDyslexic',
    'fallback': 'Arial'
}

DEFAULT_SETTINGS = {
    'color_theme': 'default',
    'ui_scale': 1.0,
    'high_contrast': False,
    'reduce_motion': True
} 