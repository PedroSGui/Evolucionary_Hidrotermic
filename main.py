
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
'''
class Swap:
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
        self.carga=carga

        self.volTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_timeStamps)]
        self.volTurb=np.array(self.volTurb)
        self.volTurb[5]=0
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
        self.powerTer=self.carga-self.powerAbu
        
    def mutate(self):
        self.volTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_timeStamps)]
        self.volTurb=np.array(self.volTurb)
        self.volTurb[5]=0
        #print(self.volTurb)
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
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
        

        score = int(custo + penalidade)
        #print("O score eh: ",score)
        return  score
#'''

if __name__ == '__main__':
    case=0
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
    n_gen=10
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
            '''
            for i in range(n_pop_half):
                for j in range(n_pop):
                    if generation[j]._score == score_book[0]:
                        best_of_generation=copy.copy(generation[j])
                    if generation[j]._score == score_book[i] and count<n_pop_half:
                        count=count+1
                        dad=copy.copy(generation[j])
                        son=copy.copy(generation[j])
                        son.mutate()
                        son_list.append(dad)
                        son_list.append(son)

            generation=[]
            generation=[copy.copy(son_list[i]) for i in range(n_pop)]
            '''
        print("\n Volume Turbinado: ",best_of_generation.volTurb)
        print("\n Potencia Turbinada: ",best_of_generation.powerAbu)
        print("\n Potencia Térmica: ",best_of_generation.powerTer)
        print("\n Sobra de Água: ",best_of_generation.sobra_abu)
        print("\n Pontuação: ",best_of_generation._score)
    #'''
    '''
    if case == 1:
        mu =40000
        sigma = 20000
        explorer=[Swap(mu,n_timeStamps,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_pop)]
        signal=0

        for k in range(n_gen):
            for i in range(n_pop):
                explorer[i].mutate()
                ponto=explorer[i].score()
                if  (k == 0 and i == 0):
                    best_score=ponto  
                if  ponto < best_score:
                    signal=1
                    best_explorer=i
                    best_score=ponto
            for p in range(n_pop):
                explorer[p]=copy.copy(explorer[best_explorer])
            if  signal == 1:
                super_explorer=copy.copy(explorer[best_explorer])
            signal=0
            #print("\n",super_explorer.score())

        print("\n Volume Turbinado: ",super_explorer.volTurb)
        print("\n Potencia Turbinada: ",super_explorer.powerAbu)
        print("\n Potencia Térmica: ",super_explorer.powerTer)
        print("\n Sobra de Água: ",super_explorer.sobra_abu)
    #'''