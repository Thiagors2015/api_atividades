from flask import Flask,request
from flask_restful import Resource,Api
from models import Pessoas,Atividades,Usuarios
from flask_httpauth import HTTPBasicAuth

auth=HTTPBasicAuth()
app=Flask(__name__)
api=Api(app)

#USUARIOS={
#    'rafael':'123',
 #   'thiago':'321'
#}

#@auth.verify_password
#def verificacao(login,senha):
#    if not (login,senha):
#        return False
#    return USUARIOS.get(login)==senha

@auth.verify_password
def verificacao(login,senha):
    if not (login,senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()



class Pessoa(Resource):
    @auth.login_required
    def get(self,nome):
        try:
            pessoa=Pessoas.query.filter_by(nome=nome).first()

            response={'nome':pessoa.nome,
                      'idade':pessoa.id,
                      'id':pessoa.id
                      }
        except AttributeError:
            response={'status':'erro','mensagem':'Pessoa {} não encontrada'.format(nome)}
        except Exception:
            response={'status':'erro','mensagem':'erro desconhecido'}
        return response
    def put(self,nome):
        try:
            pessoa=Pessoas.query.filter_by(nome=nome).first()
            dados=request.json
            if 'idade'in dados:
                pessoa.idade=dados['idade']
            if 'nome' in dados:
                pessoa.nome=dados['nome']
            pessoa.save()
            response={'nome':pessoa.nome,
                      'idade':pessoa.idade,
                      'id':pessoa.id}
        except AttributeError:
            response = {'status': 'erro', 'mensagem': 'Pessoa {} não encontrada'.format(nome)}
        except Exception:
            response={'status':'erro','mensagem':'erro desconhecido'}
        return response

    def delete(self,nome):
        try:
            pessoa=Pessoas.query.filter_by(nome=nome).first()
            dados=request.json
            pessoa.delete()
            response={'status':'sucesso','mensagem':'Pessoa {} excluida com sucesso'}
        except AttributeError:
            response = {'status': 'erro', 'mensagem': 'Pessoa {} não encontrada'.format(nome)}
        except Exception:
            response={'status':'erro','mensagem':'erro desconhecido'}
        return response

class ListaPessoas(Resource):
    def get(self):
        pessoa=Pessoas.query.all()
        response=[{'id':i.id,'nome':i.nome,'idade':i.idade} for i in pessoa]
        return response
    def post(self):
        try:
            dados = request.json
            pessoa=Pessoas(nome=dados['nome'],idade=dados['idade'])
            pessoa.save()
            response={
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        except Exception:
             response = {'status': 'erro', 'mensagem': 'erro desconhecido'}
        return response

class Atividade(Resource):
    def delete(self,nome):
        try:
            atividades=Atividades.query.filter_by(nome=nome).first()
            atividades.delete()
            response={'status':'sucesso','mensagem':'atividade {} excluída com sucesso'.format(nome)}
        except AttributeError:
            response = {'status': 'erro','mensagem':'Pessoa {} não foi encontrada ou não possuí atividades'.format(nome)}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido'}
        return response

    def get(self,nome):
        try:
            pessoa=Pessoas.query.filter_by(nome=nome).first()
            atividade=Atividades.query.filter_by(pessoa_id=pessoa.id).first()
            response=[{'id':i.id,
                       'nome':i.nome,
                       'pessoa':i.pessoa.nome} for i in atividade]
        except AttributeError:
            response={'status':'erro','mensagem':'Pessoa {} não foi encontrada ou não possuí atividades'.format(nome)}
        except Exception:
            response={'status':'erro','mensagem':'erro desconhecido'}
        return response


class ListaAtividades(Resource):
    def post(self):
        try:
            dados=request.json
            pessoa=Pessoas.query.filter_by(nome=dados['pessoa']).first()
            atividade=Atividades(nome=dados['nome'],pessoa=pessoa)
            atividade.save()
            response={
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'id':atividade.id
            }
        except AttributeError:
            response={'status':'erro','mensagem':'Pessoa informada {} não foi encontrada'.format(dados['nome'])}
        except Exception:
            response={'status':'erro','mensagem':'Erro deconhecido'}
        return response

class AlterarSituacao(Resource):
    def put(self,id):
        try:
            dados=request.json
            atividade=Atividades.query.filter_by(id=id).first()
            if 'status' in dados:
                if dados['status'] in ['Pendente','Concluida']:
                    if atividade.status==dados['status']:
                        response={'status':'erro','mensagem':'Situação informada {} é igual a situação da atividade'.format(dados['status'])}
                    else:
                        atividade.status=dados['status']

                        response={'status':'sucesso','mensagem':'Situação alterada com sucesso'}
                else:

                    response = {'status': 'erro',
                                'mensagem': 'Situação informada {} tem que ser Pendente ou Concluida'.format(
                                    dados['status'])}
        except AttributeError:
            response = {'status': 'erro',
                        'mensagem':'Atividade informada não foi encontrada'}
        except Exception:
            response = {'status': 'erro',
                        'mensagem':'Erro desconhecido'}



api.add_resource(Pessoa,'/pessoa/<string:nome>/')
api.add_resource(ListaPessoas,'/pessoas/')
api.add_resource(ListaAtividades,'/atividades/')
api.add_resource(Atividade,'/atividades/<string:nome>/')
api.add_resource(AlterarSituacao,'/atividades/<int:id>/')


if __name__ == '__main__':
    app.run(debug=True)