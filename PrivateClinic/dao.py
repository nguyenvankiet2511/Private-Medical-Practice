import hashlib
from PrivateClinic import app, db
from datetime import datetime
from sqlalchemy import func, extract
from PrivateClinic.models import TaiKhoan, Thuoc, DonViThuoc, DanhMuc, PhieuThuoc, PhieuKham, \
    DanhSachDangKy, Nguoi, DanhSachKham, ChiTietDanhSach, HoaDon, QuyDinh, UserRole, BenhNhan, BacSi


# xac thuc tai khoan
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()), TaiKhoan.password.__eq__(password)).first()


# tạo phieu kham
def create_medical_form(maBN, ngayKham, chuanDoan, trieuChung, l_maThuoc, l_soLuong, l_cachDung):
    # Tạo một phiếu khám cho bệnh nhân
    pk = PhieuKham(ngayKham=ngayKham, chuanDoan=chuanDoan, trieuChung=trieuChung, benh_nhan_id=maBN)
    db.session.add(pk)
    # Tạo các phiếu thuốc cho mỗi thuốc được kê đơn
    for i in range(len(l_maThuoc)):
        thuoc_id = l_maThuoc[i]
        soLuong = l_soLuong[i]
        cachDung = l_cachDung[i]
        phieu_thuoc = PhieuThuoc(thuoc_id=thuoc_id, soLuong=soLuong, cachDung=cachDung, phieu_kham=pk)
        db.session.add(phieu_thuoc)
    db.session.commit()


# tao lich hen
def create_appointment(ngay_hen, ma_BN):
    appoint = DanhSachDangKy(ngayHen=ngay_hen, benh_nhan_id=ma_BN)
    db.session.add(appoint)
    db.session.commit()


def create_appointment_new(hoTen, gioiTinh, ngaySinh, diaChi, soDienThoai, email, ngayHen):
    if gioiTinh == 'Nam':
        temp = True
    else:
        temp = False
    nguoi = Nguoi(hoTen=hoTen, gioiTinh=temp, ngaySinh=ngaySinh, diaChi=diaChi, soDienThoai=soDienThoai,
                  email=email)
    benh_nhan = BenhNhan(Nguoi=nguoi)
    db.session.add(nguoi)
    db.session.add(benh_nhan)
    appoint = DanhSachDangKy(ngayHen=ngayHen, benh_nhan=benh_nhan)
    db.session.add(appoint)
    db.session.commit()


# tao ds kham
def create_list_appointment(ngay_kham, l_maBN, l_maDS, bac_si):
    ds_kham = DanhSachKham(ngayKham=ngay_kham)
    db.session.add(ds_kham)
    for i in range(len(l_maBN)):
        ma_bn = l_maBN[i]
        ct_ds = ChiTietDanhSach(danh_sach_kham=ds_kham, benhNhan_id=ma_bn, bacSi_id=bac_si)
        db.session.add(ct_ds)
        ds_delete = DanhSachDangKy.query.get(l_maDS[i])
        db.session.delete(ds_delete)
    db.session.commit()


# tao hoa don
def create_invoice(ngayKham, tienThuoc, tienKham, maPK):
    hoa_don = HoaDon(ngayKham=ngayKham, tienThuoc=tienThuoc, tienKham=tienKham, phieu_kham_id=maPK)
    db.session.add(hoa_don)
    db.session.commit()


# tao tai khoan benh nhan
def create_account_patient(hoTen, gioiTinh, ngaySinh, diaChi, soDienThoai, email, username, password):
    if gioiTinh == 'Nam':
        temp = True
    else:
        temp = False
    nguoi = Nguoi(hoTen=hoTen, gioiTinh=temp, ngaySinh=ngaySinh, diaChi=diaChi, soDienThoai=soDienThoai,
                  email=email)
    benh_nhan = BenhNhan(Nguoi=nguoi)
    db.session.add(nguoi)
    db.session.add(benh_nhan)
    tai_khoan = TaiKhoan(ten=hoTen, username=username,
                         password=str(hashlib.md5(password.encode('utf-8')).hexdigest()), trangThai=True,
                         Nguoi=nguoi)
    db.session.add(tai_khoan)
    db.session.commit()


# danh sach thuoc
def get_list_medicine():
    medicine = Thuoc.query
    medicine = medicine.filter(Thuoc.trangThai == True)
    return medicine.all()


# tra cuu danh sách thuốc
def get_medicine(keyword, cate_id, page=1):
    medicine = Thuoc.query
    if keyword:
        medicine = medicine.filter(Thuoc.tenThuoc.contains(keyword))
    if cate_id:
        medicine = medicine.filter(Thuoc.danh_muc_id.__eq__(cate_id))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return medicine.slice(start, end).all()


# danh mục
def get_category():
    return DanhMuc.query.all()


