from flask import Flask, render_template, request, redirect, session, flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
from dotenv import load_dotenv


app = Flask(__name__)
# ================= SECRET KEY =================
app.secret_key = os.getenv("SECRET_KEY", "ecommerce_flask")

# ================= KONEKSI DATABASE =================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cari = request.args.get('cari', '')
    kategori = request.args.get('kategori', '')
    rating = request.args.get('rating', '')

    # Query kategori
    cursor.execute("SELECT * FROM kategori")
    semua_kategori = cursor.fetchall()

    query = """
    SELECT 
        produk.*, 
        kategori.nama_kategori,
        AVG(review.rating) as rata_rating

    FROM produk

    LEFT JOIN kategori
    ON produk.id_kategori = kategori.id_kategori

    LEFT JOIN review
    ON produk.id_produk = review.id_produk

    WHERE 1=1
    """

    params = []

    # Search
    if cari:
        query += " AND nama_produk LIKE %s"
        params.append('%' + cari + '%')

    # Filter kategori
    if kategori:
        query += " AND produk.id_kategori = %s"
        params.append(kategori)

    query += " GROUP BY produk.id_produk "

    # filter rating
    if rating == 'tertinggi':

        query += " ORDER BY rata_rating DESC "

    elif rating == 'terendah':

        query += " ORDER BY rata_rating ASC "

    else:

        query += " ORDER BY produk.id_produk DESC "

    cursor.execute(query, params)

    produk = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'dashboard_user.html',
        produk=produk,
        kategori=semua_kategori
    )

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO users (nama, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (nama, email, password))

        db.commit()

        cursor.close()
        db.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            session['user_id'] = user['id_user']
            session['nama'] = user['nama']
            session['role'] = user['role']

            # jika admin
            if user['role'] == 'admin':
                return redirect('/admin/produk')

            # jika user biasa
            flash('Login berhasil', 'success')
            return redirect('/')

        return "Email atau password salah"

    return render_template('login.html')

@app.route('/admin/produk')
def admin_produk():

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Ambil produk
    query = """
    SELECT produk.*, kategori.nama_kategori
    FROM produk
    LEFT JOIN kategori
    ON produk.id_kategori = kategori.id_kategori
    ORDER BY id_produk DESC
    """

    cursor.execute(query)
    produk = cursor.fetchall()

    # Total produk
    cursor.execute("SELECT COUNT(*) as total_produk FROM produk")
    total_produk = cursor.fetchone()['total_produk']

    # Total user
    cursor.execute("""
    SELECT COUNT(*) as total_user
    FROM users
    WHERE role='user'
    """)
    total_user = cursor.fetchone()['total_user']

    # Total kategori
    cursor.execute("""
    SELECT COUNT(*) as total_kategori
    FROM kategori
    """)
    total_kategori = cursor.fetchone()['total_kategori']

    # Total keranjang
    cursor.execute("""
    SELECT COUNT(*) as total_keranjang
    FROM keranjang
    """)
    total_keranjang = cursor.fetchone()['total_keranjang']

    cursor.close()
    db.close()

    return render_template(
        'admin_produk.html',
        produk=produk,
        total_produk=total_produk,
        total_user=total_user,
        total_kategori=total_kategori,
        total_keranjang=total_keranjang
    )

