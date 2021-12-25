
import random
import numpy as np
class HidroTerm:
    def __init__(self):  
        self.mu = 1000
        self.n_pop=6
        self.mu=1000
        self.sigma=100
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
        self.varTurb=[int(random.gauss(self.mu, self.sigma)) for x in self.volTurb]
        self.varTurb=np.array(self.varTurb)
        self.volTurb=self.volTurb+self.varTurb
        self.volTurb[5]=0
        self.powerAbu = [x*self.k/3600 for x in self.volTurb]
        self.powerAbu=np.array(self.powerAbu)
        
        #carga
        self.carga=[70,130,140,50,110,0]
        self.carga=np.array(self.carga)
        #definição da parte térmica
        self.powerTer=self.carga-self.powerAbu
        #print(powerTer)

    def score(self):
        self.custoTer=[2000+120*x+1.6*x*x for x in self.powerTer]
        self.custoTer= np.array(self.custoTer)
        custo=0
        for x in self.custoTer:
            custo=custo+x

        sobra=0
        penalidade=0
        i=0
        for j in self.volTurb:
            curr_abu=self.aflu[i]+sobra
            if j >= 0 & j<=curr_abu & j<80000:
                sobra=curr_abu-j
            else:
                penalidade=penalidade+10000000000
            i=i+1

        score = int(custo + penalidade)
        return  score
    
    
            
if __name__ == '__main__':
    p = HidroTerm()  
    print(p.score())