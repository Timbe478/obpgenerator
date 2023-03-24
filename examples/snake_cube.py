import obpgenerator

file_path1 = "examples\layer_nine_cubes.svg"
file_path2 = "examples\layer_15x15_cube.svg"

paths = obpgenerator.file_import.import_svg_layer(file_path2)
my_layer = obpgenerator.Layer.Layer()
my_layer.create_from_mplt_paths(paths)

my_layer.set_shapes(0.2)

manufacturing_settings = obpgenerator.manufacturing_settings.ManufacturingSetting()
manufacturing_settings.set_spot_size(0.1,lower=0.1,upper=1)
manufacturing_settings.set_beam_power(1500,lower=1000,upper=2000)
manufacturing_settings.set_scan_speed(1,lower=1,upper=2)
manufacturing_settings.set_dwell_time(100,lower=50,upper=150)
ramp_settings = dict(ramp_beam_power=0,ramp_dwell_time=0,ramp_scan_speed=1,ramp_spot_size=0)


my_layer.set_manufacturing_settings(manufacturing_settings)
my_layer.sorting_settings = ramp_settings
my_layer.set_melt_strategies("line_snake")
my_layer.set_nmb_of_scans(3)
my_layer.sorting_strategy = "ramp_manufacturing_settings"

my_layer.export_obp("output.obp")
