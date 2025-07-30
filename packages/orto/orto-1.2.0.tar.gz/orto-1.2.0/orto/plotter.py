import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator
import numpy as np
from numpy.typing import ArrayLike, NDArray
import itertools

from . import utils as ut


def gaussian(p: ArrayLike, fwhm: float, b: float, area: float) -> NDArray:
    """
    Gaussian g(p) with given peak position (b), fwhm, and area

    g(p) = area/(c*sqrt(2pi)) * exp(-(p-b)**2/(2c**2))

    c = fwhm/(2*np.sqrt(2*np.log(2)))

    Parameters
    ----------
    p : array_like
        Continuous variable
    fwhm: float
        Full Width at Half-Maximum
    b : float
        Peak position
    area : float
        Area of Gaussian function

    Return
    ------
    list[float]
        g(p) at each value of p
    """

    c = fwhm / (2 * np.sqrt(2 * np.log(2)))

    a = 1. / (c * np.sqrt(2 * np.pi))

    gaus = a * np.exp(-(p - b)**2 / (2 * c**2))

    gaus *= area

    return gaus


def lorentzian(p: ArrayLike, fwhm, p0, area) -> NDArray:
    """
    Lotenztian L(p) with given peak position (b), fwhm, and area

    L(p) = (0.5*area*fwhm/pi) * 1/((p-p0)**2 + (0.5*fwhm)**2)

    Parameters
    ----------
    p : array_like
        Continuous variable
    fwhm: float
        Full Width at Half-Maximum
    p0 : float
        Peak position
    area : float
        Area of Lorentzian function

    Return
    ------
    list[float]
        L(p) at each value of p
    """

    lor = 0.5 * fwhm / np.pi
    lor *= 1. / ((p - p0)**2 + (0.5 * fwhm)**2)

    lor *= area

    return lor


