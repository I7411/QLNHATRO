# QLNHATRO
BỘ CÔNG THƯƠNG
TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP.HỒ CHÍ MINH
KHOA CÔNG NGHỆ THÔNG TIN
-----o0o----


TIỂU LUẬN HỌC PHẦN: LẬP TRÌNH PYTHON


TÊN ĐỀ TÀI: ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ


ĐỀ TÀI: 04

Thành phố Hồ Chí Minh, ngày 1 tháng 06 năm 2025
 
BỘ CÔNG THƯƠNG
TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP.HỒ CHÍ MINH
KHOA CÔNG NGHỆ THÔNG TIN
-----o0o----

TIỂU LUẬN HỌC PHẦN: LẬP TRÌNH PYTHON
Sinh viên: 
                     Huỳnh Thanh Minh Tâm – 2001230789
                     Hứa Vĩnh Khang – 2001230385	Giảng viên hướng dẫn: 
Đinh Nguyễn Trọng Nghĩa



Thành phố Hồ Chí Minh, ngày 1 tháng 06 năm 2025
MỤC LỤC
1. Giới thiệu	1
1.1. Bối cảnh	1
1.2. Mục tiêu	1
1.3. Phạm vi và đối tượng sử dụng	1
1.3.1. Phạm vi sử dụng	1
1.3.2. Đối tượng sử dụng	1
2. Công nghệ và công cụ	2
2.1. Ngôn ngữ lập trình	2
2.2. Thư viện sử dụng	2
2.3. Công cụ hỗ trợ	3
2.4. Các API sử dụng	3
2.4.1. API lấy dữ liệu từ Phongtro123.com:	3
3. Phân tích yêu cầu	4
3.1. Chức năng hệ thống – CRUD	4
3.1.1. Quản lý phòng trọ	4
3.1.2. Quản lý khách thuê	5
3.1.3. Quản lý hóa đơn	5
3.2. Yêu cầu kĩ thuật	5
3.2.1. Giao diện người dùng (GUI)	5
3.2.2. Quản lý dữ liệu	5
4. Thiết kế hệ thống	7
4.1. Kiến trúc máy tính	7
4.2. Thiết kế giao diện (Tkinter)	7
4.2.1. Giao diện chính	7
4.2.2. Các cửa sổ chức năng	10
4.3. Cấu trúc dữ liệu	11
5. Cài đặt và triển khai	13
5.1. Quá trình triển khai	13
5.2. Mô tả mã nguồn	13
5.2.1. Giao diện	13
5.2.2. Quản lý dữ liệu JSON	18
5.2.3. Chức năng CRUD	20
5.3. Hướng dẫn sử dụng ứng dụng	20
5.3.1. Mở ứng dụng	20
5.3.2. Đăng nhập	20
5.3.3. Tạo tài khoản mới	21
5.3.4. Quản lý phòng	21
5.3.5. Thông báo	22
5.3.6. Quên mật khẩu	22
6. Kiểm thử và đánh giá	23
6.1. Quá trình kiểm thử	23
6.1.1. Kiểm thử CRUD	23
6.1.2. Kiểm thử đăng nhập/đăng ký	23
6.1.3. Kiểm thử giao diện (GUI Testing) với Tkinter	23
6.1.4. Kiểm thử dữ liệu JSON	23
6.2. Kết quả kiểm thử	23
7. Kết luận	24
7.1. Tóm tắt kết quả	24
7.2. Hướng phát triển	24
8. Tài liệu tham khảo	25
PHỤ LỤC	26

 
LỜI CAM ĐOAN

Em/ chúng em xin cam đoan đề tài Ứng dụng Quản lí Phòng Trọ do cá nhân/nhóm nghiên cứu và thực hiện. 
Em/ chúng em đã kiểm tra dữ liệu theo quy định hiện hành. 
Kết quả bài làm của đề tài Ứng dụng Quản lí Phòng Trọ là trung thực và không sao chép từ bất kỳ bài tập của nhóm khác. 
Các tài liệu được sử dụng trong tiểu luận có nguồn gốc, xuất xứ rõ ràng.

                                                                                 (Ký và ghi rõ họ tên)


					Hứa Vĩnh Khang – Huỳnh Thanh Minh Tâm 
 
 
