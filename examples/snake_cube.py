import obpgenerator

file_path1 = "examples\layer_nine_cubes.svg"
file_path2 = "examples\layer_15x15_cube.svg"
paths = obpgenerator.file_import.import_svg_layer(file_path1)
my_layer = obpgenerator.Layer.Layer()
my_layer.create_from_mplt_paths(paths)
my_layer.set_shapes(1)
my_layer.export_obp("output.obp")
