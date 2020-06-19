Tempo=0
Pcb=[]
Memory=[]

class Processo:
    def __init__(self,num,tempo,periodo,versao):
        self.num=num
        self.tempo=tempo
        self.periodo=periodo
        self.versao=versao

class Mem:
    def __init__(self,num,tempo,periodo,versao):
        self.num=num
        self.tempo=tempo
        self.periodo=periodo
        self.versao=versao

def verr():
    global Tempo
    global Pcb
    for i in Pcb:
        if(Tempo%i.periodo==0 or Tempo==0):
            x=Mem(i.num,i.tempo,i.periodo,i.versao)
            #print(x.num)
            #print(x.periodo)
            #print(x.tempo)
            #print("aaaa")
            #print(x.versao)
            alterar_Pcb(i.num)
            mudar_Memory(x)
    
def alterar_Pcb(x):
    global Pcb
    for i in range(len(Pcb)):
        if(Pcb[i].num==x):
            Pcb[i].versao=Pcb[i].versao+1
            break

def mudar_Memory(x):
    global Memory
    flag=0
    #print("mudar_Memory")
    #print(x.num)
    #print(x.periodo)
    #print(x.tempo)
    #print(x.versao)
    if(len(Memory)==0):
        #print("cccc")
        Memory.append(x)
    else:
        #print("ddddd")
        for i in range(len(Memory)):
            if(Memory[i].periodo>x.periodo):
                Memory.insert(i,x)
                break
            if(Memory[i].periodo==x.periodo):
                print("Dealine Miss Detected")
                Memory.insert(i+1,x)
                break
            if((i+1)==len(Memory)):
                Memory.append(x)
                break

def read_file_plan(nome):#OK
    file=open(nome,"r")
    lines=file.readlines()
    fila=[]
    for i in lines:
        a=i.strip()
        b=a.split(",")
        fila.append(b)
    return fila

def criar_Pcb(nome):
    global Pcb
    fila=read_file_plan(nome)
    for i in fila:
        x=Processo(int(i[0]),int(i[1]),int(i[2]),1)
        Pcb.append(x)

def Rate_Monotonic(x):
    global Tempo
    global Memory 
    while(Tempo<x):
        #print("xxxx")
        verr()
        print("Tempo--> %d" % (Tempo))
        if(len(Memory)!=0):
            print("P%d-V%d"%(Memory[0].num,Memory[0].versao))
            Memory[0].tempo=Memory[0].tempo-1
            #print(Memory[0].tempo)
            if(Memory[0].tempo==0):
                Memory.pop(0)
        Tempo=Tempo+1
    print("Tempo--> %d" % (Tempo))
    

def main():
    global Pcb
    criar_Pcb('/home/andre/Documentos/plan3.txt')
    aux=-1
    aux2=0
    for i in Pcb:
        aux2=aux2+(i.tempo/i.periodo)
        if(aux<i.periodo):
            aux=i.periodo
    #print("qqqq")
    #print(aux)
    print(aux2)
    Rate_Monotonic(aux)
    #Rate_Monotonic(30)

main()
