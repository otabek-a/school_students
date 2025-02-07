from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
Group = Query()
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
def register_group(update, context):
    matn = update.message.text.strip().lower()
    chat_id = update.message.chat_id

    if matn.startswith('group.'):
        otash = matn[6:].split(',')
        if len(otash) != 4:
            update.message.reply_text("⚠️ Invalid format. Please use:\n\nGroup.group_name,teacher,days,time")
            return
        
        group_name, teacher_name, days, course_time = map(str.strip, otash)
        existing_group = data_group.search(Group['group name'] == group_name)
        
        if existing_group:
            update.message.reply_text("🚫 This group already exists! Please try a different name.")
        else:
            data_group.insert({
                'group name': group_name, 
                'teacher': teacher_name, 
                'days': days, 
                'time of course': course_time
            })
            update.message.reply_text("✅ Group created successfully! 🎉")

