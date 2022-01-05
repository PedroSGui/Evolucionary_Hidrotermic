
import random
import numpy as np
import copy
import time

case=2 # caso 0 -> evolucionario_elitista    caso 1 -> evolucionario_torneio    caso 2 -> enxame de particulas caso -1 -> mostra tudo


start=time.time()

#'''
def bubble_sort(our_list):
    has_Swarmped = True

    num_of_iterations = 0

    while(has_Swarmped):
        has_Swarmped = False
        for i in range(len(our_list) - num_of_iterations - 1):
            if our_list[i] > our_list[i+1]:
                # Swarm
                our_list[i], our_list[i+1] = our_list[i+1], our_list[i]
                has_Swarmped = True
        num_of_iterations += 1
#'''

#''' 
class Evolu:
    def __init__(self,mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga):  
        self.n_timeStamps=n_timeStamps
        self.mu=mu
        self.sigma=sigma
        self.aflu = aflu
        self.aflu = np.array(self.aflu)
        self.k = k
        self.maxTurb=maxTurb
        self.maxRes=maxRes
        self.maxTer=maxTer
        self.minTer=minTer
        #definção da parte hidrica
        #self.volTurb=[0,55000,65000,0,60000,0] #caso base para 20mil iniciais
        #self.volTurb=[0,55000,65000,0,60000,0] #caso base
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_timeStamps)]
        self.varTurb=np.array(self.varTurb)
        self.volTurb=[int(random.gauss(maxTurb/2, self.sigma)) for x in range(n_timeStamps)]
        self.volTurb=np.array(self.volTurb)
        self.volTurb=self.volTurb+self.varTurb
        self.volTurb[n_timeStamps-1]=0
        
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)

        #carga
        self.carga=carga
        self.carga=np.array(self.carga)
        #definição da parte térmica
        self.powerTer=self.carga-self.powerAbu

    def score(self):
        self.custoTer=[int(2000+120*x+1.6*x*x) for x in self.powerTer]
        self.custoTer= np.array(self.custoTer)
        i=0
        custo=0
        penalidade=0
        for j in self.powerTer:
            if (j >= 0 and j<=80):
                custo=custo+j
            else:
                custo=custo+j
                penalidade=penalidade+10000000000000+(custo)^2
            i=i+1
        custo_med=custo/i
        sobra=0
        i=0
        for j in self.volTurb:
            self.curr_abu=self.aflu[i]+sobra
            if (j >= 0 and j<=self.curr_abu and j<=80000):
                sobra=self.curr_abu-j
            else:
                #print(j,self.curr_abu)
                sobra=self.curr_abu-j
                penalidade=penalidade+100000000000000+(j)^2
            if self.curr_abu > 150000:
                self.curr_abu=150000
                penalidade=penalidade+100000000000000
            if i == 5 :
                #not sure if this is right
                x=int(self.curr_abu*(10/3)/3600)
                self.sobra_abu=self.curr_abu
                poupanca=x*custo_med
                custo=custo-poupanca
            i=i+1
        

        self._score = int(custo + penalidade)
        #print("O score eh: ",score)
        return  self._score

    def mutate(self):
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in self.volTurb]
        self.varTurb=np.array(self.varTurb)
        self.volTurb=self.volTurb+self.varTurb
        self.volTurb[5]=0

        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)

        self.powerTer=self.carga-self.powerAbu
#'''  

