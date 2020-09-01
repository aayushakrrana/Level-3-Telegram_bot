import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Voice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, )
import sqlite3

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FILL, NAME, COLLEGE, SIDEPROJECT, PLANGUAGE, MULTIPLESELECT, FRAMEWORK,CHECKFRAMEWORK, PROJECTS, PSKILLS, GITHUB_, LEVEL= range(12)



def start(update, context):
    update.message.reply_text('Side Projects is a community of young developers '
    'and professionals looking for programming projects. \n\n'
    'If you are interested, press /fillup to send us about yourself')

    return FILL

def fill(update, context):
    id = update.message.chat_id
    text = update.message.text
    if text == '/fillup':
        update.message.reply_text('What is your name?')
    return NAME

def name(update, context):
    global name_
    id = update.message.chat_id
    text = update.message.text
    name_=text
    update.message.reply_text('Which college are you from?')

    return COLLEGE

def college(update, context):
    global college_name
    reply_keyboard = [['Friends'],['Whatsapp Group'],['LinkedIn'],['Facebook']]
    id = update.message.chat_id
    text = update.message.text
    college_name=text


    update.message.reply_text('How did you get to know about SideProjects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SIDEPROJECT

def side_project(update, context):
    ReplyKeyboardRemove()
    global reference_
    reply_keyboard = [['Done'],['Java'],['JavaScript'],['Python'],['CSS'],['C++'],['C'],['C#'],['HTML'],['HTML5'],['PHP'],['Objective C'],['SQL'],['R'],['Ruby']]
    id = update.message.chat_id
    text = update.message.text
    reference_=text
    update.message.reply_text('Which programming languages do you know?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard))

    return PLANGUAGE

dict = {}
final_level = 0
languages_=''
def multiple_select(update, context):
    global languages_
    global dict
    global final_level
    id = update.message.chat_id
    text = update.message.text
    languages_ += text + ', '
    if id not in dict:
        dict[id]= []
    dict[id].append(text)
    final_level =final_level+1
    return PLANGUAGE

def programming_language(update, context):
    global dict
    global final_level
    if(final_level<=3):
        final_level=1
    elif(final_level<=6 and final_level>3):
        final_level=2
    else:
        final_level=3


    ReplyKeyboardRemove()
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    dict[id] = set(dict[id])
    lang_list = dict[id]
    text = (','.join(lang_list))
    del dict[id]

    update.message.reply_text('Do you know any frameworks? ',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHECKFRAMEWORK
framework_="NONE"
def list_framework(update, context):
    global final_level
    global framework_
    final_level=final_level*10
    framework_="YES"
    ReplyKeyboardRemove()
    update.message.reply_text('List them with comma(,) seperated.')

    return FRAMEWORK

framework_list="NULL"
def framework(update, context):
    global framework_
    global framework_list
    global final_level
    if(final_level>=10):
        final_level=final_level/10
    elif(final_level<10):
        final_level=1
    else:
        pass
    ReplyKeyboardRemove()
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    text = update.message.text
    framework_list=text
    lst = text.split(",")

    if(len(lst)==0):
        final_level=1
    elif(len(lst)==1):
        if(final_level<3):
            final_level=1
        elif(final_level>=3):
            final_level=2
        else:
            pass
    elif(len(lst)<4):
        if(final_level<3):
            final_level=2
        elif(final_level>=3):
            final_level=3
        else:
            pass
    elif(len(lst)>=4):
        if(final_level<3):
            final_level=2
        elif(final_level>=3):
            final_level=3
        else:
            pass

    update.message.reply_text('Have you previously done any projects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PROJECTS
#prev_project = "YES"
def projects(update, context):
    global prev_project
    global final_level
    ReplyKeyboardRemove()
    reply_keyboard = [['Very_Confident'],['Confident_Enough'],['Still_learning']]
    id = update.message.chat_id
    text = update.message.text
    prev_project=text
    update.message.reply_text('How confident are you about your programming skills?.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return GITHUB_

def github_(update, context):
    global final_level
    global confidence_
    ReplyKeyboardRemove()
    id = update.message.chat_id
    text = update.message.text
    #print(2,text)
    confidence_= text
    if(text=='Very_Confident'):
        if(final_level<3):
            final_level=final_level+1
        else:
            final_level=final_level
    elif(text=='Confident_Enough'):
        if(final_level>=3):
            final_level=final_level-1
        else:
            final_level=final_level
    elif(text=='Still_learning'):
        if(final_level>=3):
            final_level=final_level-1
        else:
            final_level=final_level
    else:
        pass

    update.message.reply_text('Please share your github repository for us to keep track of your work.')

    return LEVEL

def level(update, context):
    global final_level
    global name_
    global college_name
    global languages_
    global framework_
    global framework_list
    global prev_project
    global confidence_
    global reference_
    global github_

    id = update.message.chat_id
    text = update.message.text
    github_=text
    update.message.reply_text('Based on your coding experience, we feel you should join Side Project levelling process at:- Level{} . Please further communicate with Side Projects admin, Happy Coding! '.format(final_level))
    conn = sqlite3.connect('side_project.db')
    c=conn.cursor()
    c.execute("""CREATE TABLE if not exists members
                            (name text,
                            college_name text,
                            reference text,
                            languages text,
                            framework text,
                            framework_list text,
                            prev_project text,
                            confidence text,
                            github text,
                            final_level text
                            )""")

    c.execute(''' INSERT INTO members(name,college_name, reference,languages, framework,framework_list,prev_project,confidence,github,final_level)
              VALUES(?,?,?,?,?,?,?,?,?,?) ''',(name_,college_name,reference_,languages_,framework_,framework_list,prev_project,confidence_,github_,final_level))
    #print(name_, college_name, reference_, languages_,framework_,framework_list,prev_project,confidence_,github_,final_level)

    conn.commit()
    conn.close()
    return ConversationHandler.END


def cancel(update, context):
    return ConversationHandler.END


def main():
    updater = Updater("bot-token", use_context=True)

    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            FILL: [MessageHandler(Filters.text, fill)],

            NAME: [MessageHandler(Filters.text, name)],

            COLLEGE: [MessageHandler(Filters.text, college)],

            SIDEPROJECT: [MessageHandler(Filters.regex('^(Friends|Whatsapp Group|LinkedIn|Facebook)$'), side_project)],
             PLANGUAGE: [MessageHandler(Filters.regex('^(Java|JavaScript|Python|CSS|C\+\+|C|C#|HTML|HTML5|PHP|Objective C|SQL|R|Ruby)$'), multiple_select),
                        MessageHandler(Filters.regex('Done$'),programming_language)
                        ],

            MULTIPLESELECT:[MessageHandler(Filters.regex('^(Java|JavaScript|Python|CSS|C\+\+|C|C#|HTML|HTML5|PHP|Objective C|SQL|R|Ruby)$'), multiple_select),
                        MessageHandler(Filters.regex('Done$'),programming_language)
                        ],

            CHECKFRAMEWORK: [MessageHandler(Filters.regex('^Yes$'),list_framework),
                       MessageHandler(Filters.regex('^No$'),framework),
                       ],

            FRAMEWORK: [MessageHandler(Filters.text, framework)],

            PROJECTS: [MessageHandler(Filters.regex('^(Yes|No)$'), projects)],

            GITHUB_: [MessageHandler(Filters.text, github_)],
            LEVEL: [MessageHandler(Filters.text,level)]

            },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
