from dataclasses import dataclass
import threading
from datetime import datetime
import random
import telebot
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass
class QueryQuestion:
    question: str
    button_rows: list[list[tuple[str, str] | str]]

    def __repr__(self):
        return f'QueryQuestion({self.question})'


def poll_bot_threaded(bot: TeleBot):
    thread = threading.Thread(target=bot.polling)
    thread.start()


def query_multiple_questions(
    bot: TeleBot,
    chat_id: int,
    questions_data: list[QueryQuestion],
    callback_name: str | None = None,
    callback_func: callable = None,
    prefix_call_values: list[str] | None = None,
    separator: str = '~',
):
    if len(questions_data) < 1:
        return
    if callback_name is None:
        callback_name = str(datetime.now().timestamp()) + str(random.randint(0, 1000))
    prefix_call_values = prefix_call_values or []
    callback_data_prefix = callback_name + separator + separator.join(prefix_call_values)
    query_single_question(
        bot=bot,
        chat_id=chat_id,
        question_data=questions_data[0],
        callback_data_prefix=callback_data_prefix,
        separator=separator
    )
    _define_query_callback_handler(
        bot=bot,
        callback_name=callback_name,
        questions_data=questions_data,
        callback_func=callback_func,
        num_prefixes=len(prefix_call_values),
        separator=separator
    )


def query_single_question(
    bot: TeleBot,
    chat_id: int,
    question_data: QueryQuestion,
    callback_data_prefix: str,
    separator='~',
    message_id=None
):
    keyboard = InlineKeyboardMarkup()
    for button_row in question_data.button_rows:
        button_objects = []
        for button_data in button_row:
            text = button_data[0] if isinstance(button_data, tuple) else button_data
            callback = button_data[1] if isinstance(button_data, tuple) else button_data
            button_callback_data = callback_data_prefix + separator + callback
            button_object = InlineKeyboardButton(
                text.capitalize(), callback_data=button_callback_data
            )
            button_objects.append(button_object)
        keyboard.row(*button_objects)
    if message_id is None:
        bot.send_message(chat_id, question_data.question, reply_markup=keyboard)
    else:
        bot.edit_message_text(question_data.question, chat_id, message_id, reply_markup=keyboard)


def _define_query_callback_handler(
    bot: TeleBot,
    callback_name: str,
    questions_data: list[QueryQuestion],
    callback_func: callable,
    num_prefixes: int,
    separator='~'
):
    @bot.callback_query_handler(func=lambda call: call.data.startswith(callback_name))
    def query_callback_handler(call: telebot.types.CallbackQuery):
        callback_data = call.data.split(separator)
        query_answers = callback_data[num_prefixes + 1:]
        if len(query_answers) < len(questions_data):
            next_question_data = questions_data[len(query_answers)]
            query_single_question(
                bot=bot,
                chat_id=call.message.chat.id,
                question_data=next_question_data,
                callback_data_prefix=call.data,
                separator=separator,
                message_id=call.message.message_id
            )
        elif callback_func is not None:
            callback_func(callback_data[1:], message_id=call.message.id, chat_id=call.message.chat.id)



if __name__ == '__main__':
    def print_results(results):
        print(results)
    from dotenv import load_dotenv
    import os
    load_dotenv()
    chat_id_ = 784020584
    bot_ = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
    poll_bot_threaded(bot_)
    questions_data_ = [
        QueryQuestion(
            question='What is your favorite color?',
            button_rows=[
                ['red', 'green', 'blue'],
                ['yellow', 'purple', 'orange']
            ]
        ),
        QueryQuestion(
            question='What is your favorite animal?',
            button_rows=[
                ['dog', 'cat', 'elephant'],
                ['lion', 'tiger', 'bear']
            ]
        )
    ]
    query_multiple_questions(bot_, chat_id_, 'query', questions_data_, print_results, ['test1', 'tesgt23'])

