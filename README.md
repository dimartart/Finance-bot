<div align="center">
  **Finance bot in telegram**
</div>

This is telegram bot for managing and checking your expenses. It is quite easy to use. When you first time will press the start button the welcome text will be displayed.

![image](https://github.com/user-attachments/assets/014aff4e-68e2-4d23-8439-4d9a5a557dcf)
 
Tap the menu button to see all possibilities of the bot.

![image](https://github.com/user-attachments/assets/57d80fc5-a7a4-4401-93a8-ca0b126d19d8)

To add your first expense just write down category of expense and amount, then send it. Bot will automatically will save information to the database.

![image](https://github.com/user-attachments/assets/7ae4409b-28cd-4601-ae67-e7f0d1abc8af)

To see all available categories use button in menu.
 
![image](https://github.com/user-attachments/assets/16adf65f-68b1-4cb0-9499-8fbd8ef9f23f)

You also can see the simple statistics about how much you have spent for the last day, month and year.

![image](https://github.com/user-attachments/assets/08b6035b-e177-4dd1-9b2a-3b88898ef7cd)

![image](https://github.com/user-attachments/assets/68fd1424-3529-4486-9c60-1f2b9e82d774)

If you want to see all your expenses just press the button in menu.

![image](https://github.com/user-attachments/assets/18dccbb6-bd27-42a2-93f3-23ca2007b8c9)

**Technical part:**
This bot was made by using telebot library which is connected to telegram API. Project contains db module which uses psycopg library for connecting and interaction with PostgreSQL database.

**Database**
For database management PgAdmin was used.
The structure of database: 

![image](https://github.com/user-attachments/assets/76b7f25e-251b-4c42-be1b-7cbf1e202861)

Database contains only 2 tables – category and expenses. It allows to show to each user his current expenses based on his id, which automatically stored to database when user enter his first expense.
