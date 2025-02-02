from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
from message import message_bot
from student_bot import student,find_student,add,search_student,register_student,show_students
from clear_data import student_clear,clear_teacher
from teacher_bot import find_teacher,teach,teacher_request,add_teacher,show_teachers,search_teacher
school = TinyDB('students.json')
teacher = TinyDB('teachers.json')

chat=TinyDB('id.json')
Student = Query()
Teacher = Query()
result={}

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
                print(f"Mistake: {e}")

        update.message.reply_text("✅ message is sended to all users!")

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
dispatcher.add_handler(MessageHandler(Filters.text("send message all students"),message_bot))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))




updater.start_polling()
updater.idle()
