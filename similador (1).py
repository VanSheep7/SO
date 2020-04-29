import multiprocessing
from multiprocessing import Process

Tempo=0
#Program_Counter=-1
PcbTabela=[]
Prontos=[]
Bloqueados=[]
RunningState=None
Terminados=[]
Memory=[]
Time_Quantum=20

#--------------- Instruction ----------------
class Instruction:
    def __init__(self,pro,ins,n,nome):
        self.pro=pro
        self.ins=ins
        self.n=n
        self.nome=nome
#-------------- Instruction -------------------

#------------- PCB ---------------------------
class PCB:
    def __init__(self,pid,pai,filho,start,pc,prioridade,estado,tamanho,inicio,fim,arrival):
        self.pid=pid
        self.pai=pai
        self.filho=filho
        self.start=start
        self.pc=pc
        self.prioridade=prioridade
        self.estado=estado
        self.tamanho=tamanho
        self.inicio=inicio
        self.fim=fim
        self.arrival=arrival
#------------- PCB ---------------------------

#--------------Alterar o PCB------------------
def alterar_Pcb(pcb):#OK
    for i in len(PcbTabela):
        a=PcbTabela[i]
        if(a.pid==pcb.pid):
            PcbTabela[i]=pcb
            break
#--------------Alterar o PCB------------------

#-------------------Validacao--------------------
def validacao(resultado):#OK
    if(resultado==1):
        RunningState=4
        RunningState.fim=Tempo
        alterar_Pcb(RunningState)
        RunningState=None
        Prontos.pop[0]
#-------------------Validacao--------------------
def prontos_correr():
    RunningState=Prontos.pop(0)
    RunningState.estado=3
    RunningState.inicio=Tempo
    alterar_Pcb(RunningState)
    instrucao=Memory[(RunningState.pc)]
    validacao(realizar_instrucao(instrucao))
#------------------------------ FCFS -------------------------------
def FCFS():
        if(RunningState==None):
            if(len(Prontos)==0):
                flag=fim()
                if(flag==0):
                    return 1
                if flag==2:
                    for i in len(Bloqueados):
                        a=Bloqueados[i]
                        if(a.pai==0):
                            a.estado=1
                            Prontos.append(a)
                            alterar_Pcb(a)
                            Bloqueados.pop(i)
                            break
                    prontos_correr()
                    return 0
            else:
                prontos_correr()
                return 0
        else:
            instrucao=Memory[(RunningState.pc)]
            validacao(realizar_instrucao(instrucao))
            return 0
#------------------------------ FCFS -------------------------------

#------------------Running.Tamanho------------------------------
def running_tamanho():#OK
    RunningState.tamanho=RunningState.tamanho-1
    if(RunningState.tamanho!=0):
        RunningState.pc=RunningState.pc+1
        alterar_Pcb(RunningState)
        Tempo=Tempo+1
        return 0
    alterar_Pcb(RunningState)
    Tempo=Tempo+1
    return 1
#------------------Running.Tamanho------------------------------

