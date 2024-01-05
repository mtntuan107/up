from app.models import TheLoai, Sach, TacGia, NhaXuatBan, Sach_TheLoai, Sach_TacGia,KhachHang
from app import app
import hashlib

def load_theloai():
    return TheLoai.query.all()

def load_sach(kw=None, theloai_id=None, page=None):
    sach = Sach.query
    theloai = TheLoai.query
    ma = Sach_TheLoai.query


    if kw:
        sach = sach.filter(Sach.name.contains(kw))

    if theloai_id:
        sach = sach.filter(Sach.sach_theloai.any(TL_id=theloai_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return sach.offset(start).limit(page_size).all()

    return sach.all()

def count_sach():
    return Sach.query.count()


def load_sachprofile(id):
    sach = Sach.query
    theloai = TheLoai.query
    sach_profile = sach.filter(Sach.id == id)

    return sach_profile.all()

def load_theloaiprofile(id):
    theloai = TheLoai.query
    ma = Sach_TheLoai.query
    sach = Sach.query
    theloai_profile = theloai.filter(TheLoai.sach_theloai.any(Sach_TheLoai.S_id == id))

    return theloai_profile.all()


def load_tacgiaprofile(id):
    tacgia = TacGia.query
    matg = Sach_TacGia.query
    sach = Sach.query
    tacgia_profile = tacgia.filter(TacGia.sach_tacgia.any(Sach_TacGia.S_id == id))

    return tacgia_profile.all()


def load_nxbrpofile(id):
    nxb = NhaXuatBan.query
    sach = Sach.query

    sach_nxb = nxb.filter(NhaXuatBan.id == Sach.nxb_id)
    nxb_profile = sach_nxb.filter(Sach.id == id)

    return nxb_profile.all()


def load_info(user_id):
    info_user = KhachHang.query

    info_user = info_user.filter(KhachHang.tk_id == user_id)

    return info_user.all()


