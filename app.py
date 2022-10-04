from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import time,os,codecs,requests
from glob import glob
from bs4 import BeautifulSoup as bs
app = Flask(__name__)

def shop_point_search(shopname):
    url='https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+shopname
    res=requests.get(url)
    html_text=res.text

    soup=bs(html_text,'lxml') # more past

    try:
        ff=soup.find('div',{'class':'dAsGb'})
        ff2=ff.find('span',{'class':'PXMot LXIwF'})
        ff2=ff2.find('em')
    except Exception as ex:
        tmp=soup.find_all('div',{'class':'Dr_06'})
        if len(tmp)!=0:
            return '여러 가게가 검색됩니다.'
        else:
            try:
                tmp=soup.find('div',{'id':'place-app-root'})
                tmp2=tmp.find('div',{'class':'api_subject_bx'})
                tmp3=tmp2.find_all('li')
            except Exception as ex:
                return 'error, 가게가 존재하지 않습니다.'
            else:
                return '가게의 별점이 존재하지 않습니다.'
    else:
        return ff2.text

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET' or request.form['keyword']=="":
        return render_template('home.html')
    else:
        print('post')
        keyword=request.form['keyword']
        print(keyword)
        ans=shop_point_search(keyword)
        print(ans)
        return render_template('home.html',ans=ans)
if __name__ == '__main__':
    port=int(os.environ.get("PORT",5000))
    app.run('0.0.0.0',port=port)