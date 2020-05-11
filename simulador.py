import os
import sys


#plan=criar_PcbTabela('/home/zezinho/Desktop/SO/plan.txt')
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
    def __init__(self,pid,pai,start,pc,prioridade,estado,tamanho,burst,inicio,fim,arrival):
        self.pid=pid
        self.pai=pai
        self.filho=[]
        self.start=start
        self.pc=pc
        self.prioridade=prioridade
        self.estado=estado
        self.tamanho=tamanho
        self.burst=burst
        self.inicio=inicio
        self.fim=fim
        self.arrival=arrival
#------------- PCB ---------------------------

#--------------Alterar o PCB------------------
def alterar_Pcb(pcb):#OK
    for i in range(len(PcbTabela)):
        a=PcbTabela[i]
        if(a.pid==pcb.pid):
            PcbTabela[i]=pcb
            break
#--------------Alterar o PCB------------------

#-------------------Validacao--------------------
def validacao(resultado):#OK
    global RunningState
    global Prontos
    if(resultado==1):
        print("validaçao")
        print(RunningState.pid)
        RunningState.estado=4
        RunningState.fim=Tempo
        alterar_Pcb(RunningState)
        RunningState=None
#-------------------Validacao--------------------
def prontos_correr():
    global RunningState
    global Memory
    RunningState=Prontos.pop(0)
    RunningState.estado=3
    RunningState.inicio=Tempo
    alterar_Pcb(RunningState)
    instrucao=Memory[(RunningState.pc)]
    validacao(realizar_instrucao(instrucao))
