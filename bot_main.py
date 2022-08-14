from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import requests
from bs4 import BeautifulSoup



REC, LYRICS = range(2) # states for conversation
# function to handle the /start command
def start(update, context):
    update.message.reply_text('Приветствую! Этот бот ищет похожие песни. Отправь /rec для рекомендации')
    return REC

def help(update, context):
    update.message.reply_text('Чем вам помочь? Отправьте /start для начала работы с ботом. ')
# function to handle errors occured in the dispatcher

def error(update, context):
    update.message.reply_text('Упс! Произошла непредвиденная ошибка. Уже исправляем...')

def rec(update, context):
    update.message.reply_text('Введите ссылку на слова без кавычек:')
    return LYRICS

def get_lyrics(update, context):
    url = update.message.text
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    # find the lyrics data.
    cols = soup.findAll(class_="lyrics__content__ok", text=True)
    if cols:
        lyrics = "\n".join(x.text for x in cols)
    elif data := soup.find(class_="lyrics__content__warning", text=True):
        lyrics = data.get_text()
    else:
        lyrics = 'Sorry, something went wrong'
    update.message.reply_text(lyrics)
    return ConversationHandler.END

def text(update, context):
    text_received = update.message.text
    if text_received == 'привет':
        update.message.reply_text(f'И вам не хворать!')
    else:
        update.message.reply_text(f'did you said "{text_received}" ?')
def hello(update, context):
    text_recieved = update.message.text
    update.message.reply_text(f'Здравствуй!')


def main():
    TOKEN = "your token"
    # create the updater, that will     automatically create also a dispatcher and a queue to
    # make them dialogue
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # add handlers for start and help commands
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    # dispatcher.add_handler(CommandHandler("hi", hello))
    #dispatcher.add_handler(CommandHandler("rec", recomend))
    #dispatcher.add_handler(MessageHandler(Filters.text, text))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[],
        states={
            REC: [CommandHandler('rec', rec)],
            LYRICS: [MessageHandler(Filters.text, get_lyrics)],
        },
    )
    # add a handler for normal text (not commands)

    dispatcher.add_handler(conv_handler)
    # add a handler for errors
    dispatcher.add_error_handler(error)
    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()

    # TODO: to write the model that takes ANY song and recommends something reliable to listen to
if __name__ == '__main__':
    main()