from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os

school = TinyDB('students.json')
teacher = TinyDB('teachers.json')
chat=TinyDB('id.json')
Student = Query()
Teacher = Query()
result={}
def message(update,context):
    update.message.reply_text('pls after your password  send me message')
def start(update: Update, context):
    global result
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    existing_user = chat.search(Student.chat_id == chat_id)
    if not existing_user:
         chat.insert({'chat_id': chat_id})
         update.message.reply_text("✅ we are glad to see you")
    
    
    
    reply = [
        ['👨‍🎓 Students 🏫', '🏫 Teachers 📚'],
        ['send message all students']]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("👋 Hello! Welcome to the School Bot 🤖!\nPlease choose an option to proceed: ⬇️", reply_markup=key)

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

def find_teacher(update, context):
    update.message.reply_text(" 🧐Please provide any information about the teache after this    🔎 " )

def student_clear(update, context):
    school.truncate()
    update.message.reply_text("🗑️ The student list has been completely cleared! 🏆")

def teach(update, context):
    reply = [
        ['🧐 Find Teacher'],
        ['📄 Show Teachers', '➕ Add Teachers'],
        ['⬅️ Main Menu 🔙'],
        ['🗑️ Clear Teacher List'],
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("🏫 Hey bro! What would you like to do with teachers? 🎓", reply_markup=key)

def clear_teacher(update, context):
    teacher.truncate()
    update.message.reply_text("🗑️ The teacher list has been completely cleared! 🎉")

def add(update, context):
    update.message.reply_text("📝 Please send student info in this format:\n👤 name/surname/phone\nExample: Otabek/Abdurasulov/991928212 📞")

def teacher_request(update, context):
    update.message.reply_text("📝 Please send teacher info in this format:\n📚 Teacher/name/surname/phone\nExample: Teacher/Aliyev/Ilyos/998901234567 📞")

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

def show_students(update, context):
    students = school.all()
    
    if not students:
        update.message.reply_text("📄 The student list is empty. 🏷️")
        return
    
    text = "📚 List of students:\n"
    for idx, student in enumerate(students, start=1):
        text += f"{idx}. {student['name']} {student['Surname']} - 📞 {student['Phone']}\n"
    
    update.message.reply_text(text)

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
    query = update.message.text.replace("🔎", "").strip()  # "🔎" ni olib tashlash
    if not query:
        update.message.reply_text("❌ Iltimos, izlash uchun ma'lumot kiriting! 🔍")
        return
    
    results = teacher.search((Teacher.name.matches(query, flags=1)) | (Teacher.Surname.matches(query, flags=1)))
    
    if not results:
        update.message.reply_text(f"❌ i could not find: {query} ")
        return
    
    text = "🔍 list of teacher:\n"
    for idx, t in enumerate(results, start=1):
        text += f"{idx}. {t['name']} {t['Surname']} - 📞 {t['Phone']}\n"
    
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

    
def check_message(update, context):
    text = update.message.text.strip()
    chat_id = update.message.chat_id
    if '🔍' in text:
        search_student(update,context)
    if '🔎' in text:
        search_teacher(update,context)
    if text.startswith("*123"): 
        message_to_send = text[4:].strip() 
        
        if not message_to_send:
            update.message.reply_text("⚠️ Xabar matni bo‘sh bo‘lishi mumkin emas! 📢")
            return
        
        subscribers = chat.all() 
        
        for user in subscribers:
            try:
                context.bot.send_message(chat_id=user['chat_id'], text=f"📢 Message from admin: {message_to_send}")
            except Exception as e:
                print(f"Xatolik: {e}")

        update.message.reply_text("✅ Xabar barcha obunachilarga yuborildi!")

    elif text.lower().startswith('teacher'):
        add_teacher(update, context)
    elif '/' in text:
        register_student(update, context)
    

TOKEN = os.environ['TOKEN']
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text('🧐 Find Teacher'), find_teacher))



dispatcher.add_handler(MessageHandler(Filters.text('➕ Add Teachers'), teacher_request))
dispatcher.add_handler(MessageHandler(Filters.text('📄 Show Teachers'), show_teachers))
dispatcher.add_handler(MessageHandler(Filters.text('📄 Show Students'), show_students))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text('⬅️ Main Menu 🔙'), start))
dispatcher.add_handler(MessageHandler(Filters.text('🗑️ Clear Teacher List'), clear_teacher))
dispatcher.add_handler(MessageHandler(Filters.text('🗑️ Clear Student List'), student_clear))
dispatcher.add_handler(MessageHandler(Filters.text('➕ Add Students'), add))
dispatcher.add_handler(MessageHandler(Filters.text('🏫 Teachers 📚'), teach))
dispatcher.add_handler(MessageHandler(Filters.text('👨‍🎓 Students 🏫'), student))
dispatcher.add_handler(MessageHandler(Filters.text('🧐 Find Students'), find_student))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))
dispatcher.add_handler(MessageHandler(Filters.text("send message all students"),message))



updater.start_polling()
updater.idle()
