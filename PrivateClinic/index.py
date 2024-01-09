import math, random
from flask import render_template, session, flash
from PrivateClinic import dao, login, mail
from PrivateClinic.admin import *
from flask_login import login_user, current_user, logout_user
from flask_mail import Mail, Message


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('support.html')


@app.route("/load_login")
def show_login():
    return render_template('login.html')


@app.route("/login", methods=['post'])
def user_login():
    username = request.form.get('username')
    password = request.form.get("password")

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
        id = int(current_user.id_nguoidung)
        nguoiDung = dao.get_info(id)
        session['roles'] = str(current_user.user_role)
        if current_user.user_role == UserRole.ADMIN:
            return redirect("/admin")
        else:
            return render_template('display.html', nguoiDung=nguoiDung)
    else:
        return render_template('login.html')


@app.route("/logout")
def user_logout():
    logout_user()
    return redirect(url_for('show_login'))


@login.user_loader
def load_user(user_id):
    return TaiKhoan.query.get(user_id)


@app.route("/appointment")
def appointment_book():
    id = int(current_user.id_nguoidung)
    benh_nhan = dao.get_info(id)
    return render_template('appointment.html', benhNhan=benh_nhan, nguoiDung=benh_nhan)


# Xem danh sách thuốc
@app.route("/view/medicine")
def view_medicine():
    keyword = request.args.get("keyword")
    cate_id = request.args.get('cate_id')
    page = request.args.get('page', 1)
    category = dao.get_category()
    medicine = dao.get_medicine(keyword=keyword, cate_id=cate_id, page=int(page))
    count = dao.count_medicine()
    return render_template('medicine_list.html', category=category, medicine=medicine,
                           page=math.ceil(count / app.config['PAGE_SIZE']), cate_id=cate_id)


@app.route("/view/invoice")
def list_invoice():
    hoaDon = dao.get_list_invoice()
    return render_template('list_invoice.html', hoaDon=hoaDon)


# Xem thông tin cá nhân
@app.route("/view/profile")
def view_profile():
    id = int(current_user.id_nguoidung)
    benh_nhan = dao.get_info(id)
    user_role = current_user.user_role
    role = dao.get_role(user_role)
    random_number = str(random.randint(1, 4))
    return render_template('profile.html', benhNhan=benh_nhan, role=role, ramdom=random_number)


@app.route("/profile/update", methods=['POST', 'GET'])
def update_profile():
    if request.method == 'POST':
        id = int(current_user.id_nguoidung)
        hoTen = str(request.form.get('hoTen'))
        diaChi = request.form.get('diaChi')
        ngaySinh = request.form.get('ngaySinh')
        soDienThoai = request.form.get('soDienThoai')
        email = request.form.get('email')

        dao.upadate_info(id=id, hoTen=hoTen, ngaySinh=ngaySinh, diaChi=diaChi, soDienThoai=soDienThoai, email=email)
        return redirect(url_for('view_profile'))


# Phiếu khám
@app.route("/medical_examination_form")
def create_medicalform():
    medicine = dao.get_list_medicine()
    return render_template('create_medical_form.html', medicine=medicine)


@app.route('/medical_examination_form/save', methods=['POST', 'GET'])
def save_medical_form():
    maBN = request.form.get('maBN')
    ngayKham = request.form.get('ngayKham')
    trieuChung = request.form.get('trieuChung')
    chuanDoan = request.form.get('chuanDoan')
    cachDung = request.form.getlist('cachDung')
    soLuong = request.form.getlist('soLuong')
    thuoc = request.form.getlist('maThuoc')
    dao.update_list_appointment(maBN)
    dao.create_medical_form(maBN=maBN, ngayKham=ngayKham, chuanDoan=chuanDoan,
                            trieuChung=trieuChung, l_cachDung=cachDung, l_soLuong=soLuong, l_maThuoc=thuoc)
    flash("Lập phiếu khám thành công!", 'success')
    return redirect(url_for('create_medicalform'))


# Danh sách khám
@app.route("/appointment_schedule")
def create_list_appoint():
    l_app = dao.get_list_appointment()
    doctor = dao.get_info_doctor()
    return render_template('create_list_appointment.html', list=l_app, doctor=doctor)


@app.route("/appointment_schedule/save", methods=['POST', 'GET'])
def save_list_appointment():
    maDS = request.form.getlist('maDS')
    maBN = request.form.getlist('maBenhNhan')
    ngayKham = request.form.get('ngayKham')
    bacSi = request.form.get('doctor')
    dao.create_list_appointment(ngay_kham=ngayKham, l_maBN=maBN, l_maDS=maDS, bac_si=bacSi)
    return redirect(url_for('create_list_appoint'))


@app.route("/view/history_patient")
def history_medical_patient():
    maBN = int(current_user.id_nguoidung)
    benhNhan = dao.get_patient_by_id(maBN)
    phieuKham = dao.get_history_medical(maBN)
    return render_template('history_patient.html', benhNhan=benhNhan, phieuKham=phieuKham)


