import telebot
import datetime
import expenses
import categories
import re
from telebot import types

#the data should put in the massage in format "category number"

bot = telebot.TeleBot("5728308228:AAHTqNKbTwJGXiKDk7q3-gCmDSLPBWnCnhc")


@bot.message_handler(commands=['start'])
def show_all_commands(message):
	markup = types.ReplyKeyboardMarkup()
	button_add = types.KeyboardButton("Добавить расход ➕")
	button_show = types.KeyboardButton("Показать все расходы 📓")
	button_statistics = types.KeyboardButton("Статистика")
	button_clear = types.KeyboardButton("Обнулить категорию")
	button_categories = types.KeyboardButton("Доступные категории")
	markup.add(button_add, button_show, button_statistics, button_clear, button_categories)

	bot.send_message(message.from_user.id, "Приветствую! Посчитаем расходы?", reply_markup=markup)


@bot.message_handler(regexp="Добавить расход")
def add_help(message):
	bot.send_message(message.from_user.id,
					 "Чтобы добавить расход,\n"
					 "просто отправьте в чат сообщение в формате\n"
					 "\"категория сумма\"\n" 
					 "Список доступных категорий вы можете посмотреть,\n"
					 "нажав кнопку \"Доступные категории\" в меню")


@bot.message_handler(regexp="Статистика")
def statistics(message):
	keyboard = types.InlineKeyboardMarkup()
	key_today = types.InlineKeyboardButton(text="Расходы за сегодня", callback_data="today")
	key_month = types.InlineKeyboardButton(text="Расходы за месяц", callback_data="month")
	key_year = types.InlineKeyboardButton(text="Расходы за год по месяцам", callback_data="year")
	keyboard.add(key_today, key_month, key_year)

	bot.send_message(message.from_user.id, "Выберете период для просмотра статистики", reply_markup=keyboard)


def today(message):
	today_date = datetime.datetime.now().strftime("%Y-%m-%d")
	answer_message = expenses.get_today_statistics(message.chat.id)
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Расходы за сегодня {today_date}:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "Сегодня расходов нет")


def month(message):
	month_date = datetime.datetime.now().strftime("%Y-%m")
	answer_message = expenses.get_month_statistics(message.chat.id)
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Расходы за месяц {month_date}:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "За месяц расходов нет")


def year(message):
	pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "today":
		today(message=call.message)
	elif call.data == "month":
		month(message=call.message)
	elif call.data == "year":
		year(message=call.message)


@bot.message_handler(regexp="Показать все расходы")
def show_expenses(message):
	answer_message = f" Расходы за все время:\n{expenses.get_expenses(message.chat.id)}"
	if answer_message != "":
		bot.send_message(message.chat.id, answer_message)
	else:
		bot.send_message(message.chat.id, """У вас нет расходов!""")


@bot.message_handler(regexp="Обнулить категорию")
def delete_expense(message):
	bot.send_message(message.chat.id, """Напишите категорию для обнуления суммы""")
	bot.register_next_step_handler(message, clear_func)


@bot.message_handler(regexp="Доступные категории")
def show_categories(message):
	categories_str = '\n'.join(categories.categories)
	bot.send_message(message.chat.id, categories_str)


@bot.message_handler(func=lambda m: True)
def add_consumption(message):
	parsed_message = message.text.split()
	if not is_message_correct(message.text):
		bot.send_message(message.chat.id, """Не могу понять сообщение. Напишите сообщение в формате, например:\nшиха 200""" )
	else:
		parsed_message.append(message.chat.id)
		expenses.add_expense(parsed_message)
		bot.send_message(message.from_user.id, "Расход успешно добавлен")


def is_message_correct(message_text : str) :
	match = re.findall(r"^([а-я]+)\s(\d+)\Z", message_text, re.MULTILINE)
	category = ''
	if match != []:
		category = match[0][0]
		if category in categories.categories:
			return True
		else:
			return False
	else:
		return False


def clear_func(message: object):
	parsed_message = [message.text, message.chat.id]
	if parsed_message[0] in categories.categories:
		expenses.clear(parsed_message)
		bot.send_message(message.chat.id, """Категория успешно обнулена""")
	else:
		bot.send_message(message.chat.id, """Такой категории нет. Показать список категорий?\n /categories """)

#
# @bot.message_handler(commands=['history'])
# def show_history(message):
# 	global list_with_all_data
# 	line_transform_from_list_to_line=''
# 	for tupl in list_with_all_data:
# 		line_transform_from_list_to_line += f'{tupl[0]} '+f'{tupl[1]} '+f'  DATE:{tupl[2]}'+'\n'
# 	bot.send_message(message.from_user.id,line_transform_from_list_to_line)
#
#
# @bot.message_handler(commands=['show'])
# def show_the_cost_of_all_things(message):
# 	global dict_for_all_consumption
# 	if len(dict_for_all_consumption)!=0:
# 		line_transform_from_dict_to_line = ''
# 		for key in dict_for_all_consumption:
# 			line_transform_from_dict_to_line += key + ' ' + str(dict_for_all_consumption[key]) + '\n'
# 		bot.send_message(message.from_user.id, line_transform_from_dict_to_line+'\n'
# 																				f'Total: {str(sum(dict_for_all_consumption.values()))}')
# 	else:
# 		bot.send_message(message.from_user.id,'Тут ничего нет!')
#
# @bot.message_handler(commands=['clear_all'])
# def clear_the_positions(message):
# 	dict_for_all_consumption.clear()
# 	bot.send_message(message.from_user.id, "категория очищена!")
#
# @bot.message_handler(commands=['delete_category'])
# def delete_category_1(message):
# 	bot.send_message(message.from_user.id,'Input category please')
# 	bot.register_next_step_handler(message,delete_category)
#
#
# def delete_category(message):
# 	if message.text in dict_for_all_consumption:
# 		del dict_for_all_consumption[message.text]
# 		bot.send_message(message.from_user.id, "deleted")
# 	else:
# 		bot.send_message(message.from_user.id,'you cant delete unknown position')

	# global our_message
	# our_message=message.text.split()
	# if len(our_message)==2 and our_message[1].isdigit():
	# 	temp_typle=(our_message[0],our_message[1],datetime.datetime.now().strftime("%d-%m-%Y"))
	# 	list_with_all_data.append(temp_typle)
	# 	if our_message[0] not in dict_for_all_consumption.keys():
	# 		dict_for_all_consumption[our_message[0]] = int(our_message[1])
	# 		bot.send_message(message.from_user.id, "Расход добавлен!")
	# 	else:
	# 		dict_for_all_consumption[our_message[0]]= dict_for_all_consumption.get(our_message[0]) + int(our_message[1])
	# 		bot.send_message(message.from_user.id, "Расход добавлен!")
	# else:
	# 	bot.send_message(message.from_user.id, "Слишком мало аргументов!")

bot.polling()