from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Hutang
from forms import HutangForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'rizal' and password == '1234':
        session['username'] = username
        return redirect(url_for('list_hutang'))
    else:
        flash('Username atau password salah. Silahkan coba lagi.')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    flash('Anda berhasil logout.')
    return redirect(url_for('index'))


@app.route('/list_hutang', methods=['GET', 'POST'])
def list_hutang():
    if 'username' not in session:
        flash('Anda harus login terlebih dahulu.')
        return redirect(url_for('index'))
    
    search_term = request.args.get('search', '')
    hutang2 = Hutang.query.filter(Hutang.kode.contains(search_term)).all()
    return render_template('list_hutang.html', hutang2=hutang2)

@app.route('/add', methods=['GET', 'POST'])
def add_hutang():
    form = HutangForm()
    if form.validate_on_submit():
        total_hutang = db.session.query(db.func.sum(Hutang.harga)).filter_by(nama=form.nama.data).scalar() or 0
        if total_hutang + form.harga.data > 500000:
            flash('Hutang Anda sudah mencapai batas 500,000!')
            return render_template('add_hutang.html', form=form)

        if Hutang.query.filter_by(kode=form.kode.data).first():
            flash('Kode sudah ada. Silahkan gunakan kode lain.')
            return render_template('add_hutang.html', form=form)
        
        new_hutang = Hutang(
            kode=form.kode.data,
            nama=form.nama.data,
            harga=form.harga.data,
            barang=form.barang.data,
            tanggal=form.tanggal.data,
        )
        db.session.add(new_hutang)
        db.session.commit()
        flash('Hutang berhasil ditambahkan!')
        return redirect(url_for('list_hutang'))
    return render_template('add_hutang.html', form=form)

@app.route('/edit/<kode>', methods=['GET', 'POST'])
def edit_hutang(kode):
    hutang = Hutang.query.filter_by(kode=kode).first_or_404()
    form = HutangForm(obj=hutang)
    
    if form.validate_on_submit():
        total_hutang = db.session.query(db.func.sum(Hutang.harga)).filter(Hutang.nama == form.nama.data).scalar() or 0
        total_hutang -= hutang.harga
        
        if total_hutang + form.harga.data > 500000:
            flash('Hutang Anda sudah mencapai batas 500,000!')
            return render_template('edit_hutang.html', form=form, kode=kode)
        
        hutang.nama = form.nama.data
        hutang.harga = form.harga.data
        hutang.barang = form.barang.data
        hutang.tanggal = form.tanggal.data
        
        db.session.commit()
        flash('Hutang berhasil diperbarui!')
        return redirect(url_for('list_hutang'))
    
    return render_template('edit_hutang.html', form=form, kode=kode)

@app.route('/delete/<kode>', methods=['POST'])
def delete_hutang(kode):
    try:
        hutang = Hutang.query.filter_by(kode=kode).first_or_404()
        db.session.delete(hutang)
        db.session.commit()
        return jsonify(message='Hutang berhasil dihapus!') # type: ignore
    except Exception as e:
        return jsonify(message='Terjadi kesalahan saat menghapus hutang'), 500 # type: ignore
    
@app.route('/peringkat_hutang', methods=['GET'])
def peringkat_hutang():
    hutang_sorted = Hutang.query.order_by(Hutang.harga.desc()).all()
    return render_template('peringkat_hutang.html', hutang_sorted=hutang_sorted)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
