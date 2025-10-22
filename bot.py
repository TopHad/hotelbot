import os
from telebot import TeleBot, types

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")  # e.g. my_hotel_admin (без @)

bot = TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")



# In-memory per-chat storage of message IDs that should be deleted on "Назад"
CHAT_TO_MESSAGE_IDS: Dict[int, List[int]] = {}
CHAT_TO_MAIN_MESSAGE_ID: Dict[int, int] = {}


MAIN_BUTTONS = [
    "Расположение отеля",
    "Время завтрака",
    "Вечерний суп",
    "Wi-Fi",
    "Гладильная комната",
    "Услуги прачечной",
    "Ежедневная уборка",
    "Заказ трансфера",
    "Контакты",
    "Написать администратору",
]

# Map of section keys to display texts
SECTION_KEY_TO_TEXT: Dict[str, str] = {
    "location": (
        "Расположение отеля\n\n"
        "Art HOTEL 4*\n"
        "Адрес: ул. Белинского, 31, Пермь, Россия, 614002\n"
        "Сайт: www.arthotelperm.ru"
    ),
    "breakfast": (
        "Время завтрака\n\n"
        "Всем гостям отеля предоставляется завтрак в зале «Русские сезоны».\n"
        "Будние дни: 07:00–10:00\n"
        "Выходные дни: 08:00–11:00"
    ),
    "soup": (
        "Вечерний суп\n\n"
        "Ежедневно с 19:00 до 21:00 в зале «Русские сезоны» — комплимент от отеля: «Вечерний суп».\n"
        "Для уточнения вида супа обратитесь на ресепшен. Приятного вечера!"
    ),
    "wifi": (
        "Wi‑Fi\n\n"
        "Сеть: Arthotelperm\n"
        "Пароль: zsedcx12*\n"
        "Примечание: символ * в пароле обязателен."
    ),
    "ironing": (
        "Гладильная комната\n\n"
        "Для вашего удобства на этаже находится гладильная комната.\n"
        "Она расположена в номерном коридоре напротив номера 16 и доступна для вас круглосуточно.\n\n"
        "Если вы предпочитаете не гладить вещи самостоятельно, наша служба горничных с радостью поможет вам.\n"
        "За дополнительной информацией, пожалуйста, обратитесь на стойку ресепшн."
    ),
    "laundry": (
        "Услуги прачечной\n\n"
        "В шкафу номера есть пакет для вещей и бланк заказа — укажите ФИО, номер комнаты и дату.\n"
        "Если не требуется срочность, оставьте пакет в номере — его заберут во время уборки после 14:00.\n"
        "Срочно? Позвоните на ресепшен по номеру 200 — горничные заберут пакет из вашего номера."
    ),
    "cleaning": (
        "Ежедневная уборка\n\n"
        "Уборка номера проводится ежедневно с 14:00 до 16:00.\n"
        "Нужна срочная уборка? Позвоните на ресепшен по номеру 200."
    ),
    "transfer": (
        "Заказ трансфера\n\n"
        "Трансфер из аэропорта или ж/д вокзала — 1000 ₽.\n"
        "Пожалуйста, предупредите нас заранее для организации."
    ),
    "contacts": (
        "Контакты\n\n"
        "Art HOTEL 4*\n"
        "Адрес: ул. Белинского, 31, Пермь, Россия, 614002\n"
        "Телефон: +7 (342) 212-2-212 (доб. 2)\n"
        "Сайт: www.arthotelperm.ru\n"
        "E‑mail: booking@arthotelperm.ru"
    ),
}

GREETING_TEXT = (
    "Добрый день, это бот Art HOTEL 4*!\n"
    "Выберите нужный пункт:"
)

