import db
import datetime


class Message:
    """Структура распаршенного сообщения о новом расходе"""
    def __init__(self, category_text, amount, created):
        self.category_text = category_text
        self.amount = amount
        self.created = created


def add_expense(message_split : list):
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    obj_message = _parse_message(message_split)
    try:
        db.insert(obj_message)
    except:
        raise ConnectionRefusedError("Проблема с базой данных")


def get_today_statistics() -> str:
    cursor = db.get_cursor()
    cursor.execute("""SELECT category_name, SUM(amount)
                      FROM expenses WHERE date(created) = date(now())	
                      GROUP BY category_name""")
    result = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in result])
    return res_in_str


def get_month_statistics() -> str:
    cursor = db.get_cursor()
    cursor.execute("""SELECT category_name, SUM(amount)
                      FROM expenses where EXTRACT(MONTH FROM created) = 
                      EXTRACT(MONTH from now())
                      GROUP BY category_name""")
    result = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in result])
    return res_in_str


def get_expenses():
    cursor = db.get_cursor()
    cursor.execute("""SELECT c.name, SUM(amount) FROM
                        expenses e INNER JOIN category c
                        ON e.category_name = c.name
                        GROUP BY c.name""")
    res = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in res])
    return res_in_str


def clear(message : str):
    category = message
    cursor = db.get_cursor()
    cursor.execute(f"""DELETE FROM expenses
                    WHERE category_name = '{message}' """)


def _parse_message(parsed_message: list) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    category_text = parsed_message[0]
    amount = parsed_message[1]
    created = _get_now_formatted()
    return Message( category_text=category_text, amount=amount, created=created)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    now = datetime.datetime.now()
    return now