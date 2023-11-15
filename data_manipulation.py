import pandas as pd
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


hyphal_rate = get_hyphal_ext_rate_by_temperature('a.gal1.s',100)
print(hyphal_rate + 2)