# thông tin lịch sử khám
def get_history_medical_all():
    query = db.session.query(Nguoi.id, Nguoi.hoTen, PhieuKham.ngayKham, PhieuKham.trieuChung, PhieuKham.chuanDoan).join(
        PhieuKham, Nguoi.id == PhieuKham.benh_nhan_id)
    return query.all()


# thông tin phieu kham
def get_history_medical(id):
    return PhieuKham.query.filter(PhieuKham.benh_nhan_id == id).all()


# danh sach dang ky
def get_list_appointment():
    return db.session.query(Nguoi.id, Nguoi.hoTen, Nguoi.diaChi, Nguoi.gioiTinh, Nguoi.ngaySinh,
                            DanhSachDangKy.ngayHen, DanhSachDangKy.id.label('id_ds')).join(
        Nguoi, Nguoi.id.__eq__(DanhSachDangKy.benh_nhan_id)).all()


# ds hoa don
def get_invoice_by_id(id_pk):
    return HoaDon.query.filter(HoaDon.phieu_kham_id.__eq__(id_pk)).all()


# chi tiet thông tin pk
def get_medical_report(id_pk):
    return db.session.query(PhieuKham.id, Nguoi.hoTen, PhieuKham.ngayKham, PhieuKham.benh_nhan_id).join(Nguoi,
                                                                                                        PhieuKham.benh_nhan_id == Nguoi.id).filter(
        PhieuKham.id == id_pk).first()


# tinh tien thuoc
def get_receipt(id):
    result = get_medicine_report(id)
    tienThuoc = 0
    for gia, so_luong, ten_thuoc, cach_dung in result:
        tienThuoc += gia * so_luong
    return tienThuoc


# giatri qd
def get_examination_fee():
    return QuyDinh.query.filter_by(id=1).first()


# lấy thông tin phieu thuoc
def get_medicine_report(id_pk):
    return db.session.query(Thuoc.gia, PhieuThuoc.soLuong, Thuoc.tenThuoc, PhieuThuoc.cachDung).join(PhieuThuoc,
                                                                                                     Thuoc.id.__eq__(
                                                                                                         PhieuThuoc.id)).filter(
        PhieuThuoc.phieu_kham_id.__eq__(id_pk)).all()


# thong tin bênh nhan
def get_patient_by_id(id):
    return db.session.query(BenhNhan.id, Nguoi.hoTen).join(Nguoi).filter(BenhNhan.id == id).first()


# lây thong tin by id
def get_info(id):
    return Nguoi.query.filter(Nguoi.id == id).first()


# lay thông tin BS
def get_info_doctor():
    return db.session.query(Nguoi.hoTen, BacSi.id).join(Nguoi, BacSi.id == Nguoi.id).all()


# update thong tin
def upadate_info(id, hoTen, diaChi, soDienThoai, ngaySinh, email):
    info = get_info(id)
    info.hoTen = hoTen
    info.diaChi = diaChi
    info.soDienThoai = soDienThoai
    info.ngaySinh = ngaySinh
    info.email = email
    db.session.commit()


# update ds dk
def update_list_appointment(id):
    result = ChiTietDanhSach.query.filter(ChiTietDanhSach.benhNhan_id == id).first()
    result.is_active = False
    db.session.commit()


# lây doang thu theo từng thang
def get_monthly_revenue():
    monthly_totals = (
        db.session.query(
            func.DATE_FORMAT(HoaDon.ngayKham, '%Y-%m').label('month'),
            func.sum(HoaDon.tienKham + HoaDon.tienThuoc).label('total')
        )
        .group_by('month')
        .all()
    )
    return monthly_totals


# tần suất sd thuoc
def get_usage_by_month_and_year(selected_month, selected_year):
    # Đếm số lần sử dụng thuốc trong tháng và năm theo PhieuKham và lấy tên thuốc
    frequency_of_usage = (
        db.session.query(Thuoc.tenThuoc, func.sum(PhieuThuoc.soLuong))
        .join(PhieuThuoc)
        .join(PhieuThuoc.phieu_kham)
        .filter(
            func.extract('month', PhieuKham.ngayKham) == selected_month,
            func.extract('year', PhieuKham.ngayKham) == selected_year
        )
        .group_by(Thuoc.tenThuoc)
        .all()
    )
    ten_thuoc_list = [ten_thuoc for ten_thuoc, _ in frequency_of_usage]
    so_luong_list = [so_luong for _, so_luong in frequency_of_usage]
    return ten_thuoc_list, so_luong_list


