class Parameter:

    ## Constructor
    # E =                   Young's Modulus             [Pa]
    # nu =                   Poisson Ratio               []
    # b =                   burgers vector length       [m]
    # L_e =                 annihilation distance       [m]
    # B =                   drag coefficient            [Pa s]
    # tau_nuc =             average strength disloc     [Pa]
    # stdtau_nuc =          std strength disloc         [Pa]
    # L_nuc =               mean nuclation distance     [L]
    # t_nuc =               nucleation time for sources [s]
    # tau_obs =             obstacle strength           [Pa]
    # SPS =                 Slip Plane Spacing          [m]
    # SPS_init_source =     initial source              [m]
    # SPS_init_obstacle =   obstacle spacing            [m]
    def __init__ ( self, E, nu, b, L_e, B, tau_nuc, stdtau_nuc, L_nuc, t_nuc, tau_obs, SPS, SPS_init_source, SPS_init_obstacle ):
        self.E=E
        self.nu=nu
        self.b=b
        self.L_e=L_e
        self.B=B
        self.tau_nuc=tau_nuc
        self.stdtau_nuc=stdtau_nuc
        self.L_nuc=L_nuc
        self.t_nuc=t_nuc
        self.tau_obs=tau_obs
        self.SPS=SPS
        self.SPS_init_source=SPS_init_source
        self.SPS_init_obstacle=SPS_init_obstacle

