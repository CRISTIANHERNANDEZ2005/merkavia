from flask import Flask
from extensions import db
from models import Pedido

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def add_puntos_usados_column():
    with app.app_context():
        try:
            # Add puntos_usados column to Pedido table
            db.session.execute('ALTER TABLE pedido ADD COLUMN puntos_usados INTEGER DEFAULT 0')
            db.session.commit()
            print("Column 'puntos_usados' added successfully to Pedido table")
        except Exception as e:
            print(f"Error adding column: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    add_puntos_usados_column()