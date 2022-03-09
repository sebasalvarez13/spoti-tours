import sqlalchemy
import pymysql

class User():
    def __init__(self):
        pass

    def user_count(self):
        '''Get number of rows in users table'''
        #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
        engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")

        #Query to add Id column 
        query = '''SELECT count(*) FROM users;'''

        #Create sql connection
        connection = engine.connect()
        #Execute query
        result = connection.execute(query)

        #Fetch count value
        user_count = result.fetchall()[0][0]

        return(user_count)

        
    def register_user(self, first_name, last_name, email, username, password):
        '''Add new user to database if user does not exist'''
        #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
        engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")

        #Create sql connection
        connection = engine.connect()
        
        #Check if this is the first user. If so, id = 1
        if self.user_count() == 0:
            id = 1
            query = '''INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);'''
            #Execute query
            connection.execute(query, [id, first_name, last_name, email, username, password])
        else:
            query = '''INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s);'''
            #Execute query
            connection.execute(query, [first_name, last_name, email, username, password])


    def login_user(self, username, password):
        #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
        engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")

        #Create sql connection
        connection = engine.connect()

        #Query to get verify username, password and count. user_exist = 0 or 1
        query = '''SELECT 
            username, 
            password, 
            count(*) as user_exists
            from users
                where username = %s and password = %s;'''
        result = connection.execute(query, [username, password])

        #Fetch count for username and pasword enterd. If count is 0, user does not exist
        user_exists = result.fetchall()[0][2]
        
        #Check if user exists and password is correct
        if user_exists == 0:
            print('Username or password incorrect')
            return False
        elif user_exists == 1:
            print('Here is your Spotify concerts data')
            return True



if __name__ == "__main__":
    user = User('Sebas', 'Alvarez', 'sebas@pena.com', 'sebas.xtreme', '1234')
    user.login_user('picoletosa', '9876')