# Stickers for each section (using popular sticker pack IDs)
SECTION_STICKERS = {
    "location": "CAACAgIAAxkBAAIBY2YAAAAA",  # 📍 Location sticker - замените на реальный ID
    "breakfast": "CAACAgIAAxkBAAIBZGYAAAAA",  # 🍳 Breakfast sticker - замените на реальный ID
    "soup": "CAACAgIAAxkBAAIBZWYAAAAA",      # 🍲 Soup sticker - замените на реальный ID
    "wifi": "CAACAgIAAxkBAAIBZmYAAAAA",      # 📶 WiFi sticker - замените на реальный ID
    "ironing": "CAACAgIAAxkBAAIBZ2YAAAAA",   # 👔 Ironing sticker - замените на реальный ID
    "laundry": "CAACAgIAAxkBAAIBaGYAAAAA",   # 🧺 Laundry sticker - замените на реальный ID
    "cleaning": "CAACAgIAAxkBAAIBaWYAAAAA",  # 🧹 Cleaning sticker - замените на реальный ID
    "transfer": "CAACAgIAAxkBAAIBamYAAAAA",  # 🚗 Transfer sticker - замените на реальный ID
    "contacts": "CAACAgIAAxkBAAIBa2YAAAAA",  # 📞 Contacts sticker - замените на реальный ID
    "admin": "CAACAgIAAxkBAAIBbGYAAAAA",     # 👨‍💼 Admin sticker - замените на реальный ID
}


def build_main_inline_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("📍 Расположение отеля", callback_data="menu:location"),
        types.InlineKeyboardButton("🍳 Время завтрака", callback_data="menu:breakfast"),
        types.InlineKeyboardButton("🍲 Вечерний суп", callback_data="menu:soup"),
        types.InlineKeyboardButton("📶 Wi-Fi", callback_data="menu:wifi"),
        types.InlineKeyboardButton("👔 Гладильная комната", callback_data="menu:ironing"),
        types.InlineKeyboardButton("🧺 Услуги прачечной", callback_data="menu:laundry"),
        types.InlineKeyboardButton("🧹 Ежедневная уборка", callback_data="menu:cleaning"),
        types.InlineKeyboardButton("🚗 Заказ трансфера", callback_data="menu:transfer"),
        types.InlineKeyboardButton("📞 Контакты", callback_data="menu:contacts"),
    )
    # 👉 кнопка со ссылкой на WhatsApp
    keyboard.add(
        types.InlineKeyboardButton(
            "👨‍💼 Написать администратору", url="https://wa.me/79194425233"
        )
    )
    return keyboard



def build_back_inline_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return keyboard


def _get_bucket(chat_id: int) -> List[int]:
    bucket = CHAT_TO_MESSAGE_IDS.get(chat_id)
    if bucket is None:
        bucket = []
        CHAT_TO_MESSAGE_IDS[chat_id] = bucket
    return bucket


def send_and_track(chat_id: int, text: str) -> None:
    sent = bot.send_message(chat_id, text, reply_markup=build_back_inline_keyboard())
    _get_bucket(chat_id).append(sent.message_id)


def ensure_main_message(chat_id: int) -> int:
    """Ensure there is a single main menu message; return its message_id."""
    mid = CHAT_TO_MAIN_MESSAGE_ID.get(chat_id)
    if mid is not None:
        try:
            bot.edit_message_text(
                GREETING_TEXT,
                chat_id=chat_id,
                message_id=mid,
                reply_markup=build_main_inline_keyboard(),
            )
            return mid
        except Exception:
            # If editing failed (deleted/invalid), fall through to send a new one
            pass
    sent = bot.send_message(chat_id, GREETING_TEXT, reply_markup=build_main_inline_keyboard())
    CHAT_TO_MAIN_MESSAGE_ID[chat_id] = sent.message_id
    return sent.message_id


def clear_tracked_messages(chat_id: int) -> None:
    bucket = CHAT_TO_MESSAGE_IDS.get(chat_id, [])
    if not bucket:
        return
    for mid in bucket:
        try:
            bot.delete_message(chat_id, mid)
        except Exception:
            # Ignore errors (e.g., message already deleted or not found)
            pass
    CHAT_TO_MESSAGE_IDS[chat_id] = []


@bot.message_handler(commands=["start", "help"])  # /start, /help
def handle_start(message):
    ensure_main_message(message.chat.id)


