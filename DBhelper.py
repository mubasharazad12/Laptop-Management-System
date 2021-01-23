from mysql.connector import MySQLConnection
from configparser import ConfigParser
from flask_bcrypt import Bcrypt

def read_from_file(filename = "config.ini" , section="mysql"):
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception("{0} not found in the {1} file".format(section , filename))
    return db_config


def connect_to_database():
    db_config = read_from_file()
    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            return conn
        else:
            print("connection failed")
    except Exception as error :
        print(error)



def Insert_into_database(username , password):
    bcrypt = Bcrypt()
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "INSERT INTO users(username , password) VALUES(%s , %s)"
    hash_password = bcrypt.generate_password_hash(password=password)
    vals = (username , hash_password)
    cursor.execute(sql , vals)
    cursor.close()
    conn.commit()
    conn.close()

def search_from_database(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username = %s" , (username , ))
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return rows

def get_password_From_database(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users where username = %s" , (username , ))
    result = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None        

def delete_record_from_database(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s" , (username , ))
    cursor.close()
    conn.commit()
    conn.close()

def update_user_to_database(old_username , old_password , new_username , new_password):
    bcypt = Bcrypt()
    password = get_password_From_database(old_username)
    if varify_password(password , old_password):
        new_password = bcypt.generate_password_hash(new_password)
        conn = connect_to_database()
        curosr = conn.cursor()
        curosr.execute("UPDATE users set password = %s , username = %s WHERE username= %s" ,( new_password , new_username , old_username))
        curosr.close()
        conn.commit()
        conn.close()

def varify_password(hashed_password, password):
    bcypt = Bcrypt()
    check = bcypt.check_password_hash(hashed_password.encode() , password)
    if check:
        return True
    return False


