# ================================================================
# main.py — Dasturni ishga tushirish va CLI foydalanuvchi interfeysi
# ================================================================

import sys
import config
from weather_service import WeatherService
from ai_recommender import AIRecommender


def main():
    print(f"=========================================")
    print(f"  {config.APP_NAME} (v{config.APP_VERSION})")
    print(f"=========================================")
    print("🤖 Tizim ishga tushmoqda...\n")

    # 1. Konfiguratsiyani tekshirish
    is_valid, errors = config.validate_config()
    if not is_valid:
        print("⚠️ Dasturni ishga tushirishda xatolik aniqlandi:")
        for error in errors:
            print(error)
        sys.exit(1)

    print("✅ Barcha sozlamalar joyida!")

    # 2. Servislarni ishga tushirish
    weather_service = WeatherService()
    ai_recommender = AIRecommender()

    # 3. Shahar nomini kiritish
    city = input(f"📍 Shahar nomini kiriting (Standart: {config.DEFAULT_CITY}): ").strip()
    if not city:
        city = config.DEFAULT_CITY

    # 4. Tadbir/Vaziyat turini tanlash
    print("\n🎯 Vaziyat turini tanlang:")
    print("  1. Kundalik (casual)")
    print("  2. Rasmiy ish (business)")
    print("  3. Sport (active)")
    print("  4. Kechki chiqish (stylish)")
    print("  5. Dam olish (relax)")

    vaziyat_tanlovi = input("💬 Raqamni kiriting (1-5, Standart: 1): ").strip()

    # Kiritilgan raqamni mos matnga o'giramiz
    vaziyat_map = {
        "1": "kundalik",
        "2": "rasmiy ish",
        "3": "sport",
        "4": "kechki chiqish",
        "5": "dam olish"
    }
    occasion = vaziyat_map.get(vaziyat_tanlovi, "kundalik")

    print(f"\n🌍 {city} shahridagi real vaqtdagi ob-havo tekshirilmoqda...")

    # 5. Ob-havo ma'lumotini olish
    weather_info = weather_service.get_weather(city)

    if not weather_info:
        print("❌ Ob-havo ma'lumotini olib bo'lmagani sababli dastur to'xtatildi.")
        sys.exit(1)

    print("\n🌤️  Hozirgi ob-havo holati aniqlandi.")
    print("🧠 AI sizning garderobingizni tahlil qilmoqda va kombinatsiya yaratyapti...")

    # 6. AI orqali kiyim tavsiyasini olish
    recommendation = ai_recommender.get_recommendation(weather_info, occasion)

    if recommendation:
        print("\n" + recommendation)
    else:
        print("\n❌ AI kiyim kombinatsiyasini yarata olmadi. Iltimos, API kalitlarini yoki internetni tekshiring.")


if __name__ == "__main__":
    main()