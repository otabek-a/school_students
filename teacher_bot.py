from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
from message import message_bot
school = TinyDB('students.json')
teacher = TinyDB('teachers.json')
Student = Query()
chat=TinyDB('id.json')
Student = Query()
Teacher = Query()
result={}

def find_teacher(update, context):
    update.message.reply_text(" 🧐Please provide any information about the teache after this    🔎 " )
def teach(update, context):
    reply = [
        ['🧐 Find Teacher'],
        ['📄 Show Teachers', '➕ Add Teachers'],
        ['⬅️ Main Menu 🔙'],
        ['🗑️ Clear Teacher List'],
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("🏫 Hey bro! What would you like to do with teachers? 🎓", reply_markup=key)


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
def show_teachers(update, context):
    teachers = teacher.all()
    if not teachers:
        update.message.reply_text("📄 The teacher list is empty. 🏷️")
        return

    text = "📚 List of teachers:\n"
    for idx, t in enumerate(teachers, start=1):
        text += f"{idx}. {t['name']} {t['Surname']} - 📞 {t['Phone']}\n"

    update.message.reply_text(text)
def search_teacher(update, context):
    query = update.message.text.replace("🔎", "").strip().lower()  # "🔎" ni olib tashlash
    if not query:
        update.message.reply_text("❌ Iltimos, izlash uchun ma'lumot kiriting! 🔍")
        return
    
    results = teacher.search((Teacher.name.matches(query, flags=1)) | (Teacher.Surname.matches(query, flags=1)))
    
    if not results:
        update.message.reply_text(f"❌ i could not find in LIST TEACHERS😓 : {query} ")
        return
    
    text = "🔍 list of teacher:\n"
    for idx, t in enumerate(results, start=1):
        text += f"{idx}. {t['name']} {t['Surname']} - 📞 {t['Phone']}\n"
    
    update.message.reply_text(text)