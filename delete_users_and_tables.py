import argparse

from db_connector.db_connector import Connector

parser = argparse.ArgumentParser()
parser.add_argument('--driver', default='{SQL Server}', type=str)
parser.add_argument('--server', default='DESKTOP-7APAP23\SQLEXPRESS', type=str)
parser.add_argument('--db', default='Poems', type=str)
parser.add_argument('--uid', default='Tester', type=str)
parser.add_argument('--pwd', default='Tester123', type=str)
args = parser.parse_args()

def delete_users():

    connector = Connector(args)
    engine = connector.get_engine()

    list_logins = engine.execute("""select name from sys.sql_logins where name not in (
                                            'Tester', '##MS_PolicyEventProcessingLogin##'
                                            , '##MS_PolicyTsqlExecutionLogin##'
                                            , 'sa')""")

    list_users = engine.execute("""select name from sys.database_principals where name not in (
                                            'guest'
                                            , 'INFORMATION_SCHEMA'
                                            , 'sys'
                                            , 'public'
                                            , 'dbo'
                                            , 'db_owner'
                                            , 'db_accessadmin'
                                            , 'db_securityadmin'
                                            , 'db_ddladmin'
                                            , 'db_backupoperator'
                                            , 'db_datareader'
                                            , 'db_datawriter'
                                            , 'db_denydatareader'
                                            , 'db_denydatawriter')
                                    """)
    for login in list_logins.fetchall():
        engine.execute(f'drop login {login[0]}')

    for user in list_users.fetchall():
        engine.execute(f"drop user {user[0]}")

    engine.execute(""" 
                        DROP TABLE [dbo].[SecondQuatrains]
                        DROP TABLE [dbo].[FirstQuatrains]
                        DROP TABLE [dbo].[PoemsTitles]
                        DROP TABLE [dbo].[Authors]  
                        DROP TABLE [dbo].[Answers]
                        """)

if __name__=='__main__':
    delete_users()
