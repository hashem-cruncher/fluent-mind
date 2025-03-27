# Fluent Mind - تطبيق دعم ذوي عسر القراءة

تطبيق ويب مبني باستخدام Streamlit لمساعدة الأشخاص الذين يعانون من عسر القراءة في قراءة وفهم النصوص العربية بشكل أفضل.

## المميزات

1. **تقسيم النص إلى مقاطع**
   - تقسيم الكلمات العربية إلى مقاطع سهلة القراءة
   - تمييز المقاطع بألوان مختلفة
   - دعم للكلمات القصيرة والطويلة

2. **تحويل النص إلى كلام**
   - دعم للتحويل عبر الإنترنت وبدون إنترنت
   - خيارات متعددة للأصوات (ذكر/أنثى)
   - التحكم في سرعة ونبرة الصوت

3. **القراءة المعززة**
   - تخصيص حجم الخط والمسافات
   - أنماط لونية مختلفة
   - وضع التباين العالي

## المتطلبات

- Python 3.8 أو أحدث
- المكتبات المذكورة في `requirements.txt`

## التثبيت

1. استنساخ المشروع:
   ```bash
   git clone https://github.com/yourusername/fluent_mind.git
   cd fluent_mind
   ```

2. إنشاء بيئة افتراضية:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. تثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

## التشغيل

تشغيل التطبيق:
```bash
streamlit run main.py
```

## هيكل المشروع

```
fluent_mind/
├── README.md
├── requirements.txt
├── main.py
├── config/
│   ├── constants.py        # الثوابت مثل الألوان وإعدادات التطبيق
│   └── settings.py         # إعدادات Streamlit
├── core/
│   ├── text_processor.py   # معالجة النص العربي
│   ├── syllable_splitter.py # تقسيم النص إلى مقاطع
│   └── tts_engine.py       # محرك تحويل النص إلى كلام
├── ui/
│   ├── styles.py          # أنماط CSS
│   ├── components.py      # مكونات واجهة المستخدم المشتركة
│   └── pages/
│       ├── syllables.py   # صفحة تقسيم النص
│       ├── tts.py         # صفحة تحويل النص إلى كلام
│       └── reader.py      # صفحة القراءة المعززة
├── utils/
│   ├── state.py          # إدارة حالة التطبيق
│   └── helpers.py        # دوال مساعدة
└── assets/
    ├── fonts/
    └── images/
        └── logo.png
```


## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## الاتصال

- البريد الإلكتروني: your.email@example.com
- تويتر: [@yourusername](https://twitter.com/yourusername)
- موقع المشروع: https://github.com/yourusername/fluent_mind 