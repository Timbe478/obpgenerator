import obpgenerator.Part as Part
import obpgenerator.support_functions.slicer as slicer
import obpgenerator.manufacturing_settings as manufacturing_settings
import time

start_time = time.time()

stl_files = [r"examples\cube1.stl", r"examples\cube2.stl"]
slices = slicer.slice_stl(stl_files,0.1) #slices the stl files with a layer height of 0.15 mm
my_part = Part.Part()
my_part.create_from_mplt_paths(slices)

pros_time = time.time() - start_time
print("1: ", pros_time)
start_time = time.time()

#Sets two different manufacturing settings for the two geometries
settings1 = manufacturing_settings.ManufacturingSetting()
settings1.set_spot_size(0.5) #[-]
settings1.set_beam_power(1000) #[W]
settings1.set_dwell_time(1) #[ns]
settings1.set_scan_speed(12) #[micrometers/second] 
settings2 = manufacturing_settings.ManufacturingSetting()
settings1.set_spot_size(0.75) #[-]
settings1.set_beam_power(1500) #[W]
settings1.set_dwell_time(1) #[ns]
settings1.set_scan_speed(10) #[micrometers/second] 

pros_time = time.time() - start_time
print("2: ", pros_time)
start_time = time.time()

my_part.set_layers(0.1, settings1, size=100, angle_between_layers=10, melt_strategy="point_random", nmb_of_scans=1, sorting_strategy="shapes_first") #First we just set one manufacturing setting

pros_time = time.time() - start_time
print("3: ", pros_time)
start_time = time.time()

my_part.set_settings(manufacturing_settings = [settings1, settings2], melt_strategies=["line_snake","point_random"]) #We can then set different settings for the seperate geometries

pros_time = time.time() - start_time
print("4: ", pros_time)
start_time = time.time()

my_part.export_build_file(r"C:\Users\antwi87\Downloads\obp_files", export_shapes_individual=False) #Exports the build file (each layer will be one obp file, if export_shapes_individual=True each geoemtry will be in seperate obp files)

pros_time = time.time() - start_time
print("5: ", pros_time)
start_time = time.time()