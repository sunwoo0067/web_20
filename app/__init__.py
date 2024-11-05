from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password=""  # XAMPP 기본 설정은 비밀번호 없음
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # 데이터베이스 생성 쿼리 (UTF8 설정 추가)
            cursor.execute("""
                CREATE DATABASE IF NOT EXISTS ownerclan_dashboard 
                DEFAULT CHARACTER SET utf8mb4 
                DEFAULT COLLATE utf8mb4_unicode_ci
            """)
            print("데이터베이스 생성 완료")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

app = Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 생성
create_database()

db = SQLAlchemy(app)

from app import routes, models

with app.app_context():
    db.create_all()