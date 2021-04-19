import csv
from copy import copy, deepcopy

class Risco:
    def __init__(self, chave, pai = None):
        self.chave = chave
        self.pai = pai

class Propriedade():
    def __init__(self, chave, valores_propriedade, pai = None):
        self.chave = chave
        self.valores_propriedade = {}
        for i in valores_propriedade:
            self.valores_propriedade[i] = None
        self.pai = pai


def mostrar_arvore(no):
    print(no.chave)
    if type(no) == Propriedade:
        for attrib in no.valores_propriedade.items():
            print(f'Atributo {attrib[0]} - {attrib[1].chave}')
            if type(attrib[1]) == Propriedade:
                mostrar_arvore(attrib[1])
                print(f'Retornando à {no.chave}')
    elif type(no) == Risco:
        pass
    


def induzir_arvore(tabela, propriedades):
    
    riscos = []
    
    for i in tabela:
        if not i['Risco'] in riscos:
            riscos.append(i['Risco'])
            #print(i['Risco'])

    
    if len(riscos) == 1: # mesma classe
        print(f'*****Retornar o nó folha {riscos[0]}*****')
        risco = Risco(riscos[0])
        return risco

    elif len(propriedades) == 0:
        print("*****Retornar o nó folha co alguma coisa*****") # Sem propriedades
        return False
    else:
        propriedades_temp = copy(propriedades)
        propriedade = propriedades_temp.pop(0) # Copiar valor exclído para a propriedade

        #print(f'removendo {propriedade} das propriedades')
        valores_propriedade = []
        for i in tabela:
            if not i[propriedade] in valores_propriedade:
                valores_propriedade.append(i[propriedade])

        propriedade_classe = Propriedade(propriedade, copy(valores_propriedade))

        #print(propriedades_temp)
        for valor in valores_propriedade:
            nova_tabela = []
    
            for linha in tabela:
                if linha[propriedade] == valor:
                    nova_tabela.append(copy(linha))
            drop_coluna = deepcopy(nova_tabela) 
        
            for linha in drop_coluna:
                linha.pop(propriedade, None)
            #----tmp----
            #for linha in drop_coluna:
            #    print(linha)
            no = induzir_arvore(copy(drop_coluna), copy(propriedades_temp))

            propriedade_classe.valores_propriedade[valor] = no
            #---tmp---
            #print('-'*20)
            #print(f'Propriedade {propriedade_classe.chave}')
            #print(propriedade_classe.valores_propriedade)
            #print('Atributos:')
            #for value in propriedade_classe.valores_propriedade.items():
            #    if value[1] !=  None:
            #        print(f'{value[0]} - {value[1].chave}')
            #    else:
            #        print(f'{value[0]} - {value[1]}')
            no.pai = propriedade_classe
            #print('-'*20)
        return propriedade_classe


def gerar_propriedades(tabela):
    propriedades = []

    propriedades = copy(list(tabela[0].keys()))
    propriedades.remove('Risco')
    return propriedades    
    
if __name__=='__main__':
    with open('Risco.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
    
        tabela = []
        for i in csv_reader:
            tabela.append(i)

        propriedades = copy(gerar_propriedades(tabela))

        arv = induzir_arvore(copy(tabela), copy(propriedades))
        print(arv) 

        mostrar_arvore(arv)
        