#''' 
class Swarm:
    def __init__(self,mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga):  
        self.best_explorer = []
        self.n_timeStamps=n_timeStamps
        self.mu=mu
        self.sigma=sigma
        self.aflu = aflu
        self.aflu = np.array(self.aflu)
        self.k = k
        self.maxTurb=maxTurb
        self.maxRes=maxRes
        self.maxTer=maxTer
        self.minTer=minTer
        #definção da parte hidrica
        #self.volTurb=[0,55000,65000,0,60000,0] #caso base para 20mil iniciais
        #self.volTurb=[0,55000,65000,0,60000,0] #caso base
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_timeStamps)]
        self.varTurb=np.array(self.varTurb)
        self.volTurb=[int(random.gauss(maxTurb/2, self.sigma)) for x in range(n_timeStamps)]
        self.volTurb=np.array(self.volTurb)
        self.volTurb=self.volTurb+self.varTurb
        self.volTurb[n_timeStamps-1]=0
        
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)

        #carga
        self.carga=carga
        self.carga=np.array(self.carga)
        #definição da parte térmica
        self.powerTer=self.carga-self.powerAbu
        self._score=100000000000000000000000000000000000000000000
        self.A=1
        self.best_gene=copy.copy(self)

    def score(self):
        self.custoTer=[int(2000+120*x+1.6*x*x) for x in self.powerTer]
        self.custoTer= np.array(self.custoTer)
        i=0
        custo=0
        penalidade=0
        for j in self.powerTer:
            if (j >= 0 and j<=80):
                custo=custo+j
            else:
                custo=custo+j
                penalidade=penalidade+10000+(custo)^2
            i=i+1
        custo_med=custo/i
        sobra=0
        i=0
        self.abu=[]
        for j in self.volTurb:
            j=int(j)
            self.curr_abu=self.aflu[i]+sobra
            if (j >= 0 and j<=self.curr_abu and j<=80000):
                sobra=self.curr_abu-j
            else:
                #print(j,self.curr_abu)
                sobra=self.curr_abu-j
                penalidade=float(penalidade+1000+(j*j))
            if self.curr_abu > 150000:
                self.curr_abu=150000
                penalidade=penalidade+1000
            self.abu.append(self.curr_abu)
            if i == 5 :
                #not sure if this is right
                x=int(self.curr_abu*(10/3)/3600)
                self.sobra_abu=self.curr_abu
                poupanca=x*custo_med*(7/10)
                custo=custo-poupanca
            i=i+1
        
        previous_score=self._score
        self._score = int(custo + penalidade)
        if self._score <= previous_score:
            self.best_score_in_this_gene= self._score
            self.best_gene=copy.copy(self)
        #print("O score eh: ",score)
        return  self._score

    def mutate(self,global_gene):
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in self.volTurb]
        self.varTurb=np.array(self.varTurb)
        self.previous_vol_turb=self.volTurb #Xj(k-1)
        self.volTurb=self.volTurb+self.varTurb #Xj(k)
        self.volTurb[5]=0
        
        self.A=self.A*(9/10)
        B=random.uniform(0, 1)*(1-self.A)
        C=random.uniform(0, 1)*(1-self.A)
        #print(self.volTurb,self.A,self.previous_vol_turb,self.best_gene._score,global_gene._score)
        
        inercia=self.A*(self.volTurb-self.previous_vol_turb)
        memoria=B*(self.best_gene.volTurb-self.volTurb)
        cooperacao=C*(global_gene.volTurb-self.volTurb)

        self.volTurb=self.volTurb+inercia+memoria+cooperacao

        self.volTurb[0]=int(self.volTurb[0])
        self.volTurb[1]=int(self.volTurb[1])
        self.volTurb[2]=int(self.volTurb[2])
        self.volTurb[3]=int(self.volTurb[3])
        self.volTurb[4]=int(self.volTurb[4])
        self.volTurb[5]=int(self.volTurb[5])

        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)

        self.powerTer=self.carga-self.powerAbu
#'''  

if __name__ == '__main__':
    n_timeStamps=6
    mu=0 
    sigma=10000  # pode mexer
    aflu = [80000,60000,70000,20000,10000,50000]  #mudar o primeiro é a agua inicial        # pode mexer no primeiro
    k = 10/3
    maxTurb=80000
    maxRes=150000
    maxTer=80000
    minTer=0
    carga = [70,130,140,50,110,0]
    n_pop=50 #pode mexer
    n_gen=100 #pode mexer
    n_pop_half=int(n_pop/2)
    #'''
    if case == 0 or case==-1:
        #Programação Evolucionaria
        generation=[Evolu(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        son_list=[]#2pop
        for k in range(n_gen):
            new_generation=[]
            for j in range(n_pop):
                #Duplicar
                dad=copy.copy(generation[j])
                son=copy.copy(generation[j])
                #Mutar
                son.mutate()
                new_generation.append(dad)
                new_generation.append(son)
            score_book=[]
            #Avaliar
            score_book=[new_generation[i].score() for i in range(2*n_pop)]
            bubble_sort(score_book)
            score_book=np.array(score_book)
            count=0
            son_list=[]
            for i in range(n_pop):
                for j in range(2*n_pop):
                    if new_generation[j]._score == score_book[0]:
                        best_of_generation=copy.copy(new_generation[j])
                    if new_generation[j]._score == score_book[i] and count<n_pop:
                        #Selecionar
                        count=count+1
                        fit=copy.copy(new_generation[j])
                        son_list.append(fit)
            generation=[copy.copy(son_list[p]) for p in range(n_pop)]
        end=time.time()
        print("\n\n Melhor caso com Programação Evolucionária Elitista: ")
        print(" População: ",n_pop,"\tGeração: ",n_gen,"\n Mu: ",best_of_generation.mu,"      Sigma: ",best_of_generation.sigma)    
        print(" Afluência Inicial: ",best_of_generation.aflu)
        print(" Volume Turbinado: ",best_of_generation.volTurb)
        print(" Potencia Turbinada: ",best_of_generation.powerAbu)
        print(" Potencia Térmica: ",best_of_generation.powerTer)
        print(" Sobra de Água: ",best_of_generation.sobra_abu)
        print(" Pontuação: ",best_of_generation._score)
        print(" Tempo de execução do algiritmo: ",(end-start))
        print("\n")
    #'''

    #'''
    if case == 1 or case==-1:
        #Enxame de Partículas
        generation_torneio=[Evolu(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        best_of_generation_torneio=copy.copy(generation_torneio[0])
        k=0
        i=0
        j=0
        p=0
        m=0
        for k in range(n_gen):
            new_generation_torneio=[]
            position_list_torneio=[]
            position_list_torneio=[i for i in range(2*n_pop)]
            for j in range(n_pop):
                dad_torneio=copy.copy(generation_torneio[j])
                son_torneio=copy.copy(generation_torneio[j])
                son_torneio.mutate()
                new_generation_torneio.append(dad_torneio)
                new_generation_torneio.append(son_torneio)
            score_book_torneio=[]
            score_book_torneio=[new_generation_torneio[i].score() for i in range(2*n_pop)]
            score_book_torneio=np.array(score_book_torneio)
            son_torneio_list=[]
            for i in range(n_pop):
                pos1=random.choice(position_list_torneio)
                position_list_torneio.remove(pos1)
                pos2=random.choice(position_list_torneio)
                position_list_torneio.remove(pos2)
                if new_generation_torneio[pos1]._score < new_generation_torneio[pos2]._score:
                    fit=copy.copy(new_generation_torneio[pos1])
                    son_torneio_list.append(fit)
                else:
                    fit=copy.copy(new_generation_torneio[pos2])
                    son_torneio_list.append(fit)
            generation_torneio=[copy.copy(son_torneio_list[p]) for p in range(n_pop)]
        for m in range(n_pop):
            '''
            print("Volume Turbinado: ",generation_torneio[m].volTurb)
            print("Potencia Turbinada: ",generation_torneio[m].powerAbu)
            print("Potencia Térmica: ",generation_torneio[m].powerTer)
            print("Sobra de Água: ",generation_torneio[m].sobra_abu)
            print("Pontuação: ",generation_torneio[m]._score)
            '''
            best_of_generation_torneio.score()
            if generation_torneio[m]._score < best_of_generation_torneio._score:
                best_of_generation_torneio=copy.copy(generation_torneio[m])
        end=time.time()
        print("\n\n Melhor caso com Programação Evolucionária Torneio: ")
        print(" População: ",n_pop,"\tGeração: ",n_gen,"\n Mu: ",best_of_generation_torneio.mu,"      Sigma: ",best_of_generation_torneio.sigma)    
        print(" Afluência Inicial: ",best_of_generation_torneio.aflu)
        print(" Volume Turbinado: ",best_of_generation_torneio.volTurb)
        print(" Potencia Turbinada: ",best_of_generation_torneio.powerAbu)
        print(" Potencia Térmica: ",best_of_generation_torneio.powerTer)
        print(" Sobra de Água: ",best_of_generation_torneio.sobra_abu)
        print(" Pontuação: ",best_of_generation_torneio._score)
        print(" Tempo de execução do algiritmo: ",(end-start))
        print("\n")
    #'''

    #'''
    if case == 2 or case==-1:
        explorer=[Swarm(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        signal=0
        best_explorer = copy.copy(explorer[0])
        best_explorer.score()
        for k in range(n_gen):
            book_of_explorers=[]
            for i in range(n_pop):
                explorer[i].mutate(best_explorer)
                book_of_explorers.append(explorer[i])
                #print("\n\n Score: ",explorer[i].score(), best_explorer._score)
                #print(explorer[i].score())
                if explorer[i].score() <= best_explorer.score():
                    #best_score = explorer[i].score()
                    best_explorer = copy.copy(explorer[i])
        end=time.time()
        print("\n\n Melhor caso com Enxame de Partículas: ")
        print(" População: ",n_pop,"\tGeração: ",n_gen,"\n Mu: ",best_explorer.mu,"      Sigma: ",best_explorer.sigma)    
        print(" Afluência Inicial: ",best_explorer.aflu)
        print(" Volume Turbinado: ",best_explorer.volTurb)
        print(" Albufeira: ",best_explorer.abu)
        print(" Potencia Turbinada: ",best_explorer.powerAbu)
        print(" Potencia Térmica: ",best_explorer.powerTer)
        print(" Sobra de Água: ",best_explorer.sobra_abu)
        print(" Pontuação: ",best_explorer._score)
        print(" Tempo de execução do algiritmo: ",(end-start))
        print("\n")
    #'''