@app.route("/appointment_schedule_new/save", methods=['POST', 'GET'])
def save_appointment_new():
    hoTen = request.form.get('hoTen')
    gioiTinh = request.form.get('gioiTinh')
    diaChi = request.form.get('diaChi')
    ngaySinh = request.form.get('ngaySinh')
    email = request.form.get('email')
    soDienThoai = request.form.get('soDienThoai')
    ngayHen = request.form.get('ngayHen')
    dao.create_appointment_new(hoTen=hoTen, gioiTinh=gioiTinh, ngaySinh=ngaySinh, ngayHen=ngayHen, email=email,
                               diaChi=diaChi, soDienThoai=soDienThoai)
    return render_template('index.html')


@app.route('/appointment/save', methods=['POST', 'GET'])
def create_appointment():
    maBN = request.form.get('maBN')
    ngay_hen = request.form.get('ngayHen')
    dao.create_appointment(ngay_hen=ngay_hen, ma_BN=maBN)
    return redirect(url_for('appointment_book'))


# Hóa đơn
@app.route("/payment", methods=['POST', 'GET'])
def create_payment():
    maPK = request.form.get('maPK')
    tienKham = dao.get_examination_fee()
    hoaDon = dao.get_invoice_by_id(maPK)
    if hoaDon:
        is_none = False
    else:
        is_none = True
    tienThuoc = dao.get_receipt(maPK)
    phieuKham = dao.get_medical_report(maPK)
    phieuThuoc = dao.get_medicine_report(maPK)
    return render_template('payment.html', thuoc=phieuThuoc, phieu=phieuKham, hoaDon=hoaDon, is_none=is_none,
                           tienThuoc=tienThuoc, tienKham=tienKham)


@app.route("/payment/complete", methods=['POST', 'GET'])
def create_invoce():
    if request.method == 'POST':
        maPK = request.form.get('maPK')
        ngayKham = request.form.get('ngayKham')
        tienThuoc = request.form.get('tienThuoc')
        tienKham = request.form.get('tienKham')
        action = request.form.get('action')
        if action == 'thanh_toan':
            dao.create_invoice(ngayKham=ngayKham, tienThuoc=tienThuoc, tienKham=tienKham, maPK=maPK)
            return redirect(url_for('create_payment'))
        return redirect(url_for('create_payment'))


# Lịch sử khám
@app.route('/view/medical_report')
def medical_report_all():
    phieu_kham = dao.get_history_medical_all()
    return render_template('medical_report.html', phieuKham=phieu_kham)


@app.route("/view/list_medical_examiniation")
def list_medical_examiniation():
    bacSi_id = int(current_user.id_nguoidung)
    list_appointment = dao.get_list_medical_examination(bacSi_id)
    return render_template('list_medical_examination.html', list=list_appointment)


@app.route("/view/list_appointment")
def list_appointment():
    list = dao.get_list_appoint_active()
    return render_template("list_appointment.html", list=list)


@app.route('/view/history_medical', methods=['POST', 'GET'])
def history_medical_report():
    maBN = request.form.get('maBN')
    session['roles'] = str(current_user.user_role)
    benh_nhan = dao.get_patient_by_id(maBN)
    phieuKham = dao.get_history_medical(maBN)

    return render_template('medical_report_detail.html', phieuKham=phieuKham, benhNhan=benh_nhan)


# dk tài khoản
@app.route("/register/patient", methods=['POST', 'GET'])
def create_account_patient():
    hoTen = request.form.get('hoTen')
    gioiTinh = request.form.get('gioiTinh')
    diaChi = request.form.get('diaChi')
    ngaySinh = request.form.get('ngaySinh')
    email = request.form.get('email')
    soDienThoai = request.form.get('soDienThoai')
    username = request.form.get('username')
    password = request.form.get('password')
    dao.create_account_patient(hoTen=hoTen, ngaySinh=ngaySinh, diaChi=diaChi, email=email, gioiTinh=gioiTinh,
                               soDienThoai=soDienThoai, username=username, password=password)
    return redirect(url_for('show_login'))


@app.route("/view/about")
def view_about():
    return render_template('display.html')


@app.route("/support")
def support_patient():
    return render_template('support.html')


# update ds dang ky
@app.route('/api/delete/<maDangKy>', methods=['DELETE'])
def delete_record(maDangKy):
    dao.delete_appointment(maDangKy)
    return redirect(url_for('list_appointment'))


@app.route("/api/update/<maDangKy>")
def update_record(maDangKy):
    appointment = dao.get_info_appointment_by_id(maDangKy)
    return render_template('update_appointment.html', appointment=appointment)


@app.route("/api/update/complete", methods=['POST', 'GET'])
def save_appointment():
    maDangKy = request.form.get('maDangKy')
    ngayHen = request.form.get("ngayHen")
    dao.update_appointment(maDK=maDangKy, ngayHen=ngayHen)
    return redirect(url_for('list_appointment'))


@app.route("/api/send_mail", methods=['POST', 'GET'])
def send_mail():
    msg = Message('Hey', sender='truongndq3@gmail.com', recipients=['2151053032kiet@ou.edu.vn'])
    msg.body="skjnfsjfwnjefw"
    mail.send(msg)
    return redirect(url_for('/'))


if __name__ == "__main__":
    from PrivateClinic import admin

    app.run(debug=True)
