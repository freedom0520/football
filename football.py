from urllib.request import urlopen
from bs4 import BeautifulSoup
import dbi
from datetime import datetime

def getdatasrc( url ):
    htmlfile = open(url, 'rb')  #以只读的方式打开本地html文件
    htmlpage = htmlfile.read()
    bsObj = BeautifulSoup(htmlpage, "html.parser")
    listsrc = bsObj.findAll("script")
    return listsrc[5]["src"]

def parsetcjs(file):
    fr = open(file,'r', encoding='utf-8')
    for line in fr.readlines():
        if "teamCount" in line:
            return line
    fr.close()

def getOne(allmatch):
    if len(allmatch) <= 0:
        return ""
    firstMatch = allmatch.pop()
    firstIndex = firstMatch.find('[',0,-1)
    lastIndex = firstMatch.find(']',0,-1)
    if firstIndex == -1 or lastIndex == -1 or firstIndex >= lastIndex:
        return ""
    loneMatch = firstMatch[firstIndex+1:lastIndex]
    firstMatch = firstMatch[lastIndex+1:-1]
    if len(firstMatch) > 0 :
        allmatch.append(firstMatch)
    return loneMatch

def groupSql(onematch):
    onematch = onematch.replace("'","")
    target_list = []
    target_list = onematch.split(",")
    for x in range(0,len(target_list)):
        lIndex = target_list[x].find("^")
        if lIndex != -1 :
            target_list[x] = target_list[x][0:lIndex]
    sql = "INSERT INTO `match`(belong,time,hnamech,vnamech,hscore,vscore,foul,yellow,red,bp,"\
    "shoot,ontarget,corner,offside,defense) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    sql = sql.format(target_list[7],target_list[3],target_list[7],target_list[8],target_list[9],target_list[10],
        target_list[11],target_list[12],target_list[13],target_list[14],target_list[15],target_list[16],target_list[21],
        target_list[22],target_list[26])
    print( sql )
    return sql

'''2018-05-02 19:00'''
def matchaftertime(imatch,itime):
    dt = datetime.strptime(itime, "%Y-%m-%d %H:%M")
    lmatch = imatch.replace("'","")
    lpara_list = []
    lpara_list = lmatch.split(",")
    dtmatch = datetime.strptime(lpara_list[3], "%Y-%m-%d %H:%M")
    print( dtmatch )
    return dtmatch > dt

def insertMatch(file):
    tcjs = getdatasrc(file)
    teamCount = parsetcjs(tcjs)
    firstindex = teamCount.find('[',1,-1)
    teamCount = teamCount[firstindex+1:-3]
    list = []
    list.append(teamCount)
    for x in range(1,17):
        oneMatch = getOne( list)
        if len(oneMatch) and matchaftertime(oneMatch,"2018-05-02 18:00"):
            dbi.modify( groupSql( oneMatch ) )



if __name__ == '__main__':
    file = r'E:/workspace/pysrc/football/198.html'
    insertMatch(file)