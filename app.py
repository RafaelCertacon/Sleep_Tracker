from flask import Flask, request, jsonify
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restx import Api, Resource, fields, reqparse
from infra.db_connection import session, SleepTracker

app = Flask(__name__)
api = Api(app,
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

@ns.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.doc(responses={
        200: 'Login realizado com sucesso',
        401: 'Erro de autenticação'
    })
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "12345":
            return {"message": "Acesso com sucesso!"}, 200
        if username != "admin" and password != "<PASSWORD>":
            return {"message": "Erro ao digitar username ou senha!"}, 401
        return {"message": "Erro ao fazer o login"}, 401

@ns.route('/dormir')
class Dormir(Resource):
    @api.doc(responses={200: 'Registro criado com sucesso'})
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dia_dormir', type=str, location=['form', 'args'])
        parser.add_argument('dia_acordar', type=str, location=['form', 'args'])
        parser.add_argument('hora_dormir', type=str, location=['form', 'args'])
        parser.add_argument('hora_acordar', type=str, location=['form', 'args'])

        args = parser.parse_args()
        dados = {
            'dia_dormir': args['dia_dormir'],
            'dia_acordar': args['dia_acordar'],
            'hora_dormir': args['hora_dormir'],
            'hora_acordar': args['hora_acordar']
        }

        sleep = SleepTracker(**dados)
        session.add(sleep)
        session.commit()
        return sleep.serialize()

@ns.route('/resultados')
class Resultados(Resource):
    @api.doc(responses={200: 'Lista de registros recuperada com sucesso'})
    def get(self):
        all_resultados = session.query(SleepTracker).all()
        return [resultado.serialize() for resultado in all_resultados]

@ns.route('/apagar_tempo/<int:id>')
class ApagarTempo(Resource):
    @api.doc(params={'id': 'ID do registro a ser deletado'},
             responses={200: 'Registro deletado com sucesso'})
    def delete(self, id):
        delete_linha = session.query(SleepTracker).get(id)
        session.delete(delete_linha)
        session.commit()
        return {
            'mensagem': 'Registro deletado com sucesso',
            'id_deletado': id
        }, 200
