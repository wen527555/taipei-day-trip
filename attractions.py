
from flask import Flask
from flask import request #負責接收請求，並且將相關資訊封裝在request之中
from mysql.connector import pooling
from flask import jsonify
import math

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
app.config["JSON_AS_ASCII"] = False #把對象序列化為ASCII-encoded JSON 
app.config["TEMPLATES_AUTO_RELOAD"] = True #當模板改變時重載
app.config['JSON_SORT_KEYS'] = False

#取得景點資料
@app.route("/api/attractions",methods=["GET"]) 
def attractions():

    try:
        input_Page=request.args.get("page") 
        input_Page=int(input_Page)
        input_keyword=request.args.get("keyword")
        connection_object=connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT COUNT(`id`) FROM `attractions` ")
        total_data = mycursor.fetchone()
        total_data= total_data["COUNT(`id`)"]
        total_Page=math.floor(total_data/12)
        # print(total_Page)
        if input_keyword != None:
            mycursor.execute("SELECT * FROM attractions WHERE LOCATE( %s ,`name`)  LIMIT %s,12 ", [input_keyword,(input_Page*12)])
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
                if total_Page > input_Page:        
                    return jsonify({
                        "nextPage":input_Page+1,
                        "data": result_all
                    })
                if total_Page == input_Page:     
                    return jsonify({
                        "nextPage":"null",
                        "data": result_all
                    })
                if total_Page < input_Page:
                    return jsonify({
                        "error":True,
                        "message":"無此頁面"
                    })
        else:
            mycursor.execute("SELECT * FROM attractions ORDER BY id LIMIT %s,12 ", [(input_Page*12)])  
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
                if total_Page > input_Page:        
                    return jsonify({
                        "nextPage":input_Page+1,
                        "data": result_all
                    })
                if total_Page == input_Page:
                    return jsonify({
                        "nextPage":"null",
                        "data": result_all
                    })
                if total_Page < input_Page:
                    return jsonify({
                        "error":True,
                        "message":"無此頁面"
                    })
    except :
        return jsonify ({
                "error":True,
                "message":"伺服器內部錯誤"
            })
    finally:    
        mycursor.close()
        connection_object.close()
        print("DONE") 


app.run(port=3000,debug=True)



