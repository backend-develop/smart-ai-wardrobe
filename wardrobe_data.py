# ================================================================
# wardrobe_data.py — Foydalanuvchi garderob ma'lumotlar bazasi
# ================================================================
# Bu fayldagi kiyimlarni O'ZINGIZNING garderobingizga moslang!
#
# Yangi kiyim qo'shish:
#   1. Tegishli kategoriyani toping
#   2. Yangi dict elementini qo'shing
#   3. Noyob ID bering (masalan: UK006, SH006, ...)
#
# Toifalar:
#   ustki_kiyim              → 🧥 Kurtka, palto, blazer, vetur
#   shimlar                  → 👖 Jinsi, klassik shim, shorts
#   poyabzal                 → 👟 Sneakers, botinka, sandal
#   aksessuarlar             → 🎩 Shapka, shal, kamar, ko'zoynagi
#   ichki_kiyim_va_futbolkalar → 👕 Futbolka, sviter, polo, termal
# ================================================================

from typing import TypedDict


# ================================================================
# 📋 KIYIM ELEMENTI STRUKTURASI
# ================================================================

class ClothingItem(TypedDict):
    """
    Har bir kiyim elementi quyidagi maydonlarga ega bo'lishi kerak.
    TypedDict ishlatilganligi uchun IDE avto-to'ldirish ishlaydi.
    """
    id         : str        # Noyob identifikator (masalan: "UK001")
    nomi       : str        # Kiyimning to'liq nomi
    turi       : str        # Kiyim turi (kurtka, jinsi, sneakers...)
    rang       : str        # Asosiy rang(lar)
    fasl       : list[str]  # Mos fasllar: ["qish", "bahor", "yoz", "kuz"]
    harorat_min: int        # Minimal mos harorat (°C)
    harorat_max: int        # Maksimal mos harorat (°C)
    izoh       : str        # Qo'shimcha tavsif va eslatma


# ================================================================
# 👗 GARDEROB MA'LUMOTLAR BAZASI
# ================================================================

