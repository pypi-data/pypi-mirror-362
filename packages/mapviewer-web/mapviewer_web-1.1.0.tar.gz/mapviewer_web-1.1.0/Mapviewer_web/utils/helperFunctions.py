import numpy as np
import os
import yaml

def getVoronoiBin(self, click_x, click_y):
    """
    Identify the Voronoi-bin/spaxel closest to the clicked location on the map
    """
    idx = np.where( np.logical_and( np.abs(self.table.X-click_x) < self.pixelsize, np.abs(self.table.Y-click_y) < self.pixelsize ) )[0]

    if len(idx) == 1:
        final_idx = idx[0]
    elif len(idx) == 4:
        xmini = np.argsort( np.abs( self.table.X[idx]        - click_x ) )[:2]
        ymini = np.argmin(  np.abs( self.table.Y[idx[xmini]] - click_y ) )
        final_idx = idx[xmini[ymini]]
    else:
        return(None)

    # Save index of chosen Voronoi-bin
    idxBinLong  = final_idx                            # In Spaxel arrays
    idxBinShort = np.abs(self.table.BIN_ID[final_idx]) # In Bin arrays
    return idxBinLong, idxBinShort

def remove_idxBin(self):
    if hasattr(self, "idxBinLong"):
        delattr(self, "idxBinLong")
    if hasattr(self, "idxBinShort"):
        delattr(self, "idxBinShort")

