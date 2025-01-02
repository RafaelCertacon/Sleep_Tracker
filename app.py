from flask import Flask, request, jsonify
import werkzeug
import jwt
from authentication.authenticate import token_required

werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restx import Api, Resource, fields, reqparse
from infra.db_connection import session, SleepTracker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e56c7ee3ac3f3e4c4bfd9be6'
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Digite: Bearer seu_token_aqui"
    }
}

api = Api(app,
    authorizations=authorizations,
    security='Bearer',
    title='Sleep Tracker API',
    version='1.0',
    description='Uma API desenvolvida em Python utilizando Flask para ajudar usuários a monitorar e gerenciar seus hábitos de sono de forma simples e eficiente.',
    doc='/swagger'
)

ns = api.namespace('api', description='Operações do Sleep Tracker')

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha')
})

post_dormir = api.model('Metodo POST para dormir', {
    'dia_dormir': fields.String(required=True, description='Dia em que estou indo dormir'),
    'dia_acordar': fields.String(required=True, description='Dia em que eu vou acordar'),
    'hora_dormir': fields.String(required=True, description='Hora em que eu vou dormir'),
    'hora_acordar': fields.String(required=True, description='Hora em que eu vou acordar'),
})

@ns.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username == "admin" and password == "12345":
            token = jwt.encode(
                {'username': username, 'password': '12345'},
                app.config['SECRET_KEY'],
                algorithm="HS256"  # Mudando para HS256
            )
            return {'token': token}, 200
        return {'message': 'Credenciais inválidas'}, 401

@ns.route('/dormir')
class Dormir(Resource):
    def post(self):
        dados = request.get_json()
        sleep = SleepTracker(**dados)
        session.add(sleep)
        session.commit()
        return sleep.serialize()

@ns.route('/resultados')
class Resultados(Resource):
    @api.doc(authorizations=authorizations, responses={200: 'Lista de registros recuperada com sucesso'})
    def get(self):
        all_resultados = session.query(SleepTracker).all()
        return [resultado.serialize() for resultado in all_resultados]

@ns.route('/apagar_tempo/<int:id>')
class ApagarTempo(Resource):
    @api.doc(authorizations=authorizations, params={'id': 'ID do registro a ser deletado'},
             responses={200: 'Registro deletado com sucesso'})
    def delete(self, id):
        delete_linha = session.query(SleepTracker).get(id)
        session.delete(delete_linha)
        session.commit()
        return {
            'mensagem': 'Registro deletado com sucesso',
            'id_deletado': id
        }, 200
