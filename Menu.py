from telegram import ReplyKeyboardMarkup

def get_main_menu():
    main_menu_keyboard = [
        ["Tahlillar haqida ma'lumot", "Qon topshirish qoidalari"],
        ["Bioximiya haqida", "Klinika haqida"],
        ["IXLA va IFA tekshiruv farqi"],
        ["Biz bilan bog'lanish", "Admin bilan bog'lanish"],
        ["Tahlil natijalarini olish", "Taklif va shikoyatlar"],
        ["Kitob (Analizlar haqida to‘liq ma’lumot)"],
        ["Botga foydalanuvchi qo‘shish", "Sizni nima bezovta qilayapti"]
    ]

    return ReplyKeyboardMarkup(
        keyboard=main_menu_keyboard,
        resize_keyboard=True
    )
