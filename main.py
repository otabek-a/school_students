from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
import os

school = TinyDB('students.json')
teacher = TinyDB('teachers.json')

Student = Query()
Teacher = Query()

def start(update: Update, context):
    reply = [
        ['Show Teachers', 'Add Students', 'Show Students'],
        ['Add Teachers']
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("Hello! Please choose an option to proceed:", reply_markup=key)

def add(update, context):
    update.message.reply_text('Please, send student info like this:\nname/surname/phonenumber\nExample: Otabek/Abdurasulov/991928212')

def teacher_request(update, context):
    update.message.reply_text('Please, send teacher info like this:\nTeacher/name/surname/phone\nExample: Teacher/Aliyev/Ilyos/998901234567')

def register_student(update, context):
    matn = update.message.text.split('/')
    
    if len(matn) != 3:
        update.message.reply_text('Error: Incomplete student information! Use this format:\nname/surname/phonenumber')
        return
    
    name, surname, phone = matn[0].strip(), matn[1].strip(), matn[2].strip()
    
    if school.search((Student.name == name) & (Student.Surname == surname) & (Student.Phone == phone)):
        update.message.reply_text('This student is already registered! You cannot add them again.')
        return

    school.insert({'name': name, 'Surname': surname, 'Phone': phone})
    update.message.reply_text('Student successfully added!')

def add_teacher(update, context):
    matn = update.message.text.split('/')
    
    if len(matn) != 4 or matn[0].strip().lower() != 'teacher':
        update.message.reply_text('Error: Incorrect format! Use this format:\nTeacher/name/surname/phone\nExample: Teacher/Aliyev/Ilyos/998901234567')
        return

    name, surname, phone = matn[1].strip(), matn[2].strip(), matn[3].strip()
    
    if teacher.search((Teacher.name == name) & (Teacher.Surname == surname) & (Teacher.Phone == phone)):
        update.message.reply_text('This teacher is already registered! You cannot add them again.')
        return

    teacher.insert({'name': name, 'Surname': surname, 'Phone': phone})
    update.message.reply_text('Teacher successfully added!')

def show_students(update, context):
    students = school.all()
    students=sorted(students)
    if not students:
        update.message.reply_text('This list is empty.')
        return
    
    text = 'List of students:\n'
    for idx, student in enumerate(students, start=1):
        text += f"{idx}. {student['name']} {student['Surname']} - {student['Phone']}\n"
    
    update.message.reply_text(text)

def show_teachers(update, context):
    teachers = teacher.all()
    if not teachers:
        update.message.reply_text('This list is empty.')
        return

    text = 'List of teachers:\n'
    for idx, t in enumerate(teachers, start=1):
        text += f"{idx}. {t['name']} {t['Surname']} - {t['Phone']}\n"

    update.message.reply_text(text)

def check_message(update, context):
    text = update.message.text.strip()
    
    if text.lower().startswith('teacher'):
        add_teacher(update, context)
    
    elif '/' in text:
        register_student(update, context)
    
    else:
        update.message.reply_text('Error: Command not recognized. Please use the menu options.')

TOKEN = os.environ['TOKEN']

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text('Add Students'), add))
dispatcher.add_handler(MessageHandler(Filters.text('Show Students'), show_students))
dispatcher.add_handler(MessageHandler(Filters.text('Add Teachers'), teacher_request))
dispatcher.add_handler(MessageHandler(Filters.text('Show Teachers'), show_teachers))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))

updater.start_polling()
updater.idle()
