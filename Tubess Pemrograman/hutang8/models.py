from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hutang(db.Model):
    __tablename__ = 'utang'
    kode = db.Column(db.String(50), primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)
    barang = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)

    def __init__(self,  kode, nama, harga, barang, tanggal):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.barang = barang
        self.tanggal = tanggal
