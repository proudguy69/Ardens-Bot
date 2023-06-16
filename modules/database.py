import sqlite3

class LevelsDatabase():
    def createTable():
        db = sqlite3.connect('database.sqlite3')
        db.execute("""
                   CREATE TABLE IF NOT EXISTS levels (
                       userid INTEGER NOT NULL,
                       level INTEGER NOT NULL,
                       xp INTEGER NOT NULL,
                       date INTEGER NOT NULL
                   )
                   """)
        db.commit()
        db.close()
    
    def DeleteTable():
        db = sqlite3.connect('database.sqlite3')
        db.execute('DROP TABLE levels')
        db.commit()
        db.close()
        
    def getRecord(data, userid):
        db = sqlite3.connect('database.sqlite3')
        cursor = db.execute(f'SELECT {data} FROM levels WHERE userid = ?', [userid,])
        returndata = cursor.fetchone()
        db.close()
        return returndata
    
    def CreateRecord(userid, level, xp, date):
        db = sqlite3.connect('database.sqlite3')
        #check if there is data
        cursor = db.execute(f'SELECT * FROM levels WHERE userid = ?', [userid,])
        data = cursor.fetchone()
        if data: db.execute("DELETE FROM levels WHERE userid = ?", [userid,]) #remove data
        db.commit()
        db.execute("""
                   INSERT OR REPLACE INTO levels (userid, level, xp, date)
                   VALUES (?,?,?,?)
                   """, [userid, level, xp, date])
        db.commit()
        db.close()
        
class ModerationDatabase():
    def createModerationTables():
        db = sqlite3.connect('database.sqlite3')
        db.execute("CREATE TABLE IF NOT EXISTS infractions (id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER)")
        db.execute("CREATE TABLE IF NOT EXISTS warns (infractionid INTEGER, userid INTEGER, date INTEGER, reason TEXT, moderator INTEGER, FOREIGN KEY (infractionid) REFERENCES infractions (id))")
        db.commit(); db.close()
    
    def DeleteModerationTables():
        db = sqlite3.connect('database.sqlite3')
        db.execute('DROP TABLE IF EXISTS infractions')
        db.execute('DROP TABLE IF EXISTS warns')
        db.commit(); db.close()

    def GetWarnRecords(data, userid):
        db = sqlite3.connect('database.sqlite3')
        cursor = db.execute(f'SELECT {data} FROM warns WHERE userid = ? ORDER BY date DESC', [userid,])
        data = cursor.fetchall()
        db.commit(); db.close()
        return data
        
        
    def CreateWarnRecord(userid, date, reason, moderator):
        db = sqlite3.connect('database.sqlite3')
        db.execute('INSERT INTO infractions (userid) VALUES (?)', [userid,])
        cursor = db.execute('SELECT * FROM infractions WHERE userid = ?', [userid,])
        data = cursor.fetchall()[len(cursor.fetchall())-1]
        #set the warns record
        db.execute('INSERT INTO warns (infractionid, userid, date, reason, moderator) VALUES (?,?,?,?,?)',[data[0], userid, date, reason, moderator])
        db.commit(); db.close()
    

    
    
