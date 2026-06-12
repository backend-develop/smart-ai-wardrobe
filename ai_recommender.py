# ================================================================
# ai_recommender.py — Gemini AI yordamida kiyim tavsiyalari
# ================================================================
# Bu modul prompt muhandisligi (Prompt Engineering) tamoyillariga
# asoslanib Google Gemini AI modeliga so'rov yuboradi va
# ob-havoga mos kiyim kombinatsiyasini qaytaradi.
#
# Prompt Engineering qoidalari:
#   1. Aniq rol berish → "Sen professional moda stilisti..."
#   2. To'liq kontekst → Ob-havo + Garderob ma'lumotlari
#   3. Qattiq cheklovlar → Faqat mavjud kiyimlar
#   4. Output formati → Markdown + O'zbek tili
#   5. Misollar → Harorat bo'yicha kiyim tanlash qoidalari
# ================================================================

from google import genai
from google.genai import types
from typing import Optional

import config
from weather_service import WeatherData
from wardrobe_data import get_wardrobe_as_text


# ================================================================
# 🤖 AIRecommender — Kiyim tavsiyasi AI servisi
# ================================================================

class AIRecommender:
    """
    Google Gemini AI orqali ob-havoga mos kiyim tavsiyasi beradigan sinf.

    Xususiyatlari:
    ✅ Faqat foydalanuvchining garderobidagi kiyimlarni ishlatadi
    ✅ O'zbek tilida chiroyli Markdown formatida javob beradi
    ✅ Ob-havo, namlik, shamol va maxsus holatlarga mos kiyim tanlaydi
    ✅ Barcha API xatoliklarini to'g'ri boshqaradi

    Usage:
        recommender = AIRecommender()
        weather     = WeatherData(...)
        result      = recommender.get_recommendation(weather, "kundalik")
        if result:
            print(result)
    """

    def __init__(self) -> None:
        """Yangi Google GenAI mijozini konfiguratsiya qiladi."""
        try:
            self._client = genai.Client(api_key=config.GEMINI_API_KEY)
            self._model_name = config.GEMINI_MODEL

        except Exception as init_err:
            print(f"❌ Gemini AI ni sozlashda xatolik: {init_err}")
            raise

    # ------------------------------------------------------------------
    # Ichki (private) yordamchi metodlar
    # ------------------------------------------------------------------

    def _build_weather_context(self, weather: WeatherData) -> str:
        """
        Ob-havo ma'lumotlarini AI uchun tuzilgan matn formatiga o'giradi.

        Args:
            weather: WeatherData obyekti

        Returns:
            str: AI uchun formatlangan ob-havo konteksti
        """
        # Maxsus ob-havo shartlari ro'yxati
        special_conditions: list[str] = []

        if weather.is_thunderstorm:
            special_conditions.append("⚡ MOMAQALDIROQ VA KUCHLI YOMG'IR")
        elif weather.is_raining:
            special_conditions.append("🌧️ YOMG'IR YOG'MOQDA")

        if weather.is_snowing:
            special_conditions.append("❄️ QOR YOG'MOQDA")

        if weather.wind_speed >= 15:
            special_conditions.append(f"🌪️ JUDA KUCHLI SHAMOL ({weather.wind_speed} m/s)")
        elif weather.wind_speed >= 8:
            special_conditions.append(f"💨 KUCHLI SHAMOL ({weather.wind_speed} m/s)")

        if weather.humidity > 85:
            special_conditions.append(f"💧 JUDA YUQORI NAMLIK ({weather.humidity}%)")

        if not special_conditions:
            special_conditions.append("☀️ YAXSHI OB-HAVO, MAXSUS SHART YO'Q")

        # Harorat toifasi va tavsifi
        temp_category = weather.get_temperature_category()
        temp_desc_map: dict[str, str] = {
            "juda_sovuq": "JUDA SOVUQ (≤0°C) — Maksimal issiq kiyim kerak",
            "sovuq"     : "SOVUQ (1–10°C) — Issiq va himoyali kiyim kerak",
            "salqin"    : "SALQIN (11–18°C) — Qatlam usuli (layering) tavsiya etiladi",
            "iliq"      : "ILIQ (19–25°C) — Yengil va qulay kiyim yetarli",
            "issiq"     : "ISSIQ (26–32°C) — Yengil va nafas oladigan kiyim kerak",
            "juda_issiq": "JUDA ISSIQ (≥33°C) — Minimal va yengil kiyim",
        }

        return (
            f"  Shahar          : {weather.city}\n"
            f"  Harorat         : {weather.temperature}°C\n"
            f"  His qilish      : {weather.feels_like}°C\n"
            f"  Harorat toifasi : {temp_desc_map.get(temp_category, temp_category)}\n"
            f"  Namlik          : {weather.humidity}%\n"
            f"  Shamol tezligi  : {weather.wind_speed} m/s\n"
            f"  Ob-havo holati  : {weather.description}\n"
            f"  Maxsus shartlar : {' | '.join(special_conditions)}\n"
        )

    def _build_prompt(self, weather: WeatherData, occasion: str) -> str:
        """
        Gemini AI uchun to'liq, tuzilmali va qattiq qoidali prompt yaratadi.

        Prompt muhandisligi tamoyillari qo'llanilgan:
        - Zero-shot role prompting (rol berish)
        - Constrained generation (cheklovlar qo'yish)
        - Format specification (output formatini belgilash)
        - Chain-of-thought hints (fikrlash zanjiri)

        Args:
            weather : Ob-havo ma'lumotlari
            occasion: Tadbir turi (kundalik, rasmiy ish, sport, ...)

        Returns:
            str: Tayyor prompt matni
        """
        wardrobe_text   = get_wardrobe_as_text()
        weather_context = self._build_weather_context(weather)

        prompt = f"""
Sen 10 yillik tajribaga ega bo'lgan professional moda stilisti va kiyim maslahatchiasan.
Sening YAGONA vazifang — berilgan ob-havo sharoiti, tadbir turi va foydalanuvchining
garderobiga qarab eng ideal kiyim kombinatsiyasini tanlash.

╔══════════════════════════════════════════════════════════════╗
║  📊 HOZIRGI OB-HAVO MA'LUMOTLARI                             ║
╚══════════════════════════════════════════════════════════════╝
{weather_context}

╔══════════════════════════════════════════════════════════════╗
║  🎯 TADBIR/VAZIYAT TURI                                       ║
╚══════════════════════════════════════════════════════════════╝
  Tadbir: {occasion.upper()}

╔══════════════════════════════════════════════════════════════╗
║  👗 FOYDALANUVCHINING TO'LIQ GARDEROB MA'LUMOTLARI           ║
╚══════════════════════════════════════════════════════════════╝
{wardrobe_text}

╔══════════════════════════════════════════════════════════════╗
║  ⚠️  QATTIQ QOIDALAR — MUTLAQ BAJARILISHI SHART!             ║
╚══════════════════════════════════════════════════════════════╝

QOIDA №1 — FAQAT MAVJUD KIYIM (ENG MUHIM!):
  Siz FAQAT yuqoridagi garderobda ro'yxatda turgan kiyimlarni
  tavsiya qilishingiz mumkin. Har bir tavsiya uchun kiyimning
  ID raqamini ko'rsating (masalan: UK001, SH002, PY003...).
  ❌ Garderobda YO'Q kiyimni HECH QACHON taklif qilmang!
  ❌ "Yangi kurtka sotib oling" kabi maslahat bermang!

QOIDA №2 — OB-HAVO QOIDALARI (Qattiq rioya qiling):
  • Harorat ≤ 0°C  → Albatta: palto (UK002) + termal (IF004) + shapka (AK001)
                      + qo'lqop (AK003) + shal (AK002) + issiq botinka/etik
  • Harorat 1–10°C → Kurtka/palto + sviter/termal + jinsi/sport shim + yopiq poyabzal
  • Harorat 11–18°C → Kurtka/blazer/jakket + futbolka/polo/ko'ylak + jinsi/chino + sneakers/botinka
  • Harorat 19–25°C → Yengil ko'ylak/polo/futbolka + jinsi/chino + sneakers
  • Harorat ≥ 26°C → Futbolka yoki tank top + shorts yoki yengil shim + sandal/sneakers
  • YOMG'IR yog'sa → soyabon (AK006) ALBATTA + suv o'tkazmaydigan poyabzal (PY002, PY005, PY006)
  • QOR yog'sa    → Issiq kiyimlar + suv o'tkazmaydigan etik/botinka ALBATTA

QOIDA №3 — TADBIR QOIDALARI:
  • "kundalik"       → Qulay, zamonaviy, erkin kombinatsiya
  • "rasmiy ish"     → Blazer/klassik shim/tufli, professional ko'rinish
  • "sport"          → Sport shim/sneakers/qulay kiyim, harakat uchun mos
  • "kechki chiqish" → Stilishli, zamonaviy, chiroyli kombinatsiya
  • "dam olish"      → Maksimal qulay, erkin, sport elementlari

QOIDA №4 — TIL: Javobni FAQAT O'ZBEK TILIDA yozing!

QOIDA №5 — FORMAT: Javobni aynan quyidagi Markdown formatida bering:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 👔 Bugungi Kiyim Tavsiyasi — {weather.city}

### 🌤️ Ob-havo sharhi
[Bugungi ob-havo va kiyim tanlash haqida do'stona, iliq 2–3 jumla.]

### 🎽 Tavsiya etilgan kombinatsiya

| 📦 Kategoriya             | 👔 Kiyim nomi            | 🏷️ ID   |
|:--------------------------|:-------------------------|:-------:|
| [kategoriya]              | [aniq kiyim nomi]        | `[ID]`  |

### 💬 Stilist maslahati
[Kombinatsiya haqida 3–4 jumlali professional va iliq maslahat.
Ranglar uyg'unligi, umumiy ko'rinish va maqsadga muvofiqligi haqida
yozing. Do'stona va rag'batlantiruvchi ohangda bo'lsin!]

### ⚠️ Muhim eslatmalar
[Agar yomg'ir, qor, kuchli shamol yoki boshqa maxsus holat bo'lsa —
shu bo'limda ogohlantirish yozing. Agar hammasi yaxshi bo'lsa,
faqat: "Bugun ob-havo ajoyib, xursand sayr qiling! 😊" deb yozing.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUHIM: Faqat yuqoridagi formatda javob bering! Boshqa hech narsa qo'shmang.
"""
        return prompt.strip()

    # ------------------------------------------------------------------
    # Ochiq (public) metod
    # ------------------------------------------------------------------

    def get_recommendation(
        self,
        weather : WeatherData,
        occasion: str = "kundalik",
    ) -> Optional[str]:
        """
        Ob-havo va tadbir turiga mos kiyim tavsiyasini oladi.

        Args:
            weather : WeatherData obyekti (ob-havo ma'lumotlari)
            occasion: Tadbir turi ("kundalik", "rasmiy ish", "sport", ...)

        Returns:
            str : Markdown formatidagi kiyim tavsiyasi (muvaffaqiyatli bo'lganda)
            None: Xatolik yuz berganda
        """
        try:
            prompt = self._build_prompt(weather, occasion)

            # Yangi SDK da so'rov shakli — model nomini aniq matn qilib yozamiz
            response = self._client.models.generate_content(
                model="gemini-2.5-flash",  # <--- Shuni matn ko'rinishida yozing
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=config.AI_TEMPERATURE,
                    max_output_tokens=config.AI_MAX_TOKENS,
                )
            )

            # Javobni tekshirish
            if not response or not hasattr(response, "text") or not response.text:
                print("❌ AI bo'sh yoki noto'g'ri javob qaytardi.")
                return None

            return response.text.strip()

        # ----- API xatoliklarini tahlil qilish -----
        except Exception as api_err:
            error_msg = str(api_err).lower()

            if any(kw in error_msg for kw in ["api_key", "api key", "invalid key", "authentication", "credentials"]):
                print(
                    "❌ Gemini API kalit noto'g'ri yoki muddati tugagan!\n"
                    "   👉 .env faylidagi GEMINI_API_KEY ni tekshiring.\n"
                    "   👉 Yangi kalit: https://aistudio.google.com/app/apikey"
                )
            elif any(kw in error_msg for kw in ["quota", "rate limit", "resource_exhausted", "429"]):
                print(
                    "❌ Gemini API so'rovlar chastotasi limiti oshdi!\n"
                    "   👉 Bir necha daqiqadan so'ng qayta urinib ko'ring.\n"
                    "   👉 Bepul tarif: daqiqada 15 ta so'rov."
                )
            elif any(kw in error_msg for kw in ["network", "connection", "timeout", "unreachable"]):
                print(
                    "❌ Gemini AI serveriga ulanishda muammo!\n"
                    "   👉 Internet ulanishingizni tekshiring."
                )
            elif any(kw in error_msg for kw in ["blocked", "safety", "harm"]):
                print(
                    "❌ AI xavfsizlik filtri so'rovni rad etdi.\n"
                    "   👉 Bu kamdan-kam hodisa. Qayta urinib ko'ring."
                )
            else:
                print(f"❌ Gemini AI da kutilmagan xatolik: {api_err}")

            return None
