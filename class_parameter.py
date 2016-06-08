## @package parameter
#  This file contains all material parameters

## Parameter object
class Parameter:

    ## Constructor
    # E =                   Young's Modulus             [Pa]
    # nu =                   Poisson Ratio               []
    def __init__ ( self, E,nu):
        self.E=E
        self.nu=nu