def plot_abs(wavenumbers: ArrayLike, foscs: ArrayLike,
             lineshape: str = 'gaussian', linewidth: float = 100.,
             x_lim: list[float] = 0., x_unit: str = 'wavenumber',
             abs_type: str = 'napierian', y_lim: list[float] = 'auto',
             show_osc: bool = True, save: bool = False,
             save_name: str = 'absorption_spectrum.png', show: bool = False,
             window_title: str = 'Absorption Spectrum') -> tuple[plt.Figure, list[plt.Axes]]: # noqa
    '''
    Plots absorption spectrum with oscillator strengths specifying intensity

    Parameters
    ----------
    wavenumbers: array_like
        Wavenumber of eac transition [cm^-1]
    foscs: array_like
        Oscillator strength of each transition
    lineshape: str {'gaussian', 'lorentzian'}
        Lineshape function to use for each transition/signal
    linewidth: float
        Linewidth used in lineshape [cm^-1]
    x_lim: list[float], default [0., 2000]
        Minimum and maximum x-values to plot [cm^-1 or nm]
    y_lim: list[float | str], default 'auto'
        Minimum and maximum y-values to plot [cm^-1 mol^-1 L]
    x_unit: str {'wavenumber', 'wavelength'}
        X-unit to use, data will be converted internally.\n
        Assumes cm^-1 for wavenumber and nm for wavelength.
    abs_type: str {'napierian', 'logarithmic'}
        Absorbance (and epsilon) type to use. Orca_mapspc uses napierian
    show_osc: bool, default True
        If True, show oscillator strength stemplots
    save: bool, default False
        If True, plot is saved to save_name
    save_name: str
        If save is True, plot is saved to this location/filename
    show: bool, default False
        If True, plot is shown on screen
    window_title: str, default 'UV-Visible Absorption Spectrum'
        Title of figure window, not of plot
    Returns
    -------
    plt.Figure
        Matplotlib Figure object
    list[plt.Axes]
        Matplotlib Axis object for main plot followed by\n
        Matplotlib Axis object for twinx oscillator strength axis
    '''

    fig, ax = plt.subplots(1, 1, num=window_title)

    ls_func = {
        'gaussian': gaussian,
        'lorentzian': lorentzian
    }

    x_range = np.linspace(x_lim[0], x_lim[1], 100000)

    # Conversion from oscillator strength to napierian integrated absorption
    # coefficient
    # This is the value of A for a harmonically oscillating electron
    A_elec = 2.31E8
    # convert to common log absorbance if desired
    if abs_type == 'log':
        A_elec /= np.log(10)
    A_logs = [fosc * A_elec for fosc in foscs]

    # Spectrum as sum of signals. Always computed in wavenumbers.
    spectrum = np.sum([
        ls_func[lineshape](x_range, linewidth, x_value, A_log)
        for x_value, A_log in zip(wavenumbers, A_logs)
    ], axis=0)

    np.savetxt('spectrum.txt', np.vstack([x_range, spectrum]).T, fmt='%.5f')

    # Convert values to wavelength
    if x_unit == 'wavelength':
        x_range = 1E7 / x_range
        wavenumbers = [1E7 / wn for wn in wavenumbers]

    # Main spectrum
    ax.plot(x_range, spectrum, color='k')

    if show_osc:
        fax = ax.twinx()
        # Oscillator strength twin axis
        plt.stem(wavenumbers, foscs, basefmt=' ')
        fax.yaxis.set_minor_locator(AutoMinorLocator())
        fax.set_ylabel(r'$f_\mathregular{osc}$')
    else:
        fax = None
        plt.subplots_adjust(right=0.2)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    if y_lim[0] != y_lim[1]:
        if isinstance(y_lim[0], str):
            y_lim[0] = ax.get_ylim()[0]
        if isinstance(y_lim[1], str):
            y_lim[1] = ax.get_ylim()[1]
        ax.set_ylim([y_lim[0], y_lim[1]])

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    xunit_to_label = {
        'wavenumber': r'Wavenumber (cm$^\mathregular{-1}$)',
        'wavelength': 'Wavelength (nm)',
    }

    ax.set_xlabel(xunit_to_label[x_unit.lower()])
    ax.set_ylabel(r'$\epsilon$ (cm$^\mathregular{-1}$ mol$^\mathregular{-1}$ L)') # noqa

    fig.tight_layout()

    if save:
        plt.savefig(save_name, dpi=500)

    if show:
        plt.show()

    return fig, [ax, fax]


def wl_to_wn(wl: float) -> float:
    if wl == 0:
        return 0.
    else:
        return 1E7 / wl


def plot_chit(chit: ArrayLike, temps: ArrayLike, fields: ArrayLike = None,
              y_unit: str = r'cm^3\,K\,mol^{-1}', # noqa
              save: bool = False, save_name: str = 'chit_vs_t.png',
              show: bool = False, window_title: str = 'Calculated Susceptibility') -> tuple[plt.Figure, plt.Axes]: # noqa
    r'''
    Plots susceptibility*T data as a function of temperature

    Parameters
    ----------
    chit: array_like
        Susceptibility * Temperature
    temps: array_like
        Temperatures in Kelvin
    fields: array_like, optional
        If specified, splits data according to applied magnetic field.\n
        One plot, with one trace per field.
    y_unit: str, default 'cm^3\ K\ mol^{-1}'
        Mathmode y-unit which matches input chit data
    save: bool, default False
        If True, plot is saved to save_name
    save_name: str, default 'chit_vs_t.png'
        If save is True, plot is saved to this location/filename
    show: bool, default False
        If True, plot is shown on screen
    window_title: str, default 'Calculated Susceptibility'
        Title of figure window, not of plot
    Returns
    -------
    plt.Figure
        Matplotlib Figure object
    plt.Axes
        Matplotlib Axis object for plot
    ''' # noqa

    # Create figure and axes
    fig, ax = plt.subplots(1, 1, figsize=(5, 4), num=window_title)

    if fields is None:
        # Plot data as it is
        ax.plot(temps, chit, color='k', label='Calculated')
    else:
        # Split data by field
        ufields = np.unique(fields)

        for ufield in ufields:
            _temp = temps[fields == ufield]
            _chit = chit[fields == ufield]
            ax.plot(
                _temp,
                _chit,
                label=f'Calculated ($H$ = {ufield:.1f} Oe)'
            )
        ax.legend(frameon=False)

    ax.set_xlabel('$T$ (K)')
    ax.set_ylabel(rf'$\chi T\,\mathregular{{({y_unit})}}$')

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    fig.tight_layout()

    if save:
        plt.savefig(save_name, dpi=500)

    if show:
        plt.show()

    return fig, ax


