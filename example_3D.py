# import slicer as slicer
# import visualization.visualization as visualization
# stl_file = r"C:\Users\antwi87\Documents\GitHub\obpgenerator\examples\fork.stl"

# slices = slicer.slice_stl(stl_file,1)

# vis = visualization.Visualization()
# z = 0
# for slice in slices:
#     vis.add_paths(slice,z)
#     z=z+1

# vis.show()
import obpgenerator.visualization.visualization as visualization
import obpgenerator.Part as Part
import obpgenerator.slicer as slicer
import obpgenerator.visualization.visualization as visualization
import obpgenerator.manufacturing_settings as manufacturing_settings

stl_file = r"C:\Users\antwi87\Documents\GitHub\obpgenerator\examples\two_cubes.stl"
slices = slicer.slice_stl(stl_file,1)
my_part = Part.Part()
my_part.create_from_mplt_paths(slices)

manuf = manufacturing_settings.ManufacturingSetting()
my_part.set_layers(1, manuf, size=60, angle_between_layers=0, melt_strategy="point_random", nmb_of_scans=1, sorting_strategy="shapes_first")
my_part.create_obps()
#print(my_part.layers[0].shapes)
visualization.visualize_part(my_part)
#my_part.export_build_file(r"C:\Users\antwi87\Downloads\obp_files")