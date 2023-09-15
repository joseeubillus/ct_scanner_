import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

'''
This script contains functions specifically for estimation of porosity and saturation in
core samples. CT and heterogeneity projects
'''
# Porosity and saturation estimations
def porosity(dry, wet):
    '''
    Function that estimates porosity under three schemes: core level, slice level, and voxel level
    Inputs:
        dry: numpy array of the dry CT scans, size = (NxNxM)
        wet: numpy array of the wet CT scans, size = (NxNxM)
    Outputs:
        Plots of the porosity estimations
    
    '''
    wet_temp = wet.copy()
    dry_temp = dry.copy()
    wet_temp[wet_temp == 0 ] = np.nan
    dry_temp[dry_temp == 0 ] = np.nan

    ct_dry_avg = np.nanmean(dry_temp)
    ct_wet_avg = np.nanmean(wet_temp)

    # Core level porosity
    por_core = (ct_wet_avg - ct_dry_avg) / (1000-0)

    # Slice level porosity
    slice_dry_avg = np.nanmean(dry_temp, axis=(0,1))
    slice_wet_avg = np.nanmean(wet_temp, axis=(0,1))

    por_slice = (slice_wet_avg - slice_dry_avg) / (1000-0)

    # Voxel-level porosity
    por_voxel = (wet - dry) / (1000-0)

    # plot both slice level and multiple-voxel level porosity
    fig, axs = plt.subplots(3,4, figsize=(15, 10),dpi=300)
    gs = axs[0,0].get_gridspec()
    for ax in axs[0:,0]:
        ax.remove()

    axbig = fig.add_subplot(gs[0:,0])
    axbig.plot(por_slice,range(len(por_slice)),color='k',linestyle="--",linewidth=2)
    axbig.set_xlabel('Porosity')
    axbig.set_ylabel('Slice')
    axbig.set_xlim(0,0.5)
    axbig.set_title('Slice-level porosity')

    s = np.linspace(0,por_voxel.shape[2]-1,12).astype(int)
    for i in range(3):
        for j in range(3):
            im = axs[i,j+1].imshow(por_voxel[:, :, s[i * 3 + j]], cmap="gray",vmin=0,vmax=0.5)
            axs[i,j+1].set_title('Slice ' + str(s[i * 3 + j]))
            axs[i, j+1].axis("off")
            
    fig.colorbar(im, ax=axs[0:,1:], orientation = 'vertical',shrink=0.5,ticks=[0,0.2,0.4,0.6,0.8,1])
    fig.text(0.35,0.06,'Core level porosity estimate: ' + str(round(por_core,3)),
             fontsize=14, bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 5})
   
    return plt.show()

def saturation(wet,co2,twophase):
    '''
    Function that estimates saturation under three schemes: core level, slice level, and voxel level
    Inputs:
        wet: numpy array of the wet CT scans, size = (NxNxM)
        co2: numpy array of the CO2 CT scans, size = (NxNxM)
        twophase: numpy array of the two-phase CT scans, size = (NxNxM)
    Outputs:
        Plots of the saturation estimations
    
    '''
    wet_temp = wet.copy()
    co2_temp = co2.copy()
    tph_temp = twophase.copy()
    wet_temp[wet_temp == 0 ] = np.nan
    co2_temp[co2_temp == 0 ] = np.nan
    tph_temp[tph_temp == 0 ] = np.nan

    # Core level saturation 
    ctexpr = np.nanmean(tph_temp)
    ctco2 = np.nanmean(co2_temp)
    ctwater = np.nanmean(wet_temp)

    sat_core = (ctwater - ctexpr) / (ctwater - ctco2)

    # Slice level saturation
    slice_expr_avg = np.nanmean(tph_temp, axis=(0,1))
    slice_co2_avg = np.nanmean(co2_temp, axis=(0,1))
    slice_water_avg = np.nanmean(wet_temp, axis=(0,1))

    sat_slice = (slice_water_avg - slice_expr_avg) / (slice_water_avg - slice_co2_avg)

    # Voxel-level saturation
    sat_voxel = (wet - twophase) / (wet - co2)

    # plot both slice level and multiple-voxel level saturation
    fig, axs = plt.subplots(3,4, figsize=(15, 10),dpi=300)
    gs = axs[0,0].get_gridspec()
    for ax in axs[0:,0]:
        ax.remove()

    axbig = fig.add_subplot(gs[0:,0])
    axbig.plot(sat_slice,range(len(sat_slice)),color='k',linestyle="--",linewidth=2)
    axbig.set_xlabel('Saturation')
    axbig.set_ylabel('Slice')
    axbig.set_xlim(0,1)
    axbig.set_title('Slice-level saturation')

    s = np.linspace(0,sat_voxel.shape[2]-1,12).astype(int)
    for i in range(3):
        for j in range(3):
            im = axs[i, j+1].imshow(sat_voxel[:, :, s[i * 3 + j]], cmap="jet",vmin=0,vmax=1)
            axs[i,j+1].set_title('Slice ' + str(s[i * 3 + j]))
            axs[i, j+1].axis("off")
    
    fig.colorbar(im, ax=axs[0:,1:], orientation = 'vertical',shrink=0.5,pad=0.04,ticks=[0,0.2,0.4,0.6,0.8,1])
    fig.text(0.35,0.06,'Core level saturation estimate: ' + str(round(sat_core,3)),
             fontsize=14, bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 5})

    return plt.show()