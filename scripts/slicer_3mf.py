import meshlabxml as mlx
import svgwrite

# Read the 3MF file using PyMeshLab
mesh = mlx.read_mesh(r"C:\Users\antwi87\Documents\GitHub\obpgenerator\src\testfiles\cube_10_10_10.3mf")

# Set the slicing parameters
layer_height = 0.2  # in millimeters
num_layers = int(mesh.bbox[4] / layer_height)

# Create the slicing commands for PyMeshLab
commands = []
for i in range(num_layers):
    z = i * layer_height
    command = (
        "slice",
        {"layers": "1", "z": f"{z}", "output": f"layer_{i}.svg", "svgwrite": "1"},
    )
    commands.append(command)

# Slice the model using PyMeshLab
result = mlx.run_script(mesh, commands)

# Combine the SVG files into a single SVG file
drawing = svgwrite.Drawing("layers.svg")
for i in range(num_layers):
    layer = svgwrite.fromfile(f"layer_{i}.svg")
    drawing.add(layer)
drawing.save()