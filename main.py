from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
from config import Token
from data_gruop import create_group, clear_group, show_group,register_group
from message import message_bot
from student_bot import student, find_student, add, search_student, register_student, show_students
from clear_data import student_clear, clear_teacher
from teacher_bot import find_teacher, teach, teacher_request, add_teacher, show_teachers, search_teacher

school = TinyDB('students.json')
teacher = TinyDB('teachers.json')
data_group = TinyDB('group.json')
chat = TinyDB('id.json')

Student = Query()
Teacher = Query()
Group = Query()
result = {}

def start(update: Update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    existing_user = chat.search(Student.chat_id == chat_id)
   
    if not existing_user:
        chat.insert({'chat_id': chat_id})
        update.message.reply_text("✅ We're glad to see you! 😊")

    reply = [
        ['👨‍🎓 Students 🏫', '🏫 Teachers 📚'],
        ['📢 Send Message to All Students'],
        ['🆕 Create Group', '🗑️ Clear Group List', '📜 Show Groups']
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("👋 Hello! Welcome to the School Bot 🤖!\nPlease choose an option to proceed: ⬇️", reply_markup=key)

def check_message(update, context):
    matn = update.message.text.strip().lower()
    chat_id = update.message.chat_id
    if matn.startswith('teacher/'):
        add_teacher(update,context)
    if matn.startswith('🔎'):
        search_teacher(update,context)
    if matn.startswith('🔍'):
        search_student(update,context)
    if matn.startswith('group.'):
        register_group(update,context)
    if '/' in matn:
        register_student(update,context)

    
    

    if matn.startswith('*123'):
        message_to_send = matn[4:].strip()
        if not message_to_send:
            update.message.reply_text("⚠️ Message cannot be empty! 📢")
            return
        for user in chat.all():
            try:
                context.bot.send_message(chat_id=user['chat_id'], text=f"📢 Message from Admin: {message_to_send}")
            except Exception as e:
                print(f"Error: {e}")
        update.message.reply_text("✅ Message sent to all users! 🚀")

TOKEN = Token
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text('🧐 Find Teacher'), find_teacher))
dispatcher.add_handler(MessageHandler(Filters.text('📜 Show Groups'), show_group))
dispatcher.add_handler(MessageHandler(Filters.text("🆕 Create Group"), create_group))
dispatcher.add_handler(MessageHandler(Filters.text('🗑️ Clear Group List'), clear_group))
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
dispatcher.add_handler(MessageHandler(Filters.text("📢 Send Message to All Students"), message_bot))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))

updater.start_polling()
updater.idle()




