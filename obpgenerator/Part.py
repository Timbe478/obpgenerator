import obpgenerator.Layer as Layer
import os
from collections import OrderedDict
import yaml

class Start_heat:
    file = ""
    temp_sensor = "Sensor1"
    target_temp = 800 #degree celsius
    timeout = 3600 #seconds timeout

class Pre_heat:
    file = ""
    repetitions = 10 #nmb of times the pre-heat is repeated

class Post_heat:
    file = ""
    repetitions = 0 #nmb of times the pre-heat is repeated

class Layerfeed:
    build_piston_distance = -0.1    # mm
    powder_piston_distance = 0.2    # mm
    recoater_advance_speed = 200.0  # mm/s
    recoater_retract_speed = 200.0  # mm/s
    recoater_dwell_time = 0         # milliseconds, wait time in fully advanced position
    recoater_full_repeats = 0       # Repeats of the full recoater stroke. No extra powder is added, the powder tank will only be raised once.    
    recoater_build_repeats = 0      # Repeated recoater passes over the build plane
    triggered_start = True # The actual trigger is defined in the `recoaterservice.yaml` config file


class Part:
    start_heat = Start_heat()
    pre_heat = Pre_heat()
    post_heat = Post_heat()
    layer_feed = Layerfeed()

    layers = [] #list of Layers

    def create_from_mplt_paths(self, matplot_paths): #matplot_paths should be array on form [[[path1 path2],[path3]],[[path4]],[[path5],[path6]]]
        for path in matplot_paths:
            layer = Layer.Layer()
            layer.create_from_mplt_paths(path)
            self.layers.append(layer)
    
    def set_layers(self, spacing, manufacturing_settings, size=150, angle_between_layers=0, melt_strategy="point_random", nmb_of_scans=1, sorting_strategy="ramp_manufacturing_settings"):
        angle = 0
        for i in range(len(self.layers)):
            self.layers[i].set_shapes(spacing, size=size, angle=angle)
            self.layers[i].set_manufacturing_settings(manufacturing_settings)
            self.layers[i].set_melt_strategies(melt_strategy)
            self.layers[i].set_nmb_of_scans(nmb_of_scans)
            self.layers[i].sorting_strategy = sorting_strategy
            angle = angle + angle_between_layers

    def export_build_file(self, folder_path, file_name="freemelt_run_file.yml"):
        
        # Create directory to save obp files
        path = os.path.join(folder_path, "obp_files")
        layer_paths = []
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        for i in range(2): #len(self.layers)):
            file_path = os.path.join(path, "layer"+str(i)+".obp")
            #self.layers[i].export_obp(file_path)
            layer_paths.append("\"" + file_path + "\"")
        
        build_file = {
            "build": {
                "start_heat": {
                    "file": self.start_heat.file,
                    "temp_sensor": self.start_heat.temp_sensor,
                    "target_temperatur": self.start_heat.target_temp,
                    "timeout": self.start_heat.timeout
                },
                "preheat": {
                    "file": self.pre_heat.file,
                    "repetitions": self.pre_heat.repetitions
                },
                "postheat": {
                    "file": self.post_heat.file,
                    "repetitions": self.post_heat.repetitions
                },
                "build": {
                    "layers": len(self.layers),
                    "files": layer_paths
                },
                "layerfeed": {
                    "build_piston_distance": self.layer_feed.build_piston_distance,
                    "powder_piston_distance": self.layer_feed.powder_piston_distance,
                    "recoater_advance_speed": self.layer_feed.recoater_advance_speed,
                    "recoater_retract_speed": self.layer_feed.recoater_retract_speed,
                    "recoater_dwell_time": self.layer_feed.recoater_dwell_time,
                    "recoater_full_repeats": self.layer_feed.recoater_full_repeats,
                    "recoater_build_repeats": self.layer_feed.recoater_build_repeats,
                    "triggered_start": self.layer_feed.triggered_start
                }
            }
        }
        out_path = os.path.join(folder_path, file_name)
        with open(out_path, 'w') as file:
            documents = yaml.dump(build_file, file)
        
        
        
        

part = Part()
part.export_build_file(r"C:\Users\antwi87\Downloads\obp_files")