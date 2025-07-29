from taurex.contributions.contribution import Contribution
import numpy as np
from taurex.data.fittable import fitparam
import numba
import scipy.stats as stats
from taurex.exceptions import InvalidModelException
from taurex.util.util import create_grid_res



@numba.jit(nopython=True, nogil=True)
def contribute_mie_tau(startK, endK, sigma, path, ngrid, layer, tau):
    for k in range(startK, endK):
        _path = path[k]
        for wn in range(ngrid):
            tau[layer, wn] += sigma[k+layer, wn]*_path

class InvalidPyMieScattException(InvalidModelException):
    """
    Exception that is called when the contributio fails
    """
    pass

class PyMieScattExtinctionAggregateContribution(Contribution):
    """
    Computes Mie scattering contribution to optica depth
    using the Bohren and Huffmann in its PyMieScatt implementation.
    Aggregate theory is from Akimasa et al. 2014 A&A, Volume 568, id.A42, 15 pp (https://ui.adsabs.harvard.edu/abs/2014A%26A...568A..42K/abstract)

    Parameters
    ----------
    mie_particle_mean_radius: Mean radius of the particles in um
    mie_particle_mix_ratio: Number density in molecules/m^3 --> Divide this number by 1,000,000 to get this in more common molecules/cm^3
    mie_midP: Middle of the clouds in Pa
    mie_rangeP: Extend of the clouds in log scale. If mie_midP = 1e5 Pa and mie_rangeP = 1 then clouds extend from 1e6 to 1e4 Pa
    """

    def __init__(self, mie_particle_mean_radius=0.001, 
                 mie_particle_logstd_radius = 0.001, ## Serves for the normaly distributed particle size distribution.
                 mie_particle_paramA = 1., mie_particle_paramB = 6., mie_particle_paramC = 6., mie_particle_paramD = 1., ## Serves for Deirmendjian particle size distribution.
                 mie_particle_radius_Nsampling = 5, mie_particle_radius_Dsampling = 2, ## Is used for sampling the particle distribution.
                 mie_particle_radius_distribution = 'normal', ## choices are 'normal', 'budaj', 'deirmendjian'.
                 mie_species_path=None, species = ['MgSiO4'], file_extension = '.refrind',
                 mie_particle_mix_ratio=1e-10, 
                 mie_filling_factors = [0.01, 0.2],
                 renormalize_factors = True,
                 mie_effective_filling_factor = 0.1,
                 #mie_bottomP=[-1],
                 #mie_topP=[-1], 
                 mie_midP = 1e3,
                 mie_rangeP = 1,
                 mie_nMedium=1, 
                 mie_resolution = 100,
                 mie_particle_altitude_distrib = 'exp_decay',
                 mie_particle_altitude_decay = -5, ## Controls the decay rate, inspired by Whitten et al. 2008 / Attreya et al. 2005
                 usecols=(0,1,2), skiprows=0, reverse=False, name = 'Agg'):
        super().__init__(name)

        self._mie_particle_mean_radius = mie_particle_mean_radius
        self._mie_particle_std_radius = mie_particle_logstd_radius
        self._mie_particle_paramA = mie_particle_paramA
        self._mie_particle_paramB = mie_particle_paramB
        self._mie_particle_paramC = mie_particle_paramC
        self._mie_particle_paramD = mie_particle_paramD

        if mie_particle_radius_distribution == 'deirmendjian':
            self._mie_particle_mean_radius = None
            self.warning('The Rmean parameter is being disabled because not needed for Deirmendjian 1964 particle distribution')
        else:
            self._mie_particle_paramA = None
            self.warning('The mie_particle_paramA parameter is being disabled because only used in Deirmendjian 1964 particle distribution')

        if mie_particle_radius_distribution == 'budaj':
            self._mie_particle_std_radius = None
            self.warning('The Rlogstd parameter is being disabled because not needed for Bujaj 2015 particle distribution')       

        self._mie_particle_radius_distribution = mie_particle_radius_distribution

        self._mie_particle_mix_ratio = mie_particle_mix_ratio
        #self._mie_bottom_pressure = mie_bottomP
        #self._mie_top_pressure = mie_topP
        self._mie_midP = mie_midP
        self._mie_rangeP = mie_rangeP

        self._Nsampling = int(mie_particle_radius_Nsampling)
        self._Dsampling = mie_particle_radius_Dsampling

        self._mie_species_path = mie_species_path
        self._species = species

        self._particle_alt_distib = mie_particle_altitude_distrib
        self._particle_alt_decay = mie_particle_altitude_decay
        self._file_extension = file_extension
        self._mie_nMedium = mie_nMedium
        self._renormalize_factors = renormalize_factors

        self._wls, self._cindexes, _ = self.load_input_files(self._mie_species_path, 
                                                self._species, self._file_extension, 
                                                int(skiprows), np.array(usecols).astype(int), reverse)
        
        self._mie_filling_factors = mie_filling_factors/np.sum(mie_filling_factors)
        self._mie_effective_filling_factor = mie_effective_filling_factor
        self._resolution = mie_resolution
        self.generate_particle_fitting_params()

    def load_input_files(self, path, species, extension, skiprows=0, usecols=(0,1,2), reverse=False):
        paths = []
        wls = []
        cindexes = []
        for idx, s in enumerate(species):  
            f = path+'/'+s+extension
            data = np.loadtxt(f, skiprows = skiprows, usecols=usecols)
            paths.append(f)
            
            order = np.argsort(data[:,0])

            wls.append(data[order,0])
            cindexes.append(data[order,1]+data[order,2]*1j)
        return wls, cindexes, paths

    def contribute(self, model, start_layer, end_layer,
                   density_offset, layer, density, tau, path_length=None):

        contribute_mie_tau(start_layer, end_layer, self.sigma_xsec, path_length, self._ngrid, layer, tau)

    def generate_particle_fitting_params(self):

        bounds_Rm = [0.01, 10]
        bounds_Rstd = [0.01, 0.2]
        bounds_X = [1e0, 1e12]
        #bounds_Pbot = [1e6, 1e0]
        #bounds_Ptop = [1e6, 1e0]
        bounds_midP = [1e6, 1e0]
        bounds_rangeP = [0.0, 3]
        bounds_decayP = [-7, 0]
        bounds_Ffill = [0.01, 1]

        ### CREATE FITPARAMS
        if self._mie_particle_mean_radius is not None:
            param_name = 'Rmean_'+self._name
            param_latex = '$R_{mean}$_'+self._name
            def read_Rmean(self):
                return self._mie_particle_mean_radius
            def write_Rmean(self, value):
                self._mie_particle_mean_radius = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_Rmean,
                                    write_Rmean, 'log', default_fit, bounds_Rm)
        if self._mie_particle_std_radius is not None:
            param_name = 'Rlogstd_'+self._name
            param_latex = '$R_{logstd}$_'+self._name
            def read_Rstd(self):
                return self._mie_particle_std_radius
            def write_Rstd(self, value):
                self._mie_particle_std_radius = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_Rstd,
                                    write_Rstd, 'linear', default_fit, bounds_Rstd)
            
        param_name = 'X_'+self._name
        param_latex = '$X$_'+self._name
        def read_X(self):
            return self._mie_particle_mix_ratio
        def write_X(self, value):
            self._mie_particle_mix_ratio = value
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_X,
                                write_X, 'log', default_fit, bounds_X)

        param_name = 'midP_'+self._name
        param_latex = '$midP$_'+self._name
        def read_midP(self):
            return self._mie_midP
        def write_midP(self, value):
            self._mie_midP = value
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_midP,
                                write_midP, 'log', default_fit, bounds_midP)

        param_name = 'rangeP_'+self._name
        param_latex = '$rangeP$_'+self._name
        def read_rangeP(self):
            return self._mie_rangeP
        def write_rangeP(self, value):
            self._mie_rangeP = value
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_rangeP,
                                write_rangeP, 'linear', default_fit, bounds_rangeP)
        
        param_name = 'decayP_'+self._name
        param_latex = '$decayP$_'+self._name
        def read_decayP(self):
            return self._particle_alt_decay
        def write_decayP(self, value):
            self._particle_alt_decay = value
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_decayP,
                                write_decayP, 'linear', default_fit, bounds_decayP)
        
        param_name = 'Ffill_eff_'+self._name
        param_latex = '$Ffill_{eff}$_'+self._name
        def read_FfillEff(self):
            return self._mie_effective_filling_factor
        def write_FfillEff(self, value):
            self._mie_effective_filling_factor = value
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_FfillEff,
                                write_FfillEff, 'linear', default_fit, bounds_Ffill)
        

        ### CREATE INDIVIDUAL SPECIES FITPARAMS
        for idx, val in enumerate(self._species):
            
            if self._mie_filling_factors is not None:
                param_name = 'Ffill_{}_'.format(val)+self._name
                param_latex = '$Ffill_{}$_'.format(val)+self._name
                def read_Ffill(self, idx=idx):
                    return self._mie_filling_factors[idx]
                def write_Ffill(self, value, idx=idx):
                    self._mie_filling_factors[idx] = value
                default_fit = False
                self.add_fittable_param(param_name, param_latex, read_Ffill,
                                        write_Ffill, 'linear', default_fit, bounds_Ffill)
    
    def prepare_each(self, model, wngrid):
        
        if self._renormalize_factors == True:
            self._mie_filling_factors = self._mie_filling_factors/np.sum(self._mie_filling_factors)
        else:
            if np.sum(self._mie_filling_factors[:-1]) > 1:
                raise InvalidPyMieScattException
            else:
                self._mie_filling_factors[-1] = 1 - np.sum(self._mie_filling_factors[:-1])
        if self._mie_effective_filling_factor > 1:
            raise InvalidPyMieScattException

        from PyMieScatt import MieQ_withWavelengthRange
        self._nlayers = model.nLayers
        self._ngrid = wngrid.shape[0]

        pressure_profile = model.pressureProfile

        wltmp = 10000/wngrid
        
        sigma_xsec = np.zeros(shape=(self._nlayers, wngrid.shape[0]))
        
        wlmin = np.min([np.min(w) for w in self._wls])
        wlmax = np.max([np.max(w) for w in self._wls])

        wlres = create_grid_res(self._resolution, wlmin, wlmax)
        self.wlres = wlres
        cindexes = [np.interp(wlres[:,0], self._wls[i], self._cindexes[i], left=0, right=0) for i in range(len(self._cindexes))]
        
        self._emonomers = np.array([np.power(c, 2) for c in cindexes])
        
        gamma = 3/(self._emonomers+2)
        emix = np.sum(self._mie_filling_factors[:,None]*gamma*self._emonomers, axis=0)/np.sum(self._mie_filling_factors[:,None]*gamma, axis=0)
        F = (emix-1)/(emix+2)
        eeff = (1+2*np.array(self._mie_effective_filling_factor)*F)/(1-np.array(self._mie_effective_filling_factor)*F)
        cindex = np.sqrt(eeff)
        self.CINDEX = cindex
        Rmean = self._mie_particle_mean_radius
        #mask = (wl >= np.min(wltmp)) & (wl <= np.max(wltmp))
        
        wl = wlres[:,0] #### THIS HAS TO BE INTERPOLATED!
        
        if self._mie_particle_radius_distribution == 'budaj': ## This distribution can be found in Budaj et al. 2015
            LogRsigma = 0.2 ## since the distribution is fixed in width, this can be set to approx 0.2 for the sampling
            #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
            radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
            weights = ((radii_log/Rmean)**6)*np.exp(-6*radii_log/Rmean)
        elif self._mie_particle_radius_distribution == 'deirmendjian': ## This distribution can be found in Deirmendjian 1964 (modified Gamma distribution)
            LogRsigma = self._mie_particle_std_radius
            #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
            radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
            weights = self._mie_particle_paramA*(radii_log**self._mie_particle_paramB)*np.exp(-self._mie_particle_paramC*(radii_log**self._mie_particle_paramD))
        else: ## This is simply a normal distribution.
            LogRsigma = self._mie_particle_std_radius
            #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
            radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
            weights = stats.norm.pdf(np.log10(radii_log), np.log10(Rmean), LogRsigma)
            
        Qexts = []
        for i in range(len(radii_log)):
            R = radii_log[i]*1e3 ## R from um to nm
            #### PyMieScatt takes and gives nm
            #print(cindex.shape, R, wl.shape)
            try:
                o = MieQ_withWavelengthRange(cindex, 2*R, nMedium=1, wavelengthRange=wl* 1e3)  
            except:
                raise InvalidPyMieScattException
            val = o[1] * np.power(R,2)
            Qexts.append(val)
            
        Qext_mean = np.average(np.array(Qexts), axis=0, weights=weights)
        Qext_int = np.interp(wltmp[::-1], wl, Qext_mean, left=0, right=0)
        Qext_int = Qext_int[::-1]
        sigma_mie = np.zeros((len(wltmp)))

        sigma_mie[Qext_int!=0] = Qext_int[Qext_int!=0]* np.pi * 1e-18
        
        if self._mie_midP == -1:
            bottom_pressure = pressure_profile[0]
            top_pressure = pressure_profile[-1]
        else:
            bottom_pressure = 10**(np.log10(self._mie_midP) + self._mie_rangeP/2)
            top_pressure = 10**(np.log10(self._mie_midP) - self._mie_rangeP/2)

        cloud_filter = (pressure_profile <= bottom_pressure) & \
            (pressure_profile >= top_pressure)

        sigma_xsec_int = np.zeros(shape=(self._nlayers, wngrid.shape[0]))

        ## This line implied that self._mie_particle_mix_ratio is expressed in m-3
        if self._particle_alt_distib == 'exp_decay':
            ## if we want it with exp decay style Whitten et al. 2008 / Attreya et al. 2005
            decay = self._particle_alt_decay
            mix = self._mie_particle_mix_ratio*(1-np.exp(decay*(pressure_profile-top_pressure)/(bottom_pressure-top_pressure)))
            sigma_xsec_int[cloud_filter, :] = sigma_mie[None] * mix[cloud_filter, None]
        else:
            sigma_xsec_int[cloud_filter, ...] = sigma_mie * self._mie_particle_mix_ratio

        self.sigma_xsec = sigma_xsec_int

        self.debug('final xsec %s', self.sigma_xsec)

        yield 'PyMieScattExtAgg', sigma_xsec

    def write(self, output):
        contrib = super().write(output)

        if self._mie_particle_mean_radius is not None:
            contrib.write_scalar('particle_mean_radius_'+self._name, self._mie_particle_mean_radius)
        if self._mie_particle_std_radius is not None:
            contrib.write_scalar('particle_std_radius_'+self._name, self._mie_particle_std_radius)
        contrib.write_scalar('particle_mix_ratio_'+self._name, self._mie_particle_mix_ratio)
        contrib.write_scalar('particle_midP_'+self._name, self._mie_midP)
        contrib.write_scalar('particle_rangeP_'+self._name, self._mie_rangeP)
        contrib.write_string_array('cloud_species_'+self._name, self._species)
        contrib.write_scalar('radius_Nsampling_'+self._name, self._Nsampling)
        contrib.write_scalar('radius_Dsampling_'+self._name, self._Dsampling)
        contrib.write_scalar('mie_nMedium_'+self._name, self._mie_nMedium)
        contrib.write_scalar('mie_FfactorEff_'+self._name, self._mie_effective_filling_factor)
        contrib.write_array('mie_Ffactors_'+self._name, np.array(self._mie_filling_factors))

        return contrib

    @classmethod
    def input_keywords(self):
        return ['PyMieScattExtinctionAggregates', ]
    
    BIBTEX_ENTRIES = [
        """
        @BOOK{1983asls.book.....B,
               author = {{Bohren}, Craig F. and {Huffman}, Donald R.},
                title = "{Absorption and scattering of light by small particles}",
                 year = 1983,
               adsurl = {https://ui.adsabs.harvard.edu/abs/1983asls.book.....B},
              adsnote = {Provided by the SAO/NASA Astrophysics Data System}
        }
        @ARTICLE{2018JQSRT.205..127S,
               author = {{Sumlin}, Benjamin J. and {Heinson}, William R. and {Chakrabarty}, Rajan K.},
                title = "{Retrieving the aerosol complex refractive index using PyMieScatt: A Mie computational package with visualization capabilities}",
              journal = {\jqsrt},
             keywords = {Aerosol optics, Mie theory, Python 3, Electromagnetic scattering and absorption, Open-source software, Physics - Optics, 78-04},
                 year = 2018,
                month = jan,
               volume = {205},
                pages = {127-134},
                  doi = {10.1016/j.jqsrt.2017.10.012},
        archivePrefix = {arXiv},
               eprint = {1710.05288},
         primaryClass = {physics.optics},
               adsurl = {https://ui.adsabs.harvard.edu/abs/2018JQSRT.205..127S},
              adsnote = {Provided by the SAO/NASA Astrophysics Data System}
        }
        """,
    ]
