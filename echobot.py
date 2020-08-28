import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Voice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, )




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FILL, NAME, COLLEGE, SIDEPROJECT, PLANGUAGE, MULTIPLESELECT, FRAMEWORK,CHECKFRAMEWORK, PROJECTS, PSKILLS, GITHUB, LEVEL= range(12)


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
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text('Which college are you from?')

    return COLLEGE

def college(update, context):
    reply_keyboard = [['Friends'],['Whatsapp Group'],['LinkedIn'],['Facebook']]
    id = update.message.chat_id
    text = update.message.text
    

    update.message.reply_text('How did you get to know about SideProjects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SIDEPROJECT

def side_project(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Done'],['Java'],['JavaScript'],['Python'],['CSS'],['C++'],['C'],['C#'],['HTML'],['HTML5'],['PHP'],['Objective C'],['SQL'],['R'],['Ruby']]
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text('Which programming languages do you know?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    
    return PLANGUAGE

dict = {}
def multiple_select(update, context):
    global dict
    id = update.message.chat_id
    text = update.message.text
    if id not in dict:
        dict[id]= []
    dict[id].append(text)

    return PLANGUAGE

def programming_language(update, context):
    global dict
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

def list_framework(update, context):
    ReplyKeyboardRemove()
    update.message.reply_text('List them with comma(,) seperated.')

    return FRAMEWORK


def framework(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Yes'],['No']]
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text('Have you previously done any projects?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PROJECTS

def projects(update, context):
    ReplyKeyboardRemove()
    reply_keyboard = [['Very Confident'],['Confident Enough'],['Still learning']]
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text('How confident are you about your programming skills?.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ConversationHandler.END
    

def cancel(update, context):
    update.message.reply_text('Bye! ',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
    
def main():
    
    updater = Updater("1378603347:AAF1gokmMrCAhDb7rkwOQmqvrw7c_G2L2G8", use_context=True)

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

            PROJECTS: [MessageHandler(Filters.regex('^(Yes|No)$'), projects)]

            
            },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

  