1. Giới thiệu
1.1. Bối cảnh 
	Trong suốt quá trình vận hành và quản lý nhà trọ/phòng trọ, chủ trọ thường xuyên phải thực hiện nhiều công việc: quản lý danh sách phòng, hợp đồng thuê, thông tin người thuê, theo dõi thanh toán tiền phòng, tiền điện nước, và giải quyết các vấn đề bảo trì, sửa chữa. Việc này thường mất nhiều thời gian, dễ xảy ra sai sót nếu quản lý thủ công bằng giấy tờ hoặc bảng tính đơn giản.
Nhận thấy được nhu cầu thực tế và sự cần thiết của việc số hóa quy trình quản lý, phần mềm quản lý phòng trọ đã được nghiên cứu và phát triển nhằm giúp chủ trọ và nhân viên có thể dễ dàng thao tác: tạo mới phòng, quản lý hợp đồng, thêm/sửa/xóa thông tin người thuê, theo dõi hóa đơn, quản lý công nợ, và báo cáo doanh thu – tất cả chỉ trong một ứng dụng duy nhất. Phần mềm này hứa hẹn nâng cao hiệu quả làm việc, giảm thiểu rủi ro, và mang đến sự hài lòng cho cả chủ trọ lẫn người thuê.
1.2. Mục tiêu
Mục tiêu của đề tài là phát triển một phần mềm quản lý phòng trọ, phục vụ các thao tác cơ bản để quản lý và theo dõi thông tin phòng trọ, hợp đồng thuê, người thuê, cũng như các khoản thu chi (tiền phòng, điện, nước, internet). Phần mềm hỗ trợ tạo tài khoản cá nhân thông qua chức năng đăng ký và đăng nhập, đồng thời phân quyền dựa trên loại người dùng là quản trị viên (chủ trọ/nhân viên quản lý) hoặc người dùng thường (người thuê trọ).
1.3. Phạm vi và đối tượng sử dụng
1.3.1. Phạm vi sử dụng
•	Quản lý thông tin phòng trọ, hợp đồng thuê, người thuê.
•	Quản lý các khoản thu chi gồm tiền phòng, điện, nước, internet.
•	Hỗ trợ chức năng đăng ký, đăng nhập và phân quyền người dùng.
1.3.2. Đối tượng sử dụng
•	Quản trị viên: Chủ trọ hoặc nhân viên quản lý có quyền quản lý toàn bộ hệ thống.
•	Người dùng thường: Người thuê trọ, có quyền truy cập xem thông tin phòng trọ, tìm kiếm và lọc phòng. 
2. Công nghệ và công cụ
2.1. Ngôn ngữ lập trình
−	Python phiên bản 3.11.11
2.2. Thư viện sử dụng
−	json: Thư viện được sử dụng để làm việc với định dạng dữ liệu JSON.
−	import tkinter as tk: Thư viện giao diện đồ họa chuẩn trong Python.
−	from tkinter import ttk, filedialog, messagebox:
•	ttk: mở rộng của tkinter, có thêm các widget nâng cao.
•	filedialog: hộp thoại chọn file, thư mục.
•	messagebox: hiển thị thông báo, cảnh báo, hỏi yes/no cho người dùng.
−	import requests: Gửi HTTP request  để lấy dữ liệu từ web, API.
−	from bs4 import BeautifulSoup: Thư viện phân tích cú pháp HTML và XML, dùng để trích xuất và xử lý dữ liệu từ trang web.
−	import os: Tương tác với hệ điều hành.
−	import customtkinter as ctk: Một thư viện tùy biến dựa trên tkinter, giúp tạo giao diện hiện đại, đẹp mắt hơn.
−	from datetime import datetime: Xử lý ngày giờ hiện tại, định dạng ngày giờ, so sánh thời gian.
−	from tkcalendar import DateEntry: Nhập widget DateEntry từ thư viện tkcalendar để chọn ngày tháng trên giao diện tkinter.
−	import re:  Xử lý biểu thức chính quy, dùng để tìm kiếm, kiểm tra, tách chuỗi theo mẫu.
−	from collections import defaultdict: Nhập lớp defaultdict để tạo dictionary với giá trị mặc định tự động khi truy cập khóa chưa tồn tại.
−	from PIL import Image, ImageTk, ImageSequence:
•	Image: xử lý hình ảnh.
•	ImageTk: chuyển hình ảnh để hiển thị lên giao diện tkinter.
•	ImageSequence: xử lý các khung ảnh trong file GIF hoặc ảnh động.
−	import smtplib: Gửi email qua giao thức SMTP.
−	from email.mime.text import MIMEText: Tạo nội dung email dạng văn bản.
−	from email.mime.multipart import MIMEMultipart: Tạo email phức tạp gồm nhiều phần. 
−	from dotenv import load_dotenv: Đọc file .env chứa biến môi trường mà không ghi trực tiếp trong code.
−	import random: Tạo số ngẫu nhiên, chọn ngẫu nhiên trong danh sách, xáo trộn thứ tự.
2.3. Công cụ hỗ trợ
−	IDE (Visual Studio Code)
−	GitHub
2.4. Các API sử dụng
2.4.1. API lấy dữ liệu từ Phongtro123.com:
−	Mục đích: Tự động thu thập thông tin phòng trọ (giá, địa chỉ, mô tả, liên hệ) từ website Phongtro123.com để hiển thị vào hệ thống quản lý nội bộ.
−	Công nghệ sử dụng:
•	requests: để gửi yêu cầu HTTP đến trang web.
•	BeautifulSoup (bs4): để phân tích cú pháp HTML và trích xuất dữ liệu.



