import logging
import numpy as np
from measurement import measurement
from devices import ke2410 # power supply
#from devices import ke3706 # switch
#from devices import ke2000 # volt meter


class iv_scan(measurement):
    """Measurement of I-V curves for individual cells across the wafer matrix."""
    
    def initialise(self):
        self.logging.info("------------------------------------------")
        self.logging.info("IV Scan")
        self.logging.info("------------------------------------------")
        self.logging.info("Measurement of I-V curves for individual cells across the wafer matrix.")
        self.logging.info("\n")
        
        self._initialise()
        self.pow_supply_address = 24
        self.volt_meter_address = 16
        self.switch_address = 18
        
        self.lim_cur = 0.0001
        self.lim_vol = 100
        self.cell_list = np.loadtxt('IVchannels.txt')
        self.volt_list = np.loadtxt('IVvoltages.txt')
        
        self.logging.info("\n")
        self.logging.info("Settings:")
        self.logging.info("Power Supply voltage limit:      %.2fV" % self.lim_vol)
        self.logging.info("Power Supply current limit:      %.6fA" % self.lim_cur)
        self.logging.info("Volt Meter voltage limit:        %.2fV" % self.lim_vol)
        self.logging.info("Volt Meter current limit:        %.6fA" % self.lim_cur)
        self.logging.info("\n")
        
        

    def execute(self):
        
        ## Set up power supply
        pow_supply = ke2410(self.pow_supply_address)
        pow_supply.set_source('voltage')
        pow_supply.set_sense('current')
        pow_supply.set_voltage_limit(self.lim_vol)
        pow_supply.set_current_limit(self.lim_cur)
        pow_supply.set_output_on()

        ## Set up volt meter
        # Set up volt meter

        ## Set up switch
        # Set up switch

        for c in self.cell_list:
            # Check all channels close
            # Open channel c
            
            ## Current is measured by voltage over 22M resistor
            ## TODO: implement real application
            for v in self.volt_list:
                pow_supply.set_voltage(v)
                vol = pow_supply.read_voltage()
                cur = pow_supply.read_voltage()

                self.logging.info("cell nr.:%d, vol %d, cur %d" % (c, vol, cur))

            # Close all channels

        ## Close connections
        pow_supply.set_output_off()
        pow_supply.reset()
    
    
    def finalise(self):
        self._finalise()