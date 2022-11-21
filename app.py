from flask import Flask
from flask import request
from flask import render_template #幫助取出樣板檔案的內容，送到前端
from flask import session
from mysql.connector import pooling
from mysql.connector import Error
from flask import jsonify #使用jsonify模块来让网页直接显示json数据

connection_pool=pooling.MySQLConnectionPool(
                                            pool_name="mysqlpool",
                                            pool_size=5,
                                            pool_reset_session='True',
                                            host='localhost',
                                            database='taipei_day_trip',
                                            user='root',
                                            password='wh1999ne123')
app=Flask(__name__)
app.secret_key="any string but secret"


#Pages
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")
@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/error", methods=["GET"]) 
def error():
    massage=request.args.get("massage","")
    return render_template("error.html",massage=massage)

#根據景點編號取得景點資料
@app.route("/api/attraction/<attractionId>",methods=["GET"]) 
def getattraction(attractionId):
    try:
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT COUNT(`id`) FROM `attractions` ")
        nums = mycursor.fetchone()
        nums= nums["COUNT(`id`)"]
        if int(nums)<int(attractionId):
            return  jsonify ({
                "error":True,
                "message":"景點編號不正確"
            }) 
        if int(nums)>=int(attractionId):
            mycursor.execute("SELECT * FROM attractions WHERE  id=%s", [attractionId])
            myresult=mycursor.fetchone()
            result_all=[]
            new_images=[]
            images=myresult["images"].split(",")
            # if '' in images:
            # images.remove('')
            for n in range(len(images)):
                images_https=images[n]
                new_images.append(images_https)

            result_all=(
                {
                    "id":myresult["id"],
                    "name":myresult["name"],
                    "category":myresult["category"],
                    "description":myresult["description"],
                    "address":myresult["address"],
                    "transport":myresult["transport"],
                    "lat":myresult["lat"],
                    "lng":myresult["lng"],
                    "images":new_images
                        
                    })
            return jsonify({
                "data": result_all
            })
    except :
        return  jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:   
        mycursor.close()
        connection_object.close()
        print("DONE") 

#取得所有的景點分類名稱列表
@app.route("/api/categories",methods=["GET"]) 
def categories():

    try:
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor()
        mycursor.execute("SELECT category FROM attractions")
        categories = mycursor.fetchall()
        results=[]
        for category in categories:
            category=category[0]
            if(category in results):
                continue
            else:
                results.append(category)
                print(results)
        return jsonify({
            "data": results
            })
    except :
            return  jsonify ({
                    "error":True,
                    "message":"伺服器內部錯誤"
                })
    finally:    
        mycursor.close()
        connection_object.close()
        print("DONE")

app.run(port=3000,debug=True)