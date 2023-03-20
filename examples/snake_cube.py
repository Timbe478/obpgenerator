import obpgenerator

file_path = "examples\layer_nine_cubes.svg"
paths = obpgenerator.file_import.import_svg_layer(file_path)
my_layer = obpgenerator.Layer.Layer()
my_layer.create_from_mplt_paths(paths)
my_layer.set_shapes(1)
my_layer.export_obpj("output.obpj")