−	Kết quả:

3. Phân tích yêu cầu
3.1. Chức năng hệ thống – CRUD
	3.1.1. Quản lý phòng trọ
−	Create: Thêm phòng mới (ID, số phòng, giá thuê,...)
−	Read: Xem danh sách tất cả phòng đang trống hoặc đã có người thuê
−	Update: Sửa thông tin phòng (giá thuê, trạng thái,...)
−	Delete: Xóa phòng trọ khỏi hệ thống (chỉ được xóa khi phòng trống; nếu đang có người thuê, cần chuyển khách sang phòng khác trước khi xóa).
3.1.2. Quản lý khách thuê
−	Create: Thêm thông tin khách thuê mới (họ tên, CCCD, SDT,...)
−	Read: Xem thông tin chi tiết khách đang thuê phòng
−	Update: Sửa thông tin khách thuê (họ tên, CCCD, SDT,...)
−	Delete: Xóa thông tin khách (sau khi chuyển đi)
3.1.3. Quản lý hóa đơn
−	Create: Tạo hóa đơn mới cho mỗi tháng
−	Read: Xem danh sách hóa đơn của từng phòng theo tháng
−	Update: Cập nhật trạng thái hóa đơn (đã thu tiền, chưa thu tiền, chỉnh sửa số tiền)
−	Delete: Xóa hóa đơn sai hoặc không hợp lệ
3.2. Yêu cầu kĩ thuật
	3.2.1. Giao diện người dùng (GUI)