def plot_ir(wavenumbers: ArrayLike, linear_absorbance: ArrayLike,
            lineshape: str = 'lorentzian', linewidth: float = 10.,
            x_lim: list[float] = [None, None],
            save: bool = False, save_name: str = 'ir.png', show: bool = False,
            window_title: str = 'Infrared spectrum'):
    '''
    Plots Infrared Spectrum

    Parameters
    ----------
    wavenumbers: array_like
        Wavenumbers of each transition [cm^-1]
    linear_absorbance: array_like
        Absorbance of each transition
    lineshape: str {'gaussian', 'lorentzian'}
        Lineshape function to use for each transition/signal
    linewidth: float
        Linewidth used in lineshape [cm^-1]
    x_lim: list[float], default [None, None]
        Minimum and maximum x-values to plot [cm^-1]
    save: bool, default False
        If True, plot is saved to save_name
    save_name: str
        If save is True, plot is saved to this location/filename
    show: bool, default False
        If True, plot is shown on screen
    window_title: str, default 'Infrared Spectrum'
        Title of figure window, not of plot
    '''

    fig, ax = plt.subplots(1, 1, num=window_title)

    ls_func = {
        'gaussian': gaussian,
        'lorentzian': lorentzian
    }

    if None not in x_lim:
        x_range = np.linspace(x_lim[0], x_lim[1], 100000)
    else:
        x_range = np.linspace(0, np.max(wavenumbers) * 1.1, 100000)

    # Spectrum as sum of signals. Always computed in wavenumbers.
    spectrum = np.sum([
        ls_func[lineshape](x_range, linewidth, wavenumber, a)
        for wavenumber, a in zip(wavenumbers, linear_absorbance)
    ], axis=0)

    np.savetxt('spectrum.txt', np.vstack([x_range, spectrum]).T, fmt='%.5f')

    # Main spectrum
    ax.plot(x_range, spectrum, color='k')

    ax.set_xlim([0, np.max(x_range)])

    plt.subplots_adjust(right=0.2)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.set_xlabel(r'Wavenumber (cm$^\mathregular{-1}$)')
    ax.set_ylabel(r'$\epsilon$ (cm$^\mathregular{-1}$ mol$^\mathregular{-1}$ L)') # noqa

    fig.tight_layout()

    if save:
        plt.savefig(save_name, dpi=500)

    if show:
        plt.show()

    return fig, ax


def plot_raman(wavenumbers: ArrayLike, intensities: ArrayLike,
               lineshape: str = 'gaussian', linewidth: float = 10.,
               x_lim: list[float] = 0., x_unit: str = 'wavenumber',
               abs_type: str = 'absorption', y_lim: list[float] = 'auto',
               save: bool = False, save_name: str = 'raman.png',
               show: bool = False,
               window_title: str = 'Raman spectrum'):
    '''
    Plots Raman Spectrum
    '''

    raise NotImplementedError


def plot_cd(save: bool = False, save_name: str = 'raman.png',
            show: bool = False,
            window_title: str = 'Raman spectrum'):
    '''
    Plots circular dichroism data
    '''

    raise NotImplementedError


