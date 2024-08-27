import db
import datetime


class Message:
    """The stucture of parsed message about the new expense"""
    def __init__(self, category_text, amount, created, user_id):
        self.category_text = category_text
        self.amount = amount
        self.created = created
        self.user_id = user_id


def add_expense(message_split : list):
    """Add new message.
    Takes as an input the new message from user."""
    obj_message = _parse_message(message_split) #obj_message == Message object
    try:
        db.insert(obj_message)
    except:
        raise ConnectionRefusedError("Problem with database")


def get_today_statistics(user_id : int) -> str:
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT category_name, SUM(amount)
                      FROM expenses WHERE date(created) = date(now())
                      AND user_id = {user_id}	
                      GROUP BY category_name""")
    result = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in result])
    return res_in_str


def get_month_statistics(user_id : int) -> str:
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT category_name, SUM(amount)
                      FROM expenses where EXTRACT(MONTH FROM created) = 
                      EXTRACT(MONTH from now()) AND user_id = {user_id}
                      GROUP BY category_name""")
    result = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in result])
    return res_in_str


def get_year_statistics(user_id : int) ->str:
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT category_name, SUM(amount)
                      FROM expenses where EXTRACT(YEAR FROM created) = 
                      EXTRACT(YEAR from now()) AND user_id = {user_id}
                      GROUP BY category_name""")
    result = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in result])
    return res_in_str


def get_expenses(user_id : int) -> str:
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT c.name, SUM(amount) FROM
                        expenses e INNER JOIN category c
                        ON e.category_name = c.name
                        WHERE e.user_id = {user_id}
                        GROUP BY c.name""")
    res = cursor.fetchall()
    res_in_str = "\n".join([f"{tpl_values[0]}: {tpl_values[1]}" for tpl_values in res])
    return res_in_str


def clear(message : list):
    category = message[0]
    user_id = message[1]
    cursor = db.get_cursor()
    cursor.execute(f"""DELETE FROM expenses
                    WHERE category_name = '{category}'
                    AND user_id = {user_id}""")


def delete_all(user_id : int):
    user_id = user_id
    cursor = db.get_cursor()
    cursor.execute(f"DELETE FROM expenses WHERE user_id = {user_id}")


def _parse_message(parsed_message: list) -> Message:
    """Parse the text of message about the new expense."""
    category_text = parsed_message[0]
    amount = parsed_message[1]
    created = _get_now_formatted()
    user_id = parsed_message[2]
    return Message( category_text=category_text, amount=amount, created=created, user_id=user_id)


def _get_now_formatted() -> str:
    """Returns todays date in str format"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Return today's datetime from Moscow timezone"""
    now = datetime.datetime.now()
    return now