−	Giao diện trực quan sử dụng Tkinter
−	Các thành phần cơ bản:
•	Form nhập liệu (Entry, Combobox)
•	Danh sách (TreeView/Listbox)
•	Nút điều hướng (Button)
•	Thông báo lỗi/thành công (messagebox)
−	Cửa sổ riêng cho từng chức năng: quản lý phòng, khách, hóa đơn
3.2.2. Quản lý dữ liệu
−	Folder ‘assets’: chứa thông tin các hình ảnh.
−	Folder ‘JSON’: quản lý thông tin các file json sử dụng trong phần mềm.
•	rooms.json: quản lý dữ liệu phòng, khách thuê và lịch sử thuê.
o	Dữ liệu phòng: ID, name, status, price.
o	Dữ liệu khách: Họ tên, Ngày sinh, Số điện thoại, Quê quán, CCCD, Tiện cọc, Ngày thuê, Ghi chú.
o	Lịch sử: Họ tên và ngày trả (nếu phòng đã từng có khách thuê).
•	role.json: quản lý nội dung xác định vai trò người dùng.
o	Admin: Quản trị toàn bộ hệ thống, có quyền tạo, sửa, xóa dữ liệu (phòng, người dùng, hóa đơn), và cấu hình các thiết lập chung.
o	User (Người dùng thông thường): Chỉ có quyền xem thông tin phòng, hóa đơn và nhận thông báo; không được phép chỉnh sửa hoặc xóa dữ liệu.
•	users.json: quản lý tài khoản cá nhân của người dùng.
o	username: Tên đăng nhập
o	password: Mật khẩu người dùng (Được mã hóa bằng SHA-256)
o	email: Địa chỉ email người dùng.
o	role: Vai trò của người dùng (admin hoặc user).
o	status: Trạng thái tài khoản (active hoặc inactive).
o	created_at: Ngày tạo tài khoản (VD: 2025-03-12T08:30:00Z theo chuẩn theo ISO 8601).
•	invoices.json: quản lý và theo dõi tình trạng thanh toán tiền thuê của từng người thuê nhà.
o	id: ID phòng.
o	name: Tên khách thuê.
o	month: Tháng thanh toán.
o	rent_amount: Số tiền thuê phòng cần thanh toán trong tháng.
o	is_paid: Trạng thái thanh toán (true nếu đã thanh toán, false nếu chưa hoặc còn nợ).
o	account_payable: Số tiền còn phải thanh toán (công nợ).
o	payment_date: Ngày thanh toán, để trống nếu chưa thanh toán.
•	notifications.json: lưu trữ và quản lý các thông báo nhắc nhở những người thuê nhà chưa thanh toán tiền thuê trong tháng.
o	invoice_id: Mã phòng hoặc hóa đơn liên quan đến thông báo.
o	name: Họ tên khách thuê.
o	message: Nội dung thông báo cụ thể, thường liên quan đến việc chưa thanh toán, sắp đến hạn, hoặc các thay đổi.
o	date_created: Ngày tạo thông báo, định dạng YYYY-MM-DD.
o	is_viewed: Trạng thái đã xem thông báo (true nếu đã xem, false nếu chưa).
•	settings.json: lưu trữ và quản lý ngày thu tiền phòng
−	File login.py: quản lý màn hình khởi động splash và giao diện đăng nhập bằng tkinter, sau khi đăng nhập thành công sẽ mở ứng dụng chính.
−	File UserManager.py: lưu trữ, mã hóa mật khẩu, đọc/ghi dữ liệu user vào file JSON và kiểm tra đăng nhập với trạng thái tài khoản.
−	File app.py: quản lý tổng thể giao diện và chức năng của ứng dụng quản lý phòng trọ.
−	File Rental_Room_Management_App.py: điểm khởi đầu của ứng dụng, chịu trách nhiệm hiển thị màn hình khởi động và khởi chạy toàn bộ hệ thống quản lý phòng trọ.
−	logo.ico: logo của ứng dụng, phục vụ cho việc đóng gói phầm mềm thành một ứng dụng hoàn chỉnh. 
4. Thiết kế hệ thống
4.1. Kiến trúc máy tính
−	Hệ thống được thiết kế theo mô hình Client – Local Storage:
•	Giao diện người dùng (GUI): Xây dựng bằng thư viện tkinter trong Python.
•	Xử lý logic: Các chức năng CRUD (Tạo, Đọc, Cập nhật, Xoá) được viết trong Python.
•	Lưu trữ dữ liệu: Lưu trữ dưới dạng các file .json (không dùng cơ sở dữ liệu).
•	Phân quyền: Có 2 vai trò là Admin và User, xác định bằng trường role trong users.json.
4.2. Thiết kế giao diện (Tkinter)
4.2.1. Giao diện chính
−	Màn hình đăng nhập:
•	Nhập “username” và “password”
•	Xác thực và phân quyền (Admin / User)
 
