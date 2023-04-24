import obpgenerator.Part as Part
import obpgenerator.slicer as slicer
import obpgenerator.manufacturing_settings as manufacturing_settings

stl_file = ["examples\\cube1.stl", "examples\\cube2.stl"]
slices = slicer.slice_stl(stl_file,1)
my_part = Part.Part()
my_part.create_from_mplt_paths(slices)

manuf = manufacturing_settings.ManufacturingSetting()
my_part.set_layers(1, manuf, size=60, angle_between_layers=0, melt_strategy="point_random", nmb_of_scans=1, sorting_strategy="shapes_first")
my_part.export_build_file(r"C:\Users\antwi87\Downloads\obp_files")