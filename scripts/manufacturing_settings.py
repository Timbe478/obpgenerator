import obplib as obp

class MyVar:
   def __init__(self, num, upper=None, lower=None):
        self.value = num
        if upper == None:
            upper = num
        if lower == None:
            lower = num
        self.upper = upper
        self.lower = lower

class ManufacturingSetting:
    spot_size = MyVar(1) #[µm]
    beam_power = MyVar(1500) #[W]
    scan_speed = MyVar(1) #[micrometers/second] 
    dwell_time = MyVar(1) #[ns]
    def __init__(self):
        pass
    def get_beam_parameters(self):
        return obp.Beamparameters(self.spot_size.value, self.beam_power.value)