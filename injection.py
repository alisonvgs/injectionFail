import random
import math
import time
import os
import numpy
from threading import Thread
from datetime import datetime

# arquivo de armazenamento do log de falhas e reparos realizados para comparar com o monitoramento do ambiente
nome_arq = 'fail_repair_log.csv'
arq = open(nome_arq, 'a+')
arq.write('Reparo;'+datetime.now().strftime('%d/%m/%Y %H:%M:%S')+';''\n')
arq.close()

# inicializacao de variavel. Tempos de down (quando falha) e up (quando e reparado)
time_down = 0
time_up = 0

# configuracao de cada bloco do modelo (bloco,mttf,mttr)
blocks = [('host1',4.1523,0.0025),('host2',12.5903,0.007685)]

# Calculo do TTF (Time To Fail), ou seja, quanto tempo o link ira falhar.
def ttf(timetofail):
    ft = numpy.random.exponential(timetofail)
    # converte em segundos
    time_down = (ft * 360)
    return time_down

# Calculo do TTR (Time To Repair), ou seja, quanto tempo o link ira voltar a ter conectividade.
def ttr(timetorepair):
    ft = numpy.random.exponential(timetorepair)
    # converte em segundos
    time_up = (ft * 360)
    return time_up

def connectionDown(a, time_down):
    # Corta a conexao de rede.
    os.system('echo ifconfig cloudbr0 down')
    arq = open(nome_arq, 'a+')
    arq.write('Falha;'+datetime.now().strftime('%d/%m/%Y %H:%M:%S')+';'+str(a)+';'+str(time_down)+'\n')
    arq.close()

# A interface de rede deve estar com IP fixo.
def connectionUp(a, time_up):
    # Corta repara a conexao de rede.
    os.system('echo ifconfig cloudbr0 up')
    arq = open(nome_arq, 'a+')
    arq.write('Reparo;'+datetime.now().strftime('%d/%m/%Y %H:%M:%S')+';'+str(a)+';'+str(time_up)+'\n')
    arq.close()

# executa a falha ou reparo em funcao do parametro do block com tempos exponencialmente distribuidos
def control(a,b,c):
    ttf_total_block = 0
    ttr_total_block = 0
    while True:
        # Fail	
        time_down = ttf(b)
        ttf_total_block = ttf_total_block + time_down
        time.sleep(time_down)
        print(str(ttf_total_block)+"  TTF Total "+str(a))
        connectionDown(a, time_down)

        # Repair
        time_up = ttr(c)
        ttr_total_block = ttr_total_block + time_up
        time.sleep(time_up)
        print(str(ttr_total_block)+"  TTR Total "+str(a))
        connectionUp(a, time_up)
 

def main():
    # Tempos acumulados para o calculo de disponbilidade
    try:
        print('Inicio: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        t0 = Thread(target=control, args=(blocks[0]))
        t0.start()
        t1 = Thread(target=control, args=(blocks[1]))
        t1.start()
    except KeyboardInterrupt as e:
        print ('Fim: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        

if __name__ == '__main__':
    main()
