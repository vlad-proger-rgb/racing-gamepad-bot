from telebot import TeleBot, types
import pyautogui as pt

from settings import BOT_TOKEN

# Key mappings
KEY_RUN = "w"
KEY_STOP = "s"
KEY_LEFT = "a"
KEY_RIGHT = "d"
KEY_NITRO = "shift"

events = {
    "run": False,
    "stop": False,
    "left": False,
    "right": False,
    "nitro": False,
}

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [
        "⏫ \n Run!",
        "⏬ \n Break!",
        "◀️ \n Left!",
        "▶️ \n Right!",
        "‼️ \n Nitro!",
        "❌ \n Stop all acts!",
    ]

    markup.add(*[types.KeyboardButton(text=btn) for btn in buttons])
    bot.send_message(message.chat.id, "Move!", reply_markup=markup)


def toggle_event(chat_id, event_name, key=None):
    events[event_name] = not events[event_name]

    if key:
        if events[event_name]:
            pt.keyDown(key)
        else:
            pt.keyUp(key)

    bot.send_message(chat_id, f"{event_name} {'started' if events[event_name] else 'stopped'}")


def stop_all_actions(chat_id):
    for event, active in events.items():
        if active:
            key = {
                "run": KEY_RUN,
                "stop": KEY_STOP,
                "left": KEY_LEFT,
                "right": KEY_RIGHT,
                "nitro": KEY_NITRO,
            }.get(event)
            if key:
                pt.keyUp(key)
            events[event] = False

    bot.send_message(chat_id, "All actions stopped!")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    actions = {
        "⏫ \n Run!": ("run", KEY_RUN),
        "⏬ \n Break!": ("stop", KEY_STOP),
        "◀️ \n Left!": ("left", KEY_LEFT),
        "▶️ \n Right!": ("right", KEY_RIGHT),
        "‼️ \n Nitro!": ("nitro", KEY_NITRO),
    }

    if message.text in actions:
        action, key = actions[message.text]
        toggle_event(message.chat.id, action, key)

    elif message.text == "❌ \n Stop all acts!":
        stop_all_actions(message.chat.id)


if __name__ == "__main__":
    print("Bot started!")
    bot.polling()
