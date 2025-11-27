import json
from datetime import datetime
import os
from tkinter import messagebox as mb
import hashlib 

'''==================PHƯƠNG THỨC TĨNH=================='''
class UserManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_DIR = os.path.join(BASE_DIR, "JSON")
    FILE_PATH = os.path.join(JSON_DIR, "users.json")

    @staticmethod
    def read_users():
        if not os.path.exists(UserManager.FILE_PATH):
            return []  

        try:
            with open(UserManager.FILE_PATH, "r", encoding="utf-8-sig") as file:  
                return json.load(file)  
        except (json.JSONDecodeError, FileNotFoundError):
            return [] 

    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest() 

    @staticmethod
    def save_user(username, password, email, status="active"):
        """Thêm user mới vào danh sách và lưu vào file JSON"""
        user_data = {
            "username": username,
            "password": UserManager.hash_password(password),  # ✅ Hash mật khẩu
            "email": email,
            "role": "user",
            "status": status,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        os.makedirs(UserManager.JSON_DIR, exist_ok=True)

        users = UserManager.read_users()

        users.append(user_data)

        with open(UserManager.FILE_PATH, "w", encoding="utf-8-sig") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

        return user_data

    @staticmethod
    def check_input_login(username, password):
        users = UserManager.read_users()

        for user in users:
            if user["username"] == username and user["password"] == password:  
                if user["status"] == "active":
                    return user["role"]
                else:
                    mb.showerror("Tài khoản không hoạt động", "Tài khoản của bạn không còn hoạt động!")
                    return False

        return False

