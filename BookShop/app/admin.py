from app import app, db, dao
from flask_admin import Admin
from app.models import Sach, TheLoai, NhaXuatBan, TacGia
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship


admin =Admin (app=app, name="Bookshop Administrator", template_mode='bootstrap4')

class SachView(ModelView):
    column_list = ('id', 'name', 'price', 'image', 'miniid', 'sach_info','quanti' , 'nxb_id')
    can_export = True
    column_filters = ['price', 'name']
    can_view_details = True


admin.add_view(SachView(Sach, db.session))
admin.add_view(ModelView(TheLoai, db.session))
admin.add_view(ModelView(NhaXuatBan, db.session))
admin.add_view(ModelView(TacGia, db.session))