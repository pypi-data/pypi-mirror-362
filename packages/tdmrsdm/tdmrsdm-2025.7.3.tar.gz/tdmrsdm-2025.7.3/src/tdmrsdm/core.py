import json
import numpy as np
from os import path as p



class TDMRSDM:
    
    """
    Temperature-Dependent Multi-Relaxation Spectroscopic Dielectric Model (TD-MRSDM)
    """

    current_dir = p.dirname(p.realpath(__file__))

    def __init__(self, freq_GHz, sst, som, sbd, ssm, optimize=None) -> None:

        self.constants_dir = p.realpath(p.join(self.current_dir, 'constants'))
        if not p.isdir(self.constants_dir):
            raise OSError(f'Cannot find constants folder: {self.constants_dir}')

        if optimize == 'v1':
            cname = 'td_mrsdm_constants_v2019_optimized_v1.json'
        elif optimize == 'v2':
            cname = 'td_mrsdm_constants_v2019_optimized_v2.json'
        else:
            cname = 'td_mrsdm_constants_v2019.json'

        self.constant_file_path = p.join(self.constants_dir, cname)

        self.f = freq_GHz * 1.0e+9      # Convert frequency to Hz
        
        # check st if not a numpy array
        if not isinstance(sst, np.ndarray):
            self.T = np.array([sst, ])
        else:
            self.T = sst     # degrees Celsius
        
        self.som = som       # percentage (%)
        self.mg = ssm / sbd  # g/g
        self.rd = sbd        # g/cm^3

        sb, st, siu = self._simga_p()

        e0_bl, e0_bm, e0_bh, e0_tl, e0_th, e0_iuh = self._e0pq()

        tau_bl, tau_tl, tau_bm, tau_bh, tau_th, tau_iuh = self._relax_time()

        er_b, ei_b = self._eps_p(e0_bl, e0_bm, e0_bh, tau_bl, tau_bm, tau_bh)
        er_t, ei_t = self._eps_p(e0_tl, e0_tl, e0_th, tau_tl, tau_tl, tau_th)
        er_iu, ei_iu = self._eps_p(e0_iuh, e0_iuh, e0_iuh, tau_iuh, tau_iuh, tau_iuh)

        nb, kb = self._RI_NAC(er_b, ei_b)
        nt, kt = self._RI_NAC(er_t, ei_t)
        niu, kiu = self._RI_NAC(er_iu, ei_iu)

        self.es = self._CRI(nb, kb, nt, kt, niu, kiu, sb, st, siu)

        return None


    def run(self):
        return self.es
    
    def _extract_model_constant(self, water_phase, data, dtype, temp, param):
        # Load the JSON data (replace 'your_file.json' with the actual filename)
        with open(self.constant_file_path, 'r') as file:
            table2_constants = json.load(file)
        
        return table2_constants["TD-MRSDM-constants"]["water-phase"][water_phase][data][dtype][temp][param]

    def _simga_p(self):
        data = 'electrical-conductivity'
        dtype = 'temperature-range'

        # Extract all positive temperatures
        s0_bp = self._extract_model_constant('bound-water', data, dtype, 't_gte_0C', 'sigma(tsp)')
        bv0_bp = self._extract_model_constant('bound-water', data, dtype, 't_gte_0C', 'betap')
        tsp_bp = self._extract_model_constant('bound-water', data, dtype, 't_gte_0C', 'tsp')

        s0_tp = self._extract_model_constant('transient-water', data, dtype, 't_gte_0C', 'sigma(tsp)')
        bv0_tp = self._extract_model_constant('transient-water', data, dtype, 't_gte_0C', 'betap')
        tsp_tp = self._extract_model_constant('transient-water', data, dtype, 't_gte_0C', 'tsp')

        s0_u = self._extract_model_constant('ice-unbound-water', data, dtype, 't_gte_0C', 'sigma(tsp)')
        bv0_u = self._extract_model_constant('ice-unbound-water', data, dtype, 't_gte_0C', 'betap')
        tsp_u = self._extract_model_constant('ice-unbound-water', data, dtype, 't_gte_0C', 'tsp')
        
        # Extract all negative temperatures
        s0_bn = self._extract_model_constant('bound-water', data, dtype, 't_lte_-1C', 'sigma(tsp)')
        bv0_bn = self._extract_model_constant('bound-water', data, dtype, 't_lte_-1C', 'betap')
        tsp_bn = self._extract_model_constant('bound-water', data, dtype, 't_lte_-1C', 'tsp')

        s0_tn = self._extract_model_constant('transient-water', data, dtype, 't_lte_-1C', 'sigma(tsp)')
        bv0_tn = self._extract_model_constant('transient-water', data, dtype, 't_lte_-1C', 'betap')
        tsp_tn = self._extract_model_constant('transient-water', data, dtype, 't_lte_-1C', 'tsp')

        s0_i = self._extract_model_constant('ice-unbound-water', data, dtype, 't_lte_-1C', 'sigma(tsp)')
        bv0_i = self._extract_model_constant('ice-unbound-water', data, dtype, 't_lte_-1C', 'betap')
        tsp_i = self._extract_model_constant('ice-unbound-water', data, dtype, 't_lte_-1C', 'tsp')
        

        sb = np.where(self.T >= 0,
                      s0_bp + bv0_bp * (self.T - tsp_bp),
                      s0_bn + bv0_bn * (self.T - tsp_bn))
        st = np.where(self.T >= 0,
                      s0_tp + bv0_tp * (self.T - tsp_tp),
                      s0_tn + bv0_tn * (self.T - tsp_tn))
        siu = np.where(self.T >= 0,
                       s0_u + bv0_u * (self.T - tsp_u),
                       s0_i + bv0_i * (self.T - tsp_i))

        return sb, st, siu


    def _CM_law(self, T, e0pQ, bvpQ, TsepQ):
        FpQ = np.log((e0pQ - 1) / (e0pQ + 2))
        return (1 + 2 * np.exp(FpQ - bvpQ * (T - TsepQ))) / (1 - np.exp(FpQ - bvpQ * (T - TsepQ)))


    def _e0pq(self):
        
        data = 'relaxation-time'

        # Bound water (p=b)
        e0_bl_neg = self._extract_model_constant('bound-water', data, 'low-frequency', 't_lte_-1C', 'e0p')
        b0_bl_neg = self._extract_model_constant('bound-water', data, 'low-frequency', 't_lte_-1C', 'bv0p')
        tse0p_bl_neg = self._extract_model_constant('bound-water', data, 'low-frequency', 't_lte_-1C', 'tse0p')

        e0_bm_neg = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_lte_-1C', 'e0p')
        b0_bm_neg = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_lte_-1C', 'bv0p')
        tse0p_bm_neg = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_lte_-1C', 'tse0p')

        e0_bh_neg = self._extract_model_constant('bound-water', data, 'high-frequency', 't_lte_-1C', 'e0p')
        b0_bh_neg = self._extract_model_constant('bound-water', data, 'high-frequency', 't_lte_-1C', 'bv0p')
        tse0p_bh_neg = self._extract_model_constant('bound-water', data, 'high-frequency', 't_lte_-1C', 'tse0p')
        
        e0_bl_pos = self._extract_model_constant('bound-water', data, 'low-frequency', 't_gte_0C', 'e0p')
        b0_bl_pos = self._extract_model_constant('bound-water', data, 'low-frequency', 't_gte_0C', 'bv0p')
        tse0p_bl_pos = self._extract_model_constant('bound-water', data, 'low-frequency', 't_gte_0C', 'tse0p')

        e0_bm_pos = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_gte_0C', 'e0p')
        b0_bm_pos = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_gte_0C', 'bv0p')
        tse0p_bm_pos = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_gte_0C', 'tse0p')

        e0_bh_pos = self._extract_model_constant('bound-water', data, 'high-frequency', 't_gte_0C', 'e0p')
        b0_bh_pos = self._extract_model_constant('bound-water', data, 'high-frequency', 't_gte_0C', 'bv0p')
        tse0p_bh_pos = self._extract_model_constant('bound-water', data, 'high-frequency', 't_gte_0C', 'tse0p')

        # Transient bound water (p=t)
        e0_tl_neg = self._extract_model_constant('transient-water', data, 'low-frequency', 't_lte_-1C', 'e0p')
        b0_tl_neg = self._extract_model_constant('transient-water', data, 'low-frequency', 't_lte_-1C', 'bv0p')
        tse0p_tl_neg = self._extract_model_constant('transient-water', data, 'low-frequency', 't_lte_-1C', 'tse0p')

        e0_th_neg = self._extract_model_constant('transient-water', data, 'high-frequency', 't_lte_-1C', 'e0p')
        b0_th_neg = self._extract_model_constant('transient-water', data, 'high-frequency', 't_lte_-1C', 'bv0p')
        tse0p_th_neg = self._extract_model_constant('transient-water', data, 'high-frequency', 't_lte_-1C', 'tse0p')

        e0_tl_pos = self._extract_model_constant('transient-water', data, 'low-frequency', 't_gte_0C', 'e0p')
        b0_tl_pos = self._extract_model_constant('transient-water', data, 'low-frequency', 't_gte_0C', 'bv0p')
        tse0p_tl_pos = self._extract_model_constant('transient-water', data, 'low-frequency', 't_gte_0C', 'tse0p')

        e0_th_pos = self._extract_model_constant('transient-water', data, 'high-frequency', 't_gte_0C', 'e0p')
        b0_th_pos = self._extract_model_constant('transient-water', data, 'high-frequency', 't_gte_0C', 'bv0p')
        tse0p_th_pos = self._extract_model_constant('transient-water', data, 'high-frequency', 't_gte_0C', 'tse0p')

        # Moistured ie (p=i)
        e0_il_neg = self._extract_model_constant('ice-unbound-water', data, 'low-frequency', 't_lte_-1C', 'e0p')
        b0_il_neg = self._extract_model_constant('ice-unbound-water', data, 'low-frequency', 't_lte_-1C', 'bv0p')
        tse0p_il_neg = self._extract_model_constant('ice-unbound-water', data, 'low-frequency', 't_lte_-1C', 'tse0p')

        # Unbound water (p=u)
        e0_uh_pos = self._extract_model_constant('ice-unbound-water', data, 'high-frequency', 't_gte_0C', 'e0p')
        b0_uh_pos = self._extract_model_constant('ice-unbound-water', data, 'high-frequency', 't_gte_0C', 'bv0p')
        tse0p_uh_pos = self._extract_model_constant('ice-unbound-water', data, 'high-frequency', 't_gte_0C', 'tse0p')

        eps_bl = np.where(self.T >= 0,
                          self._CM_law(self.T, e0_bl_pos, b0_bl_pos, tse0p_bl_pos),
                          self._CM_law(self.T, e0_bl_neg, b0_bl_neg, tse0p_bl_neg))
        eps_bm = np.where(self.T >= 0,
                          self._CM_law(self.T, e0_bm_pos, b0_bm_pos, tse0p_bm_pos),
                          self._CM_law(self.T, e0_bm_neg, b0_bm_neg, tse0p_bm_neg))
        eps_bh = np.where(self.T >= 0,
                          self._CM_law(self.T, e0_bh_pos, b0_bh_pos, tse0p_bh_pos),
                          self._CM_law(self.T, e0_bh_neg, b0_bh_neg, tse0p_bh_neg))
        eps_tl = np.where(self.T >= 0,
                          self._CM_law(self.T, e0_tl_pos, b0_tl_pos, tse0p_tl_pos),
                          self._CM_law(self.T, e0_tl_neg, b0_tl_neg, tse0p_tl_neg))
        eps_th = np.where(self.T >= 0,
                          self._CM_law(self.T, e0_th_pos, b0_th_pos, tse0p_th_pos),
                          self._CM_law(self.T, e0_th_neg, b0_th_neg, tse0p_th_neg))
        eps_iuh = np.where(self.T >= 0,
                           self._CM_law(self.T, e0_uh_pos, b0_uh_pos, tse0p_uh_pos),
                           self._CM_law(self.T, e0_il_neg, b0_il_neg, tse0p_il_neg))

        return eps_bl, eps_bm, eps_bh, eps_tl, eps_th, eps_iuh


    def _relax_time(self):

        data = 'relaxation-time'

        # Bound water (p=b)
        dHR_bl_neg = self._extract_model_constant('bound-water', data, 'low-frequency', 't_lte_-1C', 'dHp/R')
        dSR_bl_neg = self._extract_model_constant('bound-water', data, 'low-frequency', 't_lte_-1C', 'dSp/R')
        dHR_bm_neg = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_lte_-1C', 'dHp/R')
        dSR_bm_neg = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_lte_-1C', 'dSp/R')
        dHR_bh_neg = self._extract_model_constant('bound-water', data, 'high-frequency', 't_lte_-1C', 'dHp/R')
        dSR_bh_neg = self._extract_model_constant('bound-water', data, 'high-frequency', 't_lte_-1C', 'dSp/R')
        
        dHR_bl_pos = self._extract_model_constant('bound-water', data, 'low-frequency', 't_gte_0C', 'dHp/R')
        dSR_bl_pos = self._extract_model_constant('bound-water', data, 'low-frequency', 't_gte_0C', 'dSp/R')
        dHR_bm_pos = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_gte_0C', 'dHp/R')
        dSR_bm_pos = self._extract_model_constant('bound-water', data, 'mid-frequency', 't_gte_0C', 'dSp/R')
        dHR_bh_pos = self._extract_model_constant('bound-water', data, 'high-frequency', 't_gte_0C', 'dHp/R')
        dSR_bh_pos = self._extract_model_constant('bound-water', data, 'high-frequency', 't_gte_0C', 'dSp/R')

        # Transient bound water (p=t)
        dHR_tl_neg = self._extract_model_constant('transient-water', data, 'low-frequency', 't_lte_-1C', 'dHp/R')
        dSR_tl_neg = self._extract_model_constant('transient-water', data, 'low-frequency', 't_lte_-1C', 'dSp/R')
        dHR_th_neg = self._extract_model_constant('transient-water', data, 'high-frequency', 't_lte_-1C', 'dHp/R')
        dSR_th_neg = self._extract_model_constant('transient-water', data, 'high-frequency', 't_lte_-1C', 'dSp/R')
        
        dHR_tl_pos = self._extract_model_constant('transient-water', data, 'low-frequency', 't_gte_0C', 'dHp/R')
        dSR_tl_pos = self._extract_model_constant('transient-water', data, 'low-frequency', 't_gte_0C', 'dSp/R')
        dHR_th_pos = self._extract_model_constant('transient-water', data, 'high-frequency', 't_gte_0C', 'dHp/R')
        dSR_th_pos = self._extract_model_constant('transient-water', data, 'high-frequency', 't_gte_0C', 'dSp/R')

        # Moistured ie (p=i)
        dHR_il_neg = self._extract_model_constant('ice-unbound-water', data, 'low-frequency', 't_lte_-1C', 'dHp/R')
        dSR_il_neg = self._extract_model_constant('ice-unbound-water', data, 'low-frequency', 't_lte_-1C', 'dSp/R')

        # Unbound water (p=u)
        dHR_uh_pos = self._extract_model_constant('ice-unbound-water', data, 'high-frequency', 't_gte_0C', 'dHp/R')
        dSR_uh_pos = self._extract_model_constant('ice-unbound-water', data, 'high-frequency', 't_gte_0C', 'dSp/R')

        # Temp in kelvin
        t_kelvin = self.T + 273.15

        # https://en.wikipedia.org/wiki/List_of_physical_constants
        h_plank = 6.624E-34 # Planck constant
        k_boltz = 1.38E-23 # Boltzmann constant
        
        # this specific ratio doesn’t have a unique name on its own and is usually referred to as simply 
        # the "Planck-to-Boltzmann ratio" or the "dimensionless ratio h/kT" in thermal analyses.
        hkt = h_plank / k_boltz / t_kelvin

        tau_bl = np.where(self.T >= 0, 
                          hkt * np.exp((dHR_bl_pos / t_kelvin) - dSR_bl_pos), 
                          hkt * np.exp((dHR_bl_neg / t_kelvin) - dSR_bl_neg))
        tau_bm = np.where(self.T >= 0, 
                          hkt * np.exp((dHR_bm_pos / t_kelvin) - dSR_bm_pos), 
                          hkt * np.exp((dHR_bm_neg / t_kelvin) - dSR_bm_neg))
        tau_bh = np.where(self.T >= 0, 
                          hkt * np.exp((dHR_bh_pos / t_kelvin) - dSR_bh_pos), 
                          hkt * np.exp((dHR_bh_neg / t_kelvin) - dSR_bh_neg))
        tau_tl = np.where(self.T >= 0, 
                          hkt * np.exp((dHR_tl_pos / t_kelvin) - dSR_tl_pos), 
                          hkt * np.exp((dHR_tl_neg / t_kelvin) - dSR_tl_neg))
        tau_th = np.where(self.T >= 0, 
                          hkt * np.exp((dHR_th_pos / t_kelvin) - dSR_th_pos), 
                          hkt * np.exp((dHR_th_neg / t_kelvin) - dSR_th_neg))
        tau_iuh = np.where(self.T >= 0, 
                           hkt * np.exp((dHR_uh_pos / t_kelvin) - dSR_uh_pos), 
                           hkt * np.exp((dHR_il_neg / t_kelvin) - dSR_il_neg))

        return tau_bl, tau_tl, tau_bm, tau_bh, tau_th, tau_iuh


    def _eps_p(self, eps_pL, eps_pM, eps_pH, tau_pL, tau_pM, tau_pH):
        eps_inf = 4.9
        omega = 2 * np.pi * self.f
        real = ((eps_pL - eps_pM) / (1 + (omega * tau_pL)**2)) + \
                ((eps_pM - eps_pH) / (1 + (omega * tau_pM)**2)) + \
                ((eps_pH - eps_inf) / (1 + (omega * tau_pH)**2)) + eps_inf

        imag = (((eps_pL - eps_pM) / (1 + (omega * tau_pL)**2)) * omega * tau_pL) + \
                (((eps_pM - eps_pH) / (1 + (omega * tau_pM)**2)) * omega * tau_pM) + \
                (((eps_pH - eps_inf) / (1 + (omega * tau_pH)**2)) * omega * tau_pH)

        return real, imag


    def _RI_NAC(self, er_p, ei_p):
        npp = np.sqrt(np.sqrt(er_p**2 + ei_p**2) + er_p) / np.sqrt(2)
        kp = np.sqrt(np.sqrt(er_p**2 + ei_p**2) - er_p) / np.sqrt(2)

        return npp, kp


    def _CRI(self, nb0, kb0, nt0, kt0, niu0, kiu0, sb, st, siu):

        # Density of soil in thawed and frozen states (g/cm3)
        rb, rt, ru, ri = 1, 1, 1, 0.917

        # Permittivity of free space; epsilon_0: 8.85418782e-12 F/m, [Permittivity of vacuum]; https://en.wikipedia.org/wiki/List_of_physical_constants
        eps0 = 8.85418782e-12

        omega = 2 * np.pi * self.f * eps0

        nm = 0.441 + 1.68e-3 * self.som  # -30C <= T <= 25C
        km = -0.002 + 1.48e-4 * self.som # -30C <= T <= 25C

        nb = (nb0 - 1) / rb
        kb = kb0 / rb

        nt = (nt0 - 1) / rt
        kt = kt0 / rt

        nu = (niu0 - 1) / ru
        ku = kiu0 / ru

        ni = (niu0 - 1) / ri
        ki = kiu0 / ri

        # With error
        # mg1 = np.where(self.T >= 0, 0.118 + 8.7e-4 * self.som - 9.6e-4 * self.T, 0.114 + 9.5e-4 * self.som + 12.3e-4 * self.T)
        # mg2 = np.where(self.T >= 0, 0.38 + 9.2e-4 * self.som - 119.1e-4 * self.T, 0.2 + 14.9e-4 * self.som + 0.186 * np.exp(self.T / 6.59))

        # # Without error
        # mg1 = np.where(self.T >= 0, 0.118 + 8.7e-4 * self.som - 9.6e-4 * self.T, 0.114 + 9.5e-4 * self.som + 12.3e-4 * self.T)
        # mg2 = np.where(self.T >= 0, 0.38 + 9.2e-4 * self.som - 1.91e-4 * self.T, 0.2 + 14.9e-4 * self.som + 0.186 * np.exp(self.T / 6.59))

        # Paper 2019 for 1.41GHz
        mg1 = np.where(self.T >= 0, 0.118 + 8.695e-4 * self.som - 9.6e-4 * self.T, 0.114 + 9.516e-4 * self.som + 1.23e-3 * self.T)
        mg2 = np.where(self.T >= 0, 0.382 + 9.208e-4 * self.som - 1.91e-3 * self.T, 0.205 + 1.43e-3 * self.som + 0.187 * np.exp(self.T / 6.6))
        
        niu = np.where(self.T >= 0, nu, ni)
        kiu = np.where(self.T >= 0, ku, ki)
        riu = np.where(self.T >= 0, ru, ri)

        nss = np.where(self.mg <= mg1, (nm + nb * self.mg),
            np.where((mg1 <= self.mg) & (self.mg <= mg2), (nm + nb * mg1 + nt * (self.mg - mg1)),
            np.where(self.mg >= mg2, (nm + nb * mg1 + nt * (mg2 - mg1) + niu * (self.mg - mg2)), 0.)))

        kss = np.where(self.mg <= mg1, (km + kb * self.mg),
            np.where((mg1 <= self.mg) & (self.mg <= mg2), (km + kb * mg1 + kt * (self.mg - mg1)),
            np.where(self.mg >= mg2, (km + kb * mg1 + kt * (mg2 - mg1) + kiu * (self.mg - mg2)), 0.)))

        ns = nss * self.rd + 1
        ks = kss * self.rd

        esr = ns**2 - ks**2
        esi = 2 * ns * ks

        esi = np.where((0 <= self.mg) & (self.mg <= mg1),
                      esi + self.rd * ((self.mg / rb) * sb) / omega,
                      np.where((mg1 <= self.mg) & (self.mg <= mg2),
                                esi + self.rd * (((mg1 / rb) * sb) + (((self.mg - mg1) / rt) * st)) / omega,
                                np.where(self.mg >= mg2,
                                        esi + self.rd * (((mg1 / rb) * sb) + (((mg2 - mg1) / rt) * st) + (((self.mg - mg2) / riu) * siu)) / omega, 0.)
                                )
                      )

        eps = esr + esi * 1j

        return eps