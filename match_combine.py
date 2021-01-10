
import os
import glob
import pandas as pd

from sim_details import mlcosmo
mlc = mlcosmo(ini='config/config_CE-0.ini')

output = 'output/'

_file = "%s/matchedHalosSub_%s_%s.*.dat"%(output,mlc.sim_name, mlc.tag)
print(_file)

files = sorted(glob.glob(_file))
match = [None] * len(files)
for i,f in enumerate(files): match[i] = pd.read_csv(f)
match = pd.concat(match)
match.reset_index(inplace=True)

match.to_csv('%s/matchedHalosSub_%s_%s.dat'%(output,mlc.sim_name,mlc.tag))


for i,f in enumerate(files): os.remove(f)

