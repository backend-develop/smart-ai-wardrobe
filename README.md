# smart-ai-wardrobe
A Python terminal app using Google Gemini API and a live weather API to recommend daily outfits based on current temperature and user contexts.
# ClimeWear: Live Weather & AI-Driven Outfit Recommendation System (v1.0.0)

An intelligent, context-aware terminal application built in Python that automatically recommends daily outfits from a local inventory database by fetching real-time weather data and processing it via the Google Gemini AI API.

*Note: The core terminal interface and logic components are developed in Uzbek, specifically tailored for regional deployment and testing in Tashkent, Uzbekistan.*

## 🚀 Core Features
*   **Real-time Weather Integration:** Dynamically fetches current temperature and environmental conditions for any specified city via meteorological API.
*   **Contextual Recommendation Engine:** Offers 5 distinct styling modes: Casual, Business, Active, Stylish, and Relaxed.
*   **Structured Inventory Tracking:** Maps recommendations directly to unique internal inventory IDs (e.g., `IF002`, `SH004`) from a local database array.
*   **Google Gemini API Integration:** Generates highly sophisticated, human-like styling advice and vital weather warnings based on live atmospheric parameters.

## 💻 Sample Terminal Output
```text
=========================================
  🧥 Smart AI Wardrobe Assistant (v1.0.0)
=========================================
🤖 Tizim ishga tushmoqda...

✅ Barcha sozlamalar joyida!
📍 Shahar nomini kiriting (Standart: Tashkent): Tashkent

🎯 Vaziyat turini tanlang:
  1. Kundalik (casual)
...
🧠 AI sizning garderobingizni tahlil qilmoqda va kombinatsiya yaratyapti...

## 👔 Bugungi Kiyim Tavsiyasi — Tashkent
### 🌤️ Ob-havo sharhi
Bugun Toshkentda havo juda issiq, harorat 33.9°C ni tashkil etmoqda...
```

## 🛠️ Tech Stack
*   **Language:** Python 3.x
*   **AI Engine:** Google Gemini API
*   **APIs:** Live Weather Retrieval Engine
