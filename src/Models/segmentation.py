"""This file contains the segmentation preprocessing in our live visualization pipeline. 
"""

import numpy as np
from skimage.segmentation import slic, mark_boundaries
# from skimage.color import label2rgb
from skimage import io, transform, measure, util
import matplotlib.pyplot as plt
import glob

def visualize_segmentation(image, segments, mask):
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    ax[0].imshow(image)
    ax[0].set_title("Original Image")
    ax[0].axis('off')

    ax[1].imshow(mark_boundaries(image, segments))
    ax[1].set_title(f"SLIC Segments (N={len(np.unique(segments))})")
    ax[1].axis('off')

    ax[2].imshow(image * mask[..., None], cmap='gray')
    ax[2].set_title("Foliage Mask (Foreground)")
    ax[2].axis('off')

    plt.tight_layout()
    plt.show()

def visualize_centroid_histogram(image, centroids):
    plt.figure(figsize=(18, 6))

    plt.hist(centroids, bins=30)

    plt.title("Foliage Density Across Image Width")
    plt.xlabel("X-coordinate (Pixels)")
    plt.ylabel("Count of Foliage Segments")

    # Optional: Add lines for the image edges to show context
    plt.axvline(0, color='red', label='Left Edge')
    plt.axvline(image.shape[1], color='green', label='Right Edge')
    plt.axvline(np.mean(centroids), color='black', label='Center of Mass')

    plt.legend()
    plt.show()

def get_segmented_image(image = None, verbose=False) -> np.array:
    #image = io.imread(filename)
    image = transform.resize(image, (480,480))
    # compactness: higher = more square, lower = follows color boundaries better
    # n_segments: approximate number of superpixels
    # sigma: gaussian blur
    segments = slic(image, n_segments=750, compactness=30)
    # segmented_vis = label2rgb(segments, image, kind='avg')
    segment_properties = measure.regionprops(segments, intensity_image=image)

    foliage_mask = np.zeros(segments.shape, dtype=bool)
    foliage_centroids = []

    for segment in segment_properties:
        red, green, blue = segment.image_intensity.mean(axis=(0,1)) # [R, G, B]
        green_gt_red = green > red
        green_gt_blue = green > blue
        green_bias = (green / max((red + blue), 0.001)) > 0.75

        if green_gt_red and green_gt_blue and green_bias:
            foliage_mask[segments == segment.label] = True
            _, centroid_x = segment.centroid
            foliage_centroids.append(centroid_x)

    if verbose:
        visualize_centroid_histogram(image, np.array(foliage_centroids))
        visualize_segmentation(image, segments, foliage_mask)

        # NOTE: this is a naive way to cut out the peripheral rows. a better method would use a trapezoidal region and/or use a signal processing technique to identify troughs in the centroid histogram
        # foliage_mask[:,:round(center_of_mass-segment_width)] = False # eliminate left cutoff range
        # foliage_mask[:,round(center_of_mass+segment_width):] = False # eliminate right cutoff range
        # visualize_segmentation(image, segments, foliage_mask)
        # left_row_mask = foliage_mask[:,round(center_of_mass-segment_width):round(center_of_mass)]
        # right_row_mask = foliage_mask[:,round(center_of_mass):round(center_of_mass+segment_width)]
        # print(f"{filename}|{np.sum(foliage_mask) / (image.shape[0]*image.shape[1])}|{np.sum(left_row_mask) / (image.shape[0]*image.shape[1])}|{np.sum(right_row_mask) / (image.shape[0]*image.shape[1])}")
    
    result = image * foliage_mask[..., None]
    return result

if __name__ == "__main__":
    filenames = glob.glob("data/dataset/*.jpg")
    segmented_images = []
    for name in filenames:
        image = io.imread(name)
        segmented_images.append(get_segmented_image(image))
    print(f"Created {len(segmented_images)} segmented images of shape {segmented_images[0].shape}")
    for filename, image in zip(filenames, segmented_images):
        id = filename
        io.imsave(f"data/Output/{filename[13:]}", util.img_as_ubyte(image)) # filename[13:] assumes data are stored in data/dataset/