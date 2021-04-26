import os
import platform
import csv

from copy import copy
from math import log


class Resultado():
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


def limpar_janela():
    #Detectar o sistema operacional
    op_sys = platform.system()
    if op_sys == "Linux":
        os.system("clear")
    elif op_sys == "Windows":
        os.system("cls")


def mostrar_arvore(no):
    print(f'{no.chave}')
    if type(no) == Propriedade:
        for attrib in no.valores_propriedade.items():
            print(f'Atributo {attrib[0]} - {attrib[1].chave}')
            if type(attrib[1]) == Propriedade:
                mostrar_arvore(attrib[1])
                print(f'Retornando à {no.chave}')
    #elif type(no) == Resultado:
    #    pass


def entropia(tabela, propriedades):
    #                       ENTROPIA TABELA

    # Buscar todos os valores possíveis no resultado da tabela e suas respectivas frequẽncias
    resultados_frequencia = {}
    for linha_id in tabela:
        count = 0
        if not linha_id[base_resultado] in resultados_frequencia:
            for linha in tabela:
                if linha[base_resultado] == linha_id[base_resultado]:
                    count +=1
            resultados_frequencia[linha_id[base_resultado]] = count
    #print(resultados_frequencia)

    
    # Razão entre a frequencia do resultado pela qtde total na da tabela
    razao_frequencia = {}
    for frequencia in resultados_frequencia.items():
        razao_frequencia[f'p_{frequencia[0]}'] = frequencia[1]/len(tabela)
    #print(razao_frequencia)
    

    e_tabela = 0
    for frequencia in razao_frequencia.values():
        e_tabela -= frequencia * log(frequencia, 2)
    #print(e_tabela)
    

    #                       ENTROPIA ATRIBUTOS
    # Buscar todas as propriedade atual da tabela.
    propriedades_frequencia = {}
    for propriedade in propriedades:
        valores_frequencia = {}
        # Buscar todos os valores possíveis na propriedade atual da tabela.
        for linha_id in tabela: 
            count = 0
            if not linha_id[propriedade] in valores_frequencia:
                for linha in tabela:
                    if linha[propriedade] == linha_id[propriedade]:
                        count +=1
                valores_frequencia[linha_id[propriedade]] = count
        propriedades_frequencia[propriedade] = valores_frequencia
    
    #for linha in propriedades_frequencia.items():
    #    print(f'{linha[0]} - {linha[1]}')

    
    propriedades_freq_resultado = {}
    for propriedade in propriedades_frequencia.items():
        #print(propriedade)
        
        # Extrair uma nova tabela apenas com valores específio de uma determinada propriedade
        valores_frequencia = {}
        for valor in propriedade[1].keys():
            nova_tabela = []
            for linha in tabela:
                if linha[propriedade[0]] == valor:
                    nova_tabela.append(copy(linha))
            #print(valor)
        #print(valores_frequencia)

            resultados_freq = {}
            # Buscar todos os valores possíveis no resultado da tabela e suas respectivas frequẽncias da tabela extraída.
            for valor_resultado in resultados_frequencia.keys():
                for linha_id in nova_tabela: # Cada atribut
                    count = 0
                    if not linha_id[base_resultado] in resultados_freq:
                        for linha in nova_tabela: # Quantidade de cada propriedade
                            if linha[base_resultado] == linha_id[base_resultado]:
                                count +=1
                        resultados_freq[linha_id[base_resultado]] = count
                valores_frequencia[valor] = resultados_freq       
        propriedades_freq_resultado[propriedade[0]] = valores_frequencia

    #for linha in propriedades_freq_resultado.items():
    #    print(f'{linha[0]} - {linha[1]}')

    # Calcular entropia para cada valor da propriedade
    e_valores = {}
    for propriedade in propriedades_freq_resultado.items():
        #print(propriedade)
        entropia_valor = {}
        for valor in propriedade[1].items():
            #print(valor)
            entropia_calculo = 0
            for freq_resultado in valor[1].values():
                #print(freq_resultado)
                #print(sum(valor[1].values()))
                entropia_calculo -= freq_resultado/sum(valor[1].values()) * log(freq_resultado/sum(valor[1].values()), 2)
            entropia_valor[valor[0]] = entropia_calculo
            #print(entropia_valor)
        e_valores[propriedade[0]] = entropia_valor
    
    #for linha in e_valores.items():
    #    print(f' {linha[0]} - {linha[1]}')

    # Calcular entropia para cada propriedade
    e_propriedades = {}
    for propriedade in e_valores.items():
        entropia_calculo = 0
        for valor in propriedade[1].items():
            for propriedade_p in propriedades_frequencia.items():
                if propriedade[0] == propriedade_p[0]:
                    for valor_p in propriedade_p[1].items():
                        if valor[0] == valor_p[0]:
                            entropia_calculo += valor[1] * valor_p[1]/sum(propriedade_p[1].values())
        e_propriedades[propriedade[0]] = entropia_calculo
    
    #for linha in e_propriedades.items():
    #    print(f' {linha[0]} - {linha[1]}')

    for entropia in e_propriedades.items():
        if entropia[1] == min(e_propriedades.values()):
            #print(entropia[0])
            return entropia[0]