@app.route('/admin/tambah_produk', methods=['GET', 'POST'])
def tambah_produk():

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    db = get_db()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM kategori")
    kategori = cursor.fetchall()

    if request.method == 'POST':

        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        deskripsi = request.form['deskripsi']
        id_kategori = request.form['id_kategori']

        foto = request.files['foto']

        nama_foto = ''

        if foto:
            nama_foto = secure_filename(foto.filename)

            foto.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    nama_foto
                )
            )

        query = """
        INSERT INTO produk
        (
            id_kategori,
            nama_produk,
            harga,
            stok,
            foto,
            deskripsi
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            id_kategori,
            nama,
            harga,
            stok,
            nama_foto,
            deskripsi
        )

        cursor.execute(query, values)

        db.commit()

        cursor.close()
        db.close()

        return redirect('/admin/produk')

    return render_template(
        'tambah_produk.html',
        kategori=kategori
    )

@app.route('/admin/edit_produk/<int:id>', methods=['GET', 'POST'])
def edit_produk(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil data produk
    query_produk = """
    SELECT * FROM produk
    WHERE id_produk=%s
    """

    cursor.execute(query_produk, (id,))
    produk = cursor.fetchone()

    # ambil kategori
    cursor.execute("SELECT * FROM kategori")
    kategori = cursor.fetchall()

    if request.method == 'POST':

        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        deskripsi = request.form['deskripsi']
        id_kategori = request.form['id_kategori']

        foto = request.files['foto']

        # jika upload foto baru
        if foto and foto.filename != '':

            nama_foto = secure_filename(foto.filename)

            foto.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    nama_foto
                )
            )

            query_update = """
            UPDATE produk
            SET
                id_kategori=%s,
                nama_produk=%s,
                harga=%s,
                stok=%s,
                foto=%s,
                deskripsi=%s
            WHERE id_produk=%s
            """

            values = (
                id_kategori,
                nama,
                harga,
                stok,
                nama_foto,
                deskripsi,
                id
            )

        else:

            query_update = """
            UPDATE produk
            SET
                id_kategori=%s,
                nama_produk=%s,
                harga=%s,
                stok=%s,
                deskripsi=%s
            WHERE id_produk=%s
            """

            values = (
                id_kategori,
                nama,
                harga,
                stok,
                deskripsi,
                id
            )

        cursor.execute(query_update, values)

        db.commit()

        cursor.close()
        db.close()

        return redirect('/admin/produk')

    return render_template(
        'edit_produk.html',
        produk=produk,
        kategori=kategori
    )

@app.route('/admin/hapus_produk/<int:id>')
def hapus_produk(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    db = get_db()

    db = get_db()
    cursor = db.cursor()

    query = "DELETE FROM produk WHERE id_produk=%s"

    cursor.execute(query, (id,))

    db.commit()

    # ambil review
    query_review = """
    SELECT review.*, users.nama
    FROM review
    LEFT JOIN users
    ON review.id_user = users.id_user
    WHERE review.id_produk=%s
    ORDER BY id_review DESC
    """

    cursor.execute(query_review, (id,))

    review = cursor.fetchall()

    # rata-rata rating
    query_rating = """
    SELECT AVG(rating) as rata_rating
    FROM review
    WHERE id_produk=%s
    """

    cursor.execute(query_rating, (id,))

    rating_data = cursor.fetchone()

    cursor.close()
    db.close()

    return redirect('/admin/produk')

@app.route('/detail_produk/<int:id>')
def detail_produk(id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil produk
    query = """
    SELECT produk.*, kategori.nama_kategori
    FROM produk
    LEFT JOIN kategori
    ON produk.id_kategori = kategori.id_kategori
    WHERE id_produk=%s
    """

    cursor.execute(query, (id,))

    produk = cursor.fetchone()

    # ambil review
    query_review = """
    SELECT review.*, users.nama
    FROM review
    LEFT JOIN users
    ON review.id_user = users.id_user
    WHERE review.id_produk=%s
    ORDER BY id_review DESC
    """

    cursor.execute(query_review, (id,))

    review = cursor.fetchall()

    # rata-rata rating
    query_rating = """
    SELECT AVG(rating) as rata_rating
    FROM review
    WHERE id_produk=%s
    """

    cursor.execute(query_rating, (id,))

    rating_data = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        'detail_produk.html',
        produk=produk,
        review=review,
        rating_data=rating_data
    )

@app.route('/tambah_keranjang/<int:id_produk>', methods=['POST'])
def tambah_keranjang(id_produk):

    if 'user_id' not in session:
        return redirect('/login')

    qty = int(request.form['qty'])

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil produk
    query_produk = """
    SELECT * FROM produk
    WHERE id_produk=%s
    """

    cursor.execute(query_produk, (id_produk,))

    produk = cursor.fetchone()

    # cek stok
    if qty > produk['stok']:

        cursor.close()
        db.close()

        return "Stok tidak cukup"

    # cek keranjang
    query_cek = """
    SELECT * FROM keranjang
    WHERE id_user=%s AND id_produk=%s
    """

    cursor.execute(
        query_cek,
        (session['user_id'], id_produk)
    )

    cek = cursor.fetchone()

    if cek:

        qty_baru = cek['qty'] + qty
        subtotal_baru = qty_baru * produk['harga']

        query_update = """
        UPDATE keranjang
        SET qty=%s, subtotal=%s
        WHERE id_keranjang=%s
        """

        cursor.execute(
            query_update,
            (
                qty_baru,
                subtotal_baru,
                cek['id_keranjang']
            )
        )

    else:

        subtotal = qty * produk['harga']

        query_insert = """
        INSERT INTO keranjang
        (
            id_user,
            id_produk,
            qty,
            subtotal
        )
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(
            query_insert,
            (
                session['user_id'],
                id_produk,
                qty,
                subtotal
            )
        )

    db.commit()

    cursor.close()
    db.close()

    flash('Produk berhasil ditambahkan ke keranjang', 'success')
    return redirect(f'/detail_produk/{id_produk}')

