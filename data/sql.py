import json
from mysql.connector import pooling
from mysql.connector import Error
import json,re

connection_pool=pooling.MySQLConnectionPool(
                                            pool_name="mysqlpool",
                                            pool_size=5,#a pool size is a number of the connection objects that the pool can support.
                                            pool_reset_session='True',#Reset session variables when the connection is returned to the pool.
                                            host='localhost',
                                            database='taipei_day_trip',
                                            user='root',
                                            password='wh1999ne123')

with open("data/taipei-attractions.json",mode="r",encoding="utf-8") as file:
    data=json.load(file)

lis=data["result"]["results"]
nums=(len(lis))
array=[]
for i in range(0,nums):
    att=lis[i]
    id=att["_id"]
    # print(f'{id}')
    name=att["name"]
    # print(f'{name}')
    category=att["CAT"]
    # print(f'{category}')
    description=att["description"]
    # print(f'{description}')
    address=att["address"]
    # print(f'{address}')
    transport=att["direction"]
    # print(f'{transport}')
    mrt=att["MRT"]
    # print(f'{mrt}')
    lat=att["latitude"]
    # print(f'{lat}')
    lng=att["longitude"]
    # print(f'{lng}')
    image1=att["file"].split("https")
    # print(f'{image1}')
    image2 = ["https"+x for x in image1 if re.search("JPG", x)]
    image3 = ["https"+x for x in image1 if re.search("jpg", x)]
    images=",".join(image2+image3)
    # print(f'{images}')


    # 景點資料上傳資料庫
    sql = "INSERT INTO attractions ( name, category, description, address, transport, mrt, lat, lng,images) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s)"
    val = ( name, category, description, address, transport, mrt, lat, lng,images)

    try:
        connection_object=connection_pool.get_connection() 
        cursor=connection_object.cursor() 
        cursor.execute(sql,val)
        connection_object.commit()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
    # closing database connection.    
        cursor.close()
        connection_object.close()
    print("DONE")  
 