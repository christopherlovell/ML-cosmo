import numpy as np
import pandas as pd
import pickle

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid.inset_locator import inset_axes

import seaborn as sns

from sim_details import mlcosmo
# mlc = mlcosmo(ini='config/config_cosma_L0100N1504.ini')
mlc = mlcosmo(ini='config/config_cosma_L0050N0752.ini')
zoom = True
density = False
output = 'models/'
output_name = mlc.sim_name 
if zoom: output_name += '_zoom'
if density: output_name += '_density'

etree, features, predictors, feature_scaler, predictor_scaler, eagle =\
        pickle.load(open(output + output_name + '_' + mlc.tag + '_ert.model', 'rb'))

train = eagle['train_mask']

galaxy_pred = pd.DataFrame(predictor_scaler.inverse_transform(\
                           etree.predict(feature_scaler.transform(\
                           eagle[~train][features]))),columns=predictors)

# mask = np.array(galaxy_pred['Stars_Mass_EA'] > -1)
# galaxy_pred = galaxy_pred[mask]
# eagle = eagle[~train][mask]


def vplot_data(feature,zero_val=1):   
    # _temp_eag = np.array(eagle[feature].copy())
    # _temp_eag[_temp_eag == 0] = zero_val
    vdata_temp = pd.DataFrame(np.ma.array(eagle[~train][feature]),  columns=[feature])
    # vdata_temp = pd.DataFrame(np.log10(np.ma.array(eagle[~train][feature])),  columns=[feature])
    # vdata_temp = pd.DataFrame(np.log10(np.ma.array(_temp_eag)),  columns=[feature])
    vdata_temp['type'] = 'eagle'
    
    # _temp = galaxy_pred[feature].copy()# [~(_temp_eag == 0)]
    # _temp[_temp == 0] = zero_val
    # vdata = pd.DataFrame(np.log10(np.ma.array(galaxy_pred[feature])), columns=[feature])
    vdata = pd.DataFrame(np.ma.array(galaxy_pred[feature]), columns=[feature])
    # vdata = pd.DataFrame(np.log10(np.ma.array(_temp)), columns=[feature])
    vdata['type'] = 'prediction'

    vdata = vdata.append(vdata_temp)
    vdata['dummy'] = 'A'
    return vdata


fig,(ax1,ax2,ax3,ax4,ax5) = plt.subplots(1,5,figsize=(16,6))
axes = [ax1,ax2,ax3,ax4,ax5]

preds = ['Stars_Mass_EA', 'MassType_Gas_EA', 'BlackHoleMass_EA',
         'StellarVelDisp_EA', 'Stars_Metallicity_EA']#, 'StarFormationRate_EA']
preds_pretty = ['$\mathrm{log_{10}}(M_{\star}\,/\,\mathrm{M_{\odot}})$',
                '$\mathrm{log_{10}}(M_{\mathrm{gas}}\,/\,\mathrm{M_{\odot}})$',
                '$\mathrm{log_{10}}(M_{\\bullet}\,/\,\mathrm{M_{\odot}})$',
                '$\mathrm{log_{10}}(v_{\star,\mathrm{disp}})$',
                '$\mathrm{log_{10}}(Z_{*})$']#,
#                '$\mathrm{log_{10}}(SFR \,/\, \mathrm{M_{\odot}\, yr^{-1}})$']
ax_lims = [[4.8,12],[5.9,12],[4.8,7],[1,2.2],[-5.1,-1],[-3.5,0.8]]
zero_vals = np.array([6, 4, 4, 1, -4, -4.9])

for ax,pred,pretty,_lims,zero_val in zip(axes, preds, preds_pretty, ax_lims, zero_vals):

    vdata = vplot_data(pred,zero_val)
    sns.violinplot(x='dummy', y=pred, hue='type', split=True, data=vdata, 
                   palette="Set2", inner='quartile', ax=ax, cut=0)

    ax.legend_.remove()
    ax.set_ylabel('')
    ax.set_title(pretty, fontsize=14)
    ax.set_ylim(_lims[0],_lims[1])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_visible(False)


ax1.legend(loc=4, fontsize=13, frameon=False)

# plt.show()
fname = 'plots/violins_%s.png'%mlc.sim_name; print(fname)
plt.savefig(fname, dpi=150, bbox_inches='tight')