@app.route('/keranjang')
def keranjang():

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT keranjang.*, produk.*
    FROM keranjang
    LEFT JOIN produk
    ON keranjang.id_produk = produk.id_produk
    WHERE keranjang.id_user=%s
    """

    cursor.execute(query, (session['user_id'],))

    keranjang = cursor.fetchall()

    total = 0

    for item in keranjang:
        total += item['subtotal']

    cursor.close()
    db.close()

    return render_template(
        'keranjang.html',
        keranjang=keranjang,
        total=total
    )

@app.route('/hapus_keranjang/<int:id>')
def hapus_keranjang(id):

    db = get_db()
    cursor = db.cursor()

    query = """
    DELETE FROM keranjang
    WHERE id_keranjang=%s
    """

    cursor.execute(query, (id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect('/keranjang')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil data keranjang
    query = """
    SELECT keranjang.*, produk.*
    FROM keranjang
    LEFT JOIN produk
    ON keranjang.id_produk = produk.id_produk
    WHERE keranjang.id_user=%s
    """

    cursor.execute(query, (session['user_id'],))

    keranjang = cursor.fetchall()

    total = 0

    for item in keranjang:
        total += item['subtotal']

    # jika keranjang kosong
    if len(keranjang) == 0:
        cursor.close()
        db.close()
        return redirect('/keranjang')

    # proses checkout
    if request.method == 'POST':

        alamat = request.form['alamat']

        # simpan pesanan
        query_pesanan = """
        INSERT INTO pesanan
        (
            id_user,
            total_harga,
            alamat
        )
        VALUES (%s,%s,%s)
        """

        values_pesanan = (
            session['user_id'],
            total,
            alamat
        )

        cursor.execute(query_pesanan, values_pesanan)

        db.commit()

        id_pesanan = cursor.lastrowid

        # simpan detail pesanan
        for item in keranjang:

            query_detail = """
            INSERT INTO detail_pesanan
            (
                id_pesanan,
                id_produk,
                qty,
                harga,
                subtotal
            )
            VALUES (%s,%s,%s,%s,%s)
            """

            values_detail = (
                id_pesanan,
                item['id_produk'],
                item['qty'],
                item['harga'],
                item['subtotal']
            )

            cursor.execute(query_detail, values_detail)

            # kurangi stok
            query_stok = """
            UPDATE produk
            SET stok = stok - %s
            WHERE id_produk=%s
            """

            cursor.execute(
                query_stok,
                (
                    item['qty'],
                    item['id_produk']
                )
            )

        # hapus keranjang
        query_hapus = """
        DELETE FROM keranjang
        WHERE id_user=%s
        """

        cursor.execute(
            query_hapus,
            (session['user_id'],)
        )

        db.commit()

        cursor.close()
        db.close()

        flash('Checkout berhasil', 'success')
        return redirect('/pesanan')

    return render_template(
        'checkout.html',
        keranjang=keranjang,
        total=total
    )

@app.route('/pesanan')
def pesanan():

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT *
    FROM pesanan
    WHERE id_user=%s
    ORDER BY id_pesanan DESC
    """

    cursor.execute(
        query,
        (session['user_id'],)
    )

    pesanan = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'pesanan.html',
        pesanan=pesanan
    )

