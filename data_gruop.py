from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
data_group=TinyDB('group.json')
school = TinyDB('students.json')
teacher = TinyDB('teachers.json')

chat=TinyDB('id.json')
Student = Query()
Teacher = Query()
result={}
def create_group(update,context):
    update.message.reply_text('Pls enter information of group G.group_name,T.teacher_name , D.days_of_course , W.time_of_course. For eaxmple: T.Otabek,D.Monday Friday, W.14-16')
def clear_group(update,context):
    data_group.truncate()
    update.message.reply_text('This list is empty')
def show_group(update, context):
    data = data_group.all()
    if not data:
        update.message.reply_text("📄 The teacher list is empty. 🏷️")
        return

    text = "📚 List of teachers:\n"
    for idx, t in enumerate(data, start=1):
        text += f"{idx}. {t['name']} {t['Surname']} - 📞 {t['Phone']}\n"

    update.message.reply_text(text)
    
