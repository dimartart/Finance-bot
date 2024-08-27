import psycopg2
from config import host, user, password, db_name


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

connection.autocommit = True
cursor = connection.cursor()


def insert(obj_message):
    category = obj_message.category_text
    amount = obj_message.amount
    created = obj_message.created
    user_id = obj_message.user_id
    cursor.execute(
        f"""INSERT INTO expenses (amount, category_name, created, user_id)
            VALUES ({amount}, '{category}', '{created}', {user_id})  
        """
    )
    connection.commit()


def get_cursor():
    return cursor

