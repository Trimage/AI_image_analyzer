import pymysql
import convert

host_name = "ai-image-data-db.cm0jhdnc3y0u.ap-northeast-2.rds.amazonaws.com"
username = "seok_master"
password = "seok950127"
database_name = "analysis_DB"

db = pymysql.connect(
    host=host_name,  # DATABASE_HOST
    port=3306,      # DATABASE_PORT
    user=username,  # DATABASE_USERNAME
    passwd=password,  # DATABASE_PASSWORD
    db=database_name,  # DATABASE_NAME
    charset= 'utf8mb4'
)

cursor = db.cursor()


# '데이터 불러오기' 버튼 누르면 실행 ==> DB내 INFO테이블 데이터 출력
def info_load(date,id,num) :
    sql = "SELECT 위치x, 위치y, 가로width, 세로height, 가로size, 세로size, photo FROM INFO WHERE 날짜='{0}' AND ID = '{1}' AND 순번 = {2}".format(date,id,num)

    cnt = cursor.execute(sql)
    
    if cnt == 0 :
        return False

    data = cursor.fetchone()

    return data


# '데이터 불러오기' 버튼 누르면 실행 ==> DB내 PERSON테이블 데이터 출력
def person_load(date,id,num) :
    
    sql = "SELECT * FROM PERSON WHERE 날짜='{0}' AND ID = '{1}' AND 순번 = {2}".format(date,id,num)
    
    cnt = cursor.execute(sql)
    
    if cnt == 0 :
        return False
    
    return cursor.fetchone()


# '데이터 불러오기' 버튼 누르면 실행 ==> DB내 CELEB테이블 데이터 출력
def celeb_load(date,id,num) :
    sql = "SELECT * FROM CELEB WHERE 날짜='{0}' AND ID = '{1}' AND 순번 = {2}".format(date,id,num)
    
    cnt = cursor.execute(sql)
    
    if cnt == 0 :
        return False
    
    return cursor.fetchone()    



# '데이터 저장하기' 버튼 누르면 실행 ==> DB내 INFO테이블 내 데이터 저장 (순번은 최신번호를 얻어 저장)
def info_insert(date,id,image_data) :

    num = 1
    sql = "SELECT 순번 FROM INFO WHERE 날짜='{0}' AND ID='{1}' ORDER BY 순번 DESC".format(date,id)
    
    cnt = cursor.execute(sql)
    
    if cnt != 0 :
        num = cursor.fetchone()[0] + 1

    #여기까지 최신 순번을 얻어와서 num변수에 저장


    binary_data = convert.convertToBinaryData(image_data[6])

    data_tuple = (date, id, num, image_data[0], image_data[1], image_data[2], image_data[3], image_data[4], image_data[5], binary_data)
    sql = "INSERT INTO INFO(날짜, ID, 순번, 위치x, 위치y, 가로width, 세로height, 가로size, 세로size, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql,data_tuple)
    
    db.commit()

    return str(num)


# '데이터 저장하기' 버튼 누르면 실행 ==> DB내 PERSON테이블 내 데이터 저장
def person_insert(date,id,num,person_data) :

    sql = "INSERT INTO PERSON VALUES ('{0}', '{1}', {2}, '{3}', {4}, '{5}', {6}, '{7}', {8}, '{9}', {10})".format(date,id,num,person_data['sex_value'],person_data['sex_accuracy'],person_data['age_value'],person_data['age_accuracy'],person_data['emotion_value'],person_data['emotion_accuracy'],person_data['pose_value'],person_data['pose_accuracy'])
    print(sql)
    cursor.execute(sql)
    
    print("person_insert_success")

    db.commit()

    return


# '데이터 저장하기' 버튼 누르면 실행 ==> DB내 CELEB테이블 내 데이터 저장
def celeb_insert(date,id,num,celeb_data) :

    sql = "INSERT INTO CELEB(날짜,ID,순번,닮은연예인수, 닮은연예인1,닮은연예인1_정확도) VALUES ('{0}', '{1}', {2}, {3}, '{4}', {5})".format(date,id,num,celeb_data['celeb_total'],celeb_data['celeb_name1'],celeb_data['celeb_accuracy1'])
    cursor.execute(sql)

    if celeb_data['celeb_total'] == 2 :
        sql = "UPDATE CELEB SET 닮은연예인2 = '{0}', 닮은연예인2_정확도 = {1} WHERE 날짜 = '{2}' AND ID = '{3}' AND 순번={4})".format(celeb_data['celeb_name2'],celeb_data['celeb_accuracy2'],date,id,num)
        cursor.execute(sql)
    elif celeb_data['celeb_total'] == 3 :
        sql = "UPDATE CELEB SET 닮은연예인2 = '{0}', 닮은연예인2_정확도 = {1}, 닮은연예인3 = '{2}', 닮은연예인3_정확도 = {3} WHERE 날짜 = '{4}' AND ID = '{5}' AND 순번={6})".format(celeb_data['celeb_name2'],celeb_data['celeb_accuracy2'],celeb_data['celeb_name3'],celeb_data['celeb_accuracy3'],date,id,num)
        cursor.execute(sql)

    print(sql)
    
    print("celeb_insert_success")

    db.commit()

    return