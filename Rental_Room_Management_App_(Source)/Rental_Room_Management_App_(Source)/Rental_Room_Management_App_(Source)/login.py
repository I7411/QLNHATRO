import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import re
import random
import json
from UserManager import UserManager
import hashlib
#--------------------------------------login----------------------------------
class SplashScreen:
    # đổi màu cam
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ")
        self.root.configure(bg="white")

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.images = {}

        # Tạo Frame nền
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Hiển thị GIF house.gif (thay vì house.png)
        self.canvas_house = tk.Canvas(self.main_frame, width=200, height=200, bg="white", highlightthickness=0)
        self.canvas_house.pack(pady=(50, 10))

        self.house_gif_path = os.path.join(self.BASE_DIR, "assets/house.gif")
        self.load_house_gif()

        self.label = tk.Label(self.main_frame, text="ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ", font=("Arial", 30, "bold"), fg="#AA6E2D", bg="white")
        self.label.pack()

        # Hiển thị GIF shuriken di chuyển
        self.canvas_shuriken = tk.Canvas(self.main_frame, width=800, height=150, bg="white", highlightthickness=0)
        self.canvas_shuriken.pack(pady=20)

        self.shuriken_gif_path = os.path.join(self.BASE_DIR, "assets/shuriken.gif")
        self.load_shuriken_gif()

        self.x_pos = 0  # Vị trí ban đầu của GIF (bên trái màn hình)
        self.move_speed = 5  # Điều chỉnh tốc độ di chuyển

        self.animate_movement()

    def load_house_gif(self):
        if os.path.exists(self.house_gif_path):
            self.house_gif = Image.open(self.house_gif_path)

            self.house_frames = [
                ImageTk.PhotoImage(frame.copy().resize((200, 200), Image.Resampling.LANCZOS))
                for frame in ImageSequence.Iterator(self.house_gif)
            ]

            self.house_current_frame = 0
            self.update_house_gif()
        else:
            print(f"⚠ Không tìm thấy house.gif tại {self.house_gif_path}")

    def update_house_gif(self):
        if hasattr(self, "house_frames"):
            self.canvas_house.delete("all")
            self.canvas_house.create_image(100, 100, image=self.house_frames[self.house_current_frame])

            self.house_current_frame = (self.house_current_frame + 1) % len(self.house_frames)
            self.root.after(50, self.update_house_gif)

    def load_shuriken_gif(self):
        if os.path.exists(self.shuriken_gif_path):
            self.shuriken_gif = Image.open(self.shuriken_gif_path)

            self.shuriken_frames = [
                ImageTk.PhotoImage(frame.copy().resize((80, 80), Image.Resampling.LANCZOS))
                for frame in ImageSequence.Iterator(self.shuriken_gif)
            ]

            self.shuriken_current_frame = 0
        else:
            print(f"⚠ Không tìm thấy shuriken.gif tại {self.shuriken_gif_path}")

    def update_shuriken_gif(self):
        if hasattr(self, "shuriken_frames"):
            self.canvas_shuriken.delete("all")
            self.canvas_shuriken.create_image(self.x_pos, 80, image=self.shuriken_frames[self.shuriken_current_frame])

            self.shuriken_current_frame = (self.shuriken_current_frame + 1) % len(self.shuriken_frames)
            self.root.after(50, self.update_shuriken_gif)  # Cập nhật ảnh GIF nhanh hơn

    def animate_movement(self):
        if self.x_pos < 700:
            self.x_pos += self.move_speed
            self.update_shuriken_gif()
            self.root.after(40, self.animate_movement)
        else:
            self.open_main_window()

    def open_main_window(self):
        self.root.destroy()
        app = LoginApp()
        app.mainloop()

