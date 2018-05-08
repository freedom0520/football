import pymysql

g_host='localhost'
g_user='root'
g_password='root'
g_port=3306
def setHostInfo(host,user, password, port):
	g_host = host
	g_user = user
	g_password = password
	g_port = port

def testConnect():
    db = pymysql.connect(host='localhost',user='root', password='root', port=3306,charset="utf8")
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    cursor.execute("CREATE DATABASE football DEFAULT CHARACTER SET utf8")
    db.close()

def connectDB(dbname):
    db = pymysql.connect(host=g_host,user = g_user, password = g_password, port = g_port, db = dbname,charset="utf8")
    cursor = db.cursor()
    return db

def closeDB(db):
	db.close()

def createTable(tname,field):
    db = connectDB("football")
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS '
    sql += tname
    sql += '( id VARCHAR(255) NOT NULL, '
    for lfield in field:
    	sql += lfield 
    	sql += ' VARCHAR(64) NOT NULL,'
    sql += 'PRIMARY KEY (id))'
    cursor.execute(sql)
    db.close()

def addField(tname,field):
    pass

def modify(sql):
    db = connectDB("football")
    cursor = db.cursor()
    try:
        if cursor.execute(sql):
            db.commit()
    except Exception as e:
        db.rollback()
    db.close()

def query(sql):
    db = connectDB("football")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        lresults = cursor.fetchall()
    except:
        print "Error: unable to fecth data"
        lresults = []
    db.close()
    return lresults

def updateTeam(list):
    if( len(list) <= 20 ):
        return
    sql = "UPDATE team SET p = %s,w = %s,d = %s,l = %s,gf = %s,ga = %s,gd = %s,rank = %s"\
    ",hw = %s,hd = %s,hl = %s,vw = %s,vd = %s,vl = %s WHERE cname = %s"
    db = connectDB("football")
    cursor = db.cursor()
    try:
        if cursor.execute(sql, (list[2], list[3], list[4], list[5], list[6], list[7], list[8],list[0], list[10], list[11], list[12], list[16], list[17], list[18], list[1])):
            print('Successful')
            db.commit()
    except:
        db.rollback()
    db.close()

def createTeam( firstid, teamlist):
    sql = "INSERT INTO team(id, name, cname) values(%s, %s, %s)"
    if( len(teamlist) < 1 ):
        return
    db = connectDB("football")
    cursor = db.cursor()
    try:
        if cursor.execute(sql,(firstid,firstid,teamlist[0])):
            db.commit()
        else:
            return
    except Exception as e:
        db.rollback()
        raise e
    for x in range(1,len(teamlist)):
        firstid+=1
        try:
            if cursor.execute(sql,(firstid,firstid,teamlist[x])):
                db.commit()
            else:
                return
        except Exception as e:
            db.rollback()
            raise e
    db.close()