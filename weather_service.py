# ================================================================
# weather_service.py — OpenWeatherMap API servisi
# ================================================================
# Bu modul ob-havo ma'lumotlarini olish va qayta ishlash uchun
# mas'ul. Barcha tarmoq xatoliklari shu yerda boshqariladi.
# ================================================================

import requests
from dataclasses import dataclass, field
from typing import Optional

import config


# ================================================================
# 📦 WeatherData — Ob-havo ma'lumotlari uchun Data Class
# ================================================================

@dataclass
class WeatherData:
    """
    Ob-havo ma'lumotlarini tuzilgan (structured) ko'rinishda saqlaydi.

    Dataclass ishlatildi chunki:
    - Avtomatik __init__, __repr__, __eq__ metodlari
    - Tip tekshiruvi (type hints) qo'llab-quvvatlanadi
    - field() orqali default qiymatlar beriladi

    Attributes:
        city          : Shahar nomi (API dan qaytgan)
        temperature   : Haqiqiy harorat, Celsius (°C)
        feels_like    : His qilinadigan harorat, Celsius (°C)
        humidity      : Namlik darajasi (0–100%)
        wind_speed    : Shamol tezligi (m/s)
        description   : Ob-havo holati tavsifi (masalan, "Ochiq osmon")
        condition_id  : OpenWeatherMap ob-havo kod raqami
        is_raining    : Yomg'ir yog'moqdami?
        is_snowing    : Qor yog'moqdami?
        is_thunderstorm: Momaqaldiroqmi?
        is_cloudy     : Bulutlimi?
    """
    city: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    condition_id: int
    is_raining: bool     = field(default=False)
    is_snowing: bool     = field(default=False)
    is_thunderstorm: bool = field(default=False)
    is_cloudy: bool      = field(default=False)

    def get_temperature_category(self) -> str:
        """
        Harorat qiymatiga qarab toifa nomini aniqlaydi.

        Returns:
            str: "juda_sovuq" | "sovuq" | "salqin" | "iliq" | "issiq" | "juda_issiq"
        """
        t = self.temperature
        if   t <= 0:  return "juda_sovuq"
        elif t <= 10: return "sovuq"
        elif t <= 18: return "salqin"
        elif t <= 25: return "iliq"
        elif t <= 32: return "issiq"
        else:         return "juda_issiq"

    def get_summary(self) -> str:
        """
        Ob-havo ma'lumotlarini terminalga chiqarish uchun
        chiroyli formatda qaytaradi.

        Returns:
            str: Ko'p qatorli formatlangan matn
        """
        # Maxsus ob-havo belgilari
        icons = []
        if self.is_thunderstorm: icons.append("⛈️  Momaqaldiroq")
        elif self.is_raining:    icons.append("🌧️  Yomg'ir")
        if self.is_snowing:      icons.append("❄️  Qor")
        if self.wind_speed > 10: icons.append(f"💨 Kuchli shamol")
        if not icons:            icons.append("☀️  Yaxshi ob-havo")

        extra = " | ".join(icons)

        return (
            f"  📍 Shahar    :  {self.city}\n"
            f"  🌡️  Harorat   :  {self.temperature}°C  "
            f"(His qilish: {self.feels_like}°C)\n"
            f"  💧 Namlik    :  {self.humidity}%\n"
            f"  💨 Shamol    :  {self.wind_speed} m/s\n"
            f"  ☁️  Holat     :  {self.description}\n"
            f"  ✨ Maxsus    :  {extra}\n"
        )

    def to_dict(self) -> dict:
        """Ma'lumotlarni JSON-serializatsiya uchun dict ga o'giradi."""
        return {
            "city": self.city,
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "description": self.description,
            "condition_id": self.condition_id,
            "is_raining": self.is_raining,
            "is_snowing": self.is_snowing,
            "is_thunderstorm": self.is_thunderstorm,
            "is_cloudy": self.is_cloudy,
            "temperature_category": self.get_temperature_category(),
        }


# ================================================================
# 🌤️ WeatherService — Ob-havo API bilan ishlash servisi
# ================================================================

