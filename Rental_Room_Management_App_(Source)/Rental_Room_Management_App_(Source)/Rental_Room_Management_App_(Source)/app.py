import json
import tkinter as tk
from tkinter import ttk, messagebox as mb
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import os
import customtkinter
import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
import re
from collections import defaultdict

class AppTro:
    # đổi màu cam trên
    def __init__(self, root):
        self.app = root
        self.is_detail_view_requested = False

        self.role = None
        self.exam_names = []
        self.test_names = []
        self.current_list = ''
        self.logo_img = {}
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.current_detail_window = None
        self.details_text = None

        self.app.geometry("856x645")
        self.app.title("AppTro")
        #self.app.resizable(0, 0)
        self.app.resizable(True, True)
        self.app.tk_setPalette(
        background='#FF7F50',       # nền cam nhạt, sáng
        foreground='#000000',       # chữ màu đen rõ nét
        activeBackground='#FF7F50', # nền cam rực khi active
        activeForeground='#FFFFFF'  # chữ trắng khi active
    )



        self.setup_gui()

        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
    
        self.listbox.bind("<<ListboxSelect>>", self.on_room_select)
    def setup_gui(self):
        self.create_sidebar()
        self.create_listbox()
        self.create_menubar()
        self.create_buttons()
        self.login()
        
        self.load_room_data() 
        self.show_home_page()
        self.update_hoadon_file()
        self.load_invoice_data()

        self.listbox.bind("<<ListboxSelect>>", self.display_room_details)

    def on_room_select(self, event):
        self.is_detail_view_requested = True
        class DummyEvent:
            pass

        self.show_room_action_buttons()

    # đổi màu cam trái
    def create_sidebar(self):
        self.sidebar = tk.Frame(master=self.app, bg="#FF7F50", width=200, height=650)  # cam 
        self.sidebar.pack_propagate(0)
        self.sidebar.pack(fill="y", anchor="w", side="left")

        self.logo_img["logo"] = self.load_image("assets/logo.png", (130, 130))
        if self.logo_img["logo"]:
            self.logo_label = tk.Label(master=self.sidebar, image=self.logo_img["logo"], bg="#FF7F50", bd=0)  # đồng bộ bg
            self.logo_label.pack(pady=(38, 0), anchor="center")
            
    # đổi màu cam sửa phòng       
    def create_listbox(self):
        self.text_frame = tk.Frame(self.app, bg="#FFF3E0", width=680, height=645)  # nền cam nhạt hơn
        self.text_frame.pack_propagate(0)
        self.text_frame.pack(side="right", fill="both", expand=True)

        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)

        self.text_area_frame_home = tk.Frame(self.text_frame, bg="#FFF3E0", borderwidth=0, highlightthickness=0)
        self.text_area_frame_home.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.text_area_home = tk.Text(
            self.text_area_frame_home,
            width=40,
            height=20,
            font=("Arial", 12),
            fg="#5D2A00",  # nâu cam đậm, nổi bật trên nền sáng
            bg="#FFF3E0",  # nền cam nhạt
            borderwidth=0,
            highlightthickness=0,
            wrap=tk.WORD,
        )
        self.text_area_home.pack(side="left", fill="both", expand=True)

        self.text_area_frame_guide = tk.Frame(self.text_frame, bg="#FFE0B2", borderwidth=0, highlightthickness=0)  # cam sáng hơn
        self.text_area_frame_guide.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.text_area_guide = tk.Text(
            self.text_area_frame_guide,
            width=40,
            height=20,
            font=("Arial", 12),
            fg="#5D2A00",
            bg="#FFE0B2",
            borderwidth=0,
            highlightthickness=0,
            wrap=tk.WORD,
        )
        self.text_area_guide.pack(side="left", fill="both", expand=True)
        self.text_area_frame_guide.grid_remove()

        self.listbox_frame = tk.Frame(self.text_frame, bg="#FFE0B2", borderwidth=0, highlightthickness=0)
        self.listbox_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.listbox = tk.Listbox(
            self.listbox_frame,
            width=40, height=20,
            font=("Arial", 12), fg="#5D2A00",
            bg="#FFE0B2",
            borderwidth=0, highlightthickness=0
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox_frame.grid_remove()

        self.details_frame = tk.Frame(self.text_frame, bg="#FFE0B2")
        self.details_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.details_text = tk.Text(self.details_frame, height=25, width=50,
                                   bg="#FFE0B2", fg="#5D2A00")
        self.details_text.pack(side="left", fill="both", expand=True)
        self.details_scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_text.yview)
        self.details_scrollbar.pack(side="right", fill="y")
        self.details_text.config(yscrollcommand=self.details_scrollbar.set)
        self.details_frame.grid_remove()

    def hide_all_text_frames(self):
        self.text_area_frame_home.grid_remove()
        self.text_area_frame_guide.grid_remove()
        self.listbox_frame.grid_remove()
        self.details_frame.grid_remove()
        
        if hasattr(self, "add_room_button"):
            self.add_room_button.pack_forget()
        if hasattr(self, "find_room_button"):
            self.find_room_button.pack_forget()
        if hasattr(self, "filter_room_button"):
            self.filter_room_button.pack_forget()
        if hasattr(self, "receive_payment_button"):
            self.receive_payment_button.pack_forget()

        self.reset_filter()

    def reset_filter(self):
        if getattr(self, 'is_filtered', False):
            self.is_filtered = False
            self.filtered_rooms = None
            self.View_Room(self.rooms_data)

    #đổi màu cam thu tiền phòng
    def create_menubar(self):
        self.menubar = tk.Menu(self.app, tearoff=0, font=("Arial", 12))
        self.menubar.configure(background='#FFB74D', foreground='white')  # cam sáng nền, chữ trắng

        file_menu = tk.Menu(self.menubar, tearoff=0, font=("Arial", 12))
        file_menu.configure(background='#F57C00', foreground='white', activebackground='#FF9800', activeforeground='white')  # cam đậm menu con
        self.menubar.add_cascade(label="Craw Data", font="montserrat 12", menu=file_menu)
        file_menu.add_command(
            label="From Website", 
            command=self.Crawl_Display,
            compound='left'
        )

        notify_menu = tk.Menu(self.menubar, tearoff=0, font=("Arial", 12))
        notify_menu.configure(background='#F57C00', foreground='white', activebackground='#FF9800', activeforeground='white')  # cam đậm menu con
        notify_menu.add_command(
            label="Kiểm tra thông báo thu tiền", 
            command=self.check_payment_notification,
            compound='left'
        )
        self.menubar.add_cascade(label="Thông báo", menu=notify_menu)

        self.app.config(menu=self.menubar)

    def create_buttons(self):
        button_configs = [
            (self.load_image("assets/notehome.png", (30, 30)), "Trang chủ", self.show_home_page),
            (self.load_image("assets/bedroom.png", (30, 30)), "Phòng", self.View_Room),
            (self.load_image("assets/faq.png", (30, 30)), "Hướng dẫn", self.User_Manual),
            (self.load_image("assets/logout.png", (30, 30)), "Đăng xuất", self.logout),
            (self.load_image("assets/out_image.png", (30, 30)), "Thoát", self.exit)
        ]

        for img, text, command in button_configs:
            button = self.create_button(self.sidebar, img, text, command)
            button.pack(fill='x', padx=10, pady=5)

        separator = tk.Frame(self.sidebar, height=2, bg="yellow")
        separator.pack(fill='x', padx=10, pady=10)

    # đổi màu cam nút menu bo tròn
    def create_button(self, master, img, text, command=None):
        default_bg = "#E65100"    # cam đậm (orange)
        hover_bg = "#FFB74D"      # cam nhạt hơn khi hover
        default_fg = "#FFFFFF"    # chữ trắng bình thường
        hover_fg = "#FFFFFF"      # chữ trắng khi hover (giữ nguyên)
        button = ctk.CTkButton(
            master=self.sidebar,
            text=f"  {text}",
            image=img,
            fg_color="#E65100",    # nền cam đậm
            hover_color="#FFB74D", # nền cam nhạt khi hover
            text_color="#FFFFFF",  # chữ trắng
            font=("Arial Bold", 10),
            corner_radius=20,
            command=command
        )
        button.pack(fill='x', padx=10, pady=20)
        button.image = img
        return button

    # đổi màu cam chữ trang chủ
    def show_home_page(self):
        self.hide_all_text_frames()

        self.text_area_frame_home.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.text_area_home.config(state="normal")
        self.text_area_home.delete(1.0, tk.END)

        content = [
            "Chào mừng đến với 'AppTro'",
            "Ứng dụng quản lí phòng trọ",
            "Đồ án số 04",
            "",
            "Hứa Vĩnh Khang",
            "Huỳnh Thanh Minh Tâm",
            "",
            "Loại phòng:",
            "1. Phòng A (Phòng khép kín): 2,500,000 VND / tháng",
            "  - Có nhà vệ sinh riêng",
            "  - Máy quạt treo tường",
            "  - Có chỗ nấu ăn",
            "  - Wifi miễn phí",
            "  - Chỗ để xe miễn phí",
            "  - Diện tích ~18m²",
            "  - Tiền cọc: 2,500,000 VND (1 tháng)",
            "",
            "2. Phòng B (Phòng thường): 1,800,000 VND / tháng",
            "  - Dùng nhà vệ sinh chung",
            "  - Quạt treo tường",
            "  - Wifi miễn phí",
            "  - Chỗ để xe miễn phí",
            "  - Diện tích ~12m²",
            "  - Tiền cọc: 1,800,000 VND (1 tháng)",
            ""
        ]

        for line in content:
            self.text_area_home.insert(tk.END, line + "\n")

        # Đổi màu nền khung và màu chữ
        self.text_area_home.config(
            bg='#FFF3E0',                    # nền cam nhạt
            fg='#E65100',                   # chữ cam đậm
            font=('Segoe UI', 14, 'bold'),  # font đậm, rõ
            state="disabled"
        )

    def load_image(self, filename, size=None):
        path = os.path.join(self.BASE_DIR, filename)
        print(f"Đang load ảnh từ: {path}")
        try:
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            mb.showerror("Lỗi", f"Không thể tải ảnh: {path}\nLỗi: {e}")
            return None

    def read_role(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        if not os.path.exists(JSON_DIR):
                os.makedirs(JSON_DIR)

        try:
            with open(os.path.join(JSON_DIR, "role.json"), "r") as file:
                data = json.load(file)
                self.role = data.get('role', None)
                if self.role == 'user' or self.role == 'admin':
                    return self.role
                else:
                    return None
        except FileNotFoundError:
            print("File role.json not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON in role.json.")
            return None
        
    '''=====THÔNG BÁO VAI TRÒ====='''
    def login(self):
        role_ouput = self.read_role()
        if role_ouput:
            mb.showinfo("Thông báo", f"Bạn đã đăng nhập với vai trò {role_ouput}.")
        else:
            mb.showerror("Lỗi", "Không thể xác định vai trò.")
    
    '''=====ĐỌC DANH SÁCH PHÒNG======'''
    def load_room_data(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")

        if not os.path.exists(JSON_DIR):
            os.makedirs(JSON_DIR)

        file_path = os.path.join(JSON_DIR, "rooms.json")

        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                data = json.load(file)

            self.rooms_data = data.get("rooms", [])
            self.rooms_data.sort(key=lambda room: room.get("id", "").lower())
        except FileNotFoundError:
            mb.showerror("Lỗi", "Không tìm thấy file rooms.json.")
            self.rooms_data = []
        except json.JSONDecodeError:
            mb.showerror("Lỗi", "rooms.json không hợp lệ.")
            self.rooms_data = []

    '''=====ĐỌC DANH SÁCH HÓA ĐƠN======'''
    def load_invoice_data(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")

        if not os.path.exists(JSON_DIR):
            os.makedirs(JSON_DIR)

        file_path = os.path.join(JSON_DIR, "invoices.json")
        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                data = json.load(file)

            if isinstance(data, list):
                self.invoices_data = data
            elif isinstance(data, dict):
                self.invoices_data = data.get("invoices", [])
            else:
                self.invoices_data = []

            self.invoices_data.sort(key=lambda room: room.get("id", "").lower())
        except FileNotFoundError:
            mb.showerror("Error", "File invoices.json not found.")
            self.invoices_data = []
        except json.JSONDecodeError:
            mb.showerror("Error", "invoices.json is not valid.")
            self.invoices_data = []

    '''=====HIỂN THỊ DANH SÁCH PHÒNG======'''
    # đổi màu cam chữ phòng
    def View_Room(self, rooms=None):
        self.hide_all_text_frames()

        if rooms is None:
            rooms = self.rooms_data

        self.displayed_rooms = rooms

        self.listbox.delete(0, tk.END)

        for room in rooms:
            name = room.get("name", "").ljust(15)
            status = room.get("status", "").ljust(10)
            display_text = f"{name} | {status}"
            self.listbox.insert(tk.END, display_text)

        self.listbox.config(
            font=('Segoe UI', 14, 'bold'),
            selectforeground='#FFFFFF',    # chữ trắng khi chọn
            selectbackground='#FB8C00',    # cam đậm khi chọn
            bg='#FFF3E0',                  # nền cam nhạt
            fg='#E65100'                   # chữ cam đậm
        )

        if not hasattr(self, "add_room_button"):
            self.show_add_room_button()

        self.listbox_frame.grid()

    '''=====HIỂN THỊ THÔNG TIN CHI TIẾT CỦA PHÒNG======'''
    # đổi màu cam chi tiết phòng
    def show_room_info_details(self, room):
        if self.current_detail_window is not None and self.current_detail_window.winfo_exists():
            self.current_detail_window.destroy()

        self.current_detail_window = tk.Toplevel(self.app)
        self.current_detail_window.title(f"Chi tiết phòng - {room.get('name', '')}")
        self.current_detail_window.geometry("800x700")
        self.current_detail_window.configure(bg="#FFF3E0")  # cam nhạt

        def on_detail_close():
            self.current_detail_window.destroy()
            self.current_detail_window = None

        self.current_detail_window.protocol("WM_DELETE_WINDOW", on_detail_close)

        canvas = tk.Canvas(self.current_detail_window, bg="#FFF3E0")
        scrollbar = tk.Scrollbar(self.current_detail_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFF3E0")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def create_label_entry(parent, label_text, default_value="", row=0):
            label = tk.Label(parent, text=label_text, anchor="w", bg="#FFF3E0", fg="#E65100", font=("Arial", 12))
            label.grid(row=row, column=0, sticky="w", pady=5)

            width = max(len(str(default_value)) + 2, 20)
            entry = tk.Entry(parent, font=("Arial", 13, "italic"), bg="#FFE0B2", fg="#BF360C", relief="flat", bd=2, width=width, state="readonly")
            entry.grid(row=row, column=1, sticky="w", pady=5, padx=(10, 0))
            entry.config(state="normal")
            entry.insert(0, default_value)
            entry.config(state="readonly")

            return entry

        start_row = 0
        label_phong = tk.Label(scrollable_frame, text="🏠 Thông tin phòng", bg="#FFF3E0", fg="#BF360C", font=("Arial", 20, "bold"))
        label_phong.grid(row=start_row, column=0, sticky="w", pady=(15, 5))

        start_row += 1
        create_label_entry(scrollable_frame, "Mã phòng:", room.get('id', ''), row=start_row)
        create_label_entry(scrollable_frame, "Tên phòng:", room.get('name', ''), row=start_row + 1)
        create_label_entry(scrollable_frame, "Trạng thái:", room.get('status', ''), row=start_row + 2)
        create_label_entry(scrollable_frame, "Giá phòng:", room.get('price', ''), row=start_row + 3)

        start_row = 5
        khach_list = room.get("Khach", [])
        if khach_list:
            for i, khach in enumerate(khach_list, start=1):
                label_khach = tk.Label(scrollable_frame, text=f"👤 Khách {i}", bg="#FFF3E0", fg="#BF360C", font=("Arial", 20, "bold"))
                label_khach.grid(row=start_row, column=0, sticky="w", pady=(15, 5))
                start_row += 1

                for key in ["HoTen", "NgaySinh", "SoDienThoai", "QueQuan", "CCCD", "TienCoc", "NgayThue","GhiChu"]:
                    create_label_entry(scrollable_frame, key.replace("HoTen", "Họ tên").replace("SoDienThoai", "SĐT").replace("QueQuan", "Quê quán").replace("CCCD", "CCCD").replace("TienCoc", "Tiền cọc").replace("NgayThue", "Ngày thuê").replace("NgaySinh", "Ngày sinh").replace("GhiChu", "Ghi chú"), khach.get(key, '' if key != "GhiChu" else "Không có"), row=start_row)
                    start_row += 1
        else:
            no_khach_lbl = tk.Label(scrollable_frame, text="Chưa có khách thuê phòng này.", bg="#FFF3E0", fg="#E65100", font=("Arial", 12, "italic"))
            no_khach_lbl.grid(row=start_row, column=0, columnspan=2, pady=10)
            start_row += 1

        lich_su = room.get("LichSu", [])
        label_ls_title = tk.Label(scrollable_frame, text="📅 Lịch sử thuê ", bg="#FFF3E0", fg="#BF360C", font=("Arial", 20, "bold"))
        label_ls_title.grid(row=start_row, column=0, sticky="w", pady=(20, 10))
        start_row += 1

        if lich_su:
            for i, ls in enumerate(lich_su, start=1):
                label_ls = tk.Label(scrollable_frame, text=f"Lần {i}:", bg="#FFF3E0", fg="#E65100", font=("Arial", 13, "bold"))
                label_ls.grid(row=start_row, column=0, sticky="w", pady=(10, 5))
                start_row += 1

                create_label_entry(scrollable_frame, "Họ tên:", ls.get('HoTen', 'Không rõ'), row=start_row)
                start_row += 1
                create_label_entry(scrollable_frame, "Ngày trả:", ls.get('NgayTra', 'Không rõ'), row=start_row)
                start_row += 1
        else:
            no_ls_lbl = tk.Label(scrollable_frame, text="Không có lịch sử thuê.", bg="#FFF3E0", fg="#E65100", font=("Arial", 12, "italic"))
            no_ls_lbl.grid(row=start_row, column=0, columnspan=2, pady=10)
            start_row += 1

        scrollable_frame.columnconfigure(1, weight=1)

    def show_room_action_buttons(self):
        self.reset_filter()
        if not hasattr(self, "details_frame"):
            self.details_frame = tk.Frame(self.text_frame, bg="#FFF3E0")

        if not self.details_frame.winfo_ismapped():
            self.details_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if hasattr(self, "displayed_rooms") and self.displayed_rooms:
            current_rooms = self.displayed_rooms
        else:
            current_rooms = self.rooms_data

        if index >= len(current_rooms):
            return

        room = current_rooms[index]

        role = self.read_role()

        if role == "admin":
            edit_button = tk.Button(self.details_frame, text="✏️ Sửa", bg="#FFB74D",
                                    font=("Arial", 12), command=self.handle_edit_room)
            edit_button.pack(pady=5, anchor="center")

            delete_button = tk.Button(self.details_frame, text="🗑️ Xóa", bg="#FF7043",
                                      font=("Arial", 12), command=self.handle_delete_room)
            delete_button.pack(pady=5, anchor="center")

        detail_button = tk.Button(self.details_frame, text="📋 Xem chi tiết", bg="#FFE0B2",
                                  font=("Arial", 12), command=self.handle_view_details)
        detail_button.pack(pady=5, anchor="center")

        if room.get("status", "").lower() == "trống" and role == "admin":
            add_guest_button = tk.Button(self.details_frame, text="👤 Thêm khách", bg="#FFCC80",
                                         font=("Arial", 12), command=self.handle_add_guest)
            add_guest_button.pack(pady=5, anchor="center")

        if room.get("status", "").lower() == "đang thuê" and role == "admin":
            delete_guest_button = tk.Button(self.details_frame, text="👤 Xoá khách", bg="#FFAB91",
                                            font=("Arial", 12), command=self.handle_remove_guest)
            delete_guest_button.pack(pady=5, anchor="center")
    
        self.show_add_room_button()
        self.show_find_room_button()
        self.show_apply_filters_room_button()
        self.show_receive_payment_button()
    
    def display_room_details(self, event):
        if not self.is_detail_view_requested:
            return
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]

        if not hasattr(self, "displayed_rooms") or index >= len(self.displayed_rooms):
            return

        room = self.displayed_rooms[index]

        self.show_add_room_button()
        self.show_room_info_details(room)
        self.show_room_action_buttons()

    def hide_detail_buttons(self):
        if hasattr(self,"add_room_button"):
            self.add_room_button.pack_forget()
        if hasattr(self, "edit_button"):
            self.edit_button.pack_forget()
        if hasattr(self, "delete_button"):
            self.delete_button.pack_forget()
        if hasattr(self, "detail_button"):
            self.detail_button.pack_forget()
        if hasattr(self, "add_guest_button"):
            self.add_guest_button.pack_forget()
        if hasattr(self, "delete_guest_button"):
            self.delete_guest_button.pack_forget()
         
    def hide_room_list(self):
        if hasattr(self, "details_frame") and self.details_frame.winfo_ismapped():
            self.details_frame.grid_forget()
        
        self.listbox.delete(0, tk.END)

    def hide_home_page(self):
        if hasattr(self, "text_area_frame") and self.text_area_frame.winfo_ismapped():
            self.text_area_frame.grid_forget()

    '''=====THÊM PHÒNG MỚI======'''    
    def handle_add_room(self):
        def save_new_room():
            room_id = entry_id.get().strip()
            room_name = "Phòng " + room_id
            if not room_id or not room_name:
                tk.messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ mã phòng và tên phòng.")
                return
            for room in self.rooms_data:
                if room["id"] == room_id:
                    tk.messagebox.showerror("Trùng ID", f"Phòng với mã '{room_id}' đã tồn tại.")
                    return
            if not re.match(r"^[AB]\d+$", room_id):
                tk.messagebox.showerror("Sai định dạng", "Mã phòng phải bắt đầu bằng A hoặc B và theo sau là các chữ số.")
                return
            new_room = {
                "id": room_id,"name": room_name,"status": "Trống",
                "price": 2500000 if room_id[0] == 'A' else 1800000,
                "Khach": [],
                "LichSu": []
            }
            self.rooms_data.append(new_room)
            self.rooms_data.sort(key=lambda room: room.get("id", ""))
            try:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                JSON_DIR = os.path.join(BASE_DIR, "JSON")
                file_path = os.path.join(JSON_DIR, "rooms.json")

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump({"rooms": self.rooms_data}, file, indent=4, ensure_ascii=False)
                tk.messagebox.showinfo("Thành công", f"Đã thêm phòng '{room_name}' thành công.")
                self.View_Room()
                add_window.destroy()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", f"Không thể lưu phòng mới: {e}")
        
        add_window = tk.Toplevel(self.app)
        add_window.title("Thêm phòng mới")
        add_window.geometry("400x200")
        add_window.configure(bg="#FFF3E0")  # cam nhạt
        tk.Label(add_window, text="Mã phòng:", bg="#FFF3E0", font=("Arial", 12)).pack(pady=(20, 5))
        entry_id = tk.Entry(add_window, font=("Arial", 12), width=30)
        entry_id.pack()
        tk.Button(add_window, text="Lưu", font=("Arial", 12), bg="#FFB74D", command=save_new_room).pack(pady=20)

    # đổi màu xanh lá nút thêm phòng
    def show_add_room_button(self):
        role = self.read_role()
        self.add_room_button = tk.Button(self.details_frame, text="➕ Thêm phòng", bg="#90ee90", font=("Arial", 14), command=self.handle_add_room)
        
        if role == "admin":
            self.add_room_button.pack(side="bottom", pady=10)
        else:
            self.add_room_button.pack_forget()

    '''=====TÌM PHÒNG======'''   
    #đổi mài cam tìm phòng
    def handle_find_room(self):
        def find_room():
            room_id = entry_id.get().strip()
            found = None

            for room in self.rooms_data:
                if room.get("id") == room_id:
                    found = room
                    break

            if found:
                self.show_room_info_details(found)
            else:
                tk.messagebox.showerror("Không tìm thấy", f"Phòng với mã '{room_id}' không tồn tại.")

        find_window = tk.Toplevel(self.app)
        find_window.title("Tìm phòng")
        find_window.geometry("400x200")
        find_window.configure(bg="#fef9f4")

        tk.Label(find_window, text="Mã phòng:", bg="#fef9f4", font=("Arial", 12)).pack(pady=(20, 5))
        entry_id = tk.Entry(find_window, font=("Arial", 12), width=30)
        entry_id.pack()

        tk.Button(find_window, text="🔍 Tìm phòng", font=("Arial", 12), bg="#90ee90", command=find_room).pack(pady=20)
    #đổi màu tím nút tìm phòng
    def show_find_room_button(self):
        self.find_room_button = tk.Button(self.details_frame, text="🔍 Tìm phòng", bg="#7F55B1", font=("Arial", 14), fg="white",command=self.handle_find_room)
        self.find_room_button.pack(side="bottom", pady=10)

    '''=====LỌC PHÒNG======'''  
    def handle_apply_filters_room(self):
        def apply_filters():
            type_filter = combo_type.get().strip().upper()
            status_filter = combo_status.get().strip()

            filtered_rooms = []

            for room in self.rooms_data:
                room_id = room.get("id", "").upper()
                room_status = room.get("status", "").lower()

                type_filter_value = type_filter.strip().upper()
                status_filter_value = status_filter.strip().lower()

                if type_filter_value != "TẤT CẢ" and not room_id.startswith(type_filter_value):
                    continue

                if status_filter_value != "tất cả" and room_status != status_filter_value:
                    continue

                filtered_rooms.append(room)

            if filtered_rooms:
                self.filtered_rooms = filtered_rooms  
                self.View_Room(self.filtered_rooms)
            else:
                mb.showinfo("Kết quả lọc", "Không có phòng phù hợp với tiêu chí lọc.")
                self.View_Room(self.rooms_data)

            filter_window.destroy()

        def on_filter_window_close():
            self.View_Room(self.rooms_data)
            filter_window.destroy()

        filter_window = tk.Toplevel(self.app)
        filter_window.title("Lọc phòng")
        filter_window.geometry("400x250")
        filter_window.resizable(0,0)
        filter_window.configure(bg="#fef9f4")

        filter_window.protocol("WM_DELETE_WINDOW", on_filter_window_close)

        tk.Label(filter_window, text="Loại phòng:", bg="#fef9f4", font=("Arial", 12)).pack(pady=(20, 5))

        types = sorted(set(room.get("id", "")[0].upper() for room in self.rooms_data if room.get("id")))
        types.insert(0, "Tất cả")  

        combo_type = ttk.Combobox(filter_window, values=types, font=("Arial", 12), state="readonly", width=28)
        combo_type.current(0) 
        combo_type.pack()

        tk.Label(filter_window, text="Trạng thái phòng:", bg="#fef9f4", font=("Arial", 12)).pack(pady=(20, 5))

        statuses = sorted(set(room.get("status", "") for room in self.rooms_data if room.get("status")))
        statuses.insert(0, "Tất cả")

        combo_status = ttk.Combobox(filter_window, values=statuses, font=("Arial", 12), state="readonly", width=28)
        combo_status.current(0)
        combo_status.pack()

        tk.Button(filter_window, text="🔍 Lọc phòng", font=("Arial", 12), bg="#90ee90", command=apply_filters).pack(pady=20)

    # đổi màu nút xanh lá đậm
    def show_apply_filters_room_button(self):
        self.filter_room_button = tk.Button(
            self.details_frame,
            text="🔧 Lọc phòng",
            bg="#008080",
            font=("Arial", 14),
            fg="white",
            command=self.handle_apply_filters_room
        )
        self.filter_room_button.pack(side="bottom", pady=10)

    '''=====CHỈNH SỬA THÔNG TIN PHÒNG======''' 
    def handle_edit_room(self):
        selection = self.listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Chưa chọn phòng", "Vui lòng chọn phòng để sửa.")
            return

        index = selection[0]

        if not hasattr(self, "displayed_rooms") or index >= len(self.displayed_rooms):
            return

        room = self.displayed_rooms[index]

        edit_window = tk.Toplevel(self.app)
        edit_window.title(f"Sửa phòng {room['id']}")
        edit_window.geometry("800x700")
        edit_window.configure(bg="#fef9f4")

        # Frame cho thông tin phòng
        frame_room = tk.Frame(edit_window, bg="#fef9f4")
        frame_room.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        tk.Label(frame_room, text="Thông tin phòng", font=("Arial", 14, "bold"), bg="#fef9f4").grid(row=0, column=0, columnspan=2, pady=10)

        labels_room = ["Mã phòng:", "Tên phòng:", "Trạng thái:", "Giá phòng:"]
        keys_room = ["id", "name", "status", "price"]
        entries_room = {}

        for i, (label, key) in enumerate(zip(labels_room, keys_room), start=1):
            tk.Label(frame_room, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(frame_room)
            entry.insert(0, room.get(key, ""))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries_room[key] = entry

        # Frame cho thông tin khách
        frame_guest = tk.Frame(edit_window, bg="#fef9f4")
        frame_guest.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        if room.get("status") == "Đang thuê" and room.get("Khach"):
            tk.Label(frame_guest, text="Thông tin khách", font=("Arial", 14, "bold"), bg="#fef9f4").grid(row=0, column=0, columnspan=2, pady=10)

            guest_info = room["Khach"][0]
            labels_guest = ["Họ tên:", "Ngày sinh:", "Số điện thoại khách:", "Quê quán:", "CCCD:", "Ngày thuê:", "Ghi chú:"]
            keys_guest = ["HoTen", "NgaySinh", "SoDienThoai", "QueQuan", "CCCD", "NgayThue", "GhiChu"]
            entries_guest = {}

            for i, (label, key) in enumerate(zip(labels_guest, keys_guest), start=1):
                tk.Label(frame_guest, text=label).grid(row=i, column=0, padx=10, pady=5)

                if key == "NgaySinh":
                    date_str = guest_info.get("NgaySinh", "")
                    try:
                        date_val = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.today()
                    except ValueError:
                        date_val = datetime.today()
                    entry = DateEntry(frame_guest, date_pattern="yyyy/mm/dd")
                    entry.set_date(date_val)
                else:
                    entry = tk.Entry(frame_guest)
                    entry.insert(0, guest_info.get(key, ""))

                entry.grid(row=i, column=1, padx=10, pady=5)
                entries_guest[key] = entry

        else:
            # Nếu phòng không đang thuê hoặc không có khách
            tk.Label(frame_guest, text="Phòng hiện không có khách thuê.", font=("Arial", 12), bg="#fef9f4").grid(row=0, column=0, pady=10)

            entries_guest = {}

        save_button = tk.Button(edit_window, text="Lưu", command=lambda: self.save_changes(
            edit_window, index, room,
            entries_room.get("name"),
            entries_room.get("status"),
            entries_room.get("price"),
            entries_guest.get("HoTen"),
            entries_guest.get("NgaySinh"),
            entries_guest.get("SoDienThoai"),
            entries_guest.get("QueQuan"),
            entries_guest.get("CCCD"),
            entries_guest.get("NgayThue"),
            entries_guest.get("GhiChu")
        ))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def save_changes(self, edit_window, index, room,
                 id_entry, name_entry, status_value, price_entry,
                 guest_name_entry, guest_birth_entry,
                 guest_phone_entry, guest_hometown_entry,
                 guest_id_entry, guest_rent_date_entry,
                 guest_note_entry):

        room["id"] = id_entry.get().strip()
        room["name"] = name_entry.get().strip()
        room["status"] = status_value

        try:
            room["price"] = int(price_entry.get())
        except ValueError:
            tk.messagebox.showerror("Lỗi", "Giá phòng phải là số nguyên hợp lệ.")
            return

        if room["status"] == "Đang thuê":
            if guest_birth_entry:
                birth_date = guest_birth_entry.get_date()
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    tk.messagebox.showerror("Lỗi", "Khách phải đủ 18 tuổi trở lên.")
                    return

                room["Khach"] = [{
                    "HoTen": guest_name_entry.get(),
                    "NgaySinh": birth_date.strftime("%Y-%m-%d"),
                    "SoDienThoai": guest_phone_entry.get(),
                    "QueQuan": guest_hometown_entry.get(),
                    "CCCD": guest_id_entry.get(),
                    "NgayThue": guest_rent_date_entry.get(),
                    "GhiChu": guest_note_entry.get()
                }]
        else:
            room["Khach"] = []

        self.rooms_data[index] = room
        self.rooms_data.sort(key=lambda r: r["id"])
        self.save_rooms_data_to_file()
        edit_window.destroy()
        tk.messagebox.showinfo("Thành công", f"Thông tin {room['name']} đã được cập nhật.")
        self.View_Room()

    '''=====XÓA PHÒNG======''' 
    def handle_delete_room(self):
        selection = self.listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Chưa chọn phòng", "Vui lòng chọn phòng để xóa.")
            return

        index = selection[0]

        if not hasattr(self, "displayed_rooms") or index >= len(self.displayed_rooms):
            return

        room = self.displayed_rooms[index]

        if room.get("Khach"):
            current_type = room.get("id", "").strip().upper()[0]

            same_type_rooms = [
                r for r in self.rooms_data
                if r.get("id", "").strip().upper().startswith(current_type)
                and not r.get("Khach") and r != room
            ]

            if same_type_rooms:
                available_room = same_type_rooms[0]
                confirm_transfer = tk.messagebox.askyesno(
                    "Chuyển khách",
                    f"Phòng {room.get('name')} đang có khách. Bạn có muốn chuyển sang phòng {available_room['name']} (cùng loại {current_type}) không?"
                )
                if confirm_transfer:
                    available_room["Khach"] = room["Khach"]
                    available_room["status"] = "Đang thuê"
                    room["Khach"] = None
                    room["status"] = "Trống"
                    self.save_rooms_data_to_file()
                    tk.messagebox.showinfo("Thành công", f"Khách đã được chuyển sang phòng {available_room['name']}.")
                else:
                    return
            else:
                other_type_rooms = [
                    r for r in self.rooms_data
                    if not r.get("Khach") and r.get("id", "").strip().upper()[0] != current_type
                ]
                if other_type_rooms:
                    available_room = other_type_rooms[0]
                    confirm_transfer = tk.messagebox.askyesno(
                        "Chuyển khách khác loại",
                        f"Tất cả phòng loại {current_type} đều đã đầy.\nBạn có muốn chuyển sang phòng {available_room['name']} (loại {available_room.get('id')[0]}) không?"
                    )
                    if confirm_transfer:
                        available_room["Khach"] = room["Khach"]
                        available_room["status"] = "Đang thuê"
                        room["Khach"] = None
                        room["status"] = "Trống"
                        self.save_rooms_data_to_file()
                        tk.messagebox.showinfo("Thành công", f"Khách đã được chuyển sang phòng {available_room['name']}.")
                    else:
                        return
                else:
                    tk.messagebox.showwarning("Không có phòng trống", "Hiện tại không có phòng trống để chuyển khách.")
                    return

        confirm = tk.messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa phòng {room.get('name', '')}?")
        if confirm:
            tk.messagebox.showinfo("Thông báo", f"Xóa phòng {room.get('name', '')} thành công!")

            self.rooms_data = [r for r in self.rooms_data if r.get("id") != room.get("id")]
                
            self.save_rooms_data_to_file()
            self.update_hoadon_file()

            self.View_Room()

    def save_rooms_data_to_file(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        file_path = os.path.join(JSON_DIR, "rooms.json")
        
        # Ghi file JSON theo đúng định dạng có key "rooms"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({"rooms": self.rooms_data}, file, indent=4, ensure_ascii=False)
        print("Dữ liệu đã được lưu vào file JSON.")

    def handle_view_details(self):
        selection = self.listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Chưa chọn phòng", "Vui lòng chọn phòng để xem chi tiết.")
            return

        class DummyEvent:
            pass
        
        self.display_room_details(DummyEvent())  

        self.show_room_action_buttons()

    def update_button_states(self):
        role = self.read_role()
        if role == "admin":
            self.edit_button.config(state="normal")
            self.delete_button.config(state="normal")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    '''=====THÊM KHÁCH VÀO PHÒNG======''' 
    #đổi màu da thêm khách
    def handle_add_guest(self):
        selection = self.listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Chưa chọn phòng", "Vui lòng chọn một phòng để thêm khách.")
            return

        index = selection[0]
        room = self.rooms_data[index]

        if room.get("status", "").lower() != "trống":
            tk.messagebox.showerror("Không thể thêm khách", f"Phòng '{room.get('name', '')}' không còn trống.")
            return

        # Tạo cửa sổ thêm khách
        add_guest_window = tk.Toplevel(self.app)
        add_guest_window.title(f"Thêm khách cho {room.get('name', '')}")
        add_guest_window.geometry("500x500")
        add_guest_window.configure(bg="#fef9f4")

        fields = {
            "HoTen": "Họ tên",
            "NgaySinh": "Ngày sinh",
            "SoDienThoai": "SĐT",
            "QueQuan": "Quê quán",
            "CCCD": "CCCD",
            "TienCoc": "Tiền cọc",
            "NgayThue": "Ngày thuê",
            "GhiChu": "Ghi chú"
        }
        entries = {}
        
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(add_guest_window, text=label, font=("Arial", 12), bg="#fef9f4").grid(row=i, column=0, sticky="w", padx=10, pady=5)

            if key in ("NgaySinh", "NgayThue"):
                entry = DateEntry(add_guest_window, font=("Arial", 12), width=27, date_pattern='yyyy-mm-dd')
            else:
                entry = tk.Entry(add_guest_window, font=("Arial", 12), width=30)

            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry
        
        tien_coc_theo_ma = {
            "A": "2500000",
            "B": "1800000"
        }
        room_code = room.get("id", "")
        ma_loai_phong = room_code[0] if room_code else ""
        tien_coc = tien_coc_theo_ma.get(ma_loai_phong, "1800000")
        entries["TienCoc"].insert(0, tien_coc)

        def save_guest():
            new_guest = {key: entry.get().strip() for key, entry in entries.items()}

            if not new_guest["HoTen"]:
                tk.messagebox.showerror("Thiếu thông tin", "Tên khách không được để trống.")
                return
            try:
                ngay_sinh = datetime.strptime(new_guest["NgaySinh"], "%Y-%m-%d")
                today = datetime.today()
                age = today.year - ngay_sinh.year - ((today.month, today.day) < (ngay_sinh.month, ngay_sinh.day))

                if age < 18:
                    tk.messagebox.showerror("Lỗi tuổi", "Khách dưới 18 tuổi không được thuê phòng.")
                    return
            except ValueError:
                tk.messagebox.showerror("Lỗi định dạng", "Ngày sinh không đúng định dạng yyyy-mm-dd.")
                return

            room["Khach"] = room.get("Khach") or []
            room["Khach"].append(new_guest)
            room["status"] = "Đang thuê"
            
            try:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                JSON_DIR = os.path.join(BASE_DIR, "JSON")
                file_path = os.path.join(JSON_DIR, "rooms.json")

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump({"rooms": self.rooms_data}, file, indent=4, ensure_ascii=False)

                tk.messagebox.showinfo("Thành công", f"Đã thêm khách cho phòng '{room.get('name', '')}'.")
                self.View_Room()
                add_guest_window.destroy()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", f"Không thể lưu thông tin khách: {e}")


        tk.Button(add_guest_window, text="Lưu", font=("Arial", 12), bg="#90ee90", command=save_guest).grid(row=len(fields), column=0, columnspan=2, pady=20)

    '''=====XÓA KHÁCH KHỎI PHÒNG======''' 
    def handle_remove_guest(self):
        selection = self.listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Chưa chọn phòng", "Vui lòng chọn phòng để xóa khách.")
            return

        index = selection[0]
        room = self.rooms_data[index]

        # Kiểm tra xem phòng có khách hay không
        if room.get("Khach"):
            # Hỏi xác nhận xóa khách
            confirm = tk.messagebox.askyesno(
                "Xác nhận xóa khách",
                f"Bạn có chắc muốn xóa khách {room['Khach'][0]['HoTen']} khỏi phòng {room.get('name', '')}?"
            )

            if confirm:
                # Lưu lại họ tên khách và ngày trả phòng
                guest_name = room["Khach"][0]["HoTen"]
                return_date = datetime.now().strftime("%Y-%m-%d")  # Lấy ngày hiện tại

                # Thêm thông tin vào lịch sử
                room["LichSu"].append({
                    "HoTen": guest_name,
                    "NgayTra": return_date
                })

                # Xóa khách khỏi phòng
                room["Khach"] = None  # Xóa khách khỏi phòng
                room["status"] = "Trống"  # Cập nhật trạng thái phòng thành "Trống"

                # Hiển thị thông báo xóa khách thành công
                tk.messagebox.showinfo("Thông báo", f"Khách {guest_name} đã được xóa khỏi phòng {room.get('name')}. Ngày trả phòng: {return_date}.")
                
                # Lưu lại dữ liệu vào file JSON
                self.save_rooms_data_to_file()

                # Cập nhật giao diện
                self.View_Room()

        else:
            tk.messagebox.showwarning("Không có khách", "Phòng này không có khách nào.")

    '''=====THU TIỀN PHÒNG======''' 
    def update_hoadon_file(self):
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            JSON_DIR = os.path.join(BASE_DIR, "JSON")
            rooms_path = os.path.join(JSON_DIR, "rooms.json")
            hoadon_path = os.path.join(JSON_DIR, "invoices.json")
            setting_path = os.path.join(JSON_DIR, "settings.json")

            with open(rooms_path, "r", encoding="utf-8-sig") as file:
                rooms_data = json.load(file)["rooms"]

            with open(setting_path, "r") as f_setting:
                settings_data = json.load(f_setting)["ngay_thu_tien"]

            if os.path.exists(hoadon_path):
                with open(hoadon_path, "r", encoding="utf-8-sig") as f:
                    invoices_data = json.load(f).get("invoices", [])
            else:
                invoices_data = []

            today = datetime.today()
            current_day = today.day
            current_month = today.strftime("%Y-%m")

            invoices_map = {(inv["id"], inv["name"], inv["month"]): inv for inv in invoices_data}

            for room in rooms_data:
                if room.get("status") == "Đang thuê" and room.get("Khach"):
                    for khach in room["Khach"]:
                        ten_khach = khach.get("HoTen", "")
                        key = (room["id"], ten_khach, current_month)

                        last_invoice = None
                        previous_invoices = [inv for inv in invoices_data
                                            if inv["id"] == room["id"] and inv["name"] == ten_khach and inv["month"] < current_month]

                        if previous_invoices:
                            last_invoice = max(previous_invoices, key=lambda x: x["month"])

                        rent_amount = room.get("price", 0)

                        if key in invoices_map:
                            invoice = invoices_map[key]
                            invoice["rent_amount"] = rent_amount
                        else:
                            if current_day >= settings_data:
                                old_debt = 0
                                if last_invoice and not last_invoice.get("is_paid", False):
                                    old_debt = last_invoice.get("account_payable", 0)
                                updated_debt = old_debt + rent_amount

                                invoices_map[key] = {
                                    "id": room["id"],
                                    "name": ten_khach,
                                    "month": current_month,
                                    "rent_amount": rent_amount,
                                    "is_paid": False,
                                    "account_payable": updated_debt,
                                    "payment_date": ""
                                }

            with open(hoadon_path, "w", encoding="utf-8") as file:
                json.dump({"invoices": list(invoices_map.values())}, file, indent=4, ensure_ascii=False)

            print(f"✅ Đã cập nhật {len(invoices_map)} hóa đơn vào '{hoadon_path}'.")

        except Exception as e:
            print(f"❌ Lỗi khi cập nhật hóa đơn: {e}")


    def handle_receive_payment(self):
        self.update_hoadon_file()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        invoice_path = os.path.join(JSON_DIR, "invoices.json")

        settings_path = os.path.join(JSON_DIR, "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        else:
            settings = {}

        ngay_thu = settings.get("ngay_thu_tien", 1)


        if os.path.exists(invoice_path):
            with open(invoice_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                invoices_data = data.get("invoices", [])
        else:
            invoices_data = []

        def is_room_paid(room_id, ten_khach):
            invoice = next((inv for inv in invoices_data if inv.get("id") == room_id and inv.get("name") == ten_khach), None)
            if invoice:
                return invoice.get("account_payable", 0) == 0 or invoice.get("is_paid", False)
            return False

        def show_invoice(room_id):
            room = next((r for r in self.rooms_data if r.get("id") == room_id), None)
            if not room or not room.get("Khach"):
                mb.showerror("Lỗi", f"Không tìm thấy phòng hoặc khách thuê trong phòng {room_id}.")
                return
            ten_khach = room["Khach"][0]["HoTen"]

            invoice = next((inv for inv in invoices_data if inv.get("id") == room_id and inv.get("name") == ten_khach), None)
            if not invoice:
                mb.showerror("Lỗi", f"Không tìm thấy hóa đơn cho phòng {room_id} và khách {ten_khach}.")
                return
            self.show_invoice_details(invoice)

        def collect_payment(room_id):
            room = next((r for r in self.rooms_data if r.get("id") == room_id), None)
            if not room or not room.get("Khach"):
                mb.showerror("Lỗi", f"Không tìm thấy phòng hoặc khách thuê trong phòng {room_id}.")
                return
            ten_khach = room["Khach"][0]["HoTen"]

            invoice = next((inv for inv in invoices_data if inv.get("id") == room_id and inv.get("name") == ten_khach), None)
            if not invoice:
                mb.showerror("Lỗi", f"Không tìm thấy hóa đơn cho phòng {room_id} và khách {ten_khach}.")
                return
            self.show_invoice_details(invoice)

        receive_payment_window = tk.Toplevel(self.app)
        receive_payment_window.title("Thu tiền phòng")
        receive_payment_window.geometry("500x400")
        receive_payment_window.resizable(0, 0)
        receive_payment_window.configure(bg="#fef9f4")

        tk.Label(receive_payment_window, text="Chọn nhóm phòng:", bg="#fef9f4", font=("Arial", 12)).pack(pady=(15, 5))
        group_combo = ttk.Combobox(receive_payment_window, values=["Chưa thu", "Đã thu"], font=("Arial", 12), state="readonly", width=28)
        group_combo.pack(pady=5)
        group_combo.current(0)

        tk.Label(receive_payment_window, text="Chọn phòng:", bg="#fef9f4", font=("Arial", 12)).pack(pady=(15, 5))
        room_combo = ttk.Combobox(receive_payment_window, values=[], font=("Arial", 12), state="readonly", width=28)
        room_combo.pack(pady=5)

        action_button = tk.Button(receive_payment_window, font=("Arial", 12), padx=10, pady=5)
        action_button.pack(pady=20)

        ngay_thu_label = tk.Label(receive_payment_window, text=f"Ngày thu tiền hàng tháng: {ngay_thu}", bg="#fef9f4", font=("Arial", 12))
        ngay_thu_label.pack()

        def open_edit_ngay_thu():
            edit_window = tk.Toplevel(receive_payment_window)
            edit_window.title("Chỉnh sửa ngày thu")
            edit_window.geometry("300x150")
            edit_window.resizable(0, 0)
            edit_window.configure(bg="#fff9f4")

            tk.Label(edit_window, text="Chọn ngày thu tiền (1 - 27):", font=("Arial", 12), bg="#fff9f4").pack(pady=10)
            day_var = tk.IntVar(value=ngay_thu)
            day_spin = tk.Spinbox(edit_window, from_=1, to=27, textvariable=day_var, font=("Arial", 12), width=5)
            day_spin.pack()

            def save_day():
                selected_day = day_var.get()
                if selected_day < 0 or selected_day > 27:
                    mb.showerror("Lỗi", "Ngày không hợp lệ !!!")
                    return
                settings["ngay_thu_tien"] = selected_day
                with open(settings_path, "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=4)
                ngay_thu_label.config(text=f"Ngày thu tiền hàng tháng: {selected_day}")
                edit_window.destroy()
                mb.showinfo("Thành công", f"Đã lưu ngày thu tiền là ngày {selected_day} hàng tháng.")

            tk.Button(edit_window, text="Lưu", font=("Arial", 12), command=save_day, bg="#4caf50", fg="white").pack(pady=10)

        tk.Button(receive_payment_window, text="🛠️ Chỉnh sửa ngày thu", font=("Arial", 11),
                bg="#2196f3", fg="white", command=open_edit_ngay_thu).pack(pady=(5, 10))


        rented_rooms = [room for room in self.rooms_data if room.get("status", "").lower() == "đang thuê"]

        def update_room_list(event=None):
            selected_group = group_combo.get()
            filtered_rooms = []

            if selected_group == "Chưa thu":
                for room in rented_rooms:
                    ten_khach = room["Khach"][0]["HoTen"] if room.get("Khach") else ""
                    if not is_room_paid(room.get("id"), ten_khach):
                        filtered_rooms.append(room.get("id"))
            else:
                for room in rented_rooms:
                    ten_khach = room["Khach"][0]["HoTen"] if room.get("Khach") else ""
                    if is_room_paid(room.get("id"), ten_khach):
                        filtered_rooms.append(room.get("id"))

            room_combo['values'] = filtered_rooms
            if filtered_rooms:
                room_combo.current(0)
            else:
                room_combo.set('')

            update_button_label()

        def update_button_label(event=None):
            selected_room_id = room_combo.get().strip()
            if not selected_room_id:
                action_button.config(text="", command=lambda: None, bg="#fef9f4")
                return

            room = next((r for r in rented_rooms if r.get("id") == selected_room_id), None)
            if not room or not room.get("Khach"):
                action_button.config(text="", command=lambda: None, bg="#fef9f4")
                return
            ten_khach = room["Khach"][0]["HoTen"]

            if is_room_paid(selected_room_id, ten_khach):
                action_button.config(text="🧾 Xem hóa đơn", bg="#4caf50", fg="white",
                                    command=lambda: show_invoice(selected_room_id))
            else:
                action_button.config(text="💰 Thu tiền", bg="#f4a261", fg="black",
                                    command=lambda: collect_payment(selected_room_id))

        group_combo.bind("<<ComboboxSelected>>", update_room_list)
        room_combo.bind("<<ComboboxSelected>>", update_button_label)

        update_room_list()

    def show_receive_payment_button(self):
        role = self.read_role()
        if role == "admin":
            self.receive_payment_button = tk.Button(
                self.details_frame,
                text="💰 Thu tiền phòng",
                bg="#f4a261",
                font=("Arial", 14),
                fg="white",
                command=self.handle_receive_payment
            )
            self.receive_payment_button.pack(side="bottom", pady=10)

    #đổi màu cam chi tiết thông báo 
    def show_invoice_details(self, invoice):
        if self.current_detail_window is not None and self.current_detail_window.winfo_exists():
            self.current_detail_window.destroy()
    
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        invoice_path = os.path.join(JSON_DIR, "invoices.json")

        with open(invoice_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.current_detail_window = tk.Toplevel(self.app)
        self.current_detail_window.title(f"Chi tiết hóa đơn - {invoice.get('id', '')}")
        self.current_detail_window.geometry("600x500")
        self.current_detail_window.configure(bg="#FFECB3")  # cam nhạt nền tổng

        def on_detail_close():
            self.current_detail_window.destroy()
            self.current_detail_window = None

        self.current_detail_window.protocol("WM_DELETE_WINDOW", on_detail_close)

        canvas = tk.Canvas(self.current_detail_window, bg="#FFECB3")
        scrollbar = tk.Scrollbar(self.current_detail_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFECB3")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def create_label_entry(parent, label_text, default_value="", row=0):
            label = tk.Label(parent, text=label_text, anchor="w", bg="#FFECB3", font=("Arial", 12))
            label.grid(row=row, column=0, sticky="w", pady=5)

            width = max(len(str(default_value)) + 2, 20)
            entry = tk.Entry(parent, font=("Arial", 13, "italic"), bg="#FFF3E0", fg="#333333", relief="flat", bd=1, width=width, state="readonly")

            entry.grid(row=row, column=1, sticky="w", pady=5, padx=(10, 0))
            entry.config(state="normal")
            entry.insert(0, default_value)
            entry.config(state="readonly")
            return entry

        row = 0
        label_title = tk.Label(scrollable_frame, text="🧾 Chi tiết hóa đơn", bg="#FFECB3", fg="#E65100", font=("Arial", 20, "bold"))
        label_title.grid(row=row, column=0, sticky="w", pady=(15, 10))

        row += 1
        create_label_entry(scrollable_frame, "Mã phòng:", invoice.get("id", ""), row=row)
        row += 1
        create_label_entry(scrollable_frame, "Tên khách thuê:", invoice.get("name", ""), row=row)
        row += 1
        create_label_entry(scrollable_frame, "Tháng:", invoice.get("month", ""), row=row)
        row += 1
        create_label_entry(scrollable_frame, "Tiền thuê:", f"{invoice.get('rent_amount', 0):,} VND", row=row)
        row += 1
        is_paid = invoice.get("is_paid", False)
        print("DEBUG - is_paid value:", is_paid, type(is_paid))  # Debug log

        if isinstance(is_paid, str):
            is_paid = is_paid.strip().lower() in ["true", "1"]
        account_payable = invoice.get("account_payable", 0)

        if account_payable == 0:
            status_text = "Đã thanh toán"
        else:
            status_text = "Còn nợ"

        create_label_entry(
            scrollable_frame,
            "Tình trạng thanh toán:",
            status_text,
            row=row
        )
        row += 1
        create_label_entry(scrollable_frame, "Công nợ:", f"{account_payable:,} VND", row=row)
    
        if is_paid:
            row += 1
            payment_date = invoice.get("payment_date", "") 
            create_label_entry(scrollable_frame, "Ngày thu:", f"{payment_date}", row=row)
        row += 1

        if not is_paid:
            label_title_2 = tk.Label(scrollable_frame, text="💰 Thanh toán", bg="#FFECB3", fg="#E65100", font=("Arial", 20, "bold"))
            label_title_2.grid(row=row, column=0, sticky="w", pady=(15, 10))
            row += 1

            tk.Label(scrollable_frame, text="Nhập số tiền:", bg="#FFECB3", font=("Arial", 12)).grid(row=row, column=0, sticky="w", pady=5)
            amount_entry = tk.Entry(scrollable_frame, font=("Arial", 13), bg="#FFFFFF", fg="#333333", relief="solid", bd=1, width=25)
            amount_entry.grid(row=row, column=1, sticky="w", pady=5, padx=(10, 0))
            row += 1

            def handle_payment():
                amount = amount_entry.get()
                try:
                    paid_amount = int(amount.replace(",", "").strip())
                    if paid_amount <= 0:
                        raise ValueError

                    self.update_paid_file(invoice.get("id"), invoice.get("month"), paid_amount)

                    mb.showinfo("Thông báo", f"Đã thanh toán {paid_amount:,} VND cho hóa đơn {invoice.get('id', '')}")

                    with open(invoice_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    updated_invoice = next((inv for inv in data.get("invoices", []) 
                                            if inv.get("id") == invoice.get("id") and inv.get("month") == invoice.get("month")), None)

                    if updated_invoice is not None:
                        self.current_detail_window.destroy()
                        self.show_invoice_details(updated_invoice)
                    else:
                        print("Không tìm thấy hóa đơn để cập nhật lại giao diện.")

                except ValueError:
                    mb.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ.")

            pay_button = tk.Button(scrollable_frame, text="Thanh toán", font=("Arial", 12, "bold"),
                                bg="#FB8C00", fg="white", relief="flat", padx=10, pady=5,
                                command=handle_payment)
            pay_button.grid(row=row, column=1, sticky="w", pady=(10, 20), padx=(10, 0))

        scrollable_frame.columnconfigure(1, weight=1)

    def update_paid_file(self, room_id, month, amount_paid):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_DIR = os.path.join(BASE_DIR, "JSON")
        invoice_path = os.path.join(JSON_DIR, "invoices.json")

        if os.path.exists(invoice_path):
            with open(invoice_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"invoices": []}

        invoice_updated = False

        for invoice in data.get("invoices", []):
            if invoice.get("id") == room_id and invoice.get("month") == month:
                current_invoice_debt = invoice.get("account_payable", 0)
                new_invoice_debt = max(0, current_invoice_debt - amount_paid)
                invoice["account_payable"] = new_invoice_debt
                invoice["is_paid"] = (new_invoice_debt == 0)
                if new_invoice_debt == 0:
                    invoice["payment_date"] = datetime.today().strftime("%Y-%m-%d")
                invoice_updated = True
                break

        if not invoice_updated:
            print(f"Không tìm thấy hóa đơn cho phòng {room_id} tháng {month} để cập nhật.")

        with open(invoice_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print("Thanh toán đã được cập nhật.")

    '''====LẤY DỮ LIỆU PHÒNG TRỌ TỪ WEBSITE======'''
    def CrawlToFile(self):
        url = 'https://phongtro123.com/phong-tro-ngay-thanh-thai-trung-tam-quan-10-dep-trang-bi-day-du-noi-that-pr612116.html'
        response = requests.get(url)
        response.encoding = 'utf-8-sig'
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        # Lấy giá phòng
        price_section = soup.find('p', string=lambda text: text and 'Giá phòng' in text)
        price = price_section.get_text(strip=True) if price_section else 'Không tìm thấy giá'

        # Lấy diện tích phòng
        area_section = soup.find('p', string=lambda text: text and 'Phòng rộng' in text)
        area = area_section.get_text(strip=True) if area_section else 'Không tìm thấy diện tích'

        # Lấy địa chỉ cho thuê
        addresses = []
        address_sections = soup.find_all('p', string=lambda text: text and 'Địa chỉ' in text)
        for address_section in address_sections:
            addresses.append(address_section.get_text(strip=True))

        # Lấy số điện thoại liên hệ
        phone_section = soup.find('p', string=lambda text: text and 'Liên hệ thuê phòng' in text)
        phone = phone_section.get_text(strip=True) if phone_section else 'Không tìm thấy số điện thoại'

        # Trả về thông tin dưới dạng dictionary
        return {
            'price': price,
            'area': area,
            'addresses': addresses,
            'phone': phone
        }

    '''=====HIỂN THỊ PPHÒNG TRỌ TỪ HÀM 'CrawlToFile()'======'''
    #đổi màu cam CrawlToFile
    def Crawl_Display(self):
        property_info = self.CrawlToFile()

        # Tạo cửa sổ mới
        popup = tk.Toplevel(self.app)
        popup.title("Thông tin phòng trọ từ Phongtro123.com")
        popup.geometry("600x400")
        popup.configure(bg="#FFF5E1")  # nền cam nhạt

        # Tiêu đề
        label_title = tk.Label(popup, text="Thông tin phòng trọ", font=("Segoe UI", 16, "bold"), fg="#FF8C00", bg="#FFF5E1")
        label_title.pack(pady=10)

        # Hiển thị thông tin dạng Text (không chỉnh sửa được)
        text_info = tk.Text(popup, wrap=tk.WORD, font=("Arial", 12), height=15, bg="#FFF8DC")  # nền text cam nhạt
        text_info.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        text_info.insert(tk.END, f"{property_info['price']}\n")
        text_info.insert(tk.END, f"{property_info['area']}\n\n")
        text_info.insert(tk.END, "Địa chỉ:\n")
        for addr in property_info['addresses']:
            text_info.insert(tk.END, f" - {addr}\n")
        text_info.insert(tk.END, f"\n{property_info['phone']}\n")

        # Không cho chỉnh sửa nội dung
        text_info.config(state="disabled")

        # Nút đóng
        close_btn = tk.Button(popup, text="Đóng", command=popup.destroy, bg="#FF8C00", fg="white", font=("Arial", 12), activebackground="#FFA500")
        close_btn.pack(pady=10)

    '''=====GIAO DIỆN HƯỚNG DẪN SỬ DỤNG======'''
    #đổi màu cam hướng dẫn 
    def User_Manual(self):
        self.hide_all_text_frames()

        # Hiện frame hướng dẫn
        self.text_area_frame_guide.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Cập nhật nội dung hướng dẫn
        self.text_area_guide.config(state="normal")
        self.text_area_guide.delete(1.0, tk.END)

        guide_content = [
            "📘 Hướng dẫn sử dụng AppTro:",
            "",
            "🔑 Admin (Chủ trọ):",
            "- Quản lý danh sách phòng, khách thuê",
            "- Tạo & cập nhật hóa đơn",
            "- Ghi nhận tiền thuê hàng tháng",
            "- Thêm/sửa/xóa thông tin phòng & khách",
            "",
            "👤 User (Khách thuê):",
            "- Xem danh sách phòng",
            "- Tìm kiếm, lọc phòng theo nhu cầu",
            "- Xem chi tiết phòng"
        ]

        for line in guide_content:
            self.text_area_guide.insert(tk.END, line + "\n")

        # Đổi màu chữ sang cam đậm, font rõ nét
        self.text_area_guide.config(
            fg="#FF8C00",  # cam đậm
            bg="#FFF5E1",  # nền cam rất nhạt
            font=("Segoe UI", 16, "bold"),
            state="disabled"
        )

    '''=====GIAO DIỆN THÔNG BÁO======'''
    def generate_notifications_from_invoices(self):
        today = datetime.today()
        current_month = today.strftime("%Y-%m")
        room_status = defaultdict(lambda: {"paid_months": set(), "unpaid_months": set()})

        for invoice in self.invoices_data:
            room_id = invoice["id"]
            invoice_month = invoice["month"]
            is_paid = invoice["is_paid"]

            if is_paid:
                room_status[room_id]["paid_months"].add(invoice_month)
            else:
                room_status[room_id]["unpaid_months"].add(invoice_month)

        self.notifications_data = []
        for room_id, status in sorted(room_status.items()):
            if current_month in status["paid_months"]:
                if status["unpaid_months"]:
                    unpaid_str = ", ".join(sorted(status["unpaid_months"]))
                    self.notifications_data.append(
                        (room_id, f"Phòng {room_id} đã thanh toán tháng này nhưng còn nợ các tháng: {unpaid_str}", "red")
                    )
                else:
                    self.notifications_data.append(
                        (room_id, f"Phòng {room_id} đã thanh toán tháng này.", "green")
                    )
            else:
                unpaid_months_sorted = sorted(status["unpaid_months"])
                unpaid_str = ", ".join(unpaid_months_sorted)
                self.notifications_data.append(
                    (room_id, f"Phòng {room_id} chưa thanh toán tháng này và còn nợ các tháng: {unpaid_str}", "red")
                )

    def check_payment_notification(self):
        today = datetime.today()
        self.generate_notifications_from_invoices()

        if today.day == 10:
            message = "Hôm nay là ngày thu tiền phòng.\nBạn có muốn xem chi tiết?"
        else:
            message = "Hôm nay không phải ngày thu tiền phòng.\nBạn có muốn xem chi tiết?"

        if mb.askyesno("Thông báo", message):
            if self.notifications_data:
                self.show_notifications()
            else:
                mb.showinfo("Thông báo", "Hiện tại không có thông báo nào.")

    #đổi màu cam thông báo 
    def show_notifications(self):
        win = tk.Toplevel(self.app)
        win.title("Chi tiết thông báo")
        win.geometry("800x700")
        win.resizable(0, 0)
        win.configure(bg="#FFE5B4")  # nền cam nhạt

        label = tk.Label(
            win,
            text="Danh sách thông báo:",
            font=("Arial", 16, "bold"),
            bg="#FFE5B4",          # nền cam nhạt
            fg="#FF8C00",         # chữ cam đậm
            anchor="w"
        )
        label.pack(padx=10, pady=(10, 5), anchor="w")

        text_box = tk.Text(win, wrap="word", height=50, width=200, bg="#FFF5E1")
        text_box.pack(padx=10, pady=5, fill="both", expand=True)

        text_box.tag_config("green", foreground="#388E3C", font=("Arial", 16))  # xanh lá đậm
        text_box.tag_config("red", foreground="#D84315", font=("Arial", 16))    # đỏ cam

        if not self.notifications_data:
            text_box.insert("end", "Không có thông báo nào.\n", "green")
        else:
            for room_id, msg, color in self.notifications_data:
                text_box.insert("end", msg + "\n", color)

        text_box.configure(state="disabled")

    '''=====GIAO DIỆN CÀI ĐẶT======'''
    def Setting(self):
         self.hide_all_text_frames()

    """=====XỬ LÝ ĐĂNG XUẤT====="""
    def logout(self):
        self.app.quit()
        self.app.destroy()
        main()
    
    def on_close(self):
        if self.app.winfo_exists() and mb.askokcancel("Thoát", "Bạn muốn thoát ứng dụng?"):
            self.app.destroy()
            exit(0)

    '''=====THOÁT KHỎI HỆ THỐNG====='''
    def exit(self):
        if self.app.winfo_exists() and mb.askokcancel("Thoát", "Bạn muốn thoát ứng dụng?"):
            self.app.quit()
            self.app.destroy()
            exit(0)

def main():
    from login import LoginApp
    login_app = LoginApp()
    login_app.mainloop()

    try:
        with open('JSON/role.json', 'r') as f:
            data = json.load(f)
            if data.get('role') in ['user', 'admin']:
                root = ctk.CTk()
                app = AppTro(root)
                root.mainloop()
            else:
                print("Vai trò không hợp lệ.")
    except Exception as e:
        print(f"Lỗi đọc role.json: {e}")
        exit(1)
