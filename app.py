from flask import Flask, request, jsonify, send_from_directory
import werkzeug
import jwt
import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restx import Api, Resource, fields
from infra.db_connection import session, SleepTracker
from authentication.authenticate import token_required
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

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

diretorio = r'C:\PROJETOS\SleepTracker_API-main\Arquivos_Salvos'

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
    @api.expect(post_dormir)
    @token_required
    def post(self):
        dados = request.get_json()
        sleep = SleepTracker(**dados)
        session.add(sleep)
        session.commit()
        return sleep.serialize()

@ns.route('/resultados')
class Resultados(Resource):
    @api.doc(authorizations=authorizations, responses={200: 'Lista de registros recuperada com sucesso'})
    @token_required
    def get(self):
        all_resultados = session.query(SleepTracker).all()
        return [resultado.serialize() for resultado in all_resultados]

@ns.route('/apagar_tempo/<int:id>')
class ApagarTempo(Resource):
    @api.doc(authorizations=authorizations, params={'id': 'ID do registro a ser deletado'},
             responses={200: 'Registro deletado com sucesso'})
    @token_required
    def delete(self, id):
        delete_linha = session.query(SleepTracker).get(id)
        session.delete(delete_linha)
        session.commit()
        return {
            'mensagem': 'Registro deletado com sucesso',
            'id_deletado': id
        }, 200


@ns.route('/arquivos')
class Arquivos(Resource):
    @token_required
    def get(self):
        arquivos = []

        for arquivo in os.listdir(diretorio):
            endereco_arquivo = os.path.join(diretorio, arquivo)

            if os.path.isfile(endereco_arquivo):
                arquivos.append(arquivo)

        return arquivos, 200

@ns.route('/arquivos/<arquivo>')
class NomeArquivo(Resource):
    @token_required
    def get(self, arquivo):
        return send_from_directory(diretorio, arquivo, as_attachment=True)


@ns.route('/upload_arquivo')
@api.expect(upload_parser)
class UploadArquivo(Resource):
    @token_required
    def post(self):

      arquivo = request.files.get('file')
      print(arquivo)

      nome_arquivo = arquivo.filename
      arquivo.save(os.path.join(diretorio, nome_arquivo))

      return "Deu certo", 200

