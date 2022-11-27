from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pymysql

###MySQL 연동###
conn=pymysql.connect(
    user="yeji",
    passwd='1234',
    host='localhost',
    db='section3'
)

###데이터베이스 테이블 생성###
cur=conn.cursor()

# cur.execute("DROP TABLE IF EXISTS details;")

# cur.execute("""CREATE TABLE details (
#     movie_id INT NOT NULL,
#     year VARCHAR(10),
#     rating FLOAT,
#     running_time VARCHAR(10),
#     country VARCHAR(20),
#     age_limit VARCHAR(20),
#     genre VARCHAR(20),
#     director VARCHAR(20),

#     netflix INT,
#     wavve INT,
#     tving INT,
#     disney INT,
#     watcha INT,
#     coupang INT,
#     naver INT,

#     PRIMARY KEY (movie_id),
#     FOREIGN KEY (movie_id) REFERENCES movies(id)
# );""")

###동적 크롤링 및 데이터 적재###
cur.execute("SELECT id FROM movies;")
id_list=cur.fetchall()

options=webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36') #403 오류(ip 접근 제한) 해결을 위한 코드

driver=webdriver.Chrome(options=options)

for id in id_list:
    print(id)
    driver.get("https://m.kinolights.com/title/"+str(id[0]))

    year=driver.find_elements(By.CSS_SELECTOR,"span.metadata-item")[1].text
    rating=driver.find_element(By.CSS_SELECTOR,"div.movie-light-percent").text
    
    metadata=driver.find_elements(By.CSS_SELECTOR,"li.metadata")

    try:
        running_time=metadata[0].text
    except:
        running_time='없음'
    try:
        country=metadata[1].text
    except:
        country='없음'
    try:
        age_limit=metadata[2].text
    except:
        age_limit='없음'
    try:
        genre=metadata[3].text
    except:
        genre='없음'
    
    try:
        director=driver.find_elements(By.CSS_SELECTOR,"div.name")[0].text
    except:
        director='없음'

    netflix=0
    wavve=0
    tving=0
    disney=0
    watcha=0
    coupang=0
    naver=0
    otts=driver.find_elements(By.CSS_SELECTOR,'span.cell.provider-name')
    for ott in otts:
        if '넷플릭스'==ott.text:
            netflix=1
        elif '웨이브'==ott.text:
            wavve=1
        elif '티빙'==ott.text:
            tving=1
        elif '디즈니+'==ott.text:
            disney=1
        elif '왓챠'==ott.text:
            watcha=1
        elif '쿠팡플레이'==ott.text:
            coupang=1
        elif '네이버 시리즈온'==ott.text:
            naver=1
    
    cur.execute("INSERT IGNORE INTO details VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    ,(id,year,rating,running_time,country,age_limit,genre,director,netflix,wavve,tving,disney,watcha,coupang,naver))   
    conn.commit()

conn.close()