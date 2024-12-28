from flask import Flask, jsonify, request
from infra.db_connection import session, SleepTracker

app = Flask("__name__")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "12345":
        return jsonify({"message": "Acesso com sucesso!"}),200
    if username != "admin" and password != "<PASSWORD>":
        return jsonify({"message": "Erro ao digitar username ou senha!"}),401
    else:
        return jsonify({"message": "Erro ao fazer o login"}),401
@app.route('/dormir', methods=['POST'])
def post_dormir():
    dados = request.get_json()
    # O operador ** em SleepTracker(**dados) é chamado de desempacotamento de dicionário.
    # Ele pega um dicionário e transforma suas chaves em argumentos nomeados para o construtor da classe.
    sleep = SleepTracker(**dados)
    session.add(sleep)
    session.commit()
    return sleep.serialize()

@app.route('/resultados', methods=['GET'])
def get_sleep():
    all_resultados = session.query(SleepTracker).all()
    return [resultado.serialize()
            for resultado in all_resultados]

@app.route('/apagar_tempo/<int:id>', methods=['DELETE'])
def delete_tempo(id):
    delete_linha = session.query(SleepTracker).get(id)
    session.delete(delete_linha)
    session.commit()
    return jsonify({
        'mensagem': 'Registro deletado com sucesso',
        'id_deletado': id
    }), 200
