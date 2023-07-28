import argparse
import os
import random
import redis

from dotenv import load_dotenv
from enum import Enum
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from parser import parse_qa


class States(Enum):
    QUESTION = 1
    ANSWER = 2


def start(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("Привет! Я бот для викторин!", reply_markup=reply_markup)

    return States.QUESTION


def handle_new_question_request(update: Update, context: CallbackContext) -> None:
    questions = list(context.bot_data["qa_dict"].keys())
    question = random.choice(questions)

    update.message.reply_text(question)
    user_id = update.message.from_user.id
    context.bot_data["redis"].set(user_id, question)

    return States.ANSWER


def handle_solution_attempt(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_answer = update.message.text.lower()
    last_question = context.bot_data["redis"].get(user_id).decode('utf-8')

    full_correct_answer = context.bot_data["qa_dict"][last_question]
    cut_correct_answer = full_correct_answer.replace("Ответ: ", "")
    correct_answer = cut_correct_answer.split('.')[0].split('(')[0].lower()

    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    if user_answer == correct_answer:
        update.message.reply_text("Правильно! Для следующего вопроса нажми «Новый вопрос».",
                                  reply_markup=reply_markup)
    else:
        update.message.reply_text("Неправильно… Попробуешь ещё раз?", reply_markup=reply_markup)

    return States.QUESTION


def handle_give_up(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    last_question = context.bot_data["redis"].get(user_id).decode('utf-8')
    correct_answer = context.bot_data["qa_dict"][last_question]
    update.message.reply_text(correct_answer)

    return handle_new_question_request(update, context)


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='questions/1vs1200.txt', help='Путь к файлу с вопросами и ответами')
    args = parser.parse_args()

    redis_db = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASSWORD')
    )

    try:
        qa_dict = parse_qa(args.path)
    except Exception as e:
        print(f"Ошибка прочтения файла: {e}")
        return

    updater = Updater(os.getenv('TG_TOKEN'))
    updater.dispatcher.bot_data["qa_dict"] = qa_dict
    updater.dispatcher.bot_data["redis"] = redis_db

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            States.QUESTION: [MessageHandler(Filters.regex('^Новый вопрос$'), handle_new_question_request)],
            States.ANSWER: [
                MessageHandler(Filters.regex('^Сдаться$'), handle_give_up),
                MessageHandler(Filters.text & ~Filters.command, handle_solution_attempt),
            ],
        },

        fallbacks=[]
    )
    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
