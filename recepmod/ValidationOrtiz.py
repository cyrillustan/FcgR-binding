import pandas as pd
import numpy as np
from .StoneNRecep import StoneN

class Ortiz:
    def __init__(self):
        import os

        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = os.path.dirname(os.path.abspath(__file__))
        self.Igs = ['IgG1', 'IgG2', 'IgG3', 'IgG4']
        self.FcgRs = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']

        ## Define the matrix of Ka values from Bruhns
        self.kaBruhns = np.loadtxt(os.path.join(path,'./data/FcgR-Ka-Bruhns.csv'), delimiter=',')

        ## The valency and names of the different species
        self.valency = np.array([1, 2, 3, 3, 5, 5], dtype = np.int)
        self.structs = ['Fc1', 'Fc2', 'Fc3Y', 'Fc3L', 'Fc5X', 'Fc5Y']

        ## Read in the Fc responses
        self.FcResponse = pd.read_csv(os.path.join(path,'./data/ortiz/Fig2DE-response.csv'), comment='#')

    def predictResponse(self):
        ''' Predict the response measured. '''

        Ka = [self.kaBruhns[0][0], self.kaBruhns[0][0]] # The affinity of the relevant interaction
        logR = [2, 3]

        outt = []

        for ii, item in enumerate(self.structs):
            TwoModel = StoneN(logR, Ka, Kx=1E-9, gnu=self.valency[ii], L0=1E-4)

            result = TwoModel.getAllProps()
            result.name = item

            outt.append(result)

        pTable = pd.concat(outt, axis=1).T




