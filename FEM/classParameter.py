## @package class_parameter
#  This file contains all material parameters

## Parameter object
class Parameter:

    ## Constructor
    # @param E =                   Young's Modulus             [Pa]
    # @param nu =                   Poisson Ratio               []
    def __init__ ( self, E,nu):
        self.E=E
        self.nu=nu
