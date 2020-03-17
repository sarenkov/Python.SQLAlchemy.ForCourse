import argparse
import os
import random
from uuid import uuid4

from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker

from db_connector.db_connector import Connector
from models.authors import Author
from models.firstQuatrain import FirstQuatrain
from models.poem import Poem
from models.result import Result
from models.secondQuatrain import SecondQuatrain
from users.user_creator import *


def main():
    # Парсим агрументы командной строки, переданные при запуске скрипта из консоли
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver', default='{SQL Server}', type=str)
    parser.add_argument('--server', default='DESKTOP-7APAP23\SQLEXPRESS', type=str)
    parser.add_argument('--db', default='Poems', type=str)
    parser.add_argument('--uid', default='Tester', type=str)
    parser.add_argument('--pwd', default='Tester123', type=str)
    args = parser.parse_args()

    # Создаем объект коннектора к серверу и создаем базу, если ее еще не было
    connector = Connector(args)
    connector.create_database()

    # Создаем таблицы в бд
    Author().create(connector)
    Poem().create(connector)
    FirstQuatrain().create(connector)
    SecondQuatrain().create(connector)
    Result().create(connector)

    # Определяем путь к источнику данных (стихов)
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')
    data_list = os.listdir(data_directory)

    # Обьявляем список для хранения авторов
    authors_list = []

    # Создаем сессии для каждой таблицы
    session = sessionmaker()
    session.configure(bind=connector.get_engine())
    authors_session = session()
    poem_session = session()
    firstQuantrain_session = session()
    secondQuantrain_session = session()
    second_parts_list_object = []

    # Заполняем таблицы
    for data in data_list:
        file_path = os.path.join(data_directory, data)
        with open(file_path, encoding="utf-8") as file:
            file_data = file.readlines()
            poem_title = file_data[0].strip()
            author_fullname = file_data[1].strip().split(' ')
            author_firstname = author_fullname[0]
            auth_secondname = author_fullname[1]
            authors_list.append(auth_secondname)
            first_quatrain = ' '.join(x.strip() for x in file_data[2:6])
            second_quatrain = file_data[6:]

            author = Author(
                            first_name=author_firstname,
                            second_name=auth_secondname,
                            objectid=str(uuid4()))
            authors_session.add(author)
            authors_session.commit()

            poem = Poem(poem_title=poem_title,
                        objectid=str(uuid4()),
                        author_id=authors_session.query(Author).filter_by(
                            objectid=author.objectid).first().id)
            poem_session.add(poem)
            poem_session.commit()

            firstQuatrain = FirstQuatrain(objectid=str(uuid4()),
                                          quatrain=first_quatrain,
                                          poem_title_id=poem_session.query(Poem).filter_by(
                                              objectid=poem.objectid).first().id)
            firstQuantrain_session.add(firstQuatrain)
            firstQuantrain_session.commit()

            for part in second_quatrain:
                secondQuatrain = SecondQuatrain(objectid=str(uuid4()),
                                                parts=part.strip(),
                                                order_number=(second_quatrain.index(part) + 1),
                                                first_quatrain_id=firstQuantrain_session.query(FirstQuatrain).filter_by(
                                                    objectid=firstQuatrain.objectid).first().id)
                second_parts_list_object.append(secondQuatrain)
    random.shuffle(second_parts_list_object)
    secondQuantrain_session.add_all(second_parts_list_object)
    secondQuantrain_session.commit()

    # Создаем лишние записи в таблице авторов и названий стихов
    fake_author = Author(first_name='Ватрушкин',
                         second_name='Иосиф')
    authors_session.add(fake_author)
    authors_session.commit()

    fake_title = Poem(poem_title='Лишнее название',
                      objectid=str(uuid4()))
    poem_session.add(fake_title)
    poem_session.commit()


    # Закрываем сессии
    authors_session.close()
    poem_session.close()
    firstQuantrain_session.close()
    secondQuantrain_session.close()

    # Создаем файл для хранения списка пользователей + prettyTable
    file_users_path = os.path.join(current_directory, 'users.txt')
    file = open(file_users_path, 'w', encoding="utf-8")

    # Создаем и добавляем пользователей сервера. Записываем пользователей в файл
    for i in range(30):
        user = User()
        # engine = connector.get_engine()
        # engine.execute(get_sql_create_login(user))
        random.shuffle(authors_list)
        p_table = PrettyTable()
        p_table.field_names = ['Login', 'Password', 'Author name']
        print()
        p_table.add_row([user.username, user.password, authors_list.pop()])
        file.write(p_table.get_string())
        file.write('\n')

if __name__ == '__main__':
    main()
