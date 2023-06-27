import Part as Part
import slicer as slicer
import manufacturing_settings as manufacturing_settings


stl_files = ["examples\\cube1.stl", "examples\\cube2.stl"]
slices = slicer.slice_stl(stl_files,1) #slices the stl files with a layer height of 0.15 mm
my_part = Part.Part()
my_part.create_from_mplt_paths(slices)

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


my_part.set_layers(0.07, settings1, size=100, angle_between_layers=10, melt_strategy="point_random", nmb_of_scans=1, sorting_strategy="shapes_first") #First we just set one manufacturing setting
my_part.set_settings(manufacturing_settings = [settings1, settings2], melt_strategies=["line_snake","point_random"]) #We can then set different settings for the seperate geometries
my_part.export_build_file(r"C:\Users\antwi87\Downloads\obp_files", export_shapes_individual=False) #Exports the build file (each layer will be one obp file, if export_shapes_individual=True each geoemtry will be in seperate obp files)
