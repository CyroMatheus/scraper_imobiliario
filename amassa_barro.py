import telebot
from User import *
import pprint, json, os
import requests


api_key = "6766343615:AAFBjkseJO9Ee1YNaYoE3whefWzQoy2KWLc"
bot = telebot.TeleBot(api_key)

db_users = {
    "path": f'/home/cyro/Documentos/codes/palacis/db_users',
    "json_u": json.load(open(f'/home/cyro/Documentos/codes/palacis/db_users/users.json'))
}
user = User()

def verify_msg(msg):
    return True

@bot.message_handler(commands=['start'])
def check_user(msg):
    bot.send_message(msg.from_user.id, f"Olá, {msg.from_user.first_name} {msg.from_user.last_name}")
    if not msg.from_user.id in db_users['json_u']:
        text = f"""Vejo que você é novo por aqui.\nPara continuar clique em /cadastrar"""
        bot.send_message(msg.from_user.id, text)
        return False
    else:
        text = """Clique na opção que deseja:\n/postar\n/retornos"""
        bot.reply_to(msg, f"Olá, {msg.from_user.first_name} {msg.from_user.last_name}\n {text}")
        return True

@bot.message_handler(commands=['cadastrar'])
def store(msg):
    base_user = {
        "id": msg.from_user.id,
        "first_name": msg.from_user.first_name,
        "last_name": msg.from_user.last_name
    }
    text = "Pra começar preciso do email, senha e codigo que você usa no canal pro, clique em: \n/email \n/senha\n/codigo"
    for key, value in enumerate(base_user):
        user.set_data(value, base_user[value])
    bot.send_message(msg.from_user.id, text)

@bot.message_handler(commands=['email'])
def email(msg):
    bot.send_message(msg.from_user.id,"Envie o email da seguinte forma 'email:seuemailaqui@email.com'")

@bot.message_handler(commands=['senha'])
def pws(msg):
    bot.send_message(msg.from_user.id, "Envie o email da seguinte forma 'senha:suasenhaaqui'")

@bot.message_handler(commands=['codigo'])
def id_post(msg):
    bot.send_message(msg.from_user.id, "Envie o email da seguinte forma 'codigo:seucodigoaqui'")


@bot.message_handler(func=verify_msg)
def store_user(msg):
    value = None
    if "email:" in msg.text:
        value = msg.text.replace("email:", "")
        user.set_data("login", value)
    if "senha:" in msg.text:
        value = msg.text.replace("senha:", "")
        user.set_data("psw", value)
    if "codigo:" in msg.text:
        value = msg.text.replace("codigo:", "")
        user.set_data("id_post", value)

bot.polling()