#--------------------Realizar as instruçoes------------------------
def realizar_instrucao(instrucao):
    if((instrucao.ins)=='M'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1 
    elif((instrucao.ins)=='A'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1
    elif((instrucao.ins)=='S'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1
    elif((instrucao.ins)=='C'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        inst=Memory[RunningState.pc +1]
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome)) 
        aux=RunningState
        #----------------------------------
        tam=preencher_memoria(ints.nome,len(PcbTabela)+1)
        comeco=len(Memory)
        a=PCB(len(PcbTabela)+1,RunningState.pid,0,comeco,comeco,RunningState.prioridade,2,tam,-1,-1,-1)
        aux.filho=a.pid
        alterar_Pcb(aux)
        PcbTabela.append(a)
        Bloqueados.append(a)
        processo = Process(target=processos_concorrentes, args=(a.pid,))
        processo.start()
        processo.join()
        #----------------------------------
        RunningState=aux
        RunningState.tamanho=RunningState.tamanho-2
        RunningState.pc=RunningState.pc+2
        alterar_Pcb(RunningState)
        if((Tempo%Time_Quantum)!=0):
            return 0 
        else:
            if(RunningState.tamanho !=0):
                return 0
            return 1  
    else:
        #---------------------------------
        if(RunningState.filho !=0):
            aux=RunningState
            processo = Process(target=processos_concorrentes, args=(aux.filho,))
            processo.start()
            processo.join()
            RunningState=aux
        #---------------------------------
        if((Tempo%Time_Quantum)==0):
            return 0  #return especial
        RunningState.tamanho=RunningState.tamanho-1
        RunningState.estado=4
        alterar_Pcb(RunningState)
        Terminados.append(RunningState.pid)
        Tempo=Tempo+1 
        return 1
        ## Ver melhor esta parte
#--------------------Realizar as instruçoes------------------------

#-------------------Colocar os processos para fila dos Bloqueados-----------
def colocar_bloquedos(aux1,aux2):#OK -->VER SE È NECESSARIO
    for i in PcbTabela:
        if(i.pid==aux1 or i.pid==aux2):
            i.estado=2
            alterar_Pcb(i)
            Bloqueados.append(i)
#-------------------Colocar os processos para fila dos Bloqueados-----------

#----------------Processos concorrentes-------------------------------
def processos_concorrentes(pid):#OK
    for i in Bloqueados:
        if(i.pid==pid):
            RunningState=i
            RunningState.estado=3
            alterar_Pcb(RunningState)
    while(True):
        if((Tempo%Time_Quantum)==0):# caso o Tempo corresponde ao Time_Quantum
            RunningState.estado=2
            alterar_Pcb(RunningState)
            Bloqueados.append(RunningState)
            break
        else:
            instrucao=Memory[(RunningState.pc)]
            resultado=realizar_instrucao(instrucao)
            if(validacao(realizar_instrucao(instrucao))==1):
                break
#----------------Processos concorrentes-------------------------------

#---------------Colocar o processo na fila Prontos ---------
def verificar_arrival():#OK
    for i in PcbTabela:
        if(i.estado==0 and i.pai==0):
            if(i.arrival==Tempo):
                i.estado=1
                alterar_Pcb(i)
                Prontos.append(i)
#---------------Colocar o processo na fila Prontos ---------

#-------------- O processo ja executaram ------------
def fim():#OK
    flag=0
    for i in PcbTabela:
        if(i.tamanho!=0 and i.pai==0):
            flag=1
            break
    if flag==1:
        if(len(Bloqueados)!=0):
            for i in Bloqueados:
                if(i.pai==0):
                    return 2 #existe nos bloquedo
            return 1 # nenhum processo chegou
    else:
        return 0 # já nao existe mais nada para correr
#-------------- O processo ja executaram ------------

#---------------- Pode dar jeito ------------------
def numeros_de_linhas(nome):#OK                        
    file=open(nome,"r")
    cont=0
    conteudo=file.read()
    conteudolista=conteudo.split("\n")
    for i in conteudolista:
        if i:
            cont += 1
            print(i)
    return cont
#---------------- Pode dar jeito ------------------

#------------ Funçao para ler o ficheiro plan.txt-----------
def read_file_plan(nome):#OK
    file=open(nome,"r")
    lines=file.readlines()
    fila=[]
    for i in lines:
        a=i.strip()
        b=a.split(",")
        fila.append(b)
    return fila
#------------ Funçao para ler o ficheiro plan.txt-----------

#----------- Preencher a memoria------------------
def preencher_memoria(nome,index):#OK
    file=open(nome,"r")
    lines=file.readlines()
    for i in lines:
        a=i.strip()
        b=a.split(" ")
        if b[0]=='L':
            c=Instruction(index,b[0],0,b[1])
        elif b[0]=='T':
            c=Instruction(index,b[0],0,None)
        else:
            c=Instruction(index,b[0],b[1],None)
        Memory.append(c)
    return (len(lines))
#----------- Preencher a memoria------------------

#.---------- Criar PcbTabela ---------------------
def criar_PcbTabela(nome):#OK
    fila=read_file_plan(nome)
    aux=0
    for i in range(len(fila)):
        array=fila[i]
        string=array[0]+".txt"
        tam=preencher_memoria(string,i+1)
        a=PCB(i+1,0,0,aux,aux,array[2],0,tam,-1,-1,array[1])
        PcbTabela.append(a)
        aux=tam
    return fila
    #.---------- Criar PcbTabela ---------------------
#.---------- Criar PcbTabela ---------------------

def main():
    control=read_file_plan('/home/zezinho/Desktop/SO/control.txt')
    plan=criar_PcbTabela('/home/zezinho/Desktop/SO/plan.txt')

    print("Simulador--->FCFS--->1")
    val = input("Qual a opção: ")

    if(val==1):
        while(true):
            cont=control.pop(0)
            if(cont=="E"):
                while((Tempo%Time_Quantum)==0):
                    verificar_arrival()
                    if((final=FCFS())==1):
                        break
            elif(cont=="I"):
                if(RunningState != None):
                    RunningState.estado=2
                    alterar_Pcb(RunningState)
                    Bloqueados.append(RunningState)
                    RunningState=None
            elif(cont=="D"):# Tenho de ver este if
                for i in len(Bloqueados):
                        a=Bloqueados[i]
                        if(a.pai==0):
                            a.estado=1
                            Prontos.append(a)
                            alterar_Pcb(a)
                            Bloqueados.pop(i)
                            break
            elif(cont=="R"):
                print("Tempo-> %d" % Tempo)
                if(RunningState != None):
                    print("Execução-> %d" % RunningState.pid)
                print("Execução-> None")
                for i in Bloqueados:
                    if(i.pai==0)
                        print("Bloqueado-> %d" % i.pid)
                for i in Prontos:
                        print("Prontos a executar-> %d" % i.pid)
                for i in Terminados:
                    if(i.pai==0):
                        print("Terminados-> %d" % i.pid)
            else:
                while(True):
                    verificar_arrival()
                    if((final=FCFS())==1):
                        break
