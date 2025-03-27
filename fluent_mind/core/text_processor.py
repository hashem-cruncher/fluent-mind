"""
معالجة النص العربي
"""

import re
import pyarabic.araby as araby
from pyarabic.normalize import normalize_hamza, normalize_lamalef

def normalize_arabic_text(text: str) -> str:
    """تطبيع النص العربي وتوحيد أشكال الحروف"""
    text = araby.strip_tatweel(text)
    text = normalize_hamza(text)
    text = normalize_lamalef(text)
    text = re.sub('[ةه]', 'ه', text)
    text = araby.reduce_tashkeel(text)
    return text

def identify_difficult_words(text: str) -> list:
    """تحديد الكلمات الصعبة في النص"""
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