# ================================================================
# config.py — Konfiguratsiya va konstantalar
# ================================================================
# Bu modul barcha muhit o'zgaruvchilarini va dastur konstantalarini
# bitta markaziy joyda saqlaydi. Clean Code: "Single source of truth"
# ================================================================

import os
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklash (agar mavjud bo'lsa)
load_dotenv()


# ===========================
# 🔑 API KALITLARI
# ===========================

OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


# ===========================
# 🌍 SHAHAR SOZLAMASI
# ===========================

DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "Toshkent")


# ===========================
# 🌤️ OPENWEATHERMAP SOZLAMALARI
# ===========================

OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
TEMPERATURE_UNIT: str = "metric"   # "metric" = Celsius | "imperial" = Fahrenheit
REQUEST_TIMEOUT: int = 10          # Sekund (tarmoq kutish muddati)


# ===========================
# 🤖 GEMINI AI SOZLAMALARI
# ===========================

GEMINI_MODEL: str = "gemini-1.5-flash" # Tezkor va samarali model
AI_TEMPERATURE: float = 0.7             # Kreativlik: 0.0 (aniq) → 1.0 (ijodiy)
AI_MAX_TOKENS: int = 8000               # Maksimal javob uzunligi


# ===========================
# 📱 DASTUR MA'LUMOTLARI
# ===========================

APP_NAME: str = "🧥 Smart AI Wardrobe Assistant"
APP_VERSION: str = "1.0.0"


# ===========================
# ✅ KONFIGURATSIYA TEKSHIRUVI
# ===========================

def validate_config() -> tuple[bool, list[str]]:
    """
    API kalitlari va muhit o'zgaruvchilarining to'g'riligini tekshiradi.

    Bu funksiya dastur ishga tushganda chaqiriladi. Agar zaruriy
    kalitlar topilmasa, foydalanuvchiga aniq ko'rsatma beradi.

    Returns:
        tuple[bool, list[str]]:
            - bool: True = hammasi yaxshi, False = xatolik bor
            - list[str]: Topilgan xatoliklar ro'yxati (bo'sh bo'lishi mumkin)

    Example:
        >>> is_valid, errors = validate_config()
        >>> if not is_valid:
        ...     for err in errors:
        ...         print(err)
    """
    errors: list[str] = []

    if not OPENWEATHER_API_KEY:
        errors.append(
            "❌ OPENWEATHER_API_KEY topilmadi yoki bo'sh!\n"
            "   👉 Qadamlar:\n"
            "      1. https://openweathermap.org/api saytiga kiring\n"
            "      2. Bepul ro'yxatdan o'ting\n"
            "      3. 'Current Weather Data' API ni aktivlashtiring\n"
            "      4. API kalitni nusxa ko'chiring\n"
            "      5. .env fayliga qo'shing: OPENWEATHER_API_KEY=kalitingiz\n"
        )

    if not GEMINI_API_KEY:
        errors.append(
            "❌ GEMINI_API_KEY topilmadi yoki bo'sh!\n"
            "   👉 Qadamlar:\n"
            "      1. https://aistudio.google.com/app/apikey saytiga kiring\n"
            "      2. Google hisobingiz bilan kiring\n"
            "      3. 'Create API Key' tugmasini bosing\n"
            "      4. .env fayliga qo'shing: GEMINI_API_KEY=kalitingiz\n"
        )

    return len(errors) == 0, errors
