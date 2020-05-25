from models import Pessoas,Atividades

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



if __name__ == '__main__':
   insere_pessoa()
   consulta_pessoa()