class WeatherService:
    """
    OpenWeatherMap REST API bilan ishlash uchun servis klassi.

    Mas'uliyat:
    - HTTP so'rovlarni yuborish va natijani qayta ishlash
    - Barcha tarmoq va API xatoliklarini boshqarish
    - Foydalanuvchiga tushunarli xabar ko'rsatish

    Usage:
        service = WeatherService()
        weather = service.get_weather("Toshkent")
        if weather:
            print(weather.get_summary())
    """

    # OpenWeatherMap ob-havo kod diapazonlari
    _CODE_THUNDERSTORM = range(200, 300)  # Momaqaldiroq
    _CODE_DRIZZLE      = range(300, 400)  # Mayda yomg'ir
    _CODE_RAIN         = range(500, 600)  # Yomg'ir
    _CODE_SNOW         = range(600, 700)  # Qor
    _CODE_CLOUDS       = range(801, 805)  # Bulutli (800 = tiniq)

    def __init__(self) -> None:
        self._api_key  : str = config.OPENWEATHER_API_KEY
        self._base_url : str = config.OPENWEATHER_BASE_URL
        self._unit     : str = config.TEMPERATURE_UNIT
        self._timeout  : int = config.REQUEST_TIMEOUT

    # ------------------------------------------------------------------
    # Ichki yordamchi metodlar (private)
    # ------------------------------------------------------------------

    def _parse_conditions(self, condition_id: int) -> dict[str, bool]:
        """Ob-havo kodidan boolean bayroqlar (flags) hosil qiladi."""
        return {
            "is_thunderstorm": condition_id in self._CODE_THUNDERSTORM,
            "is_raining"     : (
                condition_id in self._CODE_DRIZZLE or
                condition_id in self._CODE_RAIN or
                condition_id in self._CODE_THUNDERSTORM
            ),
            "is_snowing"     : condition_id in self._CODE_SNOW,
            "is_cloudy"      : condition_id in self._CODE_CLOUDS,
        }

    def _parse_response(self, data: dict) -> WeatherData:
        """
        API JSON javobidan WeatherData obyekti yaratadi.

        Args:
            data: OpenWeatherMap API JSON javobi

        Returns:
            WeatherData: To'ldirilgan ob-havo ma'lumotlari
        """
        condition_id = int(data["weather"][0]["id"])
        conditions   = self._parse_conditions(condition_id)

        return WeatherData(
            city          = data["name"],
            temperature   = round(float(data["main"]["temp"]),       1),
            feels_like    = round(float(data["main"]["feels_like"]), 1),
            humidity      = int(data["main"]["humidity"]),
            wind_speed    = round(float(data["wind"].get("speed", 0)), 1),
            description   = data["weather"][0]["description"].capitalize(),
            condition_id  = condition_id,
            **conditions,
        )

    # ------------------------------------------------------------------
    # Ochiq (public) metod
    # ------------------------------------------------------------------

    def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Berilgan shahar uchun hozirgi ob-havo ma'lumotlarini oladi.

        Barcha xatoliklar try-except ichida boshqariladi —
        funksiya hech qachon exception ko'tarmaydi.

        Args:
            city: Shahar nomi, ingliz tilida (masalan, "Tashkent", "London")

        Returns:
            WeatherData: Muvaffaqiyatli bo'lganda
            None       : Har qanday xatolik bo'lganda
        """
        # Kirishni tekshirish
        if not city or not city.strip():
            print("❌ Shahar nomi bo'sh bo'lishi mumkin emas!")
            return None

        try:
            params: dict = {
                "q"     : city.strip(),
                "appid" : self._api_key,
                "units" : self._unit,
                "lang"  : "uz",   # O'zbek tili (qisman qo'llab-quvvatlanadi)
            }

            response = requests.get(
                self._base_url,
                params  = params,
                timeout = self._timeout,
            )

            # 4xx / 5xx xatoliklarini avtomatik ko'tarish
            response.raise_for_status()

            return self._parse_response(response.json())

        # ----- Tarmoq xatoliklari -----
        except requests.exceptions.ConnectionError:
            print(
                "❌ Internet ulanishida xatolik!\n"
                "   👉 Tarmoq ulanishingizni tekshiring va qayta urinib ko'ring."
            )

        except requests.exceptions.Timeout:
            print(
                f"❌ Server {self._timeout} soniyada javob bermadi (Timeout)!\n"
                "   👉 Keyinroq qayta urinib ko'ring."
            )

        # ----- HTTP xatoliklari -----
        except requests.exceptions.HTTPError as http_err:
            status = http_err.response.status_code

            messages = {
                401: (
                    "❌ OpenWeatherMap API kalit noto'g'ri (401 Unauthorized)!\n"
                    "   👉 .env faylidagi OPENWEATHER_API_KEY ni tekshiring.\n"
                    "   👉 Yangi kalit: https://openweathermap.org/api"
                ),
                404: (
                    f"❌ '{city}' shahri topilmadi (404 Not Found)!\n"
                    "   👉 Shahar nomini ingliz tilida kiriting.\n"
                    "   👉 Misol: Tashkent, Samarkand, Bukhara, London, Paris"
                ),
                429: (
                    "❌ API so'rovlar chastotasi limiti oshdi (429 Too Many Requests)!\n"
                    "   👉 Bir necha daqiqadan so'ng qayta urinib ko'ring.\n"
                    "   👉 Bepul tarif: soatiga 60 ta so'rov."
                ),
                500: (
                    "❌ OpenWeatherMap serveri vaqtincha ishlamayapti (500)!\n"
                    "   👉 https://status.openweathermap.org/ tekshiring."
                ),
            }

            print(messages.get(status, f"❌ HTTP xatoligi {status}: {http_err}"))

        # ----- Ma'lumot tahlil xatoliklari -----
        except (KeyError, IndexError, ValueError) as parse_err:
            print(
                f"❌ API javobini tahlil qilishda kutilmagan xatolik: {parse_err}\n"
                "   👉 Bu muammo vaqtinchalik bo'lishi mumkin. Qayta urinib ko'ring."
            )

        # ----- Boshqa barcha xatoliklar -----
        except Exception as unexpected_err:
            print(f"❌ Kutilmagan xatolik yuz berdi: {unexpected_err}")

        return None
