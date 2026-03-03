from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

class ProductForm(FlaskForm):
    name = StringField('商品名称', validators=[DataRequired()])
    price = FloatField('价格(元)', validators=[DataRequired()])
    description = TextAreaField('描述', validators=[DataRequired()])
    image = FileField('商品图片')
    submit = SubmitField('发布')

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = ProductForm()
    if form.validate_on_submit():
        image = request.files['image']
        filename = image.filename
        image.save(os.path.join('static/uploads', filename))
        
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            image_filename=filename
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))