−	Màn hình tạo tài khoản:
•	Tên đăng nhập: Ít nhất 5 ký tự, không chứa ký tự đặc biệt
•	Mật khẩu: Tối thiểu 8 ký tự (bao gồm: chữ hoa, chữ thường, số và ký tự đặc biệt)
•	Xác nhận mật khẩu: Nhập lại mật khẩu chính xác
•	Email: Đúng định dạng (VD: example@gmail.com)

−	Màn hình quên mật khẩu:
•	Email: Nhập địa chỉ email đã đăng ký để hệ thống kiểm tra tài khoản và gửi mã OTP xác thực nếu hợp lệ.
 
−	Màn hình xác nhận OTP:
Sau khi xác nhận Email thành công
 	 
Xác thực mã OTP
 

−	Màn hình cập nhập mật khẩu mới:

4.2.2. Các cửa sổ chức năng
−	Quản lý phòng trọ và khách thuê:
Danh sách phòng	 
Hiển thị ID, tên, trạng thái 
(Đang thuê / Trống)	
Xem chi tiết phòng	 
−	Thông tin khách thuê (nếu có): Họ tên, ngày sinh, số điện thoại, CCCD, địa chỉ, tiền cọc, ghi chú.
−	Lịch sử thuê: Họ tên và ngày trả của khách cũ (nếu có).	
Chức năng
−	Thêm phòng mới.
−	Sửa thông tin phòng.
−	Thêm khách thuê (chỉ khi phòng đang trống):
•	Nhập thông tin khách mới để bắt đầu hợp đồng thuê.
•	Khi thêm khách, phòng sẽ chuyển sang trạng thái “Đang thuê”.
−	Sửa thông tin khách thuê (thực hiện trong giao diện phòng)
−	Xóa khách thuê:
•	Xóa thông tin khách khỏi phòng.
•	Chuyển thông tin vào lịch sử thuê (gồm họ tên khách và ngày trả).
•	Cập nhật phòng thành “Trống”.
−	Xóa phòng:
•	Nếu phòng còn khách thuê, hệ thống sẽ tự động tìm phòng trống cùng loại để chuyển khách sang.
•	Nếu không còn phòng trống cùng loại, hệ thống sẽ hỏi ý khách có đồng ý chuyển sang loại phòng khác hay không.
o	Nếu khách đồng ý: chuyển khách sang phòng trống khác loại.
o	Nếu khách không đồng ý: hủy thao tác xóa.
•	Sau khi khách đã được chuyển đi, phòng mới có thể xóa.
−	Hóa đơn và thanh toán:
•	Giao diện hiển thị gồm:
o	Nhóm phòng (cho phép chọn hiển thị theo trạng thái Đã thu / Chưa thu).
o	Danh sách phòng theo nhóm, cho phép chọn phòng để thu tiền.
o	Ngày thu tiền hàng tháng (cho phép chọn ngày cụ thể để thực hiện thu).
•	Chức năng:
o	Xem danh sách hóa đơn theo tháng và trạng thái thanh toán.
o	Chọn phòng để thực hiện thu tiền thuê.
o	Cập nhật trạng thái thanh toán (Đã thu / Chưa thu) cho từng phòng.
o	In thông báo nợ tiền thuê phòng cho những phòng chưa thanh toán.
o	Tự động tạo thông báo nợ khi phát sinh khoản chưa thanh toán.
−	Thông báo:
•	Danh sách các thông báo:
o	Thông báo nợ tiền thuê (chưa thu)
o	Thông báo đã thu tiền
o	Thông báo còn nợ (phòng chưa thanh toán đầy đủ)
•	Tự động tạo thông báo khi phát sinh nợ.
4.3. Cấu trúc dữ liệu
−	Quản lý tài khoản (users.json):
{
  "username": "user",
  "password": "user123",
  "email": "user@gmail.com",
  "role": "user",
  "status": "active",
  "created_at": "2025-03-12T08:30:00Z"
}

