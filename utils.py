from models import Pessoas,Atividades,Usuarios

def insere_pessoa():
    pessoa=Pessoas(nome='MIguel',idade=1)
    print(pessoa)
    pessoa.save()

def consulta_pessoa():
    pessoa=Pessoas.query.all()
    print(pessoa)
    pessoa=Pessoas.query.filter_by(nome='Thiago')
    for p in pessoa:
        print(p)

def deleta_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Thiago').first()
    pessoa.delete()

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Thiago').first()
    pessoa.save()

def insere_usuarios(login,senha):
    usuario=Usuarios(login=login,senha=senha)
    usuario.save()

def consulta_todos_usuarios():
    usuarios=Usuarios.query.all()
    print(usuarios)


if __name__ == '__main__':
   #insere_usuarios("thiago","456")
    consulta_todos_usuarios()
   #insere_pessoa()
   #consulta_pessoa()


