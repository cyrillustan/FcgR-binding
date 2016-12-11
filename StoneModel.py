import numpy as np
from math import *
from scipy.optimize import brentq
from scipy.stats import norm
from scipy.misc import comb
from memoize import memoize
import warnings
from os.path import join

nan = float('nan')
inf = float('inf')

class StoneModel:
    ## The purpose of this function is to calculate the value of Req (from Equation 1 from Stone) given parameters R,
    ## kai=Ka,Li=L, vi=v, and kx=Kx. It does this by performing the bisction algorithm on Equation 2 from Stone. The
    ## bisection algorithm is used to find the value of log10(Req) which satisfies Equation 2 from Stone.
    def ReqFuncSolver(self, R, ka, Li, vi, kx):
        ## a is the lower bound for log10(Req) bisecion. By Equation 2, log10(Req) is necessarily lower than log10(R).
        a = -20
        b = log10(R)

        ## Create anonymous function diffFunAnon which calls diffFun for parameters R, vi=v, kx=Kx, and viLikdi.
        ## This function subtracts the right side of Equation 2 from Stone from the left side of the same Equation. The
        ## bisection algorithm is run using this function so as to calculate log10(Req) which satisfies all parameters.
        ## Each time this function is called: x is log10 of the value of Req being tested, R is R from Stone 2, vi is v from
        ## Stone 2, kx is Kx from Stone 2, and viLikdi is a product which is constant over all iterations of the bisection
        ## algorithm over diffFun for a single calling of ReqFuncSolver.
        diffFunAnon = lambda x: R-(10**x)*(1+vi*Li*ka*(1+kx*(10**x))**(vi-1))

        if diffFunAnon(a)*diffFunAnon(b) > 0:
            return np.nan

        ## Implement the bisection algorithm using SciPy's brentq. Please see SciPy documentation for rationale behind
        ## input parameter not described beforehand. Brentq is ~2x faster than bisect
        logReq = brentq(diffFunAnon, a, b, disp=False)

        return logReq

    @memoize
    def nchoosek(self, n, k):
        return comb(n, k, exact=True)

    def normalizeData(self, filepath):
        ## Read in the csv data for the first experiments. lux1 is an iterable data
        ## structure wherein each iterable element is a single-element list containing a
        ## string. Each such string represents a single row from the csv.
        book4 = np.loadtxt(filepath, delimiter=',', skiprows=2, usecols=list(range(2,10)))

        ## The first row in every set of five rows in book4 consists of background
        ## MFIs. book5 is made by taking each of the four non-background MFIs from
        ## reach cluster of 5 from book4, subtracting the corresponding background
        ## MFI from each, and then forming a NumPy array of shape (24,8) from all of
        ## these collectively. The final result, book5, will be a NumPy array of
        ## shape (1,192).
        book5 = np.array([])
        for j in range(len(book4)):
            if j%5 == 0:
                temp = np.array(book4[j])
            else:
                temp2 = np.array(book4[j])-temp
                book5 = np.concatenate((book5,temp2),0)
        ## Reshape book5 into a NumPy array of shape (24,8), the actual shape of the
        ## MFIs from Lux's original experiments.
        book5 = np.reshape(book5,(24,8))
        ## Transponse book5, so that all the elements in rows n and n+4 correspond to
        ## the same replicate (for all n in {0,1,2,3}; Python indexing used). Then,
        ## concatenate both rows in a single replicate, and take the mean of the
        ## resulting array. This mean will correspond to the normalizing factor by
        ## which the corresponding replicate is normalized. These are first contained
        ## the (1,4) NumPy array means.
        temp = np.transpose(book5)
        means = [np.nanmean(np.concatenate((temp[j],temp[j+4]))) for j in range(4)]
        ## Concatenate means with itself to result in a (1,8) NumPy array, means2
        means2 = np.concatenate((means,means))
        ## Concatenate means2 with itself until a NumPy array of shape (1,192) is
        ## created. This array is titled "temp." Then, reshape temp into a (24,8)
        ## NumPy array called "noise." Each element in book5 must be divided by the
        ## corresponding element in temp in order to be normalized.
        temp = means2
        for j in range(book5.shape[0]-1):
            temp = np.concatenate((temp,means2))
        noise = np.reshape(temp,(24,8))
        ## Create mfiAdjMean1 by dividing book5 by noise.
        return(book5/noise)

    def StoneMod(self,logR,Ka,v,logKx,L0,fullOutput = False,skip=False):
        ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
        ## receptors, granted each epitope of the ligand binds to the receptor
        ## kind in question with dissociation constant Kd and cross-links with
        ## other receptors with crosslinking constant Kx = 10^logKx. All
        ## equations derived from Stone et al. (2001). Assumed that ligand is at
        ## saturating concentration L0 = 7e-8 M, which is as it is (approximately)
        ## for TNP-4-BSA in Lux et al. (2013).
        Kx = 10**logKx
        v = np.int_(v)

        ## Vector of binomial coefficients
        Req = 10**self.ReqFuncSolver(10**logR,Ka,L0,v,Kx)
        if isnan(Req):
            return (nan, nan, nan, nan)

        # Calculate vieq from equation 1
        vieqIter = (L0*Ka*self.nchoosek(v,j+1)*Kx**j*Req**(j+1) for j in range(v))
        vieq = np.fromiter(vieqIter, np.float, count = v)

        ## Calculate L, according to equation 7
        Lbound = np.sum(vieq)

        # If we just need the amount of ligand bound, exit here.
        if fullOutput == False:
            return (Lbound, nan, nan, nan)

        # Calculate Rmulti from equation 5
        RmultiIter = ((j+1)*vieq[j] for j in range(1,v))
        Rmulti = np.sum(np.fromiter(RmultiIter, np.float, count = v-1))

        # Calculate Rbound
        RbndIter = ((j+1)*vieq[j] for j in range(v))
        Rbnd = np.sum(np.fromiter(RbndIter, np.float, count = v))

        # Calculate numXlinks from equation 4
        nXlinkIter = (j*vieq[j] for j in range(1,v))
        nXlink = np.sum(np.fromiter(nXlinkIter, np.float, count = v-1))

        return (Lbound, Rbnd, Rmulti, nXlink)

    ## This function returns the log likelihood of a point in an MCMC against the ORIGINAL set of data.
    ## This function takes in a NumPy array of shape (12) for x, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
    ## tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
    ## logarithms of the receptor expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
    ## the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
    ## logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
    ## of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
    ## standard deviation of MFIs for that condition.
    def NormalErrorCoefcalc(self, x, mfiAdjMean, skip=False):
        ## Set the standard deviation coefficient
        sigCoef = 10**x[11]

        ## Set thecommon logarithm of the Kx coefficient
        logKxcoef = x[6]
        logSqrErr = 0

        ## Iterate over each kind of TNP-BSA (4 or 26)
        for j in range(2):
            ## Set the effective avidity for the kind of TNP-BSA in question
            v = x[9+j]
            ## Set the MFI-per-TNP-BSA conversion ratio for the kind of TNP-BSA in question
            c = 10**x[7+j]
            ## Set the ligand (TNP-BSA) concentration for the kind of TNP-BSA in question
            L0 = self.tnpbsa[j]

            ## Iterate over each kind of FcgR
            for k in range(6):
                ## Skip over the FcgRIIA-His MFIs if using the new data
                if k == 1 and skip:
                    continue
                ## Set the common logarith of the level of receptor expression for the FcgR in question
                print(k)
                logR = x[k]

                if isnan(logR):
                    continue;

                ## Iterate over each kind of IgG
                for l in range(4):
                    ## Set the affinity for the binding of the FcgR and IgG in question
                    Ka = self.kaBruhns[k][l]
                    if isnan(Ka):
                        continue

                    # Setup the data
                    temp = mfiAdjMean[4*k+l][4*j:4*j+3]
                    # If data not available, skip
                    if np.any(np.isnan(temp)):
                        continue

                    ## Calculate the Kx value for the combination of FcgR and IgG in question. Then, take the common logarithm of this value.
                    logKx = logKxcoef - log10(Ka)

                    ## Calculate the MFI which should result from this condition according to the model
                    MFI = c*(self.StoneMod(logR,Ka,v,logKx,L0))[0]
                    if isnan(MFI):
                        return -inf

                    ## Iterate over each real data point for this combination of TNP-BSA, FcgR, and IgG in question, calculating the log-likelihood
                    ## of the point assuming the calculated point is true.
                    tempm = norm.logpdf(temp, MFI, sigCoef*MFI)
                    if np.any(np.isnan(tempm)):
                        return -inf

                    ## For each TNP-BSA, have an array which includes the log-likelihoods of all real points in comparison to the calculated values.
                    ## Calculate the log-likelihood of the entire set of parameters by summing all the calculated log-likelihoods.
                    logSqrErr = logSqrErr+np.nansum(tempm)

        return logSqrErr

    # This should do the same as NormalErrorCoef above, but with the second batch of Nimmerjahn data and specified
    # Receptor expression levels
    def NormalErrorCoefRset(self, x):
        return self.NormalErrorCoefcalc(np.concatenate((self.Rquant, x)), self.mfiAdjMean2, skip=True)

    def NormalErrorCoef(self, x):
        return self.NormalErrorCoefcalc(x, self.mfiAdjMean1)

    def __init__(self):
        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = './Nimmerjahn Lab and Bruhns Data'

        ## Define the matrix of Ka values from Bruhns
        ## For accuracy, the Python implementation of this code will use
        ## Ka values as opposed to Kd, as these were the values which Bruhns
        ## gives in his experiments. These are read in from a csv in the
        ## folder Nimmerjahn Lab and Bruhns Data. Each row represents a particular
        ## FcgR (FcgRIA, FcgRIIA-H, FcgRIIA-R, FcgRIIB, FcgRIIIA-F, FcgRIIIA-V)
        ## and each column represents a particular IgG(1, 2, 3, 4).

        ## First, read in the csv. It will result in an iterable object, wherein
        ## each element is a single-element list containing a single string, each
        ## string corresponding to a single row from the csv.
        self.kaBruhns = np.loadtxt(join(path,'FcgR-Ka-Bruhns.csv'), delimiter=',')

        ## Define concentrations of TNP-4-BSA and TNP-26-BSA, respectively
        ## These are put into the numpy array "tnpbsa"
        self.tnpbsa = np.array([1/67122,1/70928])*1e-3*5

        ## Create the NumPy array Rquant, where each row represents a particular
        ## IgG (1,2,3, or 4) and each column corresponds to a particular FcgR
        ## (FcgRIA, FcgRIIA-H,FcgRIIA-R, FcgRIIB, FcgRIIIA-F, and FcgRIIIA-V)

        ## Read in the receptor quantifications for the Nimmerjahn Lab's second
        ## set of data. Using the function reader from the csv library, this data
        ## is used to make the iterable object quant, each iterable element of
        ## which is a single-element list containing a string corresponding to
        ## a row in the original csv.
        self.Rquant = np.loadtxt(join(path,'FcgRquant.csv'), delimiter=',', skiprows=1)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.Rquant = np.nanmean(self.Rquant, axis=0)

        self.Rquant = np.log10(self.Rquant)

        ## To begin, read in the MFI measurements from both of Lux's experiments from
        ## their respective csvs. Then, subtract background MFIs from these nominal
        ## MFIs. Then, normalize the data by replicate. For each step after the
        ##reading, I manipulated the csv data in different ways, which are explained
        ## in the comments. Please refer to these comments to understand what is
        ## going on, especially with variables of the name "book$" or "temp$." All
        ## variables with such names are only meant to construct mfiAdjMean1 (from
        ## Lux's first experiments) and mfiAdjMean2 (from Lux's second experiments).

        # Load and normalize dataset one
        self.mfiAdjMean1 = self.normalizeData(join(path,'Luxetal2013-Fig2B.csv'))

        # Load and normalize dataset two
        self.mfiAdjMean2 = self.normalizeData(join(path,'New-Fig2B.csv'))
