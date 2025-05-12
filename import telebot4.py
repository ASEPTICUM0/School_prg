import telebot
from telebot import types

# тут мой токен
API_TOKEN = '7565223937:AAEONfsT_EhIjj593OWpUQ5S_H9AbXSuRHA'
bot = telebot.TeleBot(API_TOKEN)

# Описание курсов
courses = {
    "Роблокс": {
        "description": "На курсе вы научитесь создавать свои собственные игры в Roblox и погрузитесь в мир гейм-дизайна.",
        "price": 50000
    },
    "Python": {
        "description": "Изучите один из самых популярных языков программирования, который используется в веб-разработке, анализе данных и машинном обучении.",
        "price": 50000
    },
    "JavaScript": {
        "description": "Научитесь создавать интерактивные веб-приложения с помощью JavaScript, основного языка для фронтенд-разработки.",
        "price": 50000
    },
    "HTML": {
        "description": "Основы веб-разработки: изучите структуру веб-страниц с помощью HTML и создайте свои первые сайты.",
        "price": 50000
    }
}

# Функция для создания клавиатуры
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for course in courses.keys():
        button = types.InlineKeyboardButton(course, callback_data=course)
        keyboard.add(button)
    return keyboard

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Добро пожаловать в нашу школу программирования! Выберите курс для получения дополнительной информации:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_keyboard())

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    course_name = call.data
    if course_name in courses:
        course_info = f"*{course_name}*\n\n{courses[course_name]['description']}\n\nЦена: *{courses[course_name]['price']} руб.*"
        bot.send_message(call.message.chat.id, course_info, parse_mode='Markdown')
        
        # Предложение записаться на курс
        bot.send_message(call.message.chat.id, "Хотите записаться на курс?", reply_markup=create_enrollment_keyboard())
    bot.answer_callback_query(call.id)

#  создание клавиатуры для записи на курс
def create_enrollment_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = types.KeyboardButton("Записаться")
    button_no = types.KeyboardButton("Нет, спасибо")
    keyboard.add(button_yes, button_no)
    return keyboard

# Обработка ответа на запись на курс
@bot.message_handler(func=lambda message: message.text in ["Записаться", "Нет, спасибо"])
def handle_enrollment_response(message):
    if message.text == "Записаться":
# запрос данных пользователя
        bot.send_message(message.chat.id, "Вы успешно записаны на курс! Мы свяжемся с вами для подтверждения.")
        bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    else:
        bot.send_message(message.chat.id, "Спасибо за интерес! Если у вас будут вопросы, не стесняйтесь спрашивать.")


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)

