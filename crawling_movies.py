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

# cur.execute("""CREATE TABLE movies (
#     id INT NOT NULL,
#     name VARCHAR(100) NOT NULL,

#     PRIMARY KEY (id)
# );""")

###동적 크롤링 및 데이터 적재###
driver=webdriver.Chrome()
driver.implicitly_wait(5)

driver.get("https://m.kinolights.com/discover/explore")
time.sleep(20)

type_btn=driver.find_element(By.XPATH,'//*[@id="contents"]/section/div[3]/div/div/div[2]/button')
driver.execute_script("arguments[0].click();",type_btn)
time.sleep(1)

driver.find_element(By.XPATH,'//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]').send_keys(Keys.ENTER)
time.sleep(20)

driver.find_element(By.XPATH,'//*[@id="contents"]/section/div[4]/div[2]/div[2]/button[2]').send_keys(Keys.ENTER)
time.sleep(1)

before_h=driver.execute_script("return window.scrollY")
while True:
    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.END)
    time.sleep(1)

    after_h=driver.execute_script("return window.scrollY")

    if after_h==before_h:
        break
    before_h=after_h

movies=driver.find_elements(By.CSS_SELECTOR,'div.MovieItem.grid')
for movie in movies:
    id=int(movie.get_attribute('data-key'))
    name=movie.find_element(By.CSS_SELECTOR,'div.title').text
    
    cur.execute("INSERT IGNORE INTO movies VALUES (%s,%s);",(id,name))

conn.commit()

conn.close()