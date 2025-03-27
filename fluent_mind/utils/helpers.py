"""
دوال مساعدة
"""

import os
from datetime import datetime
from typing import Union

def create_temp_file(prefix: str, suffix: str) -> str:
    """إنشاء ملف مؤقت"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{suffix}"

def clean_temp_files(directory: str, prefix: str):
    """تنظيف الملفات المؤقتة"""
    for file in os.listdir(directory):
        if file.startswith(prefix):
            try:
                os.remove(os.path.join(directory, file))
            except:
                pass

def format_time(seconds: Union[int, float]) -> str:
    """تنسيق الوقت بالدقائق والثواني"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_file_size(file_path: str) -> str:
    """الحصول على حجم الملف بتنسيق مناسب"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB" 