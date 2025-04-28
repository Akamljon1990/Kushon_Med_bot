from telegram import ReplyKeyboardMarkup

main_menu_keyboard = [
    ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"],
    ["Bioximiya haqida", "Klinika haqida"],
    ["IXLA va IFA tekshuruv farqi"],
    ["Biz bilan bog'lanish", "Admin bilan bog'lanish"],
    ["Tahlil natijalarini olish", "Taklif va shikoyatlar"],
    ["Kitob (Analizlar haqida to‘liq ma'lumot)"],
    ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilyapti"]
]

main_menu = ReplyKeyboardMarkup(
    keyboard=main_menu_keyboard,
    resize_keyboard=True
)