@app.route('/admin/pesanan')
def admin_pesanan():

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT pesanan.*, users.nama
    FROM pesanan
    LEFT JOIN users
    ON pesanan.id_user = users.id_user
    ORDER BY id_pesanan DESC
    """

    cursor.execute(query)

    pesanan = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'admin_pesanan.html',
        pesanan=pesanan
    )

@app.route('/admin/update_status/<int:id>', methods=['POST'])
def update_status(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/')

    status = request.form['status']

    db = get_db()
    cursor = db.cursor()

    query = """
    UPDATE pesanan
    SET status=%s
    WHERE id_pesanan=%s
    """

    cursor.execute(query, (status, id))

    db.commit()

    cursor.close()
    db.close()

    return redirect('/admin/pesanan')

@app.route('/detail_pesanan/<int:id>')
def detail_pesanan(id):

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil pesanan
    query_pesanan = """
    SELECT *
    FROM pesanan
    WHERE id_pesanan=%s
    """

    cursor.execute(query_pesanan, (id,))

    pesanan = cursor.fetchone()

    # ambil detail produk
    query_detail = """
    SELECT detail_pesanan.*, produk.nama_produk, produk.foto
    FROM detail_pesanan
    LEFT JOIN produk
    ON detail_pesanan.id_produk = produk.id_produk
    WHERE detail_pesanan.id_pesanan=%s
    """

    cursor.execute(query_detail, (id,))

    detail = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'detail_pesanan.html',
        pesanan=pesanan,
        detail=detail
    )

@app.route('/tambah_qty/<int:id>')
def tambah_qty(id):

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # ambil keranjang
    query = """
    SELECT keranjang.*, produk.harga, produk.stok
    FROM keranjang
    LEFT JOIN produk
    ON keranjang.id_produk = produk.id_produk
    WHERE id_keranjang=%s
    """

    cursor.execute(query, (id,))

    item = cursor.fetchone()

    # cek stok
    if item['qty'] < item['stok']:

        qty_baru = item['qty'] + 1
        subtotal_baru = qty_baru * item['harga']

        query_update = """
        UPDATE keranjang
        SET qty=%s, subtotal=%s
        WHERE id_keranjang=%s
        """

        cursor.execute(
            query_update,
            (
                qty_baru,
                subtotal_baru,
                id
            )
        )

        db.commit()

    cursor.close()
    db.close()

    return redirect('/keranjang')

@app.route('/kurang_qty/<int:id>')
def kurang_qty(id):

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT keranjang.*, produk.harga
    FROM keranjang
    LEFT JOIN produk
    ON keranjang.id_produk = produk.id_produk
    WHERE id_keranjang=%s
    """

    cursor.execute(query, (id,))

    item = cursor.fetchone()

    qty_baru = item['qty'] - 1

    # qty minimal 1
    if qty_baru < 1:

        cursor.close()
        db.close()

        return redirect('/keranjang')

    subtotal_baru = qty_baru * item['harga']

    query_update = """
    UPDATE keranjang
    SET qty=%s, subtotal=%s
    WHERE id_keranjang=%s
    """

    cursor.execute(
        query_update,
        (
            qty_baru,
            subtotal_baru,
            id
        )
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect('/keranjang')

@app.route('/tambah_review/<int:id_produk>', methods=['POST'])
def tambah_review(id_produk):

    if 'user_id' not in session:
        return redirect('/login')

    rating = request.form['rating']
    komentar = request.form['komentar']

    db = get_db()
    cursor = db.cursor()

    query = """
    INSERT INTO review
    (
        id_user,
        id_produk,
        rating,
        komentar
    )
    VALUES (%s,%s,%s,%s)
    """

    values = (
        session['user_id'],
        id_produk,
        rating,
        komentar
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return redirect(f'/detail_produk/{id_produk}')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)