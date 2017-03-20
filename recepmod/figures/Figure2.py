import os
import string
from matplotlib import gridspec, rcParams
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from ..StoneHelper import read_chain, getFitMeasMergedSummarized
from .FigureCommon import Igs, FcgRidx, makeFcIgLegend, subplotLabel

def makeFigure():
    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    pBest = dset.iloc[np.argmax(dset['LL']),:][2:].as_matrix()

    rcParams['lines.markeredgewidth'] = 1.0

    # Setup plotting space
    f = plt.figure(figsize=(7,6))

    # Make grid
    gs1 = gridspec.GridSpec(3,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(1,9) ]

    # Place likelihood plot
    LLplot(dset, ax[0])

    # Show predicted versus actual
    plotFit(getFitMeasMergedSummarized(M, pBest), ax = ax[1])

    # Make histogram subplots
    histSubplots(dset, axes = [ax[2], ax[3], ax[4], ax[5]])

    violinPlot(dset, ax = ax[6])

    for ii in range(len(ax)):
        subplotLabel(ax[ii], string.ascii_uppercase[ii+1])

    return f

def plotQuant(fitMean, nameFieldX, nameFieldY, ax=None, legend=True, ylabelpad=-5):
    # This should take a merged and summarized data frame

    if ax is None:
        fig = plt.figure(figsize=(7,6))
        ax = fig.add_subplot(1, 1, 1)

    for j in Igs:
        for f in FcgRidx:
            for x in range(2):
                temp = fitMean[fitMean['Ig'] == j]
                temp = temp[temp['FcgR'] == f]
                color = FcgRidx[f]

                if x == 0:
                    temp = temp[temp['TNP'] == 'TNP-4']
                    mfcVal = 'None'
                else:
                    temp = temp[temp['TNP'] != 'TNP-4']
                    mfcVal = color

                ax.errorbar(temp[nameFieldX], temp[nameFieldY], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    if legend:
        ax.legend(handles=makeFcIgLegend())

    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.ylabel(nameFieldY,labelpad=ylabelpad)
    plt.xlabel(nameFieldX)

def violinPlot(dset, ax=None):
    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    dset = dset[['Rexp']]
    dset.columns = FcgRidx.keys()

    objs = sns.violinplot(data=dset, cut=0, ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right")

def LLplot(dset, ax = None):
    # TODO: Should this maybe be a plot of the autocorrelation or geweke criterion instead?
    if ax is None:
        ax = plt.gca()

    # Find out how many walkers we had
    nwalkers = int(np.max(dset['walker'])) + 1

    # Make an index for what step values came from
    dset = dset.assign(IDX = np.repeat(range(int(dset.shape[0]/nwalkers)), nwalkers))

    # Reorganize data for plotting
    dset = dset[['LL', 'walker', 'IDX']].pivot(index = 'IDX', columns = 'walker', values = 'LL')

    # Plot LL values
    dset.plot(ax = ax, legend = False, ylim = (-100, -50))

    # Try and fix overlapping elements
    plt.tight_layout()


def histSubplots(dset, axes=None):
    if axes is None:
        _, axes = plt.subplots(nrows=1, ncols=4)

    dsetFilter = dset.loc[dset['LL'] > (np.max(dset['LL'] - 10)),:]

    dsetFilter[['Kx1']].plot.hist(ax=axes[0], bins = 20, color=sns.color_palette()[0])
    dsetFilter[['sigConv1', 'sigConv2']].plot.hist(ax=axes[1], bins = 20, color=sns.color_palette()[0:2])
    dsetFilter[['gnu1', 'gnu2']].plot.hist(ax=axes[2],
                                           bins = np.arange(-0.5, 32.5, 1.0),
                                           color=sns.color_palette()[0:2],
                                           xlim = (-0.5, 32.5))
    dsetFilter[['sigma', 'sigma2']].plot.hist(ax=axes[3], bins = 40, color=sns.color_palette()[0:2])

    # Set all the x-labels based on which histogram is displayed
    axes[0].set_xlabel('Log10(Kx)')
    axes[1].set_xlabel('Log10(Conversion Factor)')
    axes[2].set_xlabel('Effective Avidity')
    axes[3].set_xlabel('Deviation Parameter')

    # Try and fix overlapping elements
    plt.tight_layout()

    print(np.mean(np.power(10, dsetFilter.sigConv2 - dsetFilter.sigConv1)))

    print(np.power(10, np.std(dsetFilter.sigma2)))


def plotFit(fitMean, ax=None):
    if ax is None:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(1, 1, 1)

    ax.plot([0.01, 5], [0.01, 5], color='k', linestyle='-', linewidth=1)

    for _, row in fitMean.iterrows():
        colorr = FcgRidx[row['FcgR']]
        ax.errorbar(x=row['Fit'],
                    y=row['Meas_mean'],
                    yerr=row['Meas_std'],
                    marker=Igs[row['Ig']],
                    mfc=colorr,
                    mec=colorr,
                    ms=3,
                    ecolor=colorr,
                    linestyle='None')

    ax.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_ylabel('Fitted prediction')
    ax.set_xlabel('Measured ligand binding')
    ax.loglog()
    ax.set_ylim(0.01, 5)
    ax.set_xlim(0.01, 5)
