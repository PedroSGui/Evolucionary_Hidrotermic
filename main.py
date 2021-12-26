
import random
import numpy as np
import copy
class HidroTerm:
    def __init__(self):  
        self.mu = 1000
        self.n_pop=6
        self.mu=0
        self.sigma=10000
        self.aflu = [20000,60000,70000,20000,10000,50000]
        self.aflu = np.array(self.aflu)
        self.k = 10/3
        self.maxTurb=80000
        self.maxRes=150000
        self.maxTer=80000
        self.minTer=0
        #definção da parte hidrica
        self.volTurb=[40000,40000,40000,40000,40000,0] #caso base
        self.volTurb=np.array(self.volTurb)
        
        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
        
        #carga
        self.carga=[70,130,140,50,110,0]
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
            if (j >= 0 and j<=curr_abu and j<80000):
                sobra=curr_abu-j
            else:
                sobra=curr_abu-j
                penalidade=penalidade+100000000000000
            if curr_abu > 150000:
                curr_abu=150000
                penalidade=penalidade+100000000000000
            if i == 5 :
                #not sure if this is right
                x=int(curr_abu*(10/3)/3600)
                poupanca=x*custo_med
                #custo=custo-poupanca
            i=i+1
        

        score = int(custo + penalidade)
        #print("O custo eh: ",custo_med)
        return  score

    def mutate(self):
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in self.volTurb]
        self.varTurb=np.array(self.varTurb)
        self.volTurb=self.volTurb+self.varTurb
        self.volTurb[5]=0

        self.powerAbu = [int(x*self.k/3600) for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)

        self.powerTer=self.carga-self.powerAbu
    
            
if __name__ == '__main__':
    adam = HidroTerm() 
    #print(primogenito.score())
    n_rep=10
    n_gen=30
    pai=copy.copy(adam)
    
    for k in range(n_gen):
        filho=[copy.copy(pai) for i in range(n_rep)]
        #print(filho[3].mu)
        best_score=pai.score()
        for i in range(n_rep):
            filho[i].mutate()
            ponto=filho[i].score()
            #print(ponto)
            if ponto < best_score:
                pai=copy.copy(filho[i])
                best_score=ponto
        #print(pai.score())
    print("\n\n",pai.volTurb)
    print("\n\n",pai.powerAbu)
    print(pai.powerTer)