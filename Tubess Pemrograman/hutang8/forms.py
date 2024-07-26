from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField
from wtforms.validators import DataRequired

class HutangForm(FlaskForm):
    kode = StringField('Kode', validators=[DataRequired()])
    nama = StringField('Nama', validators=[DataRequired()])
    harga = FloatField('Harga', validators=[DataRequired()])
    barang = StringField('Barang', validators=[DataRequired()])
    tanggal = DateField('Tanggal', validators=[DataRequired()])