def induzir_arvore(tabela, propriedades):
    resultados = []
    
    # Buscar todos os valores possíveis no resultado da tabela.
    for i in tabela: 
        if not i[base_resultado] in resultados:
            resultados.append(i[base_resultado])
            #print(i[base_resultado])

    # Mesmo resultado
    if len(resultados) == 1 and len(propriedades) > 0:
        #print(f'*****Retornar o nó folha {resultados[0]}*****')
        classe_resultado = Resultado(resultados[0])
        return classe_resultado

     # Sem propriedades
    elif len(propriedades) == 0:
        #print("*****Retornar o nó folha co alguma coisa*****")
        return False
    
    else:
        # Copiar valor excluído para a propriedade
        indice_propriedade = propriedades.index(entropia(copy(tabela), copy(propriedades)))
        propriedade = propriedades.pop(indice_propriedade)

        # Buscar todos os valores possíveis na propriedade da tabela.
        valores_propriedade = []
        for i in tabela:
            if not i[propriedade] in valores_propriedade:
                valores_propriedade.append(i[propriedade])

        classe_propriedade = Propriedade(propriedade, copy(valores_propriedade))

        # Atribuir valor (classe) para a cada chave (valor da propriedade)
        for valor in valores_propriedade:
            nova_tabela = []

            # Extrair uma nova tabela apenas com valores específio de uma determinada propriedade
            for linha in tabela:
                if linha[propriedade] == valor:
                    nova_tabela.append(copy(linha))

            # Remover da tabela extraída a propriedade atual
            for linha in nova_tabela:
                linha.pop(propriedade, None)
            #----tmp----
            #for linha in drop_coluna:
            #    print(linha)
            no = induzir_arvore(copy(nova_tabela), copy(propriedades))

            classe_propriedade.valores_propriedade[valor] = no
            #---tmp---
            #print('-'*20)
            #print(f'Propriedade {classe_propriedade.chave}')
            #print(classe_propriedade.valores_propriedade)
            #print('Atributos:')
            #for value in classe_propriedade.valores_propriedade.items():
            #    if value[1] !=  None:
            #        print(f'{value[0]} - {value[1].chave}')
            #    else:
            #        print(f'{value[0]} - {value[1]}')
            no.pai = classe_propriedade
            #print('-'*20)
        return classe_propriedade


def gerar_propriedades(tabela):
    propriedades = []

    propriedades = copy(list(tabela[0].keys()))
    propriedades.remove(base_resultado)
    return propriedades    
    

def consultar(tabela, propriedades):
    respostas = {}
    for propriedade in propriedades:
        valores_propriedade = {}
        op = 0
        for linha in tabela:
            if not linha[propriedade] in valores_propriedade.values():
                op +=1
                valores_propriedade[op] = linha[propriedade]
        print(f'{propriedade}: ')

        limpar_janela()
        for resposta in respostas.items():
            print(f'{resposta[0]}: {resposta[1]}') 

        print(propriedade)
        for opcao in valores_propriedade.items():
            print(f'opção {opcao[0]}: {opcao[1]}', end="      ")
        print()
        resposta = int(input(": "))
        respostas[propriedade] = valores_propriedade[resposta]
    return respostas


def buscar_arvore(respostas, no):
    if type(no) == Propriedade:
        propriedade = no.chave
        ponteiros = no.valores_propriedade

        for ponteiro in ponteiros.items():
            if respostas[propriedade] == ponteiro[0]:
                if type(ponteiro[1]) == Resultado:
                    return ponteiro[1].chave
                else:
                    resultado = buscar_arvore(copy(respostas), copy(ponteiro[1]))
                    return resultado
    else:
        return no.chave    


global base_resultado
base_resultado = 'Risco'


if __name__=='__main__':
    with open('Risco.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
    
        tabela = []
        for i in csv_reader:
            tabela.append(i)
        
        #for i in tabela:
        #    print(i)

        propriedades = copy(gerar_propriedades(tabela))
        #print(propriedades)
        
        arv = induzir_arvore(copy(tabela), copy(propriedades)) 
        #mostrar_arvore(arv)

        entropia_resultado = entropia(copy(tabela), copy(propriedades))
        #print(entropia_resultado)
        
        respostas = consultar(copy(tabela), copy(propriedades))
        #print(respostas)

        resultado = buscar_arvore(copy(respostas), copy(arv))
        limpar_janela()

        for resposta in respostas.items():
            print(f'{resposta[0]}: {resposta[1]}') 
        
        # Estilizar resultado
        estilo ='\033[1m'+'\033[47m'+'\033[41m'
        sem_estilo = '\033[0m'
        print(f'\n{estilo}{base_resultado.upper()} {resultado.upper()}{sem_estilo}\n')