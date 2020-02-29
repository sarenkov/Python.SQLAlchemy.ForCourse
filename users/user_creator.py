from faker import Faker


class User:
    # faker.random.seed(1234)
    def __init__(self):
        self.faker = Faker()
        self.username = self.faker.user_name()
        self.password = self.faker.password(10, special_chars=False, upper_case=True, lower_case=True)


def get_sql_create_login(user: User, dbname: str = 'Poems') -> str:
    return f""" CREATE LOGIN {user.username}  
                WITH PASSWORD = '{user.password}',
                DEFAULT_DATABASE = {dbname};
                ALTER LOGIN {user.username} ENABLE
                USE [{dbname}]
                CREATE USER {user.username} for login {user.username}
                WITH DEFAULT_SCHEMA = [DBO];
                USE [{dbname}]
                GRANT SELECT ON Authors TO {user.username};
                GRANT SELECT ON FirstQuatrains TO {user.username};
				GRANT SELECT ON PoemsTitles TO {user.username};
				GRANT SELECT ON SecondQuatrains TO {user.username};
                GRANT SELECT ON Answers TO {user.username};
				GRANT INSERT ON Answers TO {user.username};"""