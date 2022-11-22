from flask import Flask
from flask import request
from flask import render_template #幫助取出樣板檔案的內容，送到前端
from flask import session
from mysql.connector import pooling
from flask import jsonify 
import math
from mysql.connector import Error

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

#取得景點資料
@app.route("/api/attractions",methods=["GET"]) 
def attractions():

    try:
        input_Page=request.args.get("page")
        input_Page=int(input_Page)
        count=int(input_Page)*12
        input_keyword=request.args.get("keyword")
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT COUNT(`id`) FROM `attractions` ")
        total_data = mycursor.fetchone()
        total_data= total_data["COUNT(`id`)"]
        total_Page=math.floor(total_data/12)
        # print(total_Page)
        print(input_keyword)   
        if input_keyword != None:

            sql="SELECT * FROM attractions WHERE category=%s OR LOCATE( %s ,`name`) LIMIT %s,12"
            val=(input_keyword,"%"+input_keyword+"%",count)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            # print(myresult)
            result_all=[]
            for result in myresult:
                new_images=[]
                images=result["images"].split(",")
                for n in range(len(images)):
                    images_https=images[n]
                    new_images.append(images_https)
                result_all.append(
                    {
                        "id":result["id"],
                        "name":result["name"],
                        "category":result["category"],
                        "description":result["description"],
                        "address":result["address"],
                        "transport":result["transport"],
                        "lat":result["lat"],
                        "lng":result["lng"],
                        "images":new_images           
                    })
                if int(total_Page) > input_Page:        
                    return jsonify({
                        "nextPage":input_Page+1,
                        "data": result_all
                    })
                elif int(total_Page) == input_Page:     
                    return jsonify({
                        "nextPage":"null",
                        "data": result_all
                    })
                else:
                    return jsonify({
                        "error":True,
                        "message":"無此頁面"
                    })


        else:
            mycursor.execute("SELECT * FROM attractions ORDER BY id LIMIT %s,12 ", [count])  
            myresult = mycursor.fetchall()
            result_all=[]
            for result in myresult:
                new_images=[]
                images=result["images"].split(",")
                for n in range(len(images)):
                    images_https=images[n]
                    new_images.append(images_https)
                result_all.append(
                    {
                        "id":result["id"],
                        "name":result["name"],
                        "category":result["category"],
                        "description":result["description"],
                        "address":result["address"],
                        "transport":result["transport"],
                        "lat":result["lat"],
                        "lng":result["lng"],
                        "images":new_images           
                    })
                if int(total_Page) > input_Page:        
                    return jsonify({
                        "nextPage":input_Page+1,
                        "data": result_all
                    })
                elif int(total_Page) == input_Page:
                    return jsonify({
                        "nextPage":"null",
                        "data": result_all
                    })
                else:
                    return jsonify({
                        "error":True,
                        "message":"無此頁面"
                    })
    except:
        return jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:    
        mycursor.close()
        connection_object.close()
        print("DONE") 




app.run(host='0.0.0.0',port=3000,debug=True)