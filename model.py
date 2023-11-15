import pandas as pd
import h5py
import numpy as np
import matplotlib.pyplot as plt

#introduce organic matter input. for now, this will be modelled as a constant, but in the future it could be treated as a function of time
matter = 1

#set number of time steps 
time = 100

#set fitness values for each mushroom. to begin with this can be determined by sampling fungus data at arbitrary soil moisture and temperature. 
fungus1 = 0.6
fungus2 = 0.4

#sum hyphal extension rates
#it may be appropriate to change the fitness values into an array to support a higher number of modeled species
systemfitness = fungus1 + fungus2

fungusreal1 = 0
fungusreal2 = 0

#initialize vectors to place time-step data into
fungus1fitnessdata = np.empty((0))
fungus2fitnessdata = np.empty((0))

#loop to simulate fungal competition at each time step. 
for i in range (1, time): 
    #change input matter
    matter += 1
    #adjust realized fungal fitness based on growth rate and matter input
    fungusreal1 += (fungus1/systemfitness) * matter
    fungusreal2 += (fungus2/systemfitness) * matter

    #identify system-wide realized fungal fitness
    fungaltotalreal = fungusreal1 + fungusreal2

    #insert each fungus' individual fitness over system fitness into each respective vector
    fungus1fitnessdata = np.append(fungus1fitnessdata, fungusreal1/fungaltotalreal)
    fungus2fitnessdata = np.append(fungus2fitnessdata, fungusreal2/fungaltotalreal)
else:
    pass

#plot it
plt.plot(fungus1fitnessdata, label='fungus 1')
plt.plot(fungus2fitnessdata, label='fungus 2')
plt.xlabel('days')
plt.ylabel('relative abundnace')
plt.title("Proportional Fungal Fitnesses")
plt.legend()
plt.show()