# блок импортов
from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from constants import *
import csv
import random
from static import *


def read_csv():
    with open("victorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|"))
        return read_data


def write_to_csv(row):
    with open("victorina/database.csv", mode="a", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|", lineterminator="\n")
        writer.writerow(row)


def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(update.effective_chat.id,
                             'Добро пожаловать в викторину. Отвечай на вопросы, выбирая одну из четырех кнопок')
    update.message.reply_text(
        f"Для продолжения нажми на '{GO}'", reply_markup=markup)
    # список, внутри которого [вопрос, ответ1, ответ2, ответ3, ответ4]
    questions_list = read_csv()
    random.shuffle(questions_list)  # перемешиваем вопросы
    # длина = 5 вопросов, если такое количество есть, либо сколько вопросов есть в файле
    length = QUESTIONS_ON_ROUND if len(
        questions_list) > QUESTIONS_ON_ROUND else len(questions_list)

    questions_list = questions_list[:length]  # делаем срез
    context.user_data["questions"] = questions_list
    context.user_data["index"] = 0  # номер первого вопроса
    context.user_data["counter"] = 0
    return GAME


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Спасибо за участие в викторине!")
    update.message.reply_text("Нажми на /start, чтобы начать заново")
    return ConversationHandler.END


def game(update: Update, context: CallbackContext):
    questions_list = context.user_data["questions"]
    index = context.user_data["index"]
    if "right_answer" in context.user_data:
        right_answer = context.user_data["right_answer"]
        my_answer = update.message.text
        if right_answer == my_answer:
            context.user_data["counter"] += 1
            update.message.reply_photo(RIGHT_ANSWER_IMG)
            update.message.reply_text(random.choice(RIGHT_ANSWER_TEXTS))
        else:
            update.message.reply_photo(random.choice(WRONG_ANSWER_IMG))
            update.message.reply_text(random.choice(WRONG_ANSWER_TEXTS))
    try:
        answers = questions_list[index]  # это ответы
        question = answers.pop(0)  # это вопрос
    
        right_answer = answers[0]  # правильный ответ
        random.shuffle(answers)

        keyboard = [answers[2:], answers[:2]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(question, reply_markup=markup)

        context.user_data["index"] += 1
        context.user_data["right_answer"] = right_answer

    except IndexError:
        counter = context.user_data["counter"]
        counter_questions = len(questions_list)
        update.message.reply_text(
            f"Правильных ответов: {counter}/{counter_questions}", reply_markup=ReplyKeyboardRemove())
        if counter > QUESTIONS_ON_ROUND/2:
            update.message.reply_photo(WINNER_IMG)
            update.message.reply_text("Отличный результат!")
        else:
            update.message.reply_photo(LOSER_IMG)
            update.message.reply_text("Ты можешь лучше!")
        return ConversationHandler.END
