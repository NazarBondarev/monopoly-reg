import sqlite3



class Database:
    def __init__(self, conn=None, cursor=None):
                
                self.conn = sqlite3.connect("./venv/data/dump.db", check_same_thread=False)
                self.cursor = self.conn.cursor()
    
    def get_tables(self):
        request = "select * from sqlite_master where type = 'table'"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if result:
            dates = [x[1] for x in result]
            temp = []
            for item in dates:
                if item in ("history"):
                    continue
                request = f"select * from `{item}`"
                self.cursor.execute(request)
                result = self.cursor.fetchall()            
                temp.append(f"{item} [{len(result)}]")
            return temp
        else:
            return False


    def get_only_tables(self):
        request = "select * from sqlite_master where type = 'table'"
        self.cursor.execute(request)
        result = self.cursor.fetchall()


    def get_users(self, userid, gamedate):
        request = f"select `userid` from `{gamedate}`"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        
        result = [x[0] for x in result]
        if userid in result:
            return False
        else:
            return True
    
    def get_users_id(self, gamedate):
        request = f"select `userid` from `{gamedate}`"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        
        result = [x[0] for x in result]
        return result

    def add_new_user(self, userid, name, date, gamedate):
        request = f"INSERT INTO `{gamedate}`(name, userid, date) VALUES('{name}',{userid},'{date}')"
        self.cursor.execute(request)
        self.conn.commit()
    
    def add_to_history(self, userid, name, date, gamedate):
        request = f"INSERT INTO `history`(name, userid, date, gamedate) VALUES('{name}',{userid},'{date}', '{gamedate}')"
        self.cursor.execute(request)
        self.conn.commit()

    def get_user_history(self, userid):
        request = f"select gamedate from `history` where userid={userid}"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if result:
            return [x[0] for x in result]
        else:
            return False

    def get_usernames(self, gamedate):
        request = f"select name from `{gamedate}`"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if result:
            return [x[0] for x in result]
        else:
            return False

    def delete_reserve(self, gamedate, userid):
        request = f"delete from `{gamedate}` where userid={userid}"
        request2 = f"delete from `history` where userid={userid} and gamedate='{gamedate}'"
        self.cursor.execute(request)
        self.cursor.execute(request2)
        self.conn.commit()
