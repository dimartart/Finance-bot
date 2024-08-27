import telebot
import datetime
import expenses
import categories
import re

from config import BOT_TOKEN
from telebot import types


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def show_all_commands(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_add = types.KeyboardButton("Add expense ➕")
	button_show = types.KeyboardButton("Show all expenses 📓")
	button_statistics = types.KeyboardButton("Statistics 📈")
	button_clear = types.KeyboardButton("Reset category 0️⃣")
	button_categories = types.KeyboardButton("Available categories 📖")
	button_support = types.KeyboardButton("Delete all expenses ❌")
	markup.add(button_add, button_show, button_statistics, button_clear, button_categories, button_support)

	bot.send_message(message.from_user.id, "Hello! Let's count your expenses\n"
										   "For bot control use the menu on the left ->", reply_markup=markup)


@bot.message_handler(regexp="Add expense")
def add_expense(message):
	bot.send_message(message.from_user.id,
					 "To add the expense just send\n"
					 "in chat message in format: \n\n"
					 "<b>\"category amount\"</b>\n\n"
					 "List of all available categories you can check\n"
					 "By pressing the button \"Available catigories\" in menu", parse_mode="HTML")


@bot.message_handler(regexp="Statistic")
def statistics(message):
	keyboard = types.InlineKeyboardMarkup()
	key_today = types.InlineKeyboardButton(text="For today", callback_data="today")
	key_month = types.InlineKeyboardButton(text="For month", callback_data="month")
	key_year = types.InlineKeyboardButton(text="For year", callback_data="year")
	keyboard.add(key_today, key_month, key_year, row_width=2)

	bot.send_message(message.from_user.id, "Choose the period for cheking statistic", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "today":
		today(message=call.message)
	elif call.data == "month":
		month(message=call.message)
	elif call.data == "year":
		year(message=call.message)
	bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(regexp="Show all expenses")
def show_expenses(message):
	all_expenses = expenses.get_expenses(message.chat.id)
	if all_expenses != "":
		answer_message = f"Expenses for the whole time:\n{all_expenses}"
		bot.send_message(message.chat.id, answer_message)
	else:
		bot.send_message(message.chat.id, """You don't have any expenses!""")


@bot.message_handler(regexp="Reset category")
def delete_expense(message):
	bot.send_message(message.chat.id, """Write the category for reseting the amount""")
	bot.register_next_step_handler(message, clear_func)


@bot.message_handler(regexp="Available categories")
def show_categories(message):
	categories_str = '\n'.join(categories.categories)
	bot.send_message(message.chat.id, categories_str)


@bot.message_handler(regexp="Delete all expenses")
def delete_all_expenses(message):
	expenses.delete_all(message.chat.id)
	bot.send_message(message.chat.id, "All expenses were succesfully deleted")


@bot.message_handler(func=lambda m: True)
def add_consumption(message):
	parsed_message = message.text.split()
	if not is_message_correct(message.text):
		bot.send_message(message.chat.id,
						 "I can't understand the message, plese write it\n" 
						 "in a correct format, for example:\n"
						 "<b>\"food 200\"</b>",
						 parse_mode="HTML")
	else:
		parsed_message.append(message.chat.id)
		expenses.add_expense(parsed_message)
		bot.send_message(message.from_user.id, "Expense was added")


def today(message):
	today_date = datetime.datetime.now().strftime("%Y-%m-%d")
	answer_message = expenses.get_today_statistics(message.chat.id)
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Expense for today {today_date}:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "There are no expenses for today")


def month(message):
	month_date = datetime.datetime.now().strftime("%Y-%m")
	answer_message = expenses.get_month_statistics(message.chat.id)
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Expenses for the month {month_date}:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "There are no expenses for this month")


def year(message):
	year_date = datetime.datetime.now().strftime("%Y")
	answer_message = expenses.get_year_statistics(message.chat.id)
	if answer_message != "":
		bot.send_message(message.chat.id, f"""Expenses for the year {year_date}:\n{answer_message}""")
	else:
		bot.send_message(message.chat.id, "There are no expenses for the year")


def is_message_correct(message_text : str) :
	match = re.findall(r"^([a-z]+)\s(\d{1,8})\Z", message_text, re.MULTILINE)
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
		bot.send_message(message.chat.id, """Category was succesfully reset""")
	else:
		bot.send_message(message.chat.id, """This category doesn't exist""")

bot.polling()