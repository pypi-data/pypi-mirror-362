import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from .solver import MpcaCIResult


def _read_labels(labels, len_u, mode):
    if not labels:
        names = [str(_) for _ in range(1,len_u+1)]
    elif type(labels) is not list:
        raise ValueError('labels should be None or a list.')
    elif type(labels[0]) is list:
        names = labels[mode]
    else:
        names = labels
    if len(names) !=  len_u:
        raise ValueError('Length of labels not matching the dimension of that mode.')

    return names

def CI_plot(result: MpcaCIResult, rank: int = 1, mode: int = 1, confidence: float = 0.95, 
           labels = None, y_as_value: bool = True, flip: bool = False):
    """ Plotting multiway PC component as a x-y or y-x scatter plot with confidence intervals (error bars).

    Parameters:
    -----------
    result: MpcaCIResult
        The result dictionary returned by mpca_CI containing:
        - components: list of PC components
        - asymptotic_parameters: asymptotic parameters array
        - debiasing_factors: debiasing factors array
    rank: int
        an integer between 1 and r, default to 1
    mode: int
        an integer between 1 and the total number of modes, default to 1
    confidence: float
        0 < confidence < 1, default to 0.95
    labels:
        can be:
        (1) None
        (2) A list of length equal to the dimension of that mode, containing labels of that mode
        (3) A length = number of modes list of lists, each list contains the labels of each mode
    y_as_value: bool
        if True, plot as x-y plot
        else, plot as y-x plot
    flip: bool
        Should the sign of the plotted PC be flipped? Default to False.

    Returns:
    --------
    ax: a matplotlib axe
    """

    def CI_one(u, asy, debias, ax):
        z_value = st.norm.ppf( 1 - (1-confidence)/2 )
        if y_as_value:
            ax.errorbar(y = u*debias, x = list(range(len(u))), yerr = z_value * np.sqrt(1-u**2)*asy, capsize = 5, capthick = 1.5, fmt = 'o')
        else:
            ax.errorbar(x = u*debias, y = list(range(len(u))), xerr = z_value * np.sqrt(1-u**2)*asy, capsize = 5, capthick = 1.5, fmt = 'o')

    ### error messages
    if confidence <= 0 or confidence>= 1:
        raise ValueError('confidence should be between 0 and 1')
    ###

    u = result['components'][rank-1][mode-1]
    if flip:
        u = -u
    asy = result['asymptotic_parameters'][rank-1]
    debias = result['debiasing_factors'][rank-1, mode-1]

    names = _read_labels(labels, len(u), mode)

    ax = plt.subplot()
    if y_as_value:
        ax.set_xticks(list(range(len(names))), names)
    else:
        ax.set_yticks(list(range(len(names))), names)
    CI_one(u, asy, debias, ax)
    ax.set_title('Confidence Interval of Mode = ' + str(mode) + ', PC ' + str(rank))
    return ax

def CI_band_plot(result: MpcaCIResult, rank: int = 1, mode: int = 1, confidence: float = 0.95,
                labels = None, flip: bool = False):
    """ Plotting multiway PC component as a x-y line plot with confidence band.
    It should only be used if one of the modes can be treated as continuous, for instance, years or months, so that a line plot is appropriate.

    Parameters:
    -----------
    result: MpcaCIResult
        The result dictionary returned by mpca_CI containing:
        - components: list of PC components
        - asymptotic_parameters: asymptotic parameters array
        - debiasing_factors: debiasing factors array
    rank: int
        an integer between 1 and r, default to 1
    mode: int
        an integer between 1 and the total number of modes, default to 1
    confidence: float
        0 < confidence < 1, default to 0.95
    labels:
        can be:
        (1) None
        (2) A list of length equal to the dimension of that mode, containing labels of that mode
        (3) A length = number of modes list of lists, each list contains the labels of each mode
    flip: bool
        Should the sign of the plotted PC be flipped? Default to False.

    Returns:
    --------
    ax: a matplotlib axis
    """
    def CI_band_one(u, asy, debias, ax):
        z_value = st.norm.ppf( 1 - (1-confidence)/2 )
        ax.plot(list(range(len(u))), u*debias)
        ax.fill_between(list(range(len(u))), u*debias-z_value*np.sqrt(1-u**2)*asy, u*debias+z_value*np.sqrt(1-u**2)*asy, alpha=0.2)

    ### error messages
    if confidence <= 0 or confidence>= 1:
        raise ValueError('confidence should be between 0 and 1')
    ###

    u = result['components'][rank-1][mode-1]
    if flip:
        u = -u
    asy = result['asymptotic_parameters'][rank-1]
    debias = result['debiasing_factors'][rank-1, mode-1]

    names = _read_labels(labels, len(u), mode)

    ax = plt.subplot()
    CI_band_one(u, asy, debias, ax)
    ax.set_xticks(ticks = list(range(len(names))), labels = names)
    ax.set_title('Confidence Interval of Mode = ' + str(mode) + ', PC ' + str(rank))
    return ax

def loading_plot(result: MpcaCIResult, rank1: int = 1, rank2: int = 2, mode: int = 1, labels = None):
    """ Plotting two multiway PC components of the same mode (different ranks) on a x-y scatter plot. It is the counterpart of the loading plot of PCA.

    Parameters:
    -----------
    result: MpcaCIResult
        The result dictionary returned by mpca_CI containing:
        - components: list of PC components
        - asymptotic_parameters: asymptotic parameters array
        - debiasing_factors: debiasing factors array
    rank1: int
        an integer between 1 and r, default to 1
    rank2: int
        an integer between 1 and r, default to 1
    mode: int
        an integer between 1 and the total number of modes, default to 1
    labels:
        can be:
        (1) None
        (2) A list of length equal to the dimension of that mode, containing labels of that mode
        (3) A length = number of modes list of lists, each list contains the labels of each mode

    Returns:
    --------
    ax: a matplotlib axis
    """
    def lp_one(u1, asy1, debias1, u2, asy2, debias2, ax):
        ax.errorbar(x = u1*debias1, y = u2*debias2, xerr = np.sqrt(1-u1**2)*asy1, yerr = np.sqrt(1-u2**2)*asy2, fmt = 'o')

    u1 = result['components'][rank1-1][mode-1]
    asy1 = result['asymptotic_parameters'][rank1-1]
    debias1 = result['debiasing_factors'][rank1-1, mode-1]

    u2 = result['components'][rank2-1][mode-1]
    asy2 = result['asymptotic_parameters'][rank2-1]
    debias2 = result['debiasing_factors'][rank2-1, mode-1]

    names = _read_labels(labels, len(u1), mode)

    ax = plt.subplot()
    ax.set_title('Loading Plot of Mode = ' + str(mode))
    ax.set_xlabel("PC " + str(rank1))
    ax.set_ylabel("PC " + str(rank2))
    for name, x, y in zip(names, u1*debias1, u2*debias2):
        ax.annotate(name, (x,y),
                     textcoords="offset points", # how to position the text
                     xytext=(10,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    lp_one(u1, asy1, debias1, u2, asy2, debias2, ax)
    return ax
