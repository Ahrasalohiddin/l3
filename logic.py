import telebot
from logic import get_random_question, format_question, check_answer

# Создаем экземпляр бота
API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Переменная для хранения текущего счета
user_scores = {}

# Стартовая команда
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_scores[message.chat.id] = 0  # Инициализируем счетчик для нового пользователя
    bot.reply_to(message, "Привет! Я помогу тебе подготовиться к экзамену по математике. Готов? Напиши /test, чтобы начать.")

# Команда для начала теста
@bot.message_handler(commands=['test'])
def start_test(message):
    question = get_random_question()
    formatted_question = format_question(question)
    bot.send_message(message.chat.id, formatted_question)
    bot.register_next_step_handler(message, process_answer, question, 1)

# Обработка ответа пользователя
def process_answer(message, question, question_number):
    user_answer = message.text.strip()
    
    # Проверяем ответ
    if check_answer(user_answer, question):
        bot.reply_to(message, "Правильно! Молодец!")
        user_scores[message.chat.id] += 1  # Увеличиваем счетчик
    else:
        bot.reply_to(message, f"Неправильно. Правильный ответ: {question['correct_option']}.")
    
    # Проверяем, сколько вопросов уже задано
    if question_number < 6:  
        question = get_random_question()
        formatted_question = format_question(question)
        bot.send_message(message.chat.id, formatted_question)
        bot.register_next_step_handler(message, process_answer, question, question_number + 1)
    else:
        # Завершаем тест и выводим счет
        score = user_scores[message.chat.id]
        bot.send_message(message.chat.id, f"Тест завершен! Ты набрал {score} из 6.")
        user_scores[message.chat.id] = 0  # Сбросить счетчик для следующего теста

# Запуск бота
bot.polling()
