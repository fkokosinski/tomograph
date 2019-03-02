import matplotlib.pyplot as plt


def visualize(tomograph, alpha):
    tomograph.rotate(alpha)

    circle = plt.Circle((0, 0), radius=tomograph.radius, fill=False)
    ax = plt.gca()
    ax.add_patch(circle)

    img = tomograph.img
    extent = [-img.shape[1]/2, img.shape[1]/2, -img.shape[0]/2, img.shape[0]/2]
    plt.imshow(img, extent=extent, cmap='gray')

    plt.scatter(*zip(*tomograph.emitters), c='blue')
    plt.scatter(*zip(*tomograph.detectors), c='green')

    plt.show()
