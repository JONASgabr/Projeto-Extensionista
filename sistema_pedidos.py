from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ZD3a33Z2@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Pedido
class Pedido(db.Model):
    __tablename__ = 'pedidos'  # Especifica o nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.Integer, nullable=False)
    produto = db.Column(db.String(50), nullable=False)  # Adicionando a coluna produto
    quantidade = db.Column(db.Integer, nullable=False)
    garcom = db.Column(db.Integer, nullable=False)

# Criar o banco de dados e as tabelas
with app.app_context():
    try:
        db.create_all()  # Tenta criar as tabelas
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mesa = request.form.get('mesa')
        produto = request.form.get('produto')
        quantidade = request.form.get('quantidade')
        garcom = request.form.get('garcom')

        # Validação dos campos
        if (mesa.isdigit() and 1 <= int(mesa) <= 12 and
            produto and quantidade.isdigit() and
            garcom.isdigit() and 1 <= int(garcom) <= 4):
            try:
                novo_pedido = Pedido(
                    mesa=int(mesa),
                    produto=produto,
                    quantidade=int(quantidade),
                    garcom=int(garcom)
                )
                db.session.add(novo_pedido)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()  # Rollback em caso de erro
                print(f"Erro ao adicionar pedido: {e}")

    pedidos = Pedido.query.all()
    return render_template('index.html', pedidos=pedidos)

@app.route('/encerrar/<int:pedido_id>', methods=['POST'])
def encerrar(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if pedido:
        db.session.delete(pedido)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
