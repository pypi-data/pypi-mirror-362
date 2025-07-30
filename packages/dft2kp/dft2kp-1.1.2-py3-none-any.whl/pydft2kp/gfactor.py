import numpy as np
from .constants import s0, sx, sy, sz

class GFactor():
    """
    Class to calculate the effective g-factor tensor for a set of electronic bands.
    """
    
    def __init__(self, setA, energies, Px, Py, Pz, Sx=None, Sy=None, Sz=None, nmax=0, threshold=1e-6):
        '''
        Initialize the gfactor class to calculate the effective g-factor tensor for a set of bands.
        
        The g-factor is defined as in the Zeeman Hamiltonian: H_B = mu_B * g · B.

        Parameters
        ----------
        setA : array-like
            Indices of the bands of interest (active bands) for which the g-factor is calculated.
        energies : array-like
            Array of band energies. The length should correspond to the total number of bands.
        Px, Py, Pz : array-like
            Momentum matrix elements between bands in the x, y, and z directions, respectively.
            Each should be a 2D array of shape (n_bands, n_bands).
        Sx, Sy, Sz : array-like, optional
            Spin matrices for the x, y, and z directions. If None, spinless case is assumed.
            Each should be a 2D array of shape (len setA, len setA).
        nmax : int, optional
            Maximum number of bands to consider. If set to 0 (default), all bands are used.
        threshold : float, optional
            Threshold for energy denominators to avoid division by zero. Default is 1e-6.
        
        Attributes
        ----------
        Lx, Ly, Lz : ndarray
            Orbital angular momentum matrices for the x, y, and z directions.
        Sx, Sy, Sz : ndarray
            Spin matrices for the x, y, and z directions.
        gx, gy, gz : ndarray
            Effective g-factor matrices for the x, y, and z directions.
        '''
        
        # set nmax to 0 to use all bands
        nmax = nmax if nmax > 0 else len(energies)

        # angular momentum for QE's units: m0 = 1/2 and hbar = 1
        L = np.zeros([3, len(setA), len(setA)], dtype=complex)
        # loops over setA
        for i, n1 in zip(range(len(setA)), setA):
            for j, n2 in zip(range(len(setA)), setA):
                # loop over setB (sum over remote bands)
                for m in range(len(energies)):
                    
                    # energy denominators
                    # -------------------
                    # delta1 = 0 if e[n1] == en[m]
                    delta1 = 1/(energies[n1] - energies[m]) if np.abs(energies[n1] - energies[m]) > threshold else 0
                    
                    # delta2 = 0 if e[n2] == en[m]
                    delta2 = 1/(energies[n2] - energies[m]) if np.abs(energies[n2] - energies[m]) > threshold else 0
                    
                    # Angular momentum: expressions valid for all cases
                    # -----------------
                    
                    # Lx
                    L[0, i, j] += -1j * (Py[n1,m] * Pz[m,n2] - Pz[n1,m] * Py[m,n2]) * delta1
                    L[0, i, j] -= -1j * (Pz[n1,m] * Py[m,n2] - Py[n1,m] * Pz[m,n2]) * delta2
                    
                    # Ly
                    L[1, i, j] += -1j * (Pz[n1,m] * Px[m,n2] - Px[n1,m] * Pz[m,n2]) * delta1
                    L[1, i, j] -= -1j * (Px[n1,m] * Pz[m,n2] - Pz[n1,m] * Px[m,n2]) * delta2
                    
                    # Lz
                    L[2, i, j] += -1j * (Px[n1,m] * Py[m,n2] - Py[n1,m] * Px[m,n2]) * delta1
                    L[2, i, j] -= -1j * (Py[n1,m] * Px[m,n2] - Px[n1,m] * Py[m,n2]) * delta2
                    
                    
        
        ############################
        # g-factor = L + S
        ############################
        
        # check if spinfull or spinless
        if (Sx is None) and (Sy is None) and (Sz is None):
            # spinless case
            self.Lx = np.kron(L[0], s0)
            self.Ly = np.kron(L[1], s0)
            self.Lz = np.kron(L[2], s0)
            self.Sx = np.kron(np.eye(len(setA)), sx)
            self.Sy = np.kron(np.eye(len(setA)), sy)
            self.Sz = np.kron(np.eye(len(setA)), sz)
            self.gx = self.Lx + self.Sx
            self.gy = self.Ly + self.Sy
            self.gz = self.Lz + self.Sz
        else:
            # spinfull case
            assert (len(Sx) == len(setA)) and (len(Sy) == len(setA)) and (len(Sz) == len(setA)), "Spin matrices must match the size of setA."
            self.Lx = L[0]
            self.Ly = L[1]
            self.Lz = L[2]
            self.Sx = Sx
            self.Sy = Sy
            self.Sz = Sz
            self.gx = self.Lx + self.Sx
            self.gy = self.Ly + self.Sy
            self.gz = self.Lz + self.Sz
            
