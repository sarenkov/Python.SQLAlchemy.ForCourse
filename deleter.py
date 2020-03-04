import argparse
import os

from db_connector.db_connector import Connector

parser = argparse.ArgumentParser()
parser.add_argument('--driver', default='{SQL Server}', type=str)
parser.add_argument('--server', default='localhost\SQLEXPRESS', type=str)
parser.add_argument('--db', default='Poems', type=str)
parser.add_argument('--uid', default='Tester', type=str)
parser.add_argument('--pwd', default='123456', type=str)
args = parser.parse_args()

def delete_users_from_file():
    current_directory = os.getcwd()
    file_users_path = os.path.join(current_directory, 'users.csv')
    users_list = []
    with open(file_users_path) as file:
        users_list = file.readlines()[1:]

    connector = Connector(args)
    engine = connector.get_engine()

    for item in users_list:
        login = item.split(';;')[0]
        try:
            engine.execute(f'drop login {login}')
            engine.execute(f'drop user {login}')
        except:
            continue


    engine.execute(""" USE [Poems]
                        DROP TABLE SecondQuatrains
                        DROP TABLE FirstQuatrains
                        DROP TABLE PoemsTitles
                        DROP TABLE Authors
                        DROP TABLE Answers""")


if __name__=='__main__':
    delete_users_from_file()
