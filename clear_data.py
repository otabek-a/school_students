from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os
from message import message_bot
from student_bot import student,find_student
school = TinyDB('students.json')
teacher = TinyDB('teachers.json')
chat=TinyDB('id.json')
Student = Query()
Teacher = Query()
result={}


def student_clear(update, context):
    school.truncate()
    update.message.reply_text("🗑️ The student list has been completely cleared! 🏆")

def clear_teacher(update, context):
    teacher.truncate()
    update.message.reply_text("🗑️ The teacher list has been completely cleared! 🎉")