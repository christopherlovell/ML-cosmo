import sys

import pandas as pd

import eagle_IO.eagle_IO as E

from sim_details import mlcosmo
_config = str(sys.argv[1])
mlc = mlcosmo(ini=_config)
nthr = 16

Grp_DM = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                      "Subhalo/GroupNumber", numThreads=nthr)

data = pd.DataFrame()

data['FOF_Group_M_Crit200_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                 "FOF/Group_M_Crit200", numThreads=nthr)[Grp_DM-1] * mlc.unitMass

data['FOF_Group_R_Crit200_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                 "FOF/Group_R_Crit200", numThreads=nthr)[Grp_DM-1] * mlc.unitLength

data['M_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                            "Subhalo/Mass") * mlc.unitMass 

data['MassTwiceHalfMassRad_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
               "Subhalo/MassTwiceHalfMassRad", numThreads=nthr)[:,1] * mlc.unitMass

data['velocity_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                                   "Subhalo/Velocity", numThreads=nthr)[:,1]

data['Vmax_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                               "Subhalo/Vmax", numThreads=nthr)

data['VmaxRadius_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                                     "Subhalo/VmaxRadius", numThreads=nthr)

data['length_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                                 "Subhalo/SubLength", numThreads=nthr)

data['Sub_DM'] = E.read_array("SUBFIND", mlc.sim_dmo, mlc.tag, 
                              "Subhalo/SubGroupNumber", numThreads=nthr)

data['Subhalo_Mass_DM'] = 1.15*10**7 * data['length_DM']
data['Satellite'] = (data['Sub_DM'] != 0).astype(int)

data = data[data['M_DM'] > 1e9].reset_index()


data.to_csv('output/%s_%s_dmo.csv'%(mlc.sim_name, mlc.tag))