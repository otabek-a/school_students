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
def create_group(update,context):
    update.message.reply_text('Pls enter information of group T.teacher_name , D.days_of_course , W.time_of_course. For eaxmple: T.Otabek,D.Monday Friday, W.14-16')