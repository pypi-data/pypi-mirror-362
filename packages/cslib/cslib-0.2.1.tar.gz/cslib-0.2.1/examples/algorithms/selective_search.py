from cslib.algorithms.object_proposals import selective_search
from skimage.data import astronaut
import matplotlib.pyplot as plt
import matplotlib.patches as patches

image = astronaut()
_, regions = selective_search(image)

# 1. Use Matplotlib - from scratch

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.imshow(image)
ax1.set_title('Original Image')
ax1.set_axis_off()

ax2.imshow(image)
ax2.set_title('Selective Search Result')
for region in regions:
    rect = region['rect']
    x, y, w, h = rect
    ax2.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=1))
ax2.set_axis_off()

plt.tight_layout()
plt.show()


# 2. Use glance
# from cslib.utils import glance
# glance is (x_min, y_min, x_max, y_max), coco format
# selective_search returns (x,y,w,h) format