WARDROBE: dict[str, list[ClothingItem]] = {

    # ────────────────────────────────────────────
    # 🧥 USTKI KIYIMLAR (Outerwear)
    # ────────────────────────────────────────────
    "ustki_kiyim": [
        {
            "id"         : "UK001",
            "nomi"       : "Qora charm kurtka",
            "turi"       : "kurtka",
            "rang"       : "qora",
            "fasl"       : ["kuz", "bahor"],
            "harorat_min": 5,
            "harorat_max": 18,
            "izoh"       : "Zamonaviy charm kurtka, suv o'tkazmaydigan, kuz/bahor uchun ideal",
        },
        {
            "id"         : "UK002",
            "nomi"       : "Kulrang jun palto",
            "turi"       : "palto",
            "rang"       : "kulrang",
            "fasl"       : ["qish", "kuz"],
            "harorat_min": -15,
            "harorat_max": 8,
            "izoh"       : "Qalin ikki qatlamli jun palto, qattiq sovuqlarga mos",
        },
        {
            "id"         : "UK003",
            "nomi"       : "Ko'k denim jakket",
            "turi"       : "jakket",
            "rang"       : "ko'k",
            "fasl"       : ["bahor", "yoz", "kuz"],
            "harorat_min": 15,
            "harorat_max": 30,
            "izoh"       : "Yengil denim jakket, iliq kunlar uchun qulay",
        },
        {
            "id"         : "UK004",
            "nomi"       : "Yashil suv o'tkazmaydigan vetur (windbreaker)",
            "turi"       : "vetur",
            "rang"       : "yashil",
            "fasl"       : ["bahor", "kuz", "yoz"],
            "harorat_min": 10,
            "harorat_max": 25,
            "izoh"       : "Shamol va yomg'irdan himoya qiladi, sport va kundalik foydalanish",
        },
        {
            "id"         : "UK005",
            "nomi"       : "Qo'ng'ir klassik blazer",
            "turi"       : "blazer",
            "rang"       : "qo'ng'ir",
            "fasl"       : ["bahor", "kuz"],
            "harorat_min": 12,
            "harorat_max": 22,
            "izoh"       : "Elegant blazer, ish va yarim rasmiy uchrashuvlar uchun",
        },
    ],

    # ────────────────────────────────────────────
    # 👖 SHIMLAR VA PASTKI KIYIMLAR (Bottoms)
    # ────────────────────────────────────────────
    "shimlar": [
        {
            "id"         : "SH001",
            "nomi"       : "Ko'k to'g'ri kesim jinsi (straight fit)",
            "turi"       : "jinsi",
            "rang"       : "ko'k",
            "fasl"       : ["qish", "kuz", "bahor", "yoz"],
            "harorat_min": 0,
            "harorat_max": 35,
            "izoh"       : "Klassik ko'k jinsi, universal va har qanday kiyim bilan mos",
        },
        {
            "id"         : "SH002",
            "nomi"       : "Qora slim-fit klassik shim",
            "turi"       : "klassik shim",
            "rang"       : "qora",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": -5,
            "harorat_max": 22,
            "izoh"       : "Rasmiy va yarim rasmiy holatlar uchun, egiluvchan material",
        },
        {
            "id"         : "SH003",
            "nomi"       : "Bej chino shim",
            "turi"       : "chino",
            "rang"       : "bej",
            "fasl"       : ["bahor", "yoz", "kuz"],
            "harorat_min": 12,
            "harorat_max": 32,
            "izoh"       : "Yengil va qulay chino, kundalik va smart casual ko'rinish",
        },
        {
            "id"         : "SH004",
            "nomi"       : "Qora paxta kalta shim (shorts)",
            "turi"       : "shorts",
            "rang"       : "qora",
            "fasl"       : ["yoz"],
            "harorat_min": 24,
            "harorat_max": 45,
            "izoh"       : "Juda issiq yoz kunlari uchun yengil paxta kalta shim",
        },
        {
            "id"         : "SH005",
            "nomi"       : "Kulrang sport shim (jogger pants)",
            "turi"       : "sport shim",
            "rang"       : "kulrang",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": 0,
            "harorat_max": 20,
            "izoh"       : "Yumshoq va issiq, sport mashg'ulotlari va dam olish uchun",
        },
    ],

    # ────────────────────────────────────────────
    # 👟 POYABZAL (Footwear)
    # ────────────────────────────────────────────
    "poyabzal": [
        {
            "id"         : "PY001",
            "nomi"       : "Oq sport sneakers (low-top)",
            "turi"       : "sneakers",
            "rang"       : "oq",
            "fasl"       : ["bahor", "yoz", "kuz"],
            "harorat_min": 8,
            "harorat_max": 40,
            "izoh"       : "Klassik oq sneakers, kundalik va sport uchun universal tanlov",
        },
        {
            "id"         : "PY002",
            "nomi"       : "Qora charm Chelsea botinka",
            "turi"       : "botinka",
            "rang"       : "qora",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": -10,
            "harorat_max": 15,
            "izoh"       : "Elegant charm botinka, sovuq va yomg'irli kunlar uchun",
        },
        {
            "id"         : "PY003",
            "nomi"       : "Qo'ng'ir klassik Oxford tufli",
            "turi"       : "tufli",
            "rang"       : "qo'ng'ir",
            "fasl"       : ["bahor", "kuz"],
            "harorat_min": 10,
            "harorat_max": 25,
            "izoh"       : "Rasmiy charm tufli, ish uchrashuvlari va tadbirlar uchun",
        },
        {
            "id"         : "PY004",
            "nomi"       : "Bej ochiq sandal",
            "turi"       : "sandal",
            "rang"       : "bej",
            "fasl"       : ["yoz"],
            "harorat_min": 25,
            "harorat_max": 45,
            "izoh"       : "Ochiq poyabzal, juda issiq yoz kunlari uchun ideal",
        },
        {
            "id"         : "PY005",
            "nomi"       : "Qora rezina Wellington etik",
            "turi"       : "etik",
            "rang"       : "qora",
            "fasl"       : ["kuz", "bahor"],
            "harorat_min": 2,
            "harorat_max": 20,
            "izoh"       : "100% suv o'tkazmaydigan, yomg'ir va loyqa yo'llar uchun ideal",
        },
        {
            "id"         : "PY006",
            "nomi"       : "Qo'ng'ir trekking botasi",
            "turi"       : "trekking bota",
            "rang"       : "qo'ng'ir",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": -5,
            "harorat_max": 18,
            "izoh"       : "Suv o'tkazmaydigan, qo'shimcha issiqlik, sayr va trekking uchun",
        },
    ],

    # ────────────────────────────────────────────
    # 🎩 AKSESSUARLAR (Accessories)
    # ────────────────────────────────────────────
    "aksessuarlar": [
        {
            "id"         : "AK001",
            "nomi"       : "Qora jun shapka (beanie)",
            "turi"       : "shapka",
            "rang"       : "qora",
            "fasl"       : ["qish", "kuz"],
            "harorat_min": -15,
            "harorat_max": 8,
            "izoh"       : "Yumshoq jun shapka, quloq va boshni sovuqdan saqlaydi",
        },
        {
            "id"         : "AK002",
            "nomi"       : "Ko'k-kulrang jun shal",
            "turi"       : "shal",
            "rang"       : "ko'k/kulrang",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": -10,
            "harorat_max": 15,
            "izoh"       : "Issiq va chiroyli shal, bo'yin va ko'krakni isitadi",
        },
        {
            "id"         : "AK003",
            "nomi"       : "Qora charm qo'lqop",
            "turi"       : "qo'lqop",
            "rang"       : "qora",
            "fasl"       : ["qish"],
            "harorat_min": -15,
            "harorat_max": 3,
            "izoh"       : "Ichki qo'shimchali charm qo'lqop, kuchli sovuqlarda zarur",
        },
        {
            "id"         : "AK004",
            "nomi"       : "Qo'ng'ir charm kamar",
            "turi"       : "kamar",
            "rang"       : "qo'ng'ir",
            "fasl"       : ["qish", "kuz", "bahor", "yoz"],
            "harorat_min": -15,
            "harorat_max": 45,
            "izoh"       : "Klassik charm kamar, barcha kiyimlar bilan mos universal aksessuar",
        },
        {
            "id"         : "AK005",
            "nomi"       : "Qora Aviator quyosh ko'zoynagi",
            "turi"       : "ko'zoynagi",
            "rang"       : "qora",
            "fasl"       : ["yoz", "bahor"],
            "harorat_min": 15,
            "harorat_max": 45,
            "izoh"       : "UV400 polarizatsiyali ko'zoynagi, chiroyli va himoyali",
        },
        {
            "id"         : "AK006",
            "nomi"       : "Qora avtomatik soyabon",
            "turi"       : "soyabon",
            "rang"       : "qora",
            "fasl"       : ["kuz", "bahor", "yoz"],
            "harorat_min": -5,
            "harorat_max": 35,
            "izoh"       : "Yomg'irli kunlar uchun zarur, ixcham katlanadigan mustahkam soyabon",
        },
        {
            "id"         : "AK007",
            "nomi"       : "Ko'k-kulrang ryukzak (30L)",
            "turi"       : "ryukzak",
            "rang"       : "ko'k/kulrang",
            "fasl"       : ["qish", "kuz", "bahor", "yoz"],
            "harorat_min": -15,
            "harorat_max": 45,
            "izoh"       : "Universal 30 litrlik ryukzak, ish, maktab va sayohat uchun",
        },
    ],

    # ────────────────────────────────────────────
    # 👕 ICHKI KIYIM VA FUTBOLKALAR (Tops / Innerwear)
    # ────────────────────────────────────────────
    "ichki_kiyim_va_futbolkalar": [
        {
            "id"         : "IF001",
            "nomi"       : "Oq paxta yumaloq yoqali futbolka (t-shirt)",
            "turi"       : "futbolka",
            "rang"       : "oq",
            "fasl"       : ["yoz", "bahor", "kuz"],
            "harorat_min": 15,
            "harorat_max": 45,
            "izoh"       : "Asosiy oq futbolka, har qanday kombinatsiya uchun baza kiyim",
        },
        {
            "id"         : "IF002",
            "nomi"       : "Qora yengsiz futbolka (tank top / muscle shirt)",
            "turi"       : "tank top",
            "rang"       : "qora",
            "fasl"       : ["yoz"],
            "harorat_min": 28,
            "harorat_max": 45,
            "izoh"       : "Juda issiq kunlar yoki sport mashg'ulotlari uchun",
        },
        {
            "id"         : "IF003",
            "nomi"       : "Ko'k-oq chiziqli polo ko'ylak",
            "turi"       : "polo",
            "rang"       : "ko'k/oq chiziq",
            "fasl"       : ["bahor", "yoz", "kuz"],
            "harorat_min": 15,
            "harorat_max": 30,
            "izoh"       : "Smart casual polo, yarim rasmiy va kundalik qulay ko'rinish",
        },
        {
            "id"         : "IF004",
            "nomi"       : "Qizil uzun yengli termal kiyim (base layer)",
            "turi"       : "termal kiyim",
            "rang"       : "qizil",
            "fasl"       : ["qish", "kuz"],
            "harorat_min": -15,
            "harorat_max": 8,
            "izoh"       : "Issiqlikni saqlaydi, ustki kiyimlar tagiga kiyiladi",
        },
        {
            "id"         : "IF005",
            "nomi"       : "Kulrang yumaloq yoqali jun sviter",
            "turi"       : "sviter",
            "rang"       : "kulrang",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": -5,
            "harorat_max": 16,
            "izoh"       : "Yumshoq merino jun sviter, kundalik va dam olish uchun",
        },
        {
            "id"         : "IF006",
            "nomi"       : "To'q ko'k uzun yengli klassik ko'ylak (shirt)",
            "turi"       : "ko'ylak",
            "rang"       : "to'q ko'k",
            "fasl"       : ["qish", "kuz", "bahor"],
            "harorat_min": 5,
            "harorat_max": 22,
            "izoh"       : "Rasmiy ko'ylak, blazer ostiga ham, mustaqil ham kiyiladi",
        },
    ],
}