−	Quản lý phòng và khách thuê (rooms.json):
{
  "room_id": "A01",
  "name": "Phòng A01",
  "status": "occupied",
  "price": 2500000,
  "tenant": {
    "full_name": "Nguyễn Văn A",
    "birth_date": "2000-05-12",
    "phone": "0123456789",
    "hometown": "Hà Nội",
    "id_number": "123456789",
    "deposit": 500000,
    "start_date": "2025-04-01",
    "note": ""
  },
  "history": [
    {
      "full_name": "Trần Văn B",
      "checkout_date": "2025-03-20"
    }
  ]
}

−	Quản lý hóa đơn và thanh toán (invoices.json):
{
  "id": "A01",
  "name": "Nguyễn Văn A",
  "month": "2025-05",
  "rent_amount": 2500000,
  "is_paid": false,
  "account_payable": 2500000,
  "payment_date": ""
}
−	Thông báo (notifications.json):
{
  "invoice_id": "A01",
  "name": "Nguyễn Văn A",
  "message": "Phòng A01 (Nguyễn Văn A) còn nợ tiền thuê tháng 2025-05 (2,500,000 VNĐ).",
  "date_created": "2025-05-26",
  "is_viewed": false
}

−	Quản lý vai trò người dùng trong hệ thống (role.json):
{"role": "admin"} hoặc {"role": "user"}

5. Cài đặt và triển khai
5.1. Quá trình triển khai
−	Ứng dụng được phát triển theo quy trình tuần tự các bước như sau:
•	Phân tích yêu cầu: Xác định rõ các chức năng chính như quản lý phòng trọ, khách thuê, hóa đơn, thanh toán và thông báo.
•	Thiết kế giao diện: Sử dụng thư viện Tkinter để thiết kế các cửa sổ tương tác người dùng: danh sách phòng, thông tin khách, hóa đơn, thanh toán và thông báo.
•	Thiết kế dữ liệu: Lưu trữ thông tin bằng các tệp JSON (thay cho cơ sở dữ liệu), gồm rooms.json, users.json, invoices.json, notifications.json,…
•	Xây dựng chức năng CRUD: Phát triển các chức năng Thêm – Xem – Sửa – Xóa cho từng đối tượng: phòng, khách, hóa đơn.
•	Xử lý phân quyền người dùng: Kiểm tra vai trò (role) từ role.json sau khi đăng nhập để giới hạn quyền sử dụng giao diện.
•	Kiểm thử & sửa lỗi: Thực hiện kiểm tra toàn bộ hệ thống và sửa lỗi phát sinh trong quá trình thao tác với dữ liệu.
•	Triển khai & đóng gói: Đóng gói ứng dụng dưới dạng .exe (nếu cần) hoặc chạy trực tiếp bằng Python (python main.py).
5.2. Mô tả mã nguồn
5.2.1. Giao diện
−	Tạo các cửa sổ và bố cục bằng Tkinter.
−	Giao diện đăng nhập, giao diện chính theo vai trò (admin, user).
−	Kết nối các nút lệnh với chức năng tương ứng.
Giao diện đăng nhập: setup_login()
•	Gồm các label hiển thị chữ trên cửa sổ ứng dụng như: “Welcome Back!”, “Đăng nhập với tài khoản của bạn”, “Username”, “Password”, cảnh báo đỏ khi nhập sai thông tin. Các entry nhập liệu cần thiết như username, password.
•	Các button cho sự kiện nhấn ‘Đăng nhập’ và button ‘Đăng ký’ để chuyển sang giao diện đăng ký.
Giao diện đăng ký: setup_reg()
•	Gồm các label hiển thị chữ trên cửa sổ như: “Tạo tài khoản mới”, “Tên đăng nhập”, “Mật khẩu”, “Xác nhận mật khẩu” và “Email”. Các entry cần thiết như username, password, confirm password, email.
•	Các button cho sự kiện nhấn ‘Đăng ký’ và button trở về giao diện đăng nhập.

Xử lí ẩn/hiện giao diện đăng nhập và đăng ký:


