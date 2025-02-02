from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os

teacher = TinyDB('teachers.json')
Teacher = Query()
def find_teacher(update, context):
    update.message.reply_text("🔎 Please provide any information about the teacher: 🏫")

def teach(update, context):
    reply = [
        ['🔍 Find Teacher'],
        ['📄 Show Teachers', '➕ Add Teachers'],
        ['⬅️ Main Menu 🔙'],
        ['🗑️ Clear Teacher List'],
       ['send message all students'] ,
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("🏫 Hey bro! What would you like to do with teachers? 🎓", reply_markup=key)

def clear_teacher(update, context):
    teacher.truncate()
    update.message.reply_text("🗑️ The teacher list has been completely cleared! 🎉")

def teacher_request(update, context):
    update.message.reply_text("📝 Please send teacher info in this format:\n📚 Teacher/name/surname/phone\nExample: Teacher/Aliyev/Ilyos/998901234567 📞")

def add_teacher(update, context):
    matn = update.message.text.split('/')
    
    if len(matn) != 4 or matn[0].strip().lower() != 'teacher':
        update.message.reply_text("⚠️ Error: Incorrect format! Use this format:\n📚 Teacher/name/surname/phone")
        return
    
    name, surname, phone = matn[1].strip(), matn[2].strip(), matn[3].strip()
    
    if teacher.search((Teacher.name == name) & (Teacher.Surname == surname) & (Teacher.Phone == phone)):
        update.message.reply_text("⛔ This teacher is already registered! 📋")
        return

    teacher.insert({'name': name, 'Surname': surname, 'Phone': phone})
    update.message.reply_text("🎉 Teacher successfully added! ✅")






TOKEN = os.environ['TOKEN']









updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

updater.start_polling()
updater.idle()