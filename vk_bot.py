import os
import random
import redis
import vk_api

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from parser import parse_qa


def get_keyboard():
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def main():
    load_dotenv()
    vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    qa_dict = parse_qa()

    redis_db = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASSWORD')
    )

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id

            if event.text == 'Начать':
                vk.messages.send(user_id=user_id,
                                 message='Привет! Я бот для викторин!',
                                 random_id=random.randint(1, 1000),
                                 keyboard=get_keyboard())

            elif event.text == 'Новый вопрос':
                questions = list(qa_dict.keys())
                question = random.choice(questions)

                vk.messages.send(user_id=user_id,
                                 message=question,
                                 random_id=random.randint(1, 1000),
                                 keyboard=get_keyboard())
                redis_db.set(user_id, question)

            elif event.text == 'Сдаться':
                last_question = redis_db.get(user_id).decode('utf-8')
                correct_answer = qa_dict[last_question]
                vk.messages.send(user_id=user_id,
                                 message=correct_answer,
                                 random_id=random.randint(1, 1000),
                                 keyboard=get_keyboard())

                questions = list(qa_dict.keys())
                question = random.choice(questions)
                vk.messages.send(user_id=user_id,
                                 message=question,
                                 random_id=random.randint(1, 1000),
                                 keyboard=get_keyboard())

                redis_db.set(user_id, question)

            elif event.text == 'Мой счет':
                vk.messages.send(user_id=user_id,
                                 message='Функционал подсчета очков пока не реализован.',
                                 random_id=random.randint(1, 1000),
                                 keyboard=get_keyboard())

            else:
                last_question = redis_db.get(user_id).decode('utf-8')
                full_correct_answer = qa_dict[last_question]
                cut_correct_answer = full_correct_answer.replace("Ответ: ", "")
                correct_answer = cut_correct_answer.split('.')[0].split('(')[0].lower()

                if event.text.lower() == correct_answer:
                    vk.messages.send(user_id=user_id,
                                     message="Правильно! Для следующего вопроса нажми «Новый вопрос».",
                                     random_id=random.randint(1, 1000),
                                     keyboard=get_keyboard())
                else:
                    vk.messages.send(user_id=user_id,
                                     message="Неправильно… Попробуешь ещё раз?",
                                     random_id=random.randint(1, 1000),
                                     keyboard=get_keyboard())


if __name__ == '__main__':
    main()
