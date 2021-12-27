
import random
import numpy as np
import copy

#'''
class Evolu:
    def __init__(self,mu,n_pop,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga):  
        self.n_pop=n_pop
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
        self.volTurb=[0,55000,65000,0,60000,0] #caso base
        self.volTurb=np.array(self.volTurb)
        
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
        
        #carga
        self.carga=carga
        self.carga=np.array(self.carga)
        #definição da parte térmica
        self.powerTer=self.carga-self.powerAbu
        #print(powerTer)

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
class Swap:
    def __init__(self,mu,n_pop,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga):  
        self.n_pop=n_pop
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

        self.volTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_pop)]
        self.volTurb=np.array(self.volTurb)
        self.volTurb[5]=0
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
        self.powerTer=self.carga-self.powerAbu
        
    def mutate(self):
        self.volTurb=[int(random.gauss(self.mu, self.sigma)) for x in range(n_pop)]
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
    case=1
    n_pop=6
    mu=0 
    sigma=10000 
    aflu = [80000,60000,70000,20000,10000,50000]  #mudar o primeiro é a agua inicial
    k = 10/3
    maxTurb=80000
    maxRes=150000
    maxTer=80000
    minTer=0
    carga = [70,130,140,50,110,0]
    n_rep=100
    n_gen=10
    #'''
    if case == 0:
        adam = Evolu(mu,n_pop,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) 
        pai=copy.copy(adam)
        for k in range(n_gen):
            filho=[copy.copy(pai) for i in range(n_rep)]
            #print(filho[3].mu)
            best_score=pai.score()
            #print("Score Pai: ",best_score,"\n\n")
            for i in range(n_rep):
                filho[i].mutate()
                #print(filho[i].volTurb)
                ponto=filho[i].score()
                #print(ponto)
                if ponto < best_score:
                    pai=copy.copy(filho[i])
                    best_score=ponto
            
        print("\n Volume Turbinado: ",pai.volTurb)
        print("\n Potencia Turbinada: ",pai.powerAbu)
        print("\n Potencia Térmica: ",pai.powerTer)
        print("\n Sobra de Água: ",pai.sobra_abu)
    #'''
    #'''
    if case == 1:
        mu =40000
        sigma = 20000
        explorer=[Swap(mu,n_pop,sigma,aflu,k,maxTurb,maxRes,maxTer,minTer,carga) for i in range(n_rep)]
        signal=0

        for k in range(n_gen):
            for i in range(n_rep):
                explorer[i].mutate()
                ponto=explorer[i].score()
                if  (k == 0 and i == 0):
                    best_score=ponto  
                if  ponto < best_score:
                    signal=1
                    best_explorer=i
                    best_score=ponto
            for p in range(n_rep):
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