import pymysql

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
    charset= 'utf8mb4'
)

cursor = db.cursor()



# '데이터 불러오기' 버튼에 맞게 수행하는 SQL
def person_load(date,id,num) :
    sql = "SELECT * FROM PERSON WHERE 날짜='" + date + "' AND ID = '" + id + "' AND 순번 = " + num
    
    cnt = cursor.execute(sql)
    
    if cnt == 0 :
        return False
    
    return cursor.fetchone()

def celeb_load(date,id,num) :
    sql = "SELECT * FROM CELEB WHERE 날짜='" + date + "' AND ID = '" + id + "' AND 순번 = " + num
    
    cnt = cursor.execute(sql)
    
    if cnt == 0 :
        return False
    
    return cursor.fetchone()    


# '데이터 저장하기' 버튼에 맞게 수행하는 SQL
def info_insert(date,id) :

    num = 1
    sql = "SELECT 순번 FROM INFO WHERE 날짜='" + date + "' AND ID='" + id + "' ORDER BY 순번 DESC"
    
    cnt = cursor.execute(sql)
    
    if cnt != 0 :
        num = cursor.fetchone()[0] + 1

    sql = "INSERT INTO INFO(날짜, ID, 순번) VALUES ('" + date + "', '" + id + "', " + str(num) + ")"
    cursor.execute(sql)
    
    db.commit()

    print(sql)
    print("info_insert_success")

    
    return str(num)


def person_insert(date,id,num,person_data) :

    sql = "INSERT INTO PERSON VALUES ('" + date + "', '" + id + "', " + str(num) + ", '" + person_data['sex_value'] + "', " + person_data['sex_accuracy'] + ", '" + person_data['age_value'] + "', " + person_data['age_accuracy'] + ", '" + person_data['emotion_value'] + "', " + person_data['emotion_accuracy'] + ", '" + person_data['pose_value'] + "', " + person_data['pose_accuracy'] + ")"
    print(sql)
    cursor.execute(sql)
    
    print("person_insert_success")

    db.commit()

    return


def celeb_insert(date,id,num,celeb_data) :

    sql = "INSERT INTO CELEB(날짜,ID,순번,닮은연예인수, 닮은연예인1,닮은연예인1_정확도) VALUES ('" + date + "', '" + id + "', " + str(num) + ", " + celeb_data['celeb_total'] + ", '" + celeb_data['celeb_name1'] + "', " + celeb_data['celeb_accuracy1'] + ")"
    
    cursor.execute(sql)

    if celeb_data['celeb_total'] == 2 :
        sql = "UPDATE CELEB SET 닮은연예인2 = '" + celeb_data['celeb_name2'] + "', 닮은연예인2_정확도 = " + celeb_data['celeb_accuracy2'] + " WHERE 날짜 = '" + date + "' AND ID = '" + id + "' AND 순번=" + num + ")"
        cursor.execute(sql)
    elif celeb_data['celeb_total'] == 3 :
        sql = "UPDATE CELEB SET 닮은연예인2 = '" + celeb_data['celeb_name2'] + "', 닮은연예인2_정확도 = " + celeb_data['celeb_accuracy2'] + ", 닮은연예인3 = '" + celeb_data['celeb_name3'] + "', 닮은연예인3_정확도 = " + celeb_data['celeb_accuracy3'] + " WHERE 날짜 = '" + date + "' AND ID = '" + id + "' AND 순번=" + num + ")"
        cursor.execute(sql)

    print(sql)
    
    print("celeb_insert_success")

    db.commit()

    return