#------------------------------ FCFS -------------------------------
def FCFS():
        global RunningState
        global Bloqueados
        global Prontos
        if(RunningState==None):
            if(len(Prontos)==0):
                flag=fim()
                if(flag==0):
                    print("FCFS-->Final")
                    return 1
                if flag==2:
                    for i in range(len(Bloqueados)):
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
    global RunningState
    global Tempo
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
    global RunningState
    global Memory 
    global PcbTabela 
    global Bloqueados 
    global Terminados
    global Tempo                    #6
    if((instrucao.ins)=='M'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1                    #14
    elif((instrucao.ins)=='A'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1                    #20
    elif((instrucao.ins)=='S'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        if(running_tamanho()==0):
            return 0
        return 1            #26
    elif((instrucao.ins)=='C'):
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
        inst=Memory[(RunningState.pc) +1]
        print("Execução---> %d %c %d %s" % (inst.pro,inst.ins,inst.n,inst.nome)) 
        aux=RunningState
        #----------------------------------
        s="/home/zezinho/Desktop/SO/"+inst.nome+".txt"
        comeco=len(Memory)
        tam=preencher_memoria(s,len(PcbTabela)+1)
        a=PCB(len(PcbTabela)+1,RunningState.pid,comeco,comeco,RunningState.prioridade,2,tam,tam,-1,-1,-1)
        aux.filho.append(a.pid)
        alterar_Pcb(aux)
        PcbTabela.append(a)
        Bloqueados.append(a)
        ppid=os.fork()           #43
        if(ppid==0):
            processos_concorrentes(a.pid)
        else:
            os.waitpid(ppid,0)
            exit()
        #----------------------------------
        RunningState=aux
        RunningState.tamanho=RunningState.tamanho-2
        RunningState.pc=RunningState.pc+2
        alterar_Pcb(RunningState)           #54
        if((Tempo%Time_Quantum)!=0):
            return 0 
        else:
            if(RunningState.tamanho !=0):
                return 0
            return 1            #60
    else:
        #---------------------------------
        aux=RunningState
        if((len(RunningState.filho)) !=0):
            for i in range(len(RunningState.filho)):
                RunningState=aux
                for j in PcbTabela:
                    if(j.pid==RunningState.filho[i] and j.estado !=4):
                        pidd=os.fork()      #70
                        if(pidd==0):
                            processos_concorrentes(j.pid)
                        else:
                            os.waitpid(pidd,0)
                            exit()
                if((Tempo%Time_Quantum)==0):
                    break
        RunningState=aux
        #---------------------------------
        if((Tempo%Time_Quantum)==0):
            return 0  #return especial
        print("Execução---> %d %c %d %s" % (instrucao.pro,instrucao.ins,instrucao.n,instrucao.nome))
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
    global RunningState
    global Bloqueados
    global Memory
    global Tempo
    global Time_Quantum
    for i in Bloqueados:
        if(i.pid==pid and i.estado!=4):
            RunningState=i
            RunningState.estado=3
            alterar_Pcb(RunningState)
            break
    while(True):
        verificar_arrival()
        if((Tempo%Time_Quantum)==0):# caso o Tempo corresponde ao Time_Quantum
            RunningState.estado=2
            alterar_Pcb(RunningState)
            Bloqueados.append(RunningState)
            break
        else:
            instrucao=Memory[RunningState.pc]
            resultado=realizar_instrucao(instrucao)
            validacao(resultado)
            if(resultado==1):
                print("Final no processo_concorrentes")
                break
#----------------Processos concorrentes-------------------------------

#---------------Colocar o processo na fila Prontos ---------
def verificar_arrival():#OK
    global Tempo
    global PcbTabela
    global Prontos
    for i in PcbTabela:
        if(i.estado==0 and i.pai==0):
            if(i.arrival==Tempo):
                i.estado=1
                alterar_Pcb(i)
                Prontos.append(i)
#---------------Colocar o processo na fila Prontos ---------

#-------------- O processo ja executaram ------------
def fim():#OK
    global PcValuebTabela
    global Bloqueados
    global Tempo
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
        Tempo= Tempo + 1
        return 1
    else:
        print("fim")
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
    global Memory
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
            z=int(b[1])
            c=Instruction(index,b[0],z,None)
        Memory.append(c)
    return (len(lines))
#----------- Preencher a memoria------------------

#.---------- Criar PcbTabela ---------------------
def criar_PcbTabela(nome):#OK
    global PcbTabela
    fila=read_file_plan(nome)
    aux=0
    for i in range(len(fila)):
        array=fila[i]
        string=array[0]
        tam=preencher_memoria(string,i+1)
        z=int(array[2])
        zz=int(array[1])
        a=PCB(i+1,0,aux,aux,z,0,tam,tam,-1,-1,zz)
        PcbTabela.append(a)
        aux=tam+aux
    return fila
    #.---------- Criar PcbTabela ---------------------
#.---------- Criar PcbTabela ---------------------

def main():
    global Tempo
    global Time_Quantum
    global RunningState
    global Bloqueados
    global Prontos
    global Terminados
    control=read_file_plan('/home/zezinho/Desktop/SO/control.txt')
    plan=criar_PcbTabela('/home/zezinho/Desktop/SO/plan.txt')
    flag=0
    pode=0
    while(len(control)!=0):
        cont=control.pop(0)
        if(cont[0]=="E"):
            while((Tempo%Time_Quantum)!=0 or pode==0):
                pode=1
                print(Tempo)
                verificar_arrival()
                final=FCFS()
                if((final)==1):
                    flag=1
                    break
            pode=0
        elif(cont[0]=="I"):
            if(RunningState != None):
                RunningState.estado=2
                alterar_Pcb(RunningState)
                Bloqueados.append(RunningState)
                RunningState=None
        elif(cont[0]=="D"):
            for i in range(len(Bloqueados)):
                    a=Bloqueados[i]
                    if(a.pai==0):
                        a.estado=1
                        Prontos.append(a)
                        alterar_Pcb(a)
                        Bloqueados.pop(i)
                        break
        elif(cont[0]=="R"):
            print("Tempo-> %d" % Tempo)
            if(RunningState != None):
                print("Execução-> %d" % RunningState.pid)
            else:
                print("Execução-> None")
            for i in range(len(Bloqueados)):
                a=Bloqueados[i]
                if(a.pai==0):
                    print("Bloqueado-> %d" % a.pid)
            for i in range(len(Prontos)):
                a=Prontos[i]
                print("Prontos a executar-> %d" % a.pid)
            for i in range(len(Terminados)):
                    print("Terminados-> %d" % Terminados[i])
        else:
            while(True):
                print(Tempo)
                verificar_arrival()
                final=FCFS()
                if(final==1):
                    flag=1
                    break
    if(flag==0):
        while(True):
                verificar_arrival()
                final=FCFS()
                if(final==1):
                    flag=1
                    break
    listaf=[]
    for i in PcbTabela:
        listai=[]
        if(i.pai==0):
            tat=i.fim-i.arrival
            wt=tat-i.burst
            rt=i.inicio-i.arrival
            listai.append(tat)
            listai.append(wt)
            listai.append(rt)
            listaf.append(listai)
    for i in listaf:
        for j in i:
            print(j)
           
main()