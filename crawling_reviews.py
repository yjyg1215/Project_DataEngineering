from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# cur.execute("DROP TABLE IF EXISTS reviews;")

# cur.execute("""CREATE TABLE reviews (
#     user_id INT NOT NULL,
#     movie_id INT NOT NULL,
#     user_rating FLOAT,

#     PRIMARY KEY (user_id,movie_id),
#     FOREIGN KEY (movie_id) REFERENCES movies(id)
# );""")

###동적 크롤링 및 데이터 적재###
user_id_list=[i for i in range(1000,3000)]

options=webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')

driver=webdriver.Chrome(options=options)

for user_id in user_id_list:
    driver.get("https://m.kinolights.com/user/"+str(user_id)+"/review")
    
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"h1"))
    ) #창이 뜰 때까지 대기
    finally:
        pass

    print(user_id)

    try:
        error=driver.find_element(By.CSS_SELECTOR,"div.title").text #유저가 없을 때
    except:
        error=0

    if error=='요청하신 페이지를 찾지 못했습니다.':
        continue
    
    n_review=driver.find_element(By.CSS_SELECTOR,"span.movie-filter-wrap-title").text.split('개')[0] #리뷰가 없을 때

    if n_review=='0':
        continue
    
    reviews=driver.find_elements(By.XPATH,'//*[@id="contents"]/section/div[2]/ul/span/li')
    for review in reviews:
        movie=review.find_element(By.CSS_SELECTOR,"div.movie-info-wrap")
        movie_id=movie.find_element(By.CSS_SELECTOR,"a").get_attribute('href').split('/')[-1]
        user_rating=review.find_element(By.CSS_SELECTOR,"span.user-star-score").text

        cur.execute("INSERT IGNORE INTO reviews VALUES (%s,%s,%s);",(user_id,movie_id,user_rating))
        conn.commit()

conn.close()