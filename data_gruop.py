from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os

data_group = TinyDB('group.json')
school = TinyDB('students.json')
teacher = TinyDB('teachers.json')
chat = TinyDB('id.json')

Student = Query()
Teacher = Query()
result = {}

def create_group(update, context):
    update.message.reply_text("📌 Please enter the group details in this format:\n\n"
                              "Group.group_name, teacher, days, time ⏳")

def clear_group(update, context):
    data_group.truncate()
    update.message.reply_text("🗑️ The group list has been cleared!")

def show_group(update, context):
    data = data_group.all()
    if not data:
        update.message.reply_text("📜 The group list is empty! ❌")
        return

    text = "📚 List of Groups:\n\n"
    for idx, t in enumerate(data, start=1):
        text += f"{idx}. 📌 {t['group name']}\n"
        text += f"   👨‍🏫 Teacher: {t['teacher']}\n"
        text += f"   📅 Days: {t['days']}\n"
        text += f"   ⏰ Time: {t['time of course']}\n"
        text += "--------------------------\n"

    update.message.reply_text(text)
