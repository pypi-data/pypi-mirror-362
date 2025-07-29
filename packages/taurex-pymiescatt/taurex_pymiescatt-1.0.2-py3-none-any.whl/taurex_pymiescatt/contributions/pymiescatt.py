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

class PyMieScattExtinctionContribution(Contribution):
    """
    Computes Mie scattering contribution to optical depth
    using the Bohren and Huffmann in its PyMieScatt implementation.

    Parameters
    ----------
    mie_particle_mean_radius: Mean radius of the particles in um
    mie_particle_mix_ratio: Number density in molecules/m^3 --> Divide this number by 1,000,000 to get this in more common molecules/cm^3
    mie_midP: Middle of the clouds in Pa
    mie_rangeP: Extend of the clouds in log scale. If mie_midP = 1e5 Pa and mie_rangeP = 1 then clouds extend from 1e6 to 1e4 Pa
    """

    def __init__(self, mie_particle_mean_radius=[0.01,], 
                 mie_particle_logstd_radius = [0.001], ## Serves for the normaly distributed particle size distribution.
                 mie_particle_paramA = [1., ], mie_particle_paramB = [6.,], mie_particle_paramC = [6.,], mie_particle_paramD = [1.,], ## Serves for Deirmendjian particle size distribution.
                 mie_particle_radius_Nsampling = 5, mie_particle_radius_Dsampling = 2, ## Is used for sampling the particle distribution.
                 mie_particle_radius_distribution = 'normal', ## choices are 'normal', 'budaj', 'deirmendjian'.
                 mie_species_path=None, species = ['MgSiO4'], file_extension = '.refrind',
                 mie_particle_mix_ratio=[1e-10], 
                 mie_porosity = None,
                 #mie_bottomP=[-1],
                 #mie_topP=[-1], 
                 mie_midP = [1e3],
                 mie_rangeP = [1],
                 mie_nMedium=1, 
                 mie_resolution = 100,
                 mie_particle_altitude_distrib = 'exp_decay',
                 mie_particle_altitude_decay = [-5], ## Controls the decay rate, inspired by Whitten et al. 2008 / Attreya et al. 2005
                 usecols=(0,1,2), skiprows=0, reverse=False, name = 'PME'):
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
        self._mie_porosity = mie_porosity
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

        self._resolution = mie_resolution

        self._wls, self._cindexes, _ = self.load_input_files(self._mie_species_path, 
                                                self._species, self._file_extension, 
                                                int(skiprows), np.array(usecols).astype(int), reverse)
        
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
    
    def EMT(self, V1, m1, V2, n2=1., k2=0.):
        # ------------------------------------------------------                                                                                                                                                                                
        # Calculate Averaged Optical Constant from                                                                                                                                                                                              
        # Effective Medium Theory (See e.g., Sec 8.5, Bohren&Huffman 1983)                                                                                                                                                                      
        # Bruggeman mixing rule is applied here  
        # Another option is to use Maxwell-Garnett mixing rule
        # Voshchinnikov et al. 2007 provides comparisons for different EMT mixing rules
        # CONSTRUCTED BY KAZUMASA OHNO
        # ------------------------------------------------------                                                                                                                                                                                
        #m1   = n1 + k1*1j
        m2   = n2 + k2*1j
        eps1 = m1 * m1
        eps2 = m2 * m2
        f1   = V1/(V1+V2)
        f2   = V2/(V1+V2)
        eps_eff = (f1*eps1**(1/3)+f2*eps2**(1/3))**3.0
        for i in range(0,1000,1):
            eps_old  = eps_eff
            F        = f1*( eps1 - eps_eff )/( eps1 + 2.0e0*eps_eff )+f2*( eps2 - eps_eff )/( eps2 + 2.0e0*eps_eff )
            dF       = f1*( -3.0*eps1 + eps_eff )/( eps1 + 2.0e0*eps_eff )**2.0+f2*( -3.0*eps2 + eps_eff )/( eps2 + 2.0e0*eps_eff )**2.0
            eps_eff  = eps_eff - 0.5*F/dF # 0.5 is a safety factor
            delta_re = np.max( np.abs(eps_eff.real/eps_old.real-1.0) )
            delta_im = np.max( np.abs(eps_eff.imag/eps_old.imag-1.0) )
            #print(i,delta_re,delta_im)
            if( delta_re < 1e-14 and delta_im < 1e-14 ):
                break        
        n_eff = np.sqrt( eps_eff ).real
        k_eff = np.sqrt( eps_eff ).imag
        newc = n_eff + k_eff*1j
        return newc

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
        bounds_poro = [0,1]

        ### CREATE JOINED FITPARAMS
        if self._mie_particle_mean_radius is not None:
            param_name = 'Rmean_share'
            param_latex = '$Rmean_share$'
            def read_RmeanShare(self):
                return np.mean(self._mie_particle_mean_radius)
            def write_RmeanShare(self, value):
                self._mie_particle_mean_radius[:] = [value]*len(self._mie_particle_mean_radius)
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_RmeanShare,
                                    write_RmeanShare, 'log', default_fit, bounds_Rm)
        if self._mie_particle_std_radius is not None:
            param_name = 'Rlogstd_share'
            param_latex = '$Rlogstd_share$'
            def read_RstdShare(self):
                return np.mean(self._mie_particle_std_radius)
            def write_RstdShare(self, value):
                self._mie_particle_std_radius[:] = [value]*len(self._mie_particle_std_radius)
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_RstdShare,
                                    write_RstdShare, 'linear', default_fit, bounds_Rstd)
            
        param_name = 'X_share'
        param_latex = '$X_share$'
        def read_XShare(self):
            return np.mean(self._mie_particle_mix_ratio)
        def write_XShare(self, value):
            self._mie_particle_mix_ratio = [value]*len(self._mie_particle_mix_ratio)
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_XShare,
                                write_XShare, 'log', default_fit, bounds_X)

        param_name = 'midP_share'
        param_latex = '$midP_share$'
        def read_midPShare(self):
            return np.mean(self._mie_midP)
        def write_midPShare(self, value):
            self._mie_midP[:] = [value]*len(self._mie_midP)
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_midPShare,
                                write_midPShare, 'log', default_fit, bounds_midP)

        param_name = 'rangeP_share'
        param_latex = '$rangeP_share$'
        def read_rangePShare(self):
            return np.mean(self._mie_rangeP)
        def write_rangePShare(self, value):
            self._mie_rangeP[:] = [value]*len(self._mie_rangeP)
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_rangePShare,
                                write_rangePShare, 'linear', default_fit, bounds_rangeP)
        
        param_name = 'decayP_share'
        param_latex = '$decayP_share$'
        def read_decayPShare(self):
            return np.mean(self._particle_alt_decay)
        def write_decayPShare(self, value):
            self._particle_alt_decay[:] = [value]*len(self._particle_alt_decay)
        default_fit = False
        self.add_fittable_param(param_name, param_latex, read_decayPShare,
                                write_decayPShare, 'linear', default_fit, bounds_decayP)

        ### CREATE INDIVIDUAL SPECIES FITPARAMS
        for idx, val in enumerate(self._species):
            
            if self._mie_particle_mean_radius is not None:
                param_name = 'Rmean_{}'.format(val)
                param_latex = '$Rmean_{}$'.format(val)
                def read_Rmean(self, idx=idx):
                    return self._mie_particle_mean_radius[idx]
                def write_Rmean(self, value, idx=idx):
                    self._mie_particle_mean_radius[idx] = value
                default_fit = False
                self.add_fittable_param(param_name, param_latex, read_Rmean,
                                        write_Rmean, 'log', default_fit, bounds_Rm)

            if self._mie_particle_std_radius is not None:
                param_name = 'Rlogstd_{}'.format(val)
                param_latex = '$Rlogstd_{}$'.format(val)
                def read_Rstd(self, idx=idx):
                    return self._mie_particle_std_radius[idx]
                def write_Rstd(self, value, idx=idx):
                    self._mie_particle_std_radius[idx] = value
                default_fit = False
                self.add_fittable_param(param_name, param_latex, read_Rstd,
                                        write_Rstd, 'linear', default_fit, bounds_Rstd)
                
            if self._mie_porosity is not None:
                param_name = 'Porosity_{}'.format(val)
                param_latex = '$Porosity_{}$'.format(val)
                def read_Poro(self, idx=idx):
                    return self._mie_porosity[idx]
                def write_Poro(self, value, idx=idx):
                    self._mie_porosity[idx] = value
                default_fit = False
                self.add_fittable_param(param_name, param_latex, read_Poro,
                                        write_Poro, 'linear', default_fit, bounds_poro)

            param_name = 'X_{}'.format(val)
            param_latex = '$X_{}$'.format(val)
            def read_X(self, idx=idx):
                return self._mie_particle_mix_ratio[idx]
            def write_X(self, value, idx=idx):
                self._mie_particle_mix_ratio[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_X,
                                    write_X, 'log', default_fit, bounds_X)

            param_name = 'midP_{}'.format(val)
            param_latex = '$midP_{}$'.format(val)
            def read_midP(self, idx=idx):
                return self._mie_midP[idx]
            def write_midP(self, value, idx=idx):
                self._mie_midP[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_midP,
                                    write_midP, 'log', default_fit, bounds_midP)

            param_name = 'rangeP_{}'.format(val)
            param_latex = '$rangeP_{}$'.format(val)
            def read_rangeP(self, idx=idx):
                return self._mie_rangeP[idx]
            def write_rangeP(self, value, idx=idx):
                self._mie_rangeP[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_rangeP,
                                    write_rangeP, 'linear', default_fit, bounds_rangeP)
            
            param_name = 'decayP_{}'.format(val)
            param_latex = '$decayP_{}$'.format(val)
            def read_decayP(self, idx=idx):
                return self._particle_alt_decay[idx]
            def write_decayP(self, value, idx=idx):
                self._particle_alt_decay[idx] = value
            default_fit = False
            self.add_fittable_param(param_name, param_latex, read_decayP,
                                    write_decayP, 'linear', default_fit, bounds_decayP)
            

            #param_name = 'Pbot_{}'.format(val)
            #param_latex = '$Pbot_{}$'.format(val)
            #def read_Pbot(self, idx=idx):
            #    return self._mie_bottom_pressure[idx]
            #def write_Pbot(self, value, idx=idx):
            #    self._mie_bottom_pressure[idx] = value
            #default_fit = False
            #self.add_fittable_param(param_name, param_latex, read_Pbot,
            #                        write_Pbot, 'log', default_fit, bounds_Pbot)

            #param_name = 'Ptop_{}'.format(val)
            #param_latex = '$Ptop_{}$'.format(val)
            #def read_Ptop(self, idx=idx):
            #    return self._mie_top_pressure[idx]
            #def write_Ptop(self, value, idx=idx):
            #    self._mie_top_pressure[idx] = value
            #default_fit = False
            #self.add_fittable_param(param_name, param_latex, read_Ptop,
            #                        write_Ptop, 'log', default_fit, bounds_Ptop)
    
    def prepare_each(self, model, wngrid):

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

        for idx, s in enumerate(self._species):
            wl = self._wls[idx]
            mask = (wl >= np.min(wltmp)) & (wl <= np.max(wltmp))
            cindex = cindexes[idx]

            if ((self._mie_porosity is not None) and (self._mie_porosity != 'None')):
                cindex = self.EMT(1-self._mie_porosity[idx], cindex, self._mie_porosity[idx])
            #wl = wl[mask]
            #cindex = cindex[mask]

            Rmean = self._mie_particle_mean_radius[idx]
            
            wl = wlres[:,0] #### THIS HAS TO BE INTERPOLATED!
            
            ## GET A LOG DISTRIBUTION OF THE PARTICLE RADIUS

            if self._mie_particle_radius_distribution == 'budaj': ## This distribution can be found in Budaj et al. 2015
                LogRsigma = 0.2 ## since the distribution is fixed in width, this can be set to approx 0.2 for the sampling
                #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
                radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
                weights = ((radii_log/Rmean)**6)*np.exp(-6*radii_log/Rmean)
            elif self._mie_particle_radius_distribution == 'deirmendjian': ## This distribution can be found in Deirmendjian 1964 (modified Gamma distribution)
                LogRsigma = self._mie_particle_std_radius[idx]
                #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
                radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
                weights = self._mie_particle_paramA[idx]*(radii_log**self._mie_particle_paramB[idx])*np.exp(-self._mie_particle_paramC[idx]*(radii_log**self._mie_particle_paramD[idx]))
            else: ## This is simply a normal distribution.
                LogRsigma = self._mie_particle_std_radius[idx]
                #radii_log = np.logspace(np.log10(Rmean)+self._Dsampling*LogRsigma, np.log10(Rmean)-self._Dsampling*LogRsigma, self._Nsampling)
                radii_log = np.linspace(10**(np.log10(Rmean)+self._Dsampling*LogRsigma), 10**(np.log10(Rmean)-self._Dsampling*LogRsigma), self._Nsampling)
                weights = stats.norm.pdf(np.log10(radii_log), np.log10(Rmean), LogRsigma)
            Qexts = []
            for i in range(len(radii_log)):
                R = radii_log[i]*1e3 ## R from um to nm
                #### PyMieScatt takes and gives nm
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
            ## So here sigma_mie is in m2 (nm2 to m2 conversion is 1e-18)

            if self._mie_midP[idx] == -1:
                bottom_pressure = pressure_profile[0]
                top_pressure = pressure_profile[-1]
            else:
                bottom_pressure = 10**(np.log10(self._mie_midP[idx]) + self._mie_rangeP[idx]/2)
                top_pressure = 10**(np.log10(self._mie_midP[idx]) - self._mie_rangeP[idx]/2)

            cloud_filter = (pressure_profile <= bottom_pressure) & \
                (pressure_profile >= top_pressure)

            sigma_xsec_int = np.zeros(shape=(self._nlayers, wngrid.shape[0]))
            
            ## This line implied that self._mie_particle_mix_ratio is expressed in m-3
            if self._particle_alt_distib == 'exp_decay':
                ## if we want it with exp decay style Whitten et al. 2008 / Attreya et al. 2005
                decay = self._particle_alt_decay[idx]
                #mix = self._mie_particle_mix_ratio[idx]*(1-np.exp(decay*(pressure_profile-top_pressure)/(bottom_pressure-top_pressure)))
                mix = self._mie_particle_mix_ratio[idx]*(press/bottom_pressure)**(- decay)
                sigma_xsec_int[cloud_filter, :] = sigma_mie[None] * mix[cloud_filter, None]
            else:
                sigma_xsec_int[cloud_filter, ...] = sigma_mie * self._mie_particle_mix_ratio[idx]

            sigma_xsec += sigma_xsec_int

        self.sigma_xsec = sigma_xsec

        self.debug('final xsec %s', self.sigma_xsec)

        yield 'PyMieScattExt', sigma_xsec

    def write(self, output):
        contrib = super().write(output)

        if self._mie_particle_mean_radius is not None:
            contrib.write_array('particle_mean_radius', np.array(self._mie_particle_mean_radius))
        if self._mie_particle_std_radius is not None:
            contrib.write_array('particle_std_radius', np.array(self._mie_particle_std_radius))
        contrib.write_array('particle_mix_ratio', np.array(self._mie_particle_mix_ratio))
        contrib.write_array('particle_midP', np.array(self._mie_midP))
        contrib.write_array('particle_rangeP', np.array(self._mie_rangeP))
        contrib.write_string_array('cloud_species', self._species)
        contrib.write_scalar('radius_Nsampling', self._Nsampling)
        contrib.write_scalar('radius_Dsampling', self._Dsampling)
        contrib.write_scalar('mie_nMedium', self._mie_nMedium)
        return contrib

    @classmethod
    def input_keywords(self):
        return ['PyMieScattExtinction', ]
    
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