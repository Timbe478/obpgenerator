
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.path as mpath

def create_line(start=(0.0,0.0),end=(1.0,1.0)):
    radius = 0.1
    
    path1 = Path([[start[0],start[1]],[end[0],end[1]]])
    path2 = Path.circle(center=start,radius=0.1)
    t = path1.intersects_path(path2)
    print(t)
    line = path1.make_compound_path(path1,path2)
    return line

circle = Path.circle(center=(0.0, 0.0), radius=0.05)
line = create_line()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.plot(circle.vertices[:, 0], circle.vertices[:, 1], len(circle.vertices[:, 1])*[0])
ax.plot(line.vertices[:, 0], line.vertices[:, 1], len(line.vertices[:, 1])*[0])

plt.show()