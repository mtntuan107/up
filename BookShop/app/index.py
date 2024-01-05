import math
import utils
from flask import render_template, request, redirect, session, jsonify, url_for
import dao
from app import app, login
from app.admin import *
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user


@app.route('/')
def index():
    kw = request.args.get('kw')
    theloai_id = request.args.get('theloai_id')
    page = request.args.get("page")


    theloai = dao.load_theloai()
    sach = dao.load_sach(kw=kw, theloai_id = theloai_id, page=page)

    total = dao.count_sach()

    return render_template('index.html',theloai=theloai,
                           sach=sach,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))


@app.route('/sach/<id>')
def details(id):
    sach_profile = dao.load_sachprofile(id)
    theloai_profile = dao.load_theloaiprofile(id)
    tacgia_profile = dao.load_tacgiaprofile(id)
    nxb_profile = dao.load_nxbrpofile(id)
    return render_template('details.html', sach_profile=sach_profile,theloai_profile=theloai_profile,
                           tacgia_profile=tacgia_profile,nxb_profile=nxb_profile)

@app.route('/api/cart', methods=['post'])
def add_cart():
    """
        {
        "cart": {
                "1": {
                    "id": 1,
                    "name": "ABC",
                    "price": 12,
                    "quantity": 2
                }, "2": {
                    "id": 2,
                    "name": "ABC",
                    "price": 12,
                    "quantity": 2
                }
            }
        }
        :return:
        """
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart:  # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<sach_id>", methods=['put'])
def update_cart(sach_id):
    cart = session.get('cart')
    if cart and sach_id in cart:
        quantity = request.json.get('quantity')
        cart[sach_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<sach_id>", methods=['delete'])
def delete_cart(sach_id):
    cart = session.get('cart')
    if cart and sach_id in cart:
        del cart[sach_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/info')
def info():
    info_user = dao.load_info(user_id=current_user.id)

    return render_template('info.html', info_user=info_user)


@app.context_processor
def common_resp():
    return {
        'theloai': dao.load_theloai(),
        'cart': utils.count_cart(session.get('cart'))
    }


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        location = request.form.get('location')
        phonenum = request.form.get('phonenum')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_tk(username=username, password=password, avatar=avatar_path)
                tk_id = utils.get_id_from_username(username)
                utils.tk_link_kh(tk_id=tk_id, name=name, location=location, phonenum=phonenum, email=email)
                return redirect(url_for('index'))
            else:
                err_msg = "Password not valid"
        except Exception as ex:
            err_msg = "System is having error" + str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route('/signin',methods=['get','post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        tk = utils.check_login(username=username, password=password)
        if tk:
            login_user(user=tk)
            return redirect(url_for('index'))
        else:
            err_msg = 'Username or password is wrong'
    return render_template('login.html', err_msg=err_msg)

@login.user_loader
def tk_load(tk_id):
    return utils.get_tk_by_id(tk_id=tk_id)

@app.route('/logoutTk')
def logoutTk():
    logout_user()
    return redirect(url_for('signin'))

if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
