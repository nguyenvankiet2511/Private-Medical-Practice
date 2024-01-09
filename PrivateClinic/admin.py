from PrivateClinic import app, db, admin, dao
from PrivateClinic.models import Nguoi, NhanVien, Thuoc, YTa, TaiKhoan, DanhMuc, QuyDinh, UserRole, BacSi
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import redirect, request, url_for
from flask_login import logout_user, current_user


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


#
#
# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated

class StatsView(BaseView):
    @expose("/", methods=['GET', 'POST'])
    def index(self):
        rel = request.form.get('rel')
        if rel:
            year = int(rel.split('-')[0])
            month = int(rel.split('-')[1])
        else:
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month
        result = dao.tong_doanh_thu_theo_thang(year=year)
        tan_suat_kham = dao.tan_suat_kham(year=year)
        quy = dao.doanh_thu_theo_quy(year=year)
        ten_thuoc_list, so_luong_list = dao.get_usage_by_month_and_year(selected_month=month, selected_year=year)
        return self.render('admin/stats.html', tan_suat_kham=tan_suat_kham, result=result, quy=quy,
                           thuoc=ten_thuoc_list,
                           sl=so_luong_list, year=year, month=month)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect(url_for('show_login'))


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/home.html')


class EmployeeView(AuthenticatedModelView):
    column_list = ['id', 'bangCap']
    column_labels = {
        'id': 'Mã nhân viên',
        'bangCap': 'Bằng cấp'
    }


class NurseView(AuthenticatedModelView):
    column_list = ['id', 'bangCap']
    column_labels = {
        'id': 'Mã y tá',
        'bangCap': 'Bằng cấp'
    }


class PeopleView(AuthenticatedModelView):
    pass


class DoctorView(AuthenticatedModelView):
    column_list = ['id', 'chungChi', 'chuyenKhoa']
    column_labels = {
        'id': 'Mã bác sĩ',
        'chungChi': 'Chứng chỉ',
        'chuyenKhoa': 'Chuyên khoa'
    }


class AccountView(AuthenticatedModelView):
    column_labels = {
        'ten': 'Tên',
        'trangThai': 'Trạng thái hoạt động',
        'user_role': 'Loại tài khoản'
    }


class RegulationView(AuthenticatedModelView):
    column_labels = {
        'tenQD': 'Tên quy định',
        'giaTri': 'Giá trị quy định'
    }


class MedicineView(AuthenticatedModelView):
    column_list = ['tenThuoc', 'moTa', 'gia', 'trangThai', 'don_vi_thuoc_id', 'danh_muc_id']
    column_labels = {
        'tenThuoc': 'Tên Thuốc',
        'moTa': 'Mô Tả',
        'gia': 'Giá',
        'trangThai': 'Trạng Thái',
        'don_vi_thuoc_id': 'Đơn Vị Thuốc',
        'danh_muc_id': 'Danh Mục'
    }

    column_descriptions = {
        'tenThuoc': 'Tên của thuốc',
        'moTa': 'Mô tả về thuốc',
        'gia': 'Giá của thuốc',
        'trangThai': 'Trạng thái của thuốc',
        'don_vi_thuoc_id': 'Tên thuốc',
        'danh_muc_id': 'Danh mục thuốc'
    }

    column_filters = ['tenThuoc', 'danh_muc_id']
    column_searchable_list = ['tenThuoc', 'moTa']
    can_export = True
    can_view_details = True

    def trangThai_formatter(view, context, model, name):
        return 'Hoạt động' if model.trangThai else 'Ngừng hoạt động'

    def danhMucFormatter(view, context, model, name):
        return model.danh_muc.tenDanhMuc if model.danh_muc else 'N/A'

    def donViThuocFormatter(view, context, model, name):
        return model.don_vi_thuoc.tenDonVi if model.don_vi_thuoc else 'N/A'

    column_formatters = {
        'trangThai': trangThai_formatter,
        'danh_muc_id': danhMucFormatter,
        'don_vi_thuoc_id': donViThuocFormatter,
    }


class CategoryView(AuthenticatedModelView):
    column_list = ['id', 'tenDanhMuc', 'thuoc']
    column_labels = {
        'id': 'Mã danh mục',
        'tenDanhMuc': 'Tên danh mục',
        'thuoc': 'Thuốc'
    }


admin.add_view(PeopleView(Nguoi, db.session, name='Thông tin'))
admin.add_view(EmployeeView(NhanVien, db.session, name='Nhân viên'))
admin.add_view(DoctorView(BacSi, db.session, name='Bác sĩ'))
admin.add_view(NurseView(YTa, db.session, name='Y tá'))
admin.add_view(CategoryView(DanhMuc, db.session, name='Danh mục thuốc'))
admin.add_view(MedicineView(Thuoc, db.session, name='Thuốc'))
admin.add_view(RegulationView(QuyDinh, db.session, name='Quy định'))
admin.add_view(AccountView(TaiKhoan, db.session, name='Tài khoản'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
