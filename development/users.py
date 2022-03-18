from database import connection

class User():
    def __init__(self):
        self.connection = connection

    def user_count(self):
        '''Get number of rows in users table'''
        #Query to add Id column 
        query = '''SELECT count(*) FROM users;'''

        #Execute query
        result = self.connection.execute(query)

        #Fetch count value
        user_count = result.fetchall()[0][0]

        return(user_count)

        
    def register_user(self, first_name, last_name, email, username, password):
        '''Add new user to database if user does not exist'''      
        #Check if this is the first user. If so, id = 1
        if self.user_count() == 0:
            id = 1
            query = '''INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);'''
            #Execute query
            self.connection.execute(query, [id, first_name, last_name, email, username, password])
        else:
            query = '''INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s);'''
            #Execute query
            self.connection.execute(query, [first_name, last_name, email, username, password])


    def user_exists(self, username, password):
        '''Verifies if username and password match values from database. Returns True or False'''
        #Query to get verify username, password and count. user_exist = 0 or 1
        query = '''SELECT 
            username, 
            password, 
            count(*) as user_exists
            from users
                where username = %s and password = %s;'''
        result = self.connection.execute(query, [username, password])

        #Fetch count for username and pasword entered. If count is 0, user does not exist
        user_exists = result.fetchall()[0][2]

        if user_exists == 0:
            return False
        elif user_exists == 1:
            return True


