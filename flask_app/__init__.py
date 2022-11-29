from flask import Flask,render_template,request
import pickle
import pandas as pd
import pymysql

conn=pymysql.connect(
    user="yeji",
    passwd='1234',
    host='localhost',
    db='section3'
)

cur=conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'),200

@app.route('/report',methods=['POST'])
def report():

    where="WHERE"
    and_flag=0

    user_id=int(request.form.get('id'))
    if request.form.get('time_unit')=='any':
        time_unit='상관 없음'
    else:
        time_unit=request.form.get('time_unit')
        where=where+" time_unit="+time_unit
        and_flag+=1
    if request.form.get('country')=='any':
        country='상관 없음'
    else:
        country=request.form.get('country')
        if and_flag!=0:
            where=where+" and"
        else:
            and_flag+=1
        where=where+" country='"+country+"'"
    if request.form.get('age_limit')=='any':
        age_limit='상관 없음'
    else:
        age_limit=request.form.get('age_limit')
        if and_flag!=0:
            where=where+" and"
        else:
            and_flag+=1
        where=where+" age_limit='"+age_limit+"'"
    if request.form.get('genre')=='any':
        genre='상관 없음'
    else:
        genre=request.form.get('genre')
        if and_flag!=0:
            where=where+" and"
        else:
            and_flag+=1
        where=where+" genre='"+genre+"'"

    cur.execute("SELECT * FROM available "+where+";")

    movie_list=cur.fetchall()

    movie_df=pd.DataFrame(movie_list,columns=['movie_id','year','rating','running_time','country','age_limit','genre','director','netflix','wavve','tving','disney','watcha','coupang','naver','name','time_unit'])

    X=pd.DataFrame()
    X['user_id']=[user_id]*len(movie_df)
    X['rating']=movie_df['rating']
    X['time_unit']=movie_df['time_unit']
    X['country']=movie_df['country']
    X['age_limit']=movie_df['age_limit']
    X['genre']=movie_df['genre']
    X['director']=movie_df['director']

    with open('model.pkl','rb') as pickle_file:
        model=pickle.load(pickle_file)
        pred=model.predict(X)
    
    movie_df['pred']=pred
    report=movie_df[movie_df['pred']==1]

    ott=[sum(report['netflix']),sum(report['wavve']),sum(report['tving']),sum(report['disney']),sum(report['watcha']),sum(report['coupang']),sum(report['naver'])]
    ott_name={0:'netflix',1:'wavve',2:'tving',3:'disney',4:'watcha',5:'coupang',6:'naver'}
    max=0
    idx=0
    for i in range(7):
        if max<ott[i]:
            max=ott[i]
            idx=i
    ott=ott_name[idx]

    return render_template("report.html",ott=ott,options={'user_id':user_id,'time_unit':time_unit,'country':country,'age_limit':age_limit,'genre':genre},reports=report), 200

    if __name__=='__main__':
        app.run()
