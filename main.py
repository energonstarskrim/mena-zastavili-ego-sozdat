import telebot
import wikipedia
import re
import random
import config
from telebot import types
import sqlite3

conn = sqlite3.connect("users.db",check_same_thread=False)
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INT);")
conn.commit()
bot = telebot.TeleBot(config.token)
game = False
num = False
admins = [6017638346]
statia=["Малыш(бомба)","АКМ","Python"]
user = []
text=""
link=""
is_wiki=False
@bot.message_handler(commands=["start"])
def test(message):
    if message.chat.id in admins:
        help(message)
    else:
        info = cur.execute("SELECT * FROM users WHERE id=?", (message.chat.id,)).fetchone()
        if not info:
            cur.execute("INSERT INTO users (id) VALUES (?)",(message.chat.id,))
            conn.commit()
            bot.send_message(message.chat.id, "Теперь вы будете получать рассылку!")
    bot.send_message(message.chat.id)

def help(message):
    admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    admin_markup.add(types.KeyboardButton("Создать текст для рассылки"))
    admin_markup.add(types.KeyboardButton("Создать ссылку для рассылки"))
    admin_markup.add(types.KeyboardButton("Показать сообщение для рассылки"))
    admin_markup.add(types.KeyboardButton("Начать рассылку"))
    admin_markup.add(types.KeyboardButton("Помощь"))
    bot.send_message(message.chat.id, "Комманды бота: \n"
                    "/create_text -- Создать текст для рассылки \n"
                    "/create_link -- Создать ссылку\n"
                    "/show_message -- Показать сообщение для рассылки \n"
                    "/start_linking -- Начать рассылку \n"
                    "/help -- Помощь",reply_markup=admin_markup)

@bot.message_handler(commands=["random_statia"])
def random_statia(message):
    choice_statia=random.choice(statia)
    bot.send_message(message.chat.id, create_wiki(choice_statia))

@bot.message_handler(commands=["wiki"])
def comm_wiki(message):
    markup_wikipedia = types.InlineKeyboardMarkup()
    bts_search = types.InlineKeyboardButton(text="Yes i want", callback_data="want")
    bts_no_search = types.InlineKeyboardButton(text="no i dont want",callback_data="wantnt")
    markup_wikipedia.add(bts_search,bts_no_search)
    bot.send_message(message.chat.id, "Хочешь что-то найти?", reply_markup=markup_wikipedia)

@bot.message_handler(commands=["create_text"])
def create_text(message):
    if message.chat.id in admins:
        m = bot.send_message(message.chat.id, "введи текст для рассылки")
        bot.register_next_step_handler(m,add_text)

@bot.message_handler(commands=["show_message"])
def show_message(message):
    bot.send_message(message.chat.id, "текст: "+text)
    bot.send_message(message.chat.id, "ccылка: "+link)

def add_text(message):
    global text
    text = message.text
    if text not in ["Дайте денег в долг"]:
        bot.send_message(message.chat.id ,f"Сохранённый текст{text}")
    else:
        bot.send_message(message.chat.id ,"Переписывай")
@bot.message_handler(commands="create_link")
def create_link(message):
    if message.chat.id in admins:
        m = bot.send_message(message.chat.id, "введите ссылку")
        bot.register_next_step_handler(m,add_link)

@bot.message_handler(commands="start_linking")
def start_linking(message):
    global text,link
    if len(text) != 0:
        if len(link) != 0:
            cur.execute("SELECT id FROM users")
            massive = cur.fetchall()
            for client_id in massive:
                id = client_id[0]
                sending(id)
            else:
                text=""
                link=""
        else: bot.send_message(message.chat.id,"нет ссылки")
    else: bot.send_message(message.chat.id,"нет текста")

def sending(id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ссылка на сайт", url=link))
    bot.send_message(id,text,reply_markup=markup)
def add_link(message):
    global link
    regex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if message.text is not None and regex.search(message.text):
        link = message.text
        bot.send_message(message.chat.id, f"Сохранил ссылку: {link}")
    else:
        m = bot.send_message(message.chat.id, "Нет")
        bot.register_next_step_handler(m, add_link)
@bot.message_handler(commands=["game"])
def game_number(message):
    global game, num
    game = True
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1")
    btn2 = types.KeyboardButton("2")
    btn3 = types.KeyboardButton("3")
    markup_reply.add(btn1,btn2,btn3)
    num = random.randint(1,3)
    bot.send_message(message.chat.id, "Я загадал число от 1 до 3, угадай!", reply_markup=markup_reply)
def test(message):
    print(message)
    bot.reply_to(message, "Дарова!Как жизнь?")
@bot.message_handler(commands=["hello"])
def test(message):
    bot.send_message(message.chat.id, "Отправил сообщение")
@bot.callback_query_handler(func=lambda call:True)
def callback_but(call):
    global is_wiki
    if call.data == "yes":
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        id = types.KeyboardButton(text="id")
        username = types.KeyboardButton(text="username")
        markup_reply.add(id, username)
        bot.send_message(call.message.chat.id, "Что тебе показать интересного?", reply_markup=markup_reply)

    if call.data == "want":
        is_wiki=True
        print('я родился')
        bot.send_message(call.message.chat.id, "wikipedia")
@bot.message_handler(content_types=["text"])

def get_text(message):
    if "Привет" == message.text:
        bot.send_message(message.chat.id,"ты написал привет")
    elif "id" == message.text:
        bot.send_message(message.chat.id, f"ваш айди: {message.from_user.id}")
    elif "usr" == message.text:
        bot.send_message(message.chat.id, f"Ваш юзер нейм: {message.from_user.username}")
    elif str(num) == message.text and message.text in ["1","2","3"] and game:
        pass
    elif is_wiki:
        text = message.text
        wiki_text = create_wiki(text)
        bot.send_message(message.chat.id,wiki_text)
wikipedia.set_lang("ru")
def create_wiki(word):
    global is_wiki
    try:
        wiki = wikipedia.page(word)
        wikitext = wiki.content[:1000]
        wiki_result = wikitext.split(".")
        wiki_result = wiki_result[:-1]
        wiki_result_2 = ""
        for i in wiki_result:
            if not ("==" in i):
                wiki_result_2 = wiki_result_2 + i + "."
        wiki_result_2 = re.sub("\([^()]*\)", "", wiki_result_2)

        return wiki_result_2
    except:
            return "error 404"
bot.infinity_polling()