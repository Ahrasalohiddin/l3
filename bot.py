import telebot
from random import choice
from config import TOKEN
bot = telebot.TeleBot(TOKEN)

# Пример базы вопросов
questions = [
    {
        "question": "Чему равно 1290+3000-1500",
        "options": ["2560", "2790", "2005", "1006"],
        "correct_option": "2790"
    },
    {
        "question": "Чему равен x3 + 9 = 45?",
        "options": ["12", "23", "13", "19"],
        "correct_option": "12"
    },
    {
        "question": "Решите уравнение: 2x^2 - 3x - 2 = 0?",
        "options": ["4 и 5", "6 и -3", "2 и -1", "1 и -9"],
        "correct_option": "2 и -1"
    },
    {
        "question": "Чему равен детерминант матрицы [[1, 2], [3, 4]]?",
        "options": ["3", " -3", "-2", "-1"],
        "correct_option": "-2"
    },
    {
        "question": "Какое наименьшее значение имеет функция f(x) = x^2 + 2x + 1?",
        "options": ["-1", "0", "1", "2"],
        "correct_option": "0"
    },
    {
        "question": "Рассчитайте площадь треугольника со сторонами 7, 24 и 25.",
        "options": ["84", "96", "120", "168"],
        "correct_option": "84"
    }

]

# Стартовая команда
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я помогу тебе подготовиться к экзамену по математике.Если напишешь слово test то я тебе задам 6 вопросов Готов?")

# Команда для начала теста
@bot.message_handler(commands=['test'])
def start_test(message):
    question = choice(questions)
    options = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(question['options'])])
    bot.send_message(message.chat.id, f"{question['question']}\n{options}")
    bot.register_next_step_handler(message, check_answer, question)

# Функция проверки ответа
def check_answer(message, question):
    if message.text == question['correct_option']:
        bot.reply_to(message, "Правильно! Молодец!")
    else:
        bot.reply_to(message, f"Неправильно. Правильный ответ: {question['correct_option']}.")

# Запуск бота
bot.polling()
