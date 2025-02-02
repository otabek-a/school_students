from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
school = TinyDB('students.json')
Student = Query()
def student(update, context):
    reply = [
        ['🗑️ Clear Student List'],
        ['➕ Add Students', '📄 Show Students'],
        ['⬅️ Main Menu 🔙'],
        ['🧐 Find Students'],
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("👨‍🎓 Hey bro! What would you like to do with students? 🎓", reply_markup=key)
def find_student(update, context):
    update.message.reply_text("🧐Please provide any information about the student after this  🔍  word ")
def add(update, context):
    update.message.reply_text("📝 Please send student info in this format:\n👤 name/surname/phone\nExample: Otabek/Abdurasulov/991928212 📞")









def register_student(update, context):
    matn = update.message.text.split('/')
    
    if len(matn) != 3:
        update.message.reply_text("⚠️ Error: Incomplete student information! Use this format:\n👤 name/surname/phone")
        return
    
    name, surname, phone = matn[0].strip(), matn[1].strip(), matn[2].strip()
    
    if school.search((Student.name == name) & (Student.Surname == surname) & (Student.Phone == phone)):
        update.message.reply_text("⛔ This student is already registered! 📋")
        return

    school.insert({'name': name, 'Surname': surname, 'Phone': phone})
    update.message.reply_text("🎉 Student successfully added! ✅")



def show_students(update, context):
    students = school.all()
    
    if not students:
        update.message.reply_text("📄 The student list is empty. 🏷️")
        return
    
    text = "📚 List of students:\n"
    for idx, student in enumerate(students, start=1):
        text += f"{idx}. {student['name']} {student['Surname']} - 📞 {student['Phone']}\n"
    
    update.message.reply_text(text)



def search_student(update, context):
    query = update.message.text.replace("🔍", "").strip()  # "🔍" belgisini olib tashlash
    if not query:
        update.message.reply_text("❌ Iltimos, izlash uchun ma'lumot kiriting! 🔍")
        return
    
    results = school.search((Student.name.matches(query, flags=1)) | (Student.Surname.matches(query, flags=1)))
    
    if not results:
        update.message.reply_text(f"❌ I could not find: {query} ")
        return
    
    text = "🔍 List of students:\n"
    for idx, student in enumerate(results, start=1):
        text += f"{idx}. {student['name']} {student['Surname']} - 📞 {student['Phone']}\n"
    
    update.message.reply_text(text)