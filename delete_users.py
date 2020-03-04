import argparse

from db_connector.db_connector import Connector

parser = argparse.ArgumentParser()
parser.add_argument('--driver', default='{SQL Server}', type=str)
parser.add_argument('--server', default='VM-EDUDB', type=str)
parser.add_argument('--db', default='Poems', type=str)
parser.add_argument('--uid', default='Tester', type=str)
parser.add_argument('--pwd', default='-1987Sarenkov', type=str)
args = parser.parse_args()

def delete_users():   

    connector = Connector(args)
    engine = connector.get_engine()

    list = engine.execute("select name from sys.sql_logins where name not in ('Tester', '##MS_PolicyEventProcessingLogin##', '##MS_PolicyTsqlExecutionLogin##', 'sa')")
    for login in list.fetchall():
        engine.execute(f'drop user {login[0]}')
        engine.execute(f'drop login {login[0]}')

if __name__=='__main__':
    delete_users()
