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
            print(dates)
            temp = []
            for item in dates:
                print(item)
                request = f"select * from `{item}`"
                self.cursor.execute(request)
                result = self.cursor.fetchall()            
                temp.append(f"{item} [{len(result)}]")
            return temp
        else:
            return False


print(Database().get_tables())

