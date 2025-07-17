import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  #enables 3D plotting
import os


def display3Views(listCoord):

    x = []
    y = []
    z = []

    for coord in listCoord:
        x.append(coord.xCoord)
        y.append(coord.yCoord)
        z.append(coord.zCoord)

    #create a figure with three subplots
    fig = plt.figure(figsize=(15, 5))

    #default 3D view with connected path
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(x, y, z, color='blue', marker='o')
    ax1.plot(x, y, z, color='red')  #connects the dots
    ax1.set_title("Default 3D View")
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    #top-down view (XY plane) with connected path
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(x, y, z, color='blue', marker='o')
    ax2.plot(x, y, z, color='red')  #connect the dots
    ax2.view_init(elev=90, azim=-90)
    ax2.set_title("Top-Down View (XY Plane)")
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    #side view (YZ plane) with connected path
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(x, y, z, color='blue', marker='o')
    ax3.plot(x, y, z, color='red')  #connect the dots
    ax3.view_init(elev=0, azim=90)
    ax3.set_title("Side View (YZ Plane)")
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')

    plt.tight_layout()

    #generate file name based on the size of folder
    folder = "convImages"
    if not os.path.exists(folder):
        os.makedirs(folder)

    existing = [f for f in os.listdir(folder) if f.startswith("img") and f.endswith(".png")]
    numbers = []
    for f in existing:
        try:
            num = int(f[3:-4])
            numbers.append(num)
        except ValueError:
            continue
    next_number = max(numbers, default=0) + 1
    filename = f"img{next_number}.png"
    save_path = os.path.join(folder, filename)

    plt.savefig(save_path)

    #plt.show()
