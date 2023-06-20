import telebot
import datetime
import expenses
import categories


#the data should put in the massage in format "category number"

bot = telebot.TeleBot("5728308228:AAHTqNKbTwJGXiKDk7q3-gCmDSLPBWnCnhc")


@bot.message_handler(commands=['start', 'help'])
def show_all_commands(message):
	bot.send_message(message.from_user.id,
					 'Бот для подсчета ваших расходов\n'+
					 'Здесь команды для управления\n'+
					 'Для добавления расхода отправьте сообщение в формате "категория сумма"\n'+
					 'Для показа всех расходов /show\n'+
					 'Показать расходы за день /today\n'+
					 'Показать расходы за месяц /month\n'+
					 'Обнулить категорию /clear_category\n'+
					 'Показать список доступных категорий /categories')


@bot.message_handler(commands=["today"])
def today(message):
	answer_message = expenses.get_today_statistics()
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Расходы за сегодня:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "Сегодня расходов нет")


@bot.message_handler(commands=["month"])
def month(message):
	answer_message = expenses.get_month_statistics()
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Расходы за месяц:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "За весь месяц расходов нет")


@bot.message_handler(commands=['show'])
def show_expenses(message):
	answer_message = expenses.get_expenses()
	if answer_message != "":
		bot.send_message(message.chat.id, answer_message)
	else:
		bot.send_message(message.chat.id, """У вас нет расходов!""")


@bot.message_handler(commands=['clear_category'])
def delete_expense(message):
	bot.send_message(message.chat.id, """Напишите категорию для обнуления суммы""")
	bot.register_next_step_handler(message, clear_func)


@bot.message_handler(commands=['categories'])
def show_categories(message):
	categories_str = '\n'.join(categories.categories)
	bot.send_message(message.chat.id, categories_str)


@bot.message_handler(func=lambda m: True)
def add_consumption(message):
	parsed_message = message.text.split()
	if not is_message_correct(parsed_message):
		bot.send_message(message.chat.id, """Не могу понять сообщение. Напишите сообщение в формате, например:\nшиха 200""" )
	else:
		expenses.add_expense(parsed_message)
		bot.send_message(message.from_user.id, "Расход успешно добавлен")


def is_message_correct(parsed_message : list) :
	if (len(parsed_message) == 2 and parsed_message[1].isdigit()
			and parsed_message[0] in categories.categories):
		return True
	else:
		return False


def clear_func(message: object):
	parsed_message = message.text
	if parsed_message in categories.categories:
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