Kiểm tra thông tin đăng ký: validate_reg()
−	Sau khi nhập thông tin vào username và password, tiến hành kiểm tra:
•	Nhập thông tin đầy đủ
•	Tên đăng nhập phải có ít nhất
•	Mật khẩu phải đáp ứng tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt
•	Kiểm tra email nhập vào có đúng với định dạng
−	Kiểm tra tài khoản hoặc email có tồn tại trong hệ thống hay chưa (check_existing_user())
−	Khi xác thực thành công – thông báo thành công.

−	Dữ liệu được lưu vào file users.json có dạng.

Giao diện chính: Start_app()

5.2.2. Quản lý dữ liệu JSON
−	Đọc, ghi dữ liệu từ/đến các tệp .json

−	Cập nhập dữ liệu vào các tệp .json


5.2.3. Chức năng CRUD
−	Create: Thêm phòng, thêm khách, thêm hóa đơn
−	Read: Hiển thị danh sách và chi tiết phòng, khách, hóa đơn
−	Update: Cập nhật thông tin phòng hoặc khách thuê
−	Delete: Xóa phòng, xóa khách, xóa hóa đơn (có xác thực điều kiện logic như chuyển khách sang phòng khác)
Ví dụ: Thêm phòng mới

5.3. Hướng dẫn sử dụng ứng dụng
	5.3.1. Mở ứng dụng
−	Chạy chạy file Rental_Room_Management.exe.
5.3.2. Đăng nhập
−	Nhập tên người dùng và mật khẩu.
−	Hệ thống sẽ kiểm tra vai trò người dùng từ file role.json và chuyển đến giao diện phù hợp (Admin hoặc User).

5.3.3. Tạo tài khoản mới
−	Tại màn hình đăng nhập, chọn “Tạo tài khoản mới”.
−	Nhập đầy đủ thông tin: Username, Password, Xác nhận mật khẩu, Email.
−	Nhấn nút “Đăng ký” để tạo tài khoản mới.
−	Hệ thống kiểm tra tính hợp lệ (mật khẩu khớp, email đúng định dạng).
−	Sau khi đăng ký thành công, có thể đăng nhập bằng tài khoản mới.

5.3.4. Quản lý phòng
−	Xem danh sách phòng cùng trạng thái hiện tại (Đang thuê / Trống).
−	Thêm mới, chỉnh sửa hoặc xóa phòng trọ.
−	Xem chi tiết thông tin phòng và khách thuê (nếu có).
−	Thêm khách thuê mới cho phòng đang trống hoặc trả phòng (xóa khách).
−	Tìm kiếm và lọc danh sách phòng theo tiêu chí (ví dụ: theo loại phòng, trạng thái).
−	Thu tiền phòng theo tháng, theo phòng hoặc theo nhóm phòng.
5.3.5. Thông báo
−	Xem danh sách các thông báo thu tiền phòng (Đã thu/chưa thu).
−	Hệ thống sẽ tự động tạo thông báo khi phát sinh nợ.

5.3.6. Quên mật khẩu
−	Nhập email đăng ký tài khoản.
−	Hệ thống gửi mã OTP vào email.
−	Nhập mã OTP để xác thực và cho phép đặt lại mật khẩu mới.
 
6. Kiểm thử và đánh giá
6.1. Quá trình kiểm thử
	6.1.1. Kiểm thử CRUD