#-------------------------------log--------------------------------------
'''==================XỬ LÍ LOGIN-REG=================='''
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ")
        self.geometry("800x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.images = {}

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.warning_label = tk.Label(text="", fg="red")
        self.warning_label.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_log_ui()

    def load_image(self, filename, size=None):
        path = os.path.join(self.BASE_DIR, filename)
        try:
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy ảnh: {filename}")
            return None

    '''==================GIAO DIỆN ĐĂNG NHẬP=================='''
    #đổi màu cam
    def setup_log_ui(self):
        # Cam nhạt cho nền bên trái
        self.left_frame = ctk.CTkFrame(self.main_frame, width=300, height=500, fg_color="#FFF3E0")  # cam pastel
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.images["background"] = self.load_image("assets/house.png", (500, 500))

        if self.images["background"]:
            self.img_label = ctk.CTkLabel(self.left_frame, image=self.images["background"], text="")
            self.img_label.pack(fill="both", expand=True)

        # Cam rất nhạt hoặc trắng nhẹ cho bên phải
        self.right_frame = ctk.CTkFrame(self.main_frame, width=400, height=500, fg_color="#FFF8F0")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Tiêu đề màu cam đậm
        self.title_label = ctk.CTkLabel(self.right_frame, text="Welcome Back!", font=("Open Sans", 24, "bold"), text_color="#E65100")
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(self.right_frame, text="Đăng nhập với tài khoản của bạn", font=("Open Sans", 14), text_color="#E65100")
        self.subtitle_label.pack(pady=(0, 20))

        self.username_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent", width=300)
        self.username_frame.pack(pady=5, fill="x", padx=10)

        self.entry_username = ctk.CTkEntry(self.username_frame, placeholder_text="Tên đăng nhập")
        self.entry_username.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.password_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent", width=300)
        self.password_frame.pack(pady=5, fill="x", padx=10)

        self.entry_password = ctk.CTkEntry(self.password_frame, placeholder_text="Mật khẩu", show="*")
        self.entry_password.pack(fill="x", padx=(0, 5))

        self.toggle_frame = ctk.CTkFrame(self.password_frame, fg_color="transparent")
        self.toggle_frame.pack(pady=(5, 0), anchor="w", padx=10)

        self.show_password = False
        self.images["eye_closed"] = self.load_image("assets/hide-rmb.png", (18, 18))
        self.images["eye_open"] = self.load_image("assets/show-rmb.png", (18, 18))

        if self.images["eye_closed"] and self.images["eye_open"]:
            self.btn_toggle_password = ctk.CTkLabel(self.toggle_frame, image=self.images["eye_closed"], text="")
            self.btn_toggle_password.bind("<Button-1>", lambda e: self.toggle_password_visibility())
            self.btn_toggle_password.pack(side="left", padx=(0, 5))

        self.label_toggle_text = ctk.CTkLabel(self.toggle_frame, text="Hiện mật khẩu", font=("Open Sans", 12, "bold"), text_color="#E65100")
        self.label_toggle_text.bind("<Button-1>", lambda e: self.toggle_password_visibility())
        self.label_toggle_text.pack(side="left")

        self.username_frame.columnconfigure(0, weight=1)
        self.password_frame.columnconfigure(0, weight=1)

        # Nút đăng nhập màu cam rực
        self.btn_login = ctk.CTkButton(self.right_frame, text="Đăng nhập", fg_color="#FB8C00",
                                       hover_color="#EF6C00",
                                       command=self.validate_login, width=200, height=40, font=("Open Sans", 14, "bold"))
        self.btn_login.pack(pady=15)

        # Quên mật khẩu giữ màu xám (hoặc bạn muốn cam luôn?)
        self.forgot_password_btn = ctk.CTkLabel(self.right_frame, text="Quên mật khẩu?", font=("Open Sans", 12, "bold"),
                                                text_color="#6D4C41", cursor="hand2")  # nâu cam nhẹ
        self.forgot_password_btn.pack(pady=5)
        self.forgot_password_btn.bind("<Button-1>", lambda e: self.show_forgot_password())  

        self.register_label = ctk.CTkLabel(self.right_frame, text="Chưa có tài khoản?", font=("Open Sans", 12), text_color="gray")
        self.register_label.pack(pady=5)

        # Nút đăng ký màu cam nhạt
        self.register_btn = ctk.CTkButton(self.right_frame, text="Tạo tài khoản mới", font=("Open Sans", 14, "bold"),
                                        fg_color="#FFB74D", hover_color="#FFA726", width=170, height=40, cursor="hand2")
        self.register_btn.pack()
        self.register_btn.bind("<Button-1>", lambda e: self.show_register())

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.entry_password.configure(show="" if self.show_password else "*")
        self.btn_toggle_password.configure(image=self.images["eye_open" if self.show_password else "eye_closed"])

        self.label_toggle_text.configure(text="Ẩn mật khẩu" if self.show_password else "Hiện mật khẩu")
    
    '''==================GIAO DIỆN ĐĂNG KÝ=================='''
    #đổi màu cam
    def setup_reg_ui(self):
        # Nền cam nhạt
        self.register_frame = ctk.CTkFrame(self.main_frame, width=400, height=500, fg_color="#FFF3E0")
    
        # Tiêu đề cam đậm
        self.register_title = ctk.CTkLabel(self.register_frame, text="Tạo tài khoản mới", 
                                           font=("Open Sans", 24, "bold"), text_color="#E65100")
        self.register_title.pack(pady=(20, 5))

        self.entry_new_username = ctk.CTkEntry(self.register_frame, placeholder_text="Tên đăng nhập", width=300)
        self.entry_new_username.pack(pady=5)
        self.hint_username = ctk.CTkLabel(self.register_frame, text="Tên đăng nhập ít nhất 5 ký tự, không chứa ký tự đặc biệt",
                                      font=("Open Sans", 10), text_color="gray", fg_color="transparent")
        self.hint_username.pack()

        self.entry_new_password = ctk.CTkEntry(self.register_frame, placeholder_text="Mật khẩu", width=300, show="*")
        self.entry_new_password.pack(pady=5)
        self.hint_password = ctk.CTkLabel(self.register_frame, 
                                          text="Mật khẩu tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt",
                                      font=("Open Sans", 10), text_color="gray", fg_color="transparent", wraplength=280)
        self.hint_password.pack()

        self.entry_confirm_password = ctk.CTkEntry(self.register_frame, placeholder_text="Xác nhận mật khẩu", width=300, show="*")
        self.entry_confirm_password.pack(pady=5)
        self.hint_confirm_password = ctk.CTkLabel(self.register_frame, text="Nhập lại mật khẩu chính xác",
                                              font=("Open Sans", 10), text_color="gray", fg_color="transparent")
        self.hint_confirm_password.pack()

        self.email_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Nhập email của bạn", width=300)
        self.email_entry.pack(pady=5)
        self.hint_email = ctk.CTkLabel(self.register_frame, text="Email phải có dạng example@gmail.com",
                                   font=("Open Sans", 10), text_color="gray", fg_color="transparent")
        self.hint_email.pack()

        # Nút đăng ký màu cam rực
        self.btn_register = ctk.CTkButton(self.register_frame, text="Đăng ký", fg_color="#FB8C00", hover_color="#EF6C00",
                                          command=self.validate_reg(), width=200, height=40)
        self.btn_register.pack(pady=15)

        # Label quay lại màu cam đậm
        self.back_to_login = ctk.CTkLabel(self.register_frame, text="Quay lại đăng nhập",
                                  font=("Open Sans", 12, "bold"), text_color="#E65100", cursor="hand2")
        self.back_to_login.pack()
        self.back_to_login.bind("<Button-1>", lambda e: self.show_login())
        
    def validate_reg(self):
        username = self.entry_new_username.get().strip()
        password = self.entry_new_password.get().strip()
        confirm_password = self.entry_confirm_password.get().strip()
        email = self.email_entry.get().strip()
        if not username or not password or not confirm_password or not email:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if len(username) < 5:
            messagebox.showerror("Lỗi", "Tên đăng nhập phải có ít nhất 5 ký tự!")
            return
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            messagebox.showerror("Lỗi", "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới!")
            return
        if (len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password) 
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt!")
            return
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        if self.check_existing_user(username, email):
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc email đã tồn tại!")
            return
        self.save_user(username, password, email)
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self.show_login()

    def show_register(self):
        self.right_frame.pack_forget()
        self.setup_reg_ui()
        self.register_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    '''==================GIAO DIỆN CẤP LẠI MẬT KHẨU=============='''
    def send_otp(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập email!")
            return

        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expired = False

        if hasattr(self, 'otp_timer_id'):
            self.after_cancel(self.otp_timer_id)
        if hasattr(self, 'otp_expire_id'):
            self.after_cancel(self.otp_expire_id)

        self.otp_time_remaining = 120
        self.update_timer_label()

        self.otp_expire_id = self.after(120000, self.expire_otp)

        load_dotenv()
        sender_email = os.getenv("SYSTEM_EMAIL")
        sender_password = os.getenv("SYSTEM_PASS")
        subject = "Mã xác nhận đặt lại mật khẩu"
        body = f"Mã xác nhận của bạn là: {self.otp_code}\nVui lòng nhập mã này vào ứng dụng trong vòng 2 phút."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
            messagebox.showinfo("Thành công", "Mã OTP đã được gửi đến email của bạn!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi email thất bại: {e}")

    #đổi màu cam
    def update_timer_label(self):
        if not hasattr(self, 'otp_timer_label'):
            # Label màu cam đậm thay vì đỏ
            self.otp_timer_label = tk.Label(self, text="", font=("Arial", 12), fg="#E65100")
            self.otp_timer_label.pack(pady=5)

        if self.otp_time_remaining > 0:
            self.otp_timer_label.configure(
                text=f"⏳ Mã OTP sẽ hết hạn sau {self.otp_time_remaining} giây",
                fg="#FB8C00"  # cam tươi khi đang đếm
            )
            self.otp_time_remaining -= 1
            self.otp_timer_id = self.after(1000, self.update_timer_label)
        else:
            self.otp_expired = True
            self.otp_timer_label.configure(
                text="❌ Mã OTP đã hết hạn.",
                fg="#E65100"  # cam đậm khi hết hạn
            )
            self.send_otp_button.configure(state="normal")
            self.resend_otp_button.configure(state="disabled")

    def expire_otp(self):
        self.otp_expired = True
        if hasattr(self, 'otp_timer_label'):
            self.otp_timer_label.config(text="❌ Mã OTP đã hết hạn.")

    #đổi màu cam
    def show_forgot_password(self):
        self.right_frame.pack_forget()  
        self.forgot_frame = ctk.CTkFrame(self.main_frame, width=400, height=500, fg_color="#FFF3E0")  # nền cam nhạt
        self.forgot_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.forgot_title = ctk.CTkLabel(self.forgot_frame, text="Quên mật khẩu", font=("Open Sans", 24, "bold"),
                                         text_color="#E65100")  # cam đậm
        self.forgot_title.pack(pady=(20, 5))

        self.forgot_description = ctk.CTkLabel(self.forgot_frame, text="Nhập email để kiểm tra tài khoản của bạn.",
                                             font=("Open Sans", 12), text_color="#5D4037")  # nâu cam nhẹ, dịu mắt
        self.forgot_description.pack(pady=(0, 10))

        self.email_entry = ctk.CTkEntry(self.forgot_frame, placeholder_text="Nhập email của bạn", width=300)
        self.email_entry.pack(pady=5)

        self.hint_email = ctk.CTkLabel(self.forgot_frame, text="Email phải có dạng example@gmail.com",
                                    font=("Open Sans", 10), text_color="gray", fg_color="transparent")
        self.hint_email.pack()

        self.btn_continue = ctk.CTkButton(self.forgot_frame, text="Tiếp tục", fg_color="#FB8C00", hover_color="#EF6C00",
                                         command=self.validate_email, width=200, height=40)
        self.btn_continue.pack(pady=15)

        self.back_to_login = ctk.CTkLabel(self.forgot_frame, text="Quay lại đăng nhập",
                                         font=("Open Sans", 12, "bold"), text_color="#E65100", cursor="hand2")
        self.back_to_login.pack()
        self.back_to_login.bind("<Button-1>", lambda e: self.show_login())
    def validate_email(self):
        email = self.email_entry.get().strip().lower()

        if "@" not in email:
            email += "@gmail.com"

        GMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

        if not re.match(GMAIL_REGEX, email):
            messagebox.showerror("Lỗi định dạng", "⚠️ Email không hợp lệ hoặc không phải Gmail!")
            return

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, email)

        username = self.get_username_by_email(email)

        if username:
            self.user_email = email
            self.user_username = username
            self.show_confirm_account()
        else:
            messagebox.showwarning("Thông báo", "⚠️ Email không tồn tại trong hệ thống!")

    def get_username_by_email(self, email):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        file_path = os.path.join(JSON_DIR, "users.json")

        try:
            if not os.path.exists(file_path):
                print("⚠️ Lỗi: Không tìm thấy file users.json")
                return None

            with open(file_path, "r", encoding="utf-8-sig") as file:
                users = json.load(file)

            for user in users:
                if user.get("email", "").strip().lower() == email:
                    return user.get("username")

            print(f"⚠️ Lỗi: Email '{email}' không tồn tại trong hệ thống")
            return None  

        except json.JSONDecodeError:
            print("❌ Lỗi: File users.json không hợp lệ hoặc bị hỏng")
            return None
        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")
            return None

    # đổi màu cam
    def show_confirm_account(self):
        self.forgot_frame.pack_forget()
        self.confirm_frame = ctk.CTkFrame(self.main_frame, width=400, height=500, fg_color="#FFF3E0")  # nền cam nhạt
        self.confirm_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.confirm_title = ctk.CTkLabel(self.confirm_frame, text="Xác nhận tài khoản", 
                                         font=("Open Sans", 24, "bold"), text_color="#E65100")  # cam đậm
        self.confirm_title.pack(pady=(20, 5))

        self.confirm_label = ctk.CTkLabel(self.confirm_frame, text=f"Tài khoản tìm thấy: {self.user_username}", 
                                         font=("Open Sans", 16), text_color="#5D4037")  # nâu cam dịu mắt
        self.confirm_label.pack(pady=10)

        self.send_otp()

        self.otp_entry = ctk.CTkEntry(self.confirm_frame, placeholder_text="Nhập mã OTP", width=200)
        self.otp_entry.pack(pady=5)

        self.btn_confirm = ctk.CTkButton(self.confirm_frame, text="Xác nhận OTP", fg_color="#FB8C00", hover_color="#EF6C00", 
                                         command=self.verify_otp, width=200, height=40)
        self.btn_confirm.pack(pady=15)

        self.back_to_login = ctk.CTkLabel(self.confirm_frame, text="Quay lại", font=("Open Sans", 12, "bold"), 
                                          text_color="#E65100", cursor="hand2")
        self.back_to_login.pack()
        self.back_to_login.bind("<Button-1>", lambda e: self.show_login())
    def verify_otp(self):
        if self.otp_expired:
            messagebox.showerror("Hết hạn", "Mã OTP đã hết hạn. Vui lòng gửi lại mã mới.")
            return

        entered_otp = self.otp_entry.get()
        if entered_otp == self.otp_code:
            if hasattr(self, 'otp_timer_id'):
                self.after_cancel(self.otp_timer_id)
            if hasattr(self, 'otp_expire_id'):
                self.after_cancel(self.otp_expire_id)

            self.otp_code = None
            self.otp_expired = True

            if hasattr(self, 'otp_timer_label'):
                self.otp_timer_label.pack_forget()

            self.otp_entry.configure(state="disabled")

            messagebox.showinfo("Thành công", "Xác thực OTP thành công!")
            self.show_reset_password()
        else:
            messagebox.showerror("Thất bại", "Mã OTP không đúng!")

    #đổi màu cam
    def show_reset_password(self):
        self.confirm_frame.pack_forget()
        self.reset_frame = ctk.CTkFrame(self.main_frame, width=400, height=500, fg_color="#FFF3E0")  # nền cam nhạt
        self.reset_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.reset_title = ctk.CTkLabel(self.reset_frame, text="Đặt lại mật khẩu", 
                                       font=("Open Sans", 24, "bold"), text_color="#E65100")  # cam đậm
        self.reset_title.pack(pady=(20, 5))

        self.username_label = ctk.CTkLabel(self.reset_frame, text=f"Tài khoản: {self.user_username}", 
                                           font=("Open Sans", 16), text_color="#5D4037")  # nâu cam dịu mắt
        self.username_label.pack(pady=10)

        self.new_password_entry = ctk.CTkEntry(self.reset_frame, placeholder_text="Mật khẩu mới", width=300, show="*")
        self.new_password_entry.pack(pady=5)

        self.confirm_password_entry = ctk.CTkEntry(self.reset_frame, placeholder_text="Nhập lại mật khẩu mới", width=300, show="*")
        self.confirm_password_entry.pack(pady=5)

        self.btn_register = ctk.CTkButton(self.reset_frame, text="Xác nhận", fg_color="#FB8C00", hover_color="#EF6C00",
                                          command=self.reset_password, width=200, height=40)
        self.btn_register.pack(pady=15)

        self.back_to_login = ctk.CTkLabel(self.reset_frame, text="Quay lại đăng nhập", 
                                          font=("Open Sans", 12, "bold"), text_color="#E65100", cursor="hand2")
        self.back_to_login.pack()
        self.back_to_login.bind("<Button-1>", lambda e: self.show_login())

    def update_password(self, username, email, new_password):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        file_path = os.path.join(JSON_DIR, "users.json")

        if not os.path.exists(file_path):
            print("❌ File users.json không tồn tại!")
            return False

        try:
            if os.stat(file_path).st_size == 0:
                print("❌ File JSON trống!")
                return False

            with open(file_path, "r", encoding="utf-8-sig") as file:
                users = json.load(file)

            print(f"Dữ liệu trong file JSON: {users}")
            print(f"Username nhập vào: {username}")
            print(f"Email nhập vào: {email}")

            user_found = False

            for user in users:
                print(f"🔍 Kiểm tra: {user['username']} - {user['email']}")
                if user["username"].lower() == username.lower() or user["email"].lower() == email.lower():
                    user["password"] = new_password  # Cập nhật mật khẩu
                    print(f"✅ Cập nhật thành công cho: {user['username']}")
                    user_found = True
                    break

            if not user_found:
                print("❌ Không tìm thấy tài khoản phù hợp!")
                return False

            with open(file_path, "w", encoding="utf-8-sig") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

            return True 

        except json.JSONDecodeError:
            print("❌ Lỗi đọc file JSON! File có thể bị hỏng.")
            return False
        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")
            return False
        
    def reset_password(self):
        email = self.user_email
        username = self.get_username_by_email(email) 
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()  

        if not username:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản tương ứng với email!")
            return

        if not new_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu mới!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu mới và mật khẩu xác nhận không khớp!")
            return

        new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        if self.update_password(username, email, new_password):
            messagebox.showinfo("Thành công", "Mật khẩu đã được cập nhật!")
            self.show_login()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật mật khẩu!")

    '''==================HIỂN THỊ GIAO DIỆN ĐĂNG NHẬP=============='''
    def show_login(self):
        if hasattr(self, 'register_frame'):
            self.register_frame.pack_forget()

        if hasattr(self, 'forgot_frame'):
            self.forgot_frame.pack_forget()

        if hasattr(self, 'confirm_frame'):
            self.confirm_frame.pack_forget()

        if hasattr(self, 'reset_frame'):
            self.reset_frame.pack_forget()

        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    '''==================KIỂM TRA THÔNG TIN ĐK=================='''
    def check_existing_user(self, username, email):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        file_path = os.path.join(JSON_DIR, "users.json")
        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                users = json.load(file)
                for user in users:
                    if user is None:
                        continue 
                    if user.get("username") == username or user.get("email") == email:
                        return True
        except FileNotFoundError:
            return False
        return False

    def save_user(self, username, password, email):
        if not self.check_existing_user(username, email):
            new_user = UserManager.save_user(username, password, email, status="active")
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            JSON_DIR = os.path.join(BASE_DIR, "JSON")
            file_path = os.path.join(JSON_DIR, "users.json")

            try:
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                users = []

            users.append(new_user)

            with open(file_path, "w", encoding="utf-8-sig") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

            messagebox.showinfo("Thành công", "Đăng ký thành công!")
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc email đã tồn tại!")

    '''==================KIỂM TRA THÔNG TIN ĐN=================='''
    def validate_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        password = UserManager.hash_password(password)
        role = UserManager.check_input_login(username, password)

        if role:
            messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nVai trò: {role}")

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            JSON_DIR = os.path.join(BASE_DIR, "JSON")
            if not os.path.exists(JSON_DIR):
                os.makedirs(JSON_DIR)

            with open(os.path.join(JSON_DIR, "role.json"), "w") as role_file:
                json.dump({"role": role}, role_file)

            self.destroy() 
            self.Start_app()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    '''====VÀO TRANG CHỦ===='''
    def Start_app(self):
        from app import AppTro
        root = ctk.CTk()  
        app = AppTro(root)
        root.mainloop()
    
    '''====XỬ LÝ THOÁT ỨNG DỤNG===='''
    def on_close(self):
        if self.winfo_exists() and messagebox.askokcancel("Thoát", "Bạn muốn thoát ứng dụng?"):
            self.destroy()
        exit(0)
        

if __name__ == "__main__":
    root = tk.Tk()
    SplashScreen(root)
    root.mainloop()
