from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.loop import MessageLoop
from update import *
from animator import *
import pprint as pp
import subprocess
import telepot
import time
import json

TOKEN = '432078963:AAH3BLtr7JxgHL-RcsdHYZzWpjB1wMsITr0'
bot = telepot.Bot(TOKEN)

state = 0

def handle(msg):
    global state
    global query
    global found
    global served
    global drink
    global updater
    global x
    global y

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    pp.pprint(msg)

    if (state == 0 and msg['text']=='/start') or (state == 10 and msg['text'] == 'Yes') or (state == 5 and msg['text'] == 'Thank you!'):
        kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Go to the Customer 1")], [KeyboardButton(text="Go to the Customer 2")],[KeyboardButton(text="Tidy up")]], one_time_keyboard=True)
        bot.sendMessage(chat_id, text='What should I do ?', reply_markup=kb_markup)
        state = 1

    if state == 1 and (msg['text'] == 'Go to the Customer 1' or msg['text'] == 'Go to the Customer 2'):
        query = []
        query = ([msg['text'].split()[0].lower()] + [msg['text'][-1]])
        if query[1] not in served:
            served.append(query[1])
            updater.writer_goal(query)
            x,y = updater.take_robot_position()
            subprocess.call('../full_project/run_fast.sh')
            updater.writer_robot_position(query)        
            ani = Animator('sas_plan',[x,y])
            ani.plotter()
            del ani
            subprocess.call('../full_project/delete_plan.sh')
            kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Coke")], [KeyboardButton(text="Beer")],[KeyboardButton(text="Water")]], one_time_keyboard=True)
            bot.sendMessage(chat_id, text="Hi, I'm the service robot of this bar, what do you want to drink?", reply_markup=kb_markup)
            state = 2

        else:
            kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Yes")], [KeyboardButton(text="No")]], one_time_keyboard=True)
            bot.sendMessage(chat_id, text='I have already served the Customer '+str(query[1])+'. Do I have to do anything else?', reply_markup = kb_markup)
            state = 10

    if state == 1 and msg['text'] == 'Tidy up':
        query = []
        query.append(msg['text'].lower())
        updater.writer_goal(query)
        x,y = updater.take_robot_position()
        subprocess.call('../full_project/run_fast.sh')
        updater.writer_robot_position(query)
        updater.writer_init(query)
        with open('sas_plan','r') as f:
            lines = f.readlines()
            if len(lines) == 1 and lines == ['; cost = 0 (unit cost)\n']:         
                found = False
            else:
                found = True
        
        if found == True:
            served = []
            ani = Animator('sas_plan',[x,y])
            ani.plotter()
            del ani
            subprocess.call('../full_project/delete_plan.sh')
            kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Yes")], [KeyboardButton(text="No")]], one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Ok, I have done that. Do I have to do anything else?', reply_markup = kb_markup)
            state  = 10

        else:
            kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Yes")], [KeyboardButton(text="No")]], one_time_keyboard=True)
            bot.sendMessage(chat_id, text="It's all already clean. Do I have to do anything else?", reply_markup = kb_markup)
            state = 10

    if state == 2 and (msg['text'] == 'Coke' or msg['text'] == 'Beer' or msg['text'] == 'Water'):
        drink = msg['text']
        bot.sendMessage(chat_id, text='Ok, give me few seconds')
        updater.writer_goal(['bar',query[1]])
        x,y = updater.take_robot_position()
        subprocess.call('../full_project/run_fast.sh')
        updater.writer_robot_position(['bar',query[1]])
        updater.writer_init(['bar',query[1]])
        ani = Animator('sas_plan',[x,y])
        ani.plotter()
        del ani
        subprocess.call('../full_project/delete_plan.sh')
        state = 3

    if state == 3:
        bot.sendMessage(chat_id, text='Hey John, can you put on the tray a bottle of '+str(drink)+' for the Customer '+str(query[1])+' ?')
        time.sleep(3)
        bot.sendMessage(chat_id, text='Thank you man!')
        updater.writer_goal(['come_back',query[1]])
        x,y = updater.take_robot_position()
        subprocess.call('../full_project/run_fast.sh')
        updater.writer_robot_position(['come_back',query[1]])
        updater.writer_init(['come_back',query[1]])
        ani = Animator('sas_plan',[x,y])
        ani.plotter()
        del ani
        subprocess.call('../full_project/delete_plan.sh')
        state = 4

    if state == 4:
        kb_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Thank you!")]], one_time_keyboard=True)
        bot.sendMessage(chat_id, text='A bottle of '+str(drink)+' as you asked.', reply_markup = kb_markup)
        state = 5

    if state == 10 and msg['text'] == 'No':
        bot.sendMessage(chat_id, text='Bye bye.')
        state = 100

served = []
updater = Update('./downward/problem.pddl')
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(100)