def tong_doanh_thu_theo_thang(year):
    result = []
    # Tính tổng doanh thu bằng cách sử dụng func.sum và func.coalesce để gán 0 nếu kết quả là None
    for month in range(1, 13):
        query = (
            db.session.query(
                func.coalesce(func.sum(HoaDon.tienKham + HoaDon.tienThuoc), 0).label('tong_doanh_thu')
            )
            .filter(extract('year', HoaDon.ngayKham) == year, extract('month', HoaDon.ngayKham) == month)
            .group_by(func.extract('month', HoaDon.ngayKham))
            .order_by(func.extract('month', HoaDon.ngayKham))
            .first()
        )
        result.append(query.tong_doanh_thu if query else 0)
    return result


# daonh thu theo quy
def doanh_thu_theo_quy(year):
    result = []
    for quarter in range(1, 5):
        query = (
            db.session.query(
                func.coalesce(func.sum(HoaDon.tienKham + HoaDon.tienThuoc), 0).label('tong_doanh_thu')
            )
            .filter(extract('year', HoaDon.ngayKham) == year, extract('quarter', HoaDon.ngayKham) == quarter)
            .first()
        )
        result.append(query.tong_doanh_thu if query else 0)
    return result


# tần suất khám theo thang
def get_examination_frequency():
    result = (
        db.session.query(
            func.count(PhieuKham.id).label('so_luong_kham'),
            func.extract('month', PhieuKham.ngayKham).label('thang_kham')
        )
        .filter(func.extract('year', PhieuKham.ngayKham) == 2024)
        .group_by('thang_kham')
        .order_by('thang_kham')
        .all()
    )
    return result


# tần suất khám theo tháng
def tan_suat_kham(year):
    value = []
    for month in range(1, 13):
        result = (
            db.session.query(
                func.count(PhieuKham.id).label('so_luong_kham')
            )
            .filter(func.extract('year', PhieuKham.ngayKham) == year,
                    func.extract('month', PhieuKham.ngayKham) == month)
            .group_by(func.extract('month', PhieuKham.ngayKham))
            .order_by(func.extract('month', PhieuKham.ngayKham))
            .first()
        )
        value.append(result.so_luong_kham if result else 0)
    return value


def get_role(role):
    if role == UserRole.NURSE:
        return 'Y tá'
    elif role == UserRole.PATIENT:
        return 'Bệnh nhân'
    elif role == UserRole.DOCTOR:
        return 'Bác sĩ'
    elif role == UserRole.EMPLOYEE:
        return 'Nhân viên thu ngân'


def get_name_patient(id):
    return db.session.query(Nguoi.hoTen).filter_by(id)


def get_list_medical_examination(bacSi_id):
    results = db.session.query(DanhSachKham.id, ChiTietDanhSach.benhNhan_id, ChiTietDanhSach.is_active,
                               DanhSachKham.ngayKham,
                               Nguoi.hoTen.label('TenBacSi')) \
        .join(ChiTietDanhSach, DanhSachKham.id == ChiTietDanhSach.danhSachKham_id) \
        .join(BacSi, ChiTietDanhSach.bacSi_id == BacSi.id) \
        .join(Nguoi, BacSi.id == Nguoi.id).all()
    return results


def get_list_appoint_active():
    result = (
        db.session.query(
            Nguoi.id,
            Nguoi.hoTen,
            DanhSachDangKy.ngayDK,
            DanhSachDangKy.ngayHen,
            DanhSachDangKy.id.label('maDangKy')
        )
        .join(DanhSachDangKy, DanhSachDangKy.benh_nhan_id == Nguoi.id)
        .all()
    )
    return result


def delete_appointment(maDK):
    res = DanhSachDangKy.query.filter(DanhSachDangKy.id == maDK).first()
    db.session.delete(res)
    db.session.commit()


def get_info_appointment_by_id(maDK):
    result = (
        db.session.query(
            Nguoi.id,
            Nguoi.hoTen,
            DanhSachDangKy.ngayDK,
            DanhSachDangKy.ngayHen,
            DanhSachDangKy.id.label('maDangKy')
        )
        .join(DanhSachDangKy, DanhSachDangKy.benh_nhan_id == Nguoi.id)
        .filter(DanhSachDangKy.id == maDK)
        .first()
    )
    return result


def get_list_invoice():
    result = db.session.query(HoaDon.tienKham, Nguoi.hoTen, HoaDon.tienThuoc, HoaDon.ngayKham, PhieuKham.benh_nhan_id,
                              HoaDon.id, HoaDon.phieu_kham_id).join(PhieuKham, PhieuKham.id == HoaDon.phieu_kham_id).join(Nguoi,
                                                                                                    Nguoi.id == PhieuKham.benh_nhan_id).all()
    return result


def update_appointment(maDK, ngayHen):
    res = DanhSachDangKy.query.filter(DanhSachDangKy.id == maDK).first()
    res.ngayHen = ngayHen
    db.session.commit()


def count_medicine():
    return Thuoc.query.count()