−	Tạo (Create): Thêm mới phòng, khách thuê, hóa đơn.
−	Đọc (Read): Xem danh sách phòng, khách, hóa đơn, thông báo.
−	Cập nhật (Update): Sửa thông tin phòng, khách, trạng thái hóa đơn.
−	Xóa (Delete): Xóa phòng (có xử lý kiểm tra chuyển khách nếu có), trả phòng (xóa khách), xóa thông báo.
6.1.2. Kiểm thử đăng nhập/đăng ký
−	Đăng ký tài khoản mới với kiểm tra email, username trùng lặp.
−	Đăng nhập với đúng/sai tài khoản.
−	Quên mật khẩu: Gửi OTP qua email để đặt lại mật khẩu.
6.1.3. Kiểm thử giao diện (GUI Testing) với Tkinter
−	Kiểm tra hiển thị đầy đủ các Label, Entry, Button tương ứng theo chức năng.
−	Kiểm tra luồng chuyển đổi giữa các giao diện.
6.1.4. Kiểm thử dữ liệu JSON
−	Đọc/ghi dữ liệu từ các file: users.json, rooms.json, invoice.json, notifications.json, role.json.
−	Đảm bảo tính nhất quán dữ liệu sau các thao tác.
6.2. Kết quả kiểm thử
−	Các chức năng CRUD hoạt động chính xác.
−	Dữ liệu JSON được cập nhật đầy đủ, không lỗi.
−	Giao diện hoạt động ổn định, thân thiện với người dùng.
−	Hệ thống xử lý đúng các trường hợp đặc biệt như:
•	Không cho thêm khách khi phòng đang có người.
•	Chuyển khách sang phòng khác khi xóa phòng.
•	Tự động tạo thông báo khi có nợ.
−	Thời gian phản hồi nhanh, không gặp lỗi nghiêm trọng trong quá trình sử dụng.

7. Kết luận
Với đề tài ‘Ứng dụng Quản Lý Phòng Trọ’, sinh viên được làm quen với thư viện tkinter – thư viện hỗ trợ xây dựng giao diện người dùng, từ đó nghiên cứu và thực hiện một phần mềm có thể giúp chủ nhà trọ quản lý phòng, hợp đồng, hóa đơn, và thông tin khách thuê một cách dễ dàng. Phần mềm được triển khai với các thao tác đơn giản như thêm, xóa, sửa, tìm kiếm phòng trọ, hợp đồng, khách thuê, từ đó làm bước đệm cho những phát triển sau này, giúp sinh viên cải thiện kỹ năng lập trình giao diện và nâng cao tư duy lập trình ứng dụng.
7.1. Tóm tắt kết quả
−	Ứng dụng quản lý phòng trọ đã được phát triển hoàn chỉnh với các chức năng chính như:
•	Quản lý thông tin phòng, khách thuê và hóa đơn.
•	Hỗ trợ đăng ký, đăng nhập, quên mật khẩu qua OTP.
•	Giao diện thân thiện, trực quan với Tkinter.
•	Dữ liệu được lưu trữ bằng file JSON, dễ truy cập và chỉnh sửa.
•	Tự động tạo thông báo nợ, phân loại trạng thái hóa đơn đã thu / chưa thu.
•	Đáp ứng tốt quy trình thực tế của người quản lý nhà trọ, từ việc thêm phòng, quản lý khách đến thu tiền.
7.2. Hướng phát triển
−	Trong tương lai, ứng dụng có thể được nâng cấp với các tính năng sau:
•	Đồng bộ dữ liệu với cơ sở dữ liệu SQL hoặc Firebase để đảm bảo bảo mật và truy cập từ nhiều thiết bị.
•	Gửi email/tin nhắn tự động khi có thông báo nợ hoặc đến hạn thanh toán.
•	Bổ sung hệ thống phân quyền nâng cao: Quản lý nhiều chủ trọ, mỗi chủ có danh sách phòng riêng.
•	Xuất báo cáo thống kê theo tháng/năm (số phòng đã thuê, doanh thu, khách còn nợ,...).
•	Tích hợp thanh toán điện tử (Momo, ZaloPay, chuyển khoản) để người thuê có thể thanh toán trực tuyến.
•	Giao diện web/mobile giúp dễ dàng truy cập từ điện thoại hoặc trình duyệt. 
8. Tài liệu tham khảo
[1] tkinter — Python interface to Tcl/Tk. (n.d.). Python Documentation. Retrieved June 14, 2024, from https://docs.python.org/3/library/tkinter.html
[2] Fitzpatrick, M. (2022, June 14). Create Python GUI with tkinter. Python GUIs. https://www.pythonguis.com/tutorials/create-gui-tkinter/
[3] Python, R. (2019, March 6). Using PyInstaller to easily distribute Python applications. Realpython.com; Real Python. https://realpython.com/pyinstaller-python/ 
PHỤ LỤC
Mã nguồn: https://github.com/huavinhkhang0405/room-rent-manager.git


















