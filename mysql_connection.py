import pymysql
from datetime import datetime

host_name = "ai-image-data-db.cm0jhdnc3y0u.ap-northeast-2.rds.amazonaws.com"
username = "seok_master"
password = "seok950127"
database_name = "analysis_DB"

db = pymysql.connect(
    host=host_name,  # DATABASE_HOST
    port=3306,
    user=username,  # DATABASE_USERNAME
    passwd=password,  # DATABASE_PASSWORD
    db=database_name,  # DATABASE_NAME
    charset='utf8'
)

cursor = db.cursor()

# '데이터 저장하기' 버튼에 맞게 수행하는 SQL
def insert(id) :
    
    date = datetime.today().strftime("%Y-%m-%d")
    num = 1;
    sql = "SELECT 순번 FROM INFO WHERE 날짜='" + date + "' AND ID='" + id + "' ORDER BY 순번 DESC"
    
    cnt = cursor.execute(sql)
    
    if cnt != 0 :
        num = cursor.fetchone()[0]

    sql = "INSERT INTO INFO(날짜, ID, 순번) VALUES ('" + date + "', '" + id + "', " + str(num) + ")"
    cnt = cursor.execute(sql)
    
    print("success")