from pprintpp import pprint as pp
from db.database import Graph


class PersonDAO(object):
    def __init__(self):
        self.db = Graph(uri='bolt://35.172.234.92:7687',
                        user='neo4j', password='machinery-yell-bangs')

    def read_by_father(self, nome):
        return self.db.execute_query('MATCH (n:Pai {nome:$nome}) -- (f:Filho) RETURN f',
                                     {'nome': nome})

    def read_by_engineer(self):
        return self.db.execute_query('MATCH (n:Engenheiro) RETURN n')

    def read_by_boyfriend(self, nome):
        return self.db.execute_query('MATCH (f:Filho {nome:$nome}) <-[n:NAMORADO_DE]- (c:Cunhado) RETURN n, c',
                                     {'nome': nome})


def divider():
    print('\n' + '-' * 80 + '\n')


dao = PersonDAO()

pp('Quem da família é Engenheiro?')
engineer = dao.read_by_engineer()
if len(engineer) == 0:
    pp('Não possui nenhum engenheiro na familia, ainda')
else:
    pp(engineer)

divider()

pp('Fulano de tal é pai de quem?')
pai = input('Digite o nome do pai:')
sons = dao.read_by_father(pai)
if len(sons) == 0:
    pp('Este pai não possui filhos')
else:
    pp(sons)

divider()

pp('Sicrana de tal namora com quem desde quando?')
girl = input('Digite o nome da sicrana:')
boy = dao.read_by_boyfriend(girl)
if len(boy) == 0:
    pp('Não possui nenhum namorado')
else:
    pp(boy)

divider()

dao.db.close()
