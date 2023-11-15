import pandas as pd
import h5py
import numpy as np
import matplotlib.pyplot as plt
import bisect


fungi_names = pd.read_csv('./fungal_biogeography/fungi_data/Fungal_climate_data.csv', index_col=0).loc[:,['gen.name2']]
fungi_temperature_curves = pd.read_csv('./fungal_biogeography/fungi_data/Fungi_temperature_curves.csv', index_col=0)
fungi_temperature_curves = fungi_temperature_curves.loc[fungi_temperature_curves['type']=='smoothed']

def get_fungus_name(shortname):
  return fungi_names.loc[[shortname]].values[0][0]

def get_nearest_value(values, val):
  i = bisect.bisect_left(values, val)
  if i:
      return values[i-1]
  raise ValueError

# Will get the hyphal ext rate of the shortnamed fungus at the temperature CLOSEST
# to <temperature>. There may not be data for the given temperature.
def get_hyphal_ext_rate_by_temperature(shortname, temperature):
  single_fungus_temperature_curve = fungi_temperature_curves.loc[[shortname]]
  indices = single_fungus_temperature_curve.loc[[shortname],['temp_c']]['temp_c'].tolist()
  index = get_nearest_value(indices, temperature)
  row = single_fungus_temperature_curve.loc[single_fungus_temperature_curve['temp_c']==index]
  hyphal_ext_rate = row['hyphal_rate'][0]
  return float(hyphal_ext_rate)





#introduce organic matter input. for now, this will be modelled as a constant, but in the future it could be treated as a function of time
dead_organic_matter = 1

#set number of time steps 
time = 100

#set fitness values for each mushroom. to begin with this can be determined by sampling fungus data at arbitrary soil moisture and temperature. 
fungus_1_hyphal_extension_rate = 0.6
fungus_2_hyphal_extension_rate = 0.4

#sum hyphal extension rates
#it may be appropriate to change the fitness values into an array to support a higher number of modeled species
total_hyphal_extension_demand = fungus_1_hyphal_extension_rate + fungus_2_hyphal_extension_rate

fungus_1_total_hyphae = 0
fungus_2_total_hyphae = 0

#initialize vectors to place time-step data into
fungus_1_hyphae_over_time = np.empty((0))
fungus_2_hyphae_over_time = np.empty((0))

#loop to simulate fungal competition at each time step. 
for i in range (1, time): 
    #change input matter
    dead_organic_matter += 1
    #adjust realized fungal fitness based on growth rate and matter input
    fungus_1_total_hyphae += (fungus_1_hyphal_extension_rate/total_hyphal_extension_demand) * dead_organic_matter
    fungus_2_total_hyphae += (fungus_2_hyphal_extension_rate/total_hyphal_extension_demand) * dead_organic_matter

    #identify system-wide realized fungal fitness
    system_total_hyphae = fungus_1_total_hyphae + fungus_2_total_hyphae

    #insert each fungus' individual fitness over system fitness into each respective vector
    fungus_1_hyphae_over_time = np.append(fungus_1_hyphae_over_time, fungus_1_total_hyphae/system_total_hyphae)
    fungus_2_hyphae_over_time = np.append(fungus_2_hyphae_over_time, fungus_2_total_hyphae/system_total_hyphae)
else:
    pass

#plot it
plt.plot(fungus_1_hyphae_over_time, label='fungus 1')
plt.plot(fungus_2_hyphae_over_time, label='fungus 2')
plt.xlabel('days')
plt.ylabel('relative abundance')
plt.title("Proportional Fungal Fitnesses")
plt.legend()
plt.show()