# ================================================================
# 🔧 YORDAMCHI FUNKSIYALAR
# ================================================================

def get_wardrobe_as_text() -> str:
    """
    Garderobdagi barcha kiyimlarni AI uchun tushunarli tuzilmali
    matn formatiga o'giradi.

    AI bu matnga asoslanib kiyim tanlaydi. Format aniq va strukturali
    bo'lgani uchun AI xato qilish ehtimoli kamayadi.

    Returns:
        str: Barcha kiyimlar ro'yxati — formatlangan matn
    """
    category_labels: dict[str, str] = {
        "ustki_kiyim"              : "🧥 USTKI KIYIMLAR (Outerwear)",
        "shimlar"                  : "👖 SHIMLAR (Bottoms)",
        "poyabzal"                 : "👟 POYABZAL (Footwear)",
        "aksessuarlar"             : "🎩 AKSESSUARLAR (Accessories)",
        "ichki_kiyim_va_futbolkalar": "👕 ICHKI KIYIM VA FUTBOLKALAR (Tops)",
    }

    lines: list[str] = []
    total: int = 0

    for cat_key, items in WARDROBE.items():
        label = category_labels.get(cat_key, cat_key.upper())
        lines.append(f"\n{label}:")
        lines.append("─" * 58)

        for item in items:
            lines.append(
                f"  • [{item['id']}] {item['nomi']}\n"
                f"    Rang: {item['rang']}  |  "
                f"Harorat oralig'i: {item['harorat_min']}°C – {item['harorat_max']}°C  |  "
                f"Fasllari: {', '.join(item['fasl'])}"
            )
            total += 1

    header = f"JAMI GARDEROBDA: {total} ta kiyim elementi\n{'═' * 58}"
    return header + "\n" + "\n".join(lines)


def get_total_items() -> int:
    """Garderobbagi umumiy kiyim elementlari sonini qaytaradi."""
    return sum(len(items) for items in WARDROBE.values())


def get_items_by_category(category: str) -> list[ClothingItem]:
    """
    Berilgan toifadagi barcha kiyimlarni qaytaradi.

    Args:
        category: Toifa kaliti (masalan, "shimlar", "poyabzal")

    Returns:
        list: Toifadagi kiyimlar ro'yxati (bo'sh bo'lishi mumkin)
    """
    return WARDROBE.get(category, [])