def send_section_by_key(chat_id: int, key: str, base_message_id: int | None) -> None:
    if key == "admin":
        text = (
            f"Связаться с администратором: @{ADMIN_USERNAME}"
            if ADMIN_USERNAME
            else (
                "Для связи с администратором укажите имя пользователя в переменной "
                "окружения ADMIN_USERNAME (без @)."
            )
        )
        # Send admin message normally
        message_id = base_message_id or CHAT_TO_MAIN_MESSAGE_ID.get(chat_id)
        if message_id is not None:
            try:
                bot.edit_message_text(
                    text,
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=build_back_inline_keyboard(),
                )
                CHAT_TO_MAIN_MESSAGE_ID[chat_id] = message_id
                return
            except Exception:
                pass
        # Fallback to sending a new message
        sent = bot.send_message(chat_id, text, reply_markup=build_back_inline_keyboard())
        CHAT_TO_MAIN_MESSAGE_ID[chat_id] = sent.message_id
    elif key == "location":
        # Special handling for location with image
        text = SECTION_KEY_TO_TEXT.get(key)
        if not text:
            return
        
        # Delete the main message first
        if base_message_id:
            try:
                bot.delete_message(chat_id, base_message_id)
            except Exception:
                pass
        
        # Send sticker first (temporarily disabled until real sticker IDs are added)
        # sticker_id = SECTION_STICKERS.get("location")
        # if sticker_id:
        #     try:
        #         sent_sticker = bot.send_sticker(chat_id, sticker_id)
        #         _get_bucket(chat_id).append(sent_sticker.message_id)
        #     except Exception:
        #         pass  # If sticker fails, continue with text
        
        # Send location info with image
        try:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, 'map.PNG')
            
            with open(image_path, 'rb') as photo:
                sent = bot.send_photo(
                    chat_id, 
                    photo, 
                    caption=text,
                    reply_markup=build_back_inline_keyboard()
                )
                # Don't track this as main message, it will be deleted on back
                _get_bucket(chat_id).append(sent.message_id)
        except FileNotFoundError:
            # If image not found, send text only
            sent = bot.send_message(chat_id, text, reply_markup=build_back_inline_keyboard())
            _get_bucket(chat_id).append(sent.message_id)
        except Exception:
            # If any error, send text only
            sent = bot.send_message(chat_id, text, reply_markup=build_back_inline_keyboard())
            _get_bucket(chat_id).append(sent.message_id)
    else:
        text = SECTION_KEY_TO_TEXT.get(key)
        if not text:
            return
        
        # Send sticker first (temporarily disabled until real sticker IDs are added)
        # sticker_id = SECTION_STICKERS.get(key)
        # if sticker_id:
        #     try:
        #         sent_sticker = bot.send_sticker(chat_id, sticker_id)
        #         _get_bucket(chat_id).append(sent_sticker.message_id)
        #     except Exception:
        #         pass  # If sticker fails, continue with text
        
        # Prefer editing the tapped message to keep chat compact
        message_id = base_message_id or CHAT_TO_MAIN_MESSAGE_ID.get(chat_id)
        if message_id is not None:
            try:
                bot.edit_message_text(
                    text,
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=build_back_inline_keyboard(),
                )
                CHAT_TO_MAIN_MESSAGE_ID[chat_id] = message_id
                return
            except Exception:
                pass
        # Fallback to sending a new message (and remember it as main)
        sent = bot.send_message(chat_id, text, reply_markup=build_back_inline_keyboard())
        CHAT_TO_MAIN_MESSAGE_ID[chat_id] = sent.message_id


@bot.callback_query_handler(func=lambda call: call.data.startswith("menu:"))
def handle_menu_callback(call):
    key = call.data.split(":", 1)[1]
    chat_id = call.message.chat.id
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    send_section_by_key(chat_id, key, base_message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def handle_back_callback(call):
    chat_id = call.message.chat.id
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    
    # Delete the current message (which could be a photo or text)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    
    # Delete previously sent section messages (legacy)
    clear_tracked_messages(chat_id)
    
    # Send fresh main menu
    ensure_main_message(chat_id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def handle_back_to_main_callback(call):
    # Alias to the same behavior as back
    handle_back_callback(call)


def main() -> None:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")
        print("Trying to restart...")
        main()


if __name__ == "__main__":
    main()



