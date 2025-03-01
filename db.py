import pymysql
import pymysql.cursors

conn = pymysql.connect(host="192.168.1.12", user= "mi_usuario", password="mi_password", database="mi_base_de_datos", charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor.execute("SELECT * FROM puntajes")
response = cursor.fetchall()
print(response)

cursor.close()
conn.close()