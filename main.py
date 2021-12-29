
import random
import numpy as np
import copy

#'''
def bubble_sort(our_list):
    has_swapped = True

    num_of_iterations = 0

    while(has_swapped):
        has_swapped = False
        for i in range(len(our_list) - num_of_iterations - 1):
            if our_list[i] > our_list[i+1]:
                # Swap
                our_list[i], our_list[i+1] = our_list[i+1], our_list[i]
                has_swapped = True
        num_of_iterations += 1
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
                penalidade=penalidade+100000000000000000
            i=i+1
        custo_med=custo/i
        sobra=0
        i=0
        for j in self.volTurb:
            curr_abu=self.aflu[i]+sobra
            if (j >= 0 and j<=curr_abu and j<=80000):
                sobra=curr_abu-j
            else:
                #print(j,curr_abu)
                sobra=curr_abu-j
                penalidade=penalidade+100000000000000
            if curr_abu > 150000:
                curr_abu=150000
                penalidade=penalidade+100000000000000
            if i == 5 :
                #not sure if this is right
                x=int(curr_abu*(10/3)/3600)
                self.sobra_abu=curr_abu
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
class Swap:
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
                penalidade=penalidade+100000000000000000
            i=i+1
        custo_med=custo/i
        sobra=0
        i=0
        for j in self.volTurb:
            curr_abu=self.aflu[i]+sobra
            if (j >= 0 and j<=curr_abu and j<=80000):
                sobra=curr_abu-j
            else:
                #print(j,curr_abu)
                sobra=curr_abu-j
                penalidade=penalidade+100000000000000
            if curr_abu > 150000:
                curr_abu=150000
                penalidade=penalidade+100000000000000
            if i == 5 :
                #not sure if this is right
                x=int(curr_abu*(10/3)/3600)
                self.sobra_abu=curr_abu
                poupanca=x*custo_med
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
        B=random.uniform(0, 1)
        C=random.uniform(0, 1)
        #print(self.volTurb,self.A,self.previous_vol_turb,self.best_gene._score,global_gene._score)
        self.volTurb=self.volTurb+self.A*(self.volTurb-self.previous_vol_turb)+B*(self.best_gene.volTurb-self.volTurb)+C*(global_gene.volTurb-self.volTurb)
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
    case=2
    n_timeStamps=6
    mu=0 
    sigma=10000 
    aflu = [90000,60000,70000,20000,10000,50000]  #mudar o primeiro é a agua inicial
    k = 10/3
    maxTurb=80000
    maxRes=150000
    maxTer=80000
    minTer=0
    carga = [70,130,140,50,110,0]
    n_pop=50
    n_gen=100
    n_pop_half=int(n_pop/2)
    #'''
    if case == 0:
        generation=[Evolu(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        son_list=[]#2pop
        for k in range(n_gen):
            new_generation=[]
            for j in range(n_pop):
                dad=copy.copy(generation[j])
                son=copy.copy(generation[j])
                son.mutate()
                new_generation.append(dad)
                new_generation.append(son)
            score_book=[]
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
                        count=count+1
                        fit=copy.copy(new_generation[j])
                        son_list.append(fit)
            generation=[copy.copy(son_list[p]) for p in range(n_pop)]
            
        print("\n Volume Turbinado: ",best_of_generation.volTurb)
        print("\n Potencia Turbinada: ",best_of_generation.powerAbu)
        print("\n Potencia Térmica: ",best_of_generation.powerTer)
        print("\n Sobra de Água: ",best_of_generation.sobra_abu)
        print("\n Pontuação: ",best_of_generation._score)
    #'''

    #'''
    if case == 1:
        generation=[Evolu(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        for k in range(n_gen):
            new_generation=[]
            position_list=[]
            position_list=[i for i in range(2*n_pop)]
            for j in range(n_pop):
                dad=copy.copy(generation[j])
                son=copy.copy(generation[j])
                son.mutate()
                new_generation.append(dad)
                new_generation.append(son)
            score_book=[]
            score_book=[new_generation[i].score() for i in range(2*n_pop)]
            score_book=np.array(score_book)
            son_list=[]
            for i in range(n_pop):
                pos1=random.choice(position_list)
                position_list.remove(pos1)
                pos2=random.choice(position_list)
                position_list.remove(pos2)
                if new_generation[pos1]._score < new_generation[pos2]._score:
                    fit=copy.copy(new_generation[pos1])
                    son_list.append(fit)
                else:
                    fit=copy.copy(new_generation[pos2])
                    son_list.append(fit)
            generation=[copy.copy(son_list[p]) for p in range(n_pop)]
        for m in range(n_pop):
            print("Volume Turbinado: ",generation[m].volTurb)
            print("Potencia Turbinada: ",generation[m].powerAbu)
            print("Potencia Térmica: ",generation[m].powerTer)
            print("Sobra de Água: ",generation[m].sobra_abu)
            print("Pontuação: ",generation[m]._score)
    #'''


    #'''
    if case == 2:
        explorer=[Swap(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        signal=0
        best_explorer = copy.copy(explorer[0])
        best_explorer.score()
        for k in range(n_gen):
            book_of_explorers=[]
            for i in range(n_pop):
                explorer[i].mutate(best_explorer)
                book_of_explorers.append(explorer[i])
                #print("\n\n Score: ",explorer[i].score(), best_explorer._score)
                if explorer[i].score() <= best_explorer.score():
                    #best_score = explorer[i].score()
                    best_explorer = copy.copy(explorer[i])

        print("\n Volume Turbinado: ",best_explorer.volTurb)
        print("\n Potencia Turbinada: ",best_explorer.powerAbu)
        print("\n Potencia Térmica: ",best_explorer.powerTer)
        print("\n Sobra de Água: ",best_explorer.sobra_abu)
        print("Pontuação: ",best_explorer._score)
    #'''