import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Define the path vertices
vertices = [(0, 0), (1, 1), (1.5, 0.5)]
codes = [mpath.Path.MOVETO, mpath.Path.LINETO, mpath.Path.LINETO]

# Create the path
path = mpath.Path(vertices, codes)

# Create a patch for the path with an arrow
patch = mpatches.FancyArrowPatch(
    path=path,
    arrowstyle='->',
    mutation_scale=20,
    facecolor='black',
    edgecolor='black'
)

# Add the patch to the axis
ax.add_patch(patch)

# Set the axis limits
ax.set_xlim(-0.2, 1.7)
ax.set_ylim(-0.2, 1.2)

# Show the plot
plt.show()