def plot_ailft_orb_energies(energies: ArrayLike, labels: ArrayLike = None,
                            groups: ArrayLike = None,
                            occupations: ArrayLike = None,
                            y_unit: str = r'cm^{-1}',
                            save: bool = False,
                            save_name: str = 'ai_lft_energies.png',
                            show: bool = False,
                            window_title: str = 'AI-LFT Orbital Energies',
                            verbose: bool = True) -> tuple[plt.Figure, plt.Axes]: # noqa
    '''
    Parameters
    ----------
    energies: array_like
        Energies which are in same unit as y_unit
    labels: array_like | None, optional
        If provided, labels are added next to energy levels.
    groups: array_like | None, optional
        If provided, groups orbitals together by offsetting x coordinate
    occupations: array_like | None, optional
        If provided, each orbital is populated with either 0, 1 or 2 electrons
    y_unit: str, default 'cm^{-1}'
        Mathmode y-unit which matches input chit data
    save: bool, default False
        If True, plot is saved to save_name
    save_name: str, default 'ai_lft_energies.png'
        If save is True, plot is saved to this location/filename
    show: bool, default False
        If True, plot is shown on screen
    window_title: str, default 'AI-LFT Orbital Energies'
        Title of figure window, not of plot
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    plt.Figure
        Matplotlib Figure object
    plt.Axes
        Matplotlib Axis object for plot
    '''

    fig, ax = plt.subplots(1, 1, figsize=(3.5, 3.5), num=window_title)
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    if groups is not None:
        groups = list(groups)
        groups = ut.flatten_recursive(groups)
        if len(groups) != len(energies):
            raise ValueError('Number of groups does not match number of states') # noqa
        # Split group by differing value
        groups = [list(x) for _, x in itertools.groupby(groups)]
        # X values for each group
        xvals = [list(range(len(grp))) for grp in groups]
        # Centre each group so that the middle is zero
        xvals = [g - sum(grp)/len(grp) for grp in xvals for g in grp]
    else:
        xvals = [1] * len(energies)

    ax.plot(
        xvals,
        energies,
        lw=0,
        marker='_',
        mew=1.5,
        color='k',
        markersize=25
    )

    if occupations is not None:
        if len(occupations) != len(energies):
            raise ValueError('Number of occupation numbers does not match number of states') # noqa

        # Make spin up and spin down arrow markers
        spup = mpl.markers.MarkerStyle(marker=r'$\leftharpoondown$')
        spup._transform = spup.get_transform().rotate_deg(-90)

        spdown = mpl.markers.MarkerStyle(marker=r'$\leftharpoondown$')
        spdown._transform = spdown.get_transform().rotate_deg(90)

        # Plot each marker
        for occ, en, xval in zip(occupations, energies, xvals):
            lx = xval - 1 / 10
            rx = xval + 1 / 10
            # Up and down
            if occ == 2:
                ax.scatter(lx, en, s=400, marker=spup, color='k', linewidths=0.001) # noqa
                ax.scatter(rx, en, s=400, marker=spdown, color='k', lw=0.001)
            # up
            elif occ == 1:
                ax.scatter(lx, en, s=400, marker=spup, color='k', lw=0.001)
            # down
            elif occ == -1:
                ax.scatter(rx, en, s=400, marker=spdown, color='k', lw=0.001)

    if labels is not None:
        for xval, energy, label in zip(xvals, energies, labels):
            ax.text(
                xval * 1.05,
                energy,
                rf'${label}$'
            )

    ax.set_xticklabels([])
    ax.set_xticks([])
    _lims = ax.get_xlim()
    if groups is None:
        ax.set_xlim([_lims[0]*0.9, _lims[1]*1.2])
    else:
        ax.set_xlim([_lims[0]*1.2, _lims[1]*1.2])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_ylabel(rf'Energy $\mathregular{{({y_unit})}}$')

    fig.tight_layout()

    if save:
        plt.savefig(save_name, dpi=500)
        if verbose:
            ut.cprint(f'\nAI-LFT orbitals saved to\n{save_name}', 'cyan')

    if show:
        plt.show()
