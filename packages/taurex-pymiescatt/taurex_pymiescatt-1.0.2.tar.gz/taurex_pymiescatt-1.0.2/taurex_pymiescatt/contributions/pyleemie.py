from taurex.contributions import Contribution
import numpy as np
import numba
from taurex.data.fittable import fitparam
from taurex.exceptions import InvalidModelException

@numba.jit(nopython=True, nogil=True)
def contribute_mie_tau(startK, endK, sigma, path, ngrid, layer, tau):
    for k in range(startK, endK):
        _path = path[k]
        for wn in range(ngrid):
            tau[layer, wn] += sigma[k+layer, wn]*_path

class PyLeeMieMultiContribution(Contribution):
    """
    Computes Mie scattering contribution to optica depth
    Formalism taken from: Lee et al. 2013, ApJ, 778, 97
    Parameters
    ----------
    lee_mie_radius: list
        Particle radius in um
    lee_mie_q: list
        Extinction coefficient
    lee_mie_mix_ratio: list
        Mixing ratio in atmosphere
    lee_mie_bottomP: list
        Bottom of cloud deck in Pa
    lee_mie_topP: list
        Top of cloud deck in Pa
    """

    def __init__(self, lee_mie_radius=[0.01], lee_mie_q=[40],
                 lee_mie_mix_ratio=[1e-10], lee_mie_midP=[-1],
                 lee_mie_rangeP=[1], particle_distrib = 'exp_decay'):

        self._mie_radius = np.array(lee_mie_radius) if isinstance(lee_mie_radius,list) else np.array([lee_mie_radius,])
        self._mie_q = np.array(lee_mie_q) if isinstance(lee_mie_q,list) else np.array([lee_mie_q,])
        self._mie_mix = np.array(lee_mie_mix_ratio) if isinstance(lee_mie_mix_ratio,list) else np.array([lee_mie_mix_ratio,])
        self._mie_midP = np.array(lee_mie_midP) if isinstance(lee_mie_midP,list) else np.array([lee_mie_midP,])
        self._mie_rangeP = np.array(lee_mie_rangeP) if isinstance(lee_mie_rangeP,list) else np.array([lee_mie_rangeP,])
        self._numMie = len(self._mie_radius)
        self._particle_distib = particle_distrib
        if (len(self._mie_mix) != self._numMie) or (len(self._mie_q) != self._numMie) or (len(self._mie_midP) != self._numMie) or (len(self._mie_rangeP) != self._numMie):
            print('Lee arrays are not the same len')
            raise InvalidModelException

        super().__init__('Mie')
        
        self.generate_radius_fitting_params()
        self.generate_mix_fitting_params()
        self.generate_q_fitting_params()
        self.generate_press_fitting_params()

    def contribute(self, model, start_layer, end_layer,
                    density_offset, layer, density, tau, path_length=None):

            contribute_mie_tau(start_layer, end_layer, self.sigma_xsec, path_length, self._ngrid, layer, tau)
        
    def mieRadius(self):
        """
        Particle radius in um
        """
        return self._mie_radius

    def mieQ(self):
        """
        Extinction coefficient
        """
        return self._mie_q

    def mieMidPressure(self):
        """
        Pressure at top of cloud deck in Pa
        """
        return self._mie_midP

    def mieRangePressure(self):
        """
        Pressure at bottom of cloud deck in Pa
        """
        return self._mie_rangeP

    def mieMixing(self):
        """
        Mixing ratio in atmosphere
        """
        return self._mie_mix
    
    
    def generate_radius_fitting_params(self):
        """Generates the fitting parameters
        """
        bounds = [0.01, 10]
        for idx, val in enumerate(self._mie_radius):
            num = idx+1
            param_name = 'lee_mie_radius_{}'.format(num)
            param_latex = '$LeeRadius_{}$'.format(num)

            def read_radius(self, idx=idx):
                return self._mie_radius[idx]

            def write_radius(self, value, idx=idx):
                self._mie_radius[idx] = value

            fget_radius = read_radius
            fset_radius = write_radius
            default_fit = False
            self.add_fittable_param(param_name, param_latex, fget_radius,
                                    fset_radius, 'log', default_fit, bounds)
    def generate_mix_fitting_params(self):
        """Generates the fitting parameters
        """
        bounds = [1e-22, 1e-4]
        for idx, val in enumerate(self._mie_mix):
            num = idx+1
            param_name = 'lee_mie_mix_ratio_{}'.format(num)
            param_latex = '$LeeX_{}$'.format(num)

            def read_mix(self, idx=idx):
                return self._mie_mix[idx]

            def write_mix(self, value, idx=idx):
                self._mie_mix[idx] = value

            fget_mix = read_mix
            fset_mix = write_mix
            default_fit = False
            self.add_fittable_param(param_name, param_latex, fget_mix,
                                    fset_mix, 'log', default_fit, bounds)
    def generate_q_fitting_params(self):
        """Generates the fitting parameters
        """
        bounds = [1, 99]
        for idx, val in enumerate(self._mie_q):
            num = idx+1
            param_name = 'lee_mie_q_{}'.format(num)
            param_latex = '$LeeQ_{}$'.format(num)

            def read_q(self, idx=idx):
                return self._mie_q[idx]

            def write_q(self, value, idx=idx):
                self._mie_q[idx] = value

            fget_q = read_q
            fset_q = write_q
            default_fit = False
            self.add_fittable_param(param_name, param_latex, fget_q,
                                    fset_q, 'log', default_fit, bounds)
    def generate_press_fitting_params(self):
        """Generates the fitting parameters
        """
        bounds_midP = [1e6, 1e0]
        bounds_rangeP = [0.0, 3]
        for idx, val in enumerate(self._mie_midP):
            num = idx+1
            param_name = 'lee_mie_midP_{}'.format(num)
            param_latex = '$LeeMidP_{}$'.format(num)
            def read_midP(self, idx=idx):
                return self._mie_midP[idx]
            def write_midP(self, value, idx=idx):
                self._mie_midP[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_midP,
                                    write_midP, 'log', default_fit, bounds_midP)

            param_name = 'lee_mie_rangeP_{}'.format(num)
            param_latex = '$LeeRangeP_{}$'.format(num)
            def read_rangeP(self, idx=idx):
                return self._mie_rangeP[idx]
            def write_rangeP(self, value, idx=idx):
                self._mie_rangeP[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_rangeP,
                                    write_rangeP, 'linear', default_fit, bounds_rangeP)

    def prepare_each(self, model, wngrid):
        """
        Computes and weights the mie opacity for
        the pressure regions given
        Parameters
        ----------
        model: :class:`~taurex.model.model.ForwardModel`
            Forward model
        wngrid: :obj:`array`
            Wavenumber grid
        Yields
        ------
        component: :obj:`tuple` of type (str, :obj:`array`)
            ``Lee`` and the weighted mie opacity.
        """
        self._nlayers = model.nLayers
        self._ngrid = wngrid.shape[0]

        pressure_profile = model.pressureProfile
        sigma_xsec = np.zeros(shape=(self._nlayers, wngrid.shape[0]))
        
        for i in range(0,self._numMie):

            wltmp = 10000/wngrid

            a = self._mie_radius[i]

            x = 2.0 * np.pi * a / wltmp
            self.debug('wngrid %s', wngrid)
            self.debug('x %s', x)
            Qext = 5.0 / (self._mie_q[i] * x**(-4.0) + x**(0.2))

            sigma_xsec_int = np.zeros(shape=(self._nlayers, wngrid.shape[0]))

            # This must transform um to the xsec format in TauREx (m2)
            am = a * 1e-6

            sigma_mie = Qext * np.pi * (am**2.0)

            self.debug('Qext %s', Qext)
            self.debug('radius um %s', a)
            self.debug('sigma %s', sigma_mie)

            if self._mie_midP[i] == -1:
                bottom_pressure = pressure_profile[0]
                top_pressure = pressure_profile[-1]
            else:
                bottom_pressure = 10**(np.log10(self._mie_midP[i]) + self._mie_rangeP[i]/2)
                top_pressure = 10**(np.log10(self._mie_midP[i]) - self._mie_rangeP[i]/2)

            self.debug('bottome_pressure %s', bottom_pressure)
            self.debug('top_pressure %s', top_pressure)

            cloud_filter = (pressure_profile <= bottom_pressure) & \
                (pressure_profile >= top_pressure)

            sigma_xsec_int[cloud_filter, ...] = sigma_mie * self._mie_mix[i]
            ## This line implied that self._mie_mix is expressed in m-3
            if self._particle_distib == 'exp_decay':
                ## if we want it with exp decay style Whitten et al. 2008 / Attreya et al. 2005
                decay = -5
                mix = self._mie_mix[i]*(1-np.exp(decay*(pressure_profile-top_pressure)/(bottom_pressure-top_pressure)))
                sigma_xsec_int[cloud_filter, :] = sigma_mie[None] * mix[cloud_filter, None]
            else:
                sigma_xsec_int[cloud_filter, ...] = sigma_mie * self._mie_mix[i]

            sigma_xsec += sigma_xsec_int
        self.sigma_xsec =sigma_xsec

        self.debug('final xsec %s', self.sigma_xsec)

        yield 'Lee', sigma_xsec

    def write(self, output):
        contrib = super().write(output)
        contrib.write_array('lee_mie_radius', self._mie_radius)
        contrib.write_array('lee_mie_q', self._mie_q)
        contrib.write_array('lee_mie_mix_ratio', self._mie_mix)
        contrib.write_array('lee_mie_midP', self._mie_midP)
        contrib.write_array('lee_mie_rangeP', self._mie_rangeP)
        return contrib

    @classmethod
    def input_keywords(self):
        return ['PyLeeMieMultiple', ]
    
    BIBTEX_ENTRIES = [
        """
        @article{Lee_2013,
            doi = {10.1088/0004-637x/778/2/97},
            url = {https://doi.org/10.1088%2F0004-637x%2F778%2F2%2F97},
            year = 2013,
            month = {nov},
            publisher = {{IOP} Publishing},
            volume = {778},
            number = {2},
            pages = {97},
            author = {Jae-Min Lee and Kevin Heng and Patrick G. J. Irwin},
            title = {{ATMOSPHERIC} {RETRIEVAL} {ANALYSIS} {OF} {THE} {DIRECTLY} {IMAGED} {EXOPLANET} {HR} 8799b},
            journal = {The Astrophysical Journal},
            abstract = {Directly imaged exoplanets are unexplored laboratories for the application of the spectral and temperature retrieval method, where the chemistry and composition of their atmospheres are inferred from inverse modeling of the available data. As a pilot study, we focus on the extrasolar gas giant HR 8799b, for which more than 50 data points are available. We upgrade our non-linear optimal estimation retrieval method to include a phenomenological model of clouds that requires the cloud optical depth and monodisperse particle size to be specified. Previous studies have focused on forward models with assumed values of the exoplanetary properties; there is no consensus on the best-fit values of the radius, mass, surface gravity, and effective temperature of HR 8799b. We show that cloud-free models produce reasonable fits to the data if the atmosphere is of super-solar metallicity and non-solar elemental abundances. Intermediate cloudy models with moderate values of the cloud optical depth and micron-sized particles provide an equally reasonable fit to the data and require a lower mean molecular weight. We report our best-fit values for the radius, mass, surface gravity, and effective temperature of HR 8799b. The mean molecular weight is about 3.8, while the carbon-to-oxygen ratio is about unity due to the prevalence of carbon monoxide. Our study emphasizes the need for robust claims about the nature of an exoplanetary atmosphere to be based on analyses involving both photometry and spectroscopy and inferred from beyond a few photometric data points, such as are typically reported for hot Jupiters.}
        }
        """,
    ]