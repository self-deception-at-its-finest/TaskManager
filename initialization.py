import os
import django
from time import sleep
from colorama import Fore
from mysql.connector import connect
from mysql.connector.errors import Error, ProgrammingError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()


def database_creations():
    bd_creation_connect = connect(host='127.0.0.1',
                                  port='3306',
                                  user='root',
                                  passwd='1111')

    bd_creation_cursor = bd_creation_connect.cursor(buffered=True)

    try:
        bd_creation_cursor.execute('create database task_manager_db;')
    except Error:
        print(Fore.RED + f"Database already exists!\n" + Fore.YELLOW)
        bd_creation_cursor.execute('drop database task_manager_db;')
        sleep(2)
        print(Fore.GREEN + "Database successfully deleted!\n" + Fore.YELLOW)
        bd_creation_cursor.execute('create database task_manager_db;')
        print(Fore.GREEN + "Database task_manager_db has been created!\n" + Fore.YELLOW)
    else:
        print(Fore.GREEN + "Database task_manager_db has been created!\n" + Fore.YELLOW)


def database_migrations():
    files_list = os.listdir('application/migrations')

    for file in files_list:
        if file != '__init__.py' and file != '__pycache__':
            os.remove(f'application/migrations/{file}')
            print(Fore.CYAN + f'File {file} has been removed!' + Fore.YELLOW)
    print()

    os.system('python manage.py makemigrations')
    print(Fore.GREEN + f"\nMigration file created!\n" + Fore.BLUE)

    os.system('python manage.py migrate')
    print(Fore.GREEN + f"\nMigration successfully applied!\n")


def users_creations():
    from application.models import CustomUser
    from django.db.utils import IntegrityError, ProgrammingError

    user_info = [{'username': 'AndrewMelnyk',
                  'email': 'AndrewMelnyk@gmail.ua',
                  'first_name': 'Андрій',
                  'last_name': 'Мельник',
                  'password': '1111'},
                 {'username': 'IlonaKhmelnytska',
                  'email': 'IlonaKhmelnytska@gmail.ua',
                  'first_name': 'Ilona',
                  'last_name': 'Khmelnytska',
                  'password': '1111'}]

    for user in user_info:
        try:
            CustomUser.objects.create_user(username=user.get('username'),
                                           password=user.get('password'),
                                           email=user.get('email'),
                                           first_name=user.get('first_name'),
                                           last_name=user.get('last_name'),
                                           is_active=True,
                                           is_staff=True,
                                           is_superuser=True)

        except IntegrityError:
            print(Fore.RED + f"Username `{user.get('username')}` already exist!\n")
        except ProgrammingError:
            print(Fore.RED + f"Problem with database! Maybe it doesn't exist.\n")
        else:
            print(Fore.MAGENTA + f"User profile `{user.get('username')}` has been created!")
    print()


def insert_information_info_db():
    db_already_exist_connect = connect(host='127.0.0.1',
                                       port='3306',
                                       user='root',
                                       passwd='1111',
                                       database='task_manager_db')

    db_already_exist_cursor = db_already_exist_connect.cursor(buffered=True)

    categories_data = ('INSERT INTO task_manager_db.categories (category) VALUES '
                       '("Робота"),'
                       '("Відпочинок"),'
                       '("Домашні справи"),'
                       '("Хобі"),'
                       '("Зустрічі"),'
                       '("Спілкування"),'
                       '("Купівля");')

    try:
        db_already_exist_cursor.execute(categories_data)
        db_already_exist_connect.commit()
    except ProgrammingError:
        print(Fore.RED + "Inserting error!")
    else:
        print(Fore.LIGHTMAGENTA_EX + f"Tasks categories information successfully inserted into database!")

    tasks_data = ('INSERT INTO task_manager_db.tasks (task, user_id, category_id, prioritize, status, '
                  'creation_datetime, deadline, description) VALUES '
                  '("Сходити в магазин", 1, 7, 2, 0, "2024-09-10 18:40:22", "2024-09-25 22:00:00", "Купити хліб та '
                  'молоко"),'
                  '("Завезти інструменти", 1, 1, 1, 1, "2024-09-08 14:20:05", "2024-09-11 14:00:00", "Завести '
                  'інструменти на роботу"),'
                  '("Зібратись на рибалку", 1, 2, 3, 1, "2024-09-10 09:11:44", "2024-09-12 17:30:00", "Зібрати всі '
                  'необхідні для рибалки речі"),'
                  '("Купити пиво та закуску", 1, 7, 1, 1, "2024-09-10 09:10:12", "2024-09-12 17:30:00", "Revo, '
                  'Somersby, Тетерів"),'
                  '("Прибрати в гаражі", 1, 3, 3, 0, "2024-09-18 23:14:09", "2024-09-28 19:00:00", "Нарешті зробити '
                  'порядок в гаражі"),'
                  '("Зустрітись з подругами", 2, 5, 2, 0, "2024-09-20 17:54:59", "2024-09-30 09:20:00", "-"),'
                  '("Обговорити серіал", 2, 6, 3, 0, "2024-09-20 15:24:17", "2024-09-30 09:20:00", "Обговорити новий '
                  'серіал"),'
                  '("Виконати Task №44", 2, 1, 1, 1, "2024-09-11 10:30:02", "2024-09-12 18:40:00", "-"),'
                  '("Виконати Task №45", 2, 1, 1, 1, "2024-09-11 10:35:10", "2024-09-12 19:00:00", "-"),'
                  '("Зайнятись рукоділлям", 2, 4, 3, 1, "2024-09-04 15:40:50", "2024-09-05 17:00:00", "-");')

    try:
        db_already_exist_cursor.execute(tasks_data)
        db_already_exist_connect.commit()
    except ProgrammingError:
        print(Fore.RED + "Inserting error!")
    else:
        print(Fore.LIGHTMAGENTA_EX + f"Tasks information successfully inserted into database!")


if __name__ == '__main__':
    database_creations()
    sleep(1)
    database_migrations()
    sleep(1)
    users_creations()
    sleep(1)
    insert_information_info_db()
