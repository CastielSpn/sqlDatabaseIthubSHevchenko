from flask import Flask, request, jsonify
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bd_host = config['MYSQL']['host']
bd_user = config['MYSQL']['user']
bd_password = config['MYSQL']['password']
bd_database = config['MYSQL']['database']

mydb = mysql.connector.connect(
    host=bd_host,
    user=bd_user,
    password=bd_password,
    database=bd_database)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM mytable")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

app = Flask(__name__)


def get_bd():
    return mysql.connector.connect(host=bd_host, port=3306,
                              user=bd_user, password=bd_password,
                              database=bd_database)

@app.route('/logs', methods=['GET'])
def get_logs():
    ip_address = request.args.get('ip_address')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = '''SELECT ip_address, COUNT(id) AS request_count, DATE_FORMAT(request_time, '%%Y-%%m-%%d') AS date 
               FROM apache_access_logs 
               WHERE (%s IS NULL OR ip_address = %s)
                 AND (%s IS NULL OR request_time >= %s)
                 AND (%s IS NULL OR request_time <= %s)
               GROUP BY DATE_FORMAT(request_time, '%%Y-%%m-%%d'), ip_address'''
    bd = get_bd()
    cursor = bd.cursor(dictionary=True)
    cursor.execute(query, (ip_address, ip_address, start_date, start_date, end_date, end_date))
    logs = cursor.fetchall()
    cursor.close()
    bd.close()
    return jsonify(logs)

@app.route('/api/logs', methods=['GET'])
def get_logs_api():
    ip_address = request.args.get('ip_address')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = '''SELECT ip_address, COUNT(id) AS request_count, DATE_FORMAT(request_time, '%%Y-%%m-%%d') AS date 
               FROM apache_access_logs 
               WHERE (%s IS NULL OR ip_address = %s)
                 AND (%s IS NULL OR request_time >= %s)
                 AND (%s IS NULL OR request_time <= %s)
               GROUP BY DATE_FORMAT(request_time, '%%Y-%%m-%%d'), ip_address'''
    bd = get_bd()
    cursor = bd.cursor(dictionary=True)
    cursor.execute(query, (ip_address, ip_address, start_date, start_date, end_date, end_date))
    logs = cursor.fetchall()
    cursor.close()
    bd.close()
    return jsonify(logs)

if __name__ == '__main__':
    app.run()