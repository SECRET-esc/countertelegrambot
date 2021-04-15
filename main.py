from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import telebot
import database

bot = telebot.TeleBot(config.token, parse_mode=None)
chat_id = ""
wait_sum = False
wait_show = False
is_autorizated = False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    global is_autorizated
    chat_id = message.chat.id
    if database.registerUser(message.from_user.username, message.from_user.id):
        bot.send_message(chat_id, "Привет, ты зарегестрирован и можешь работать!")
        is_autorizated = True
        send_menu(message)
    else:
        # bot.send_message(chat_id, "Ты уже зарегестрирован!")
        is_autorizated = True
        send_menu(message)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Посмотреть сумму 💵", callback_data="show_sum"), InlineKeyboardButton("Добавить сумму 💰", callback_data="add_sum"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "show_sum":
        global wait_show
        wait_show = True
        show_sum(call.message)
    elif call.data == "add_sum":
        global wait_sum
        wait_sum = True
        bot.send_message(call.message.chat.id, 'Введи сумму которую ты хочешь добавить (твое имя будет добавленно автоматически)')
        # bot.answer_callback_query(call.id, "Answer is No")
    elif call.data == "backShow":
        wait_show = False
        send_menu(call.message)


def send_menu(message):
    bot.send_message(message.chat.id, "Добро пожаловать в меню!", reply_markup=gen_markup())


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global wait_sum
    if is_autorizated:
        if wait_sum:
            if message.text.isnumeric():
                if database.addSum(message.text, message.from_user.id):
                    bot.send_message(message.chat.id, "Получилось!🎉 Данные успешно сохранены!", reply_markup=getButtonBackShow())
                    wait_sum = False
                else:
                    bot.send_message(message.chat.id, "Ошибка!😔 Что-то пошло не так!", reply_markup=getButtonBackShow())
                    wait_sum = False

            else:
                bot.send_message(message.chat.id, "Сумма должна указыватся в положительных цифрах! \n\n Пример:\n\n  900", reply_markup=getButtonBackShow())
                wait_sum = False
        else:
            send_menu(message)
    else:
        send_welcome(message)


def getButtonBackShow():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="backShow"))
    return markup


def getButtonBackAdd():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="backAdd"))
    return markup


def show_sum(message):
    res = database.showSum()
    string = ''
    i = 1
    for row in res:
        string += f'{i}. {row[2]} - {row[3]}\n\n'
        i = i + 1
    bot.send_message(message.chat.id, f"Топ 3 суммы на данный момент:\n\n{string}", reply_markup=getButtonBackShow())
    # send_menu(message)


bot.polling()
