from telegram import ReplyKeyboardMarkup

# Asosiy menyu tugmalarining ro‘yxati
main_menu_keyboard = [
    ["Tahlillar", "Biz bilan bog‘lanish"],
    ["Instagram manzil", "Admin bilan bog‘lanish"],
    ["Tahlil natijalari", "Taklif va shikoyat"],
    ["Qon topshirishga tayyorgarlik", "IXLA va IFA tekshiruv farqi"]
]

# ReplyKeyboardMarkup obyekti yaratish (tugmalar bilan)
main_menu = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
