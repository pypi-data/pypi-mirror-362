from pathlib import Path

import numpy as np
from io_op import convert_h5ad, load_and_process_labelled_image, load_non_binary_images
from properties import (
    PVE_gradient,
    calculate_properties,
    calculate_surface_areas,
    count_erosions,
)
from utils import (
    delete_small_particles,
    erosion_based_on_labels,
    extract_histograms,
    filter_mask_image,
    get_unique_labels,
    replace_extra_rows_with_zeros,
)

##################################################################################
############################### Inputs ###########################################


class C:
    Size_threshold = 9
    numberTreads = -1
    Stepsize = 1
    Angle_spacing = 10
    Voxel_size = 16
    Background_mean = 800
    start_slice = None
    end_slice = None
    path = "/home/jpa/Data/mspacman_kemi_new/"
    properties_list = "label,area,min_intensity,max_intensity,equivalent_diameter,mean_intensity,bbox,centroid"


args = C()

### link to inputs
# Size threshold in number of voxels, default 1000
size_threshold = args.Size_threshold  # 800
# Defines the number of logical processors used in paralel. -1 is default (uses all)
# Only change if it crashes.
numb_threads = args.numberTreads  # -1
# Stepsize for creating mesh (called mesh size in window - resolution of mesh)
stepsize = args.Stepsize  # 1
# Voxel spacing for creating mesh (keep constant)
voxel_spacing = (1, 1, 1)
# Enter angle spacing for calculationg Feret dia
angle_spacing = args.Angle_spacing  # 10
# voxel size in micron
voxel_size = args.Voxel_size  # 16
background_mean = args.Background_mean  # 6600
# To load only part of the data
start_slice = args.start_slice  # If loading all data set to: None
end_slice = args.end_slice

if start_slice == -1:
    start_slice = None

if end_slice == -1:
    end_slice = None

#################################################################################
############################### Load-Save Paths #################################
### it reads tif, tiff, nii.gz and nii

path = Path(args.path)
# Load binary image with particle mask
binary_image_path = path.joinpath("mask")
print(binary_image_path)
# Load non binary image (grey-scale 16bit)
non_binary_image_path = path.joinpath("gray")
print(non_binary_image_path)
# save geometrical properties
path_to_save_geometrical_properties = path.joinpath("analysis", "Properties.csv")
# save inner histograms (inside the particle without the eroded voxels)
path_to_save_inner_volume_histograms = path.joinpath(
    "analysis", "Inner_histograms.h5ad"
)
# save outer (surface layers consisting of all voxels eroded) volume histograms
path_to_save_outer_volume_histograms = path.joinpath(
    "analysis", "Outer_histograms.h5ad"
)
# save bulk histograms (= Inner + Outer)
path_to_save_bulk_histogram = path.joinpath("analysis", "Bulk_histograms.h5ad")
# save mesh histograms
path_to_save_surface_mesh_histograms = path.joinpath(
    "analysis", "Surface_histogram.h5ad"
)
# save bulk histograms obtained sfter sobel and smoothening
path_to_save_bulk_eroded_histogram = path.joinpath("analysis", "Eroded_histograms.h5ad")
# save gradient
path_to_save_gradient = path.joinpath("analysis", "Gradient.csv")

###################################################################################
########################### load the images from stacks ###########################
print("loading from:", path)

label_mask, binary_mask = load_and_process_labelled_image(
    binary_image_path, start_slice, end_slice
)
print("Label loaded!")

gray_scale_volume = load_non_binary_images(
    non_binary_image_path, start_slice, end_slice
)
print("Grey image loaded!")

unique_labels = get_unique_labels(label_mask)
print("Image labeled loaded!")

###################################################################################
########################### Image processing ######################################
label_mask, binary, gray_scale_thresh = delete_small_particles(
    label_mask, binary_mask, gray_scale_volume, size_threshold
)

# remove non unique labels
label_mask_filtered = filter_mask_image(label_mask, unique_labels)
del label_mask

unique_labels = np.unique(label_mask_filtered)

# remove background
unique_labels = unique_labels[unique_labels != 0]

print("Number of particles after processing", len(unique_labels))

surface_areas_df = calculate_surface_areas(
    label_mask_filtered, unique_labels, voxel_spacing, stepsize
)
surface_properties_mean_intensity, eroded_image_1, eroded_image_2 = PVE_gradient(
    binary, gray_scale_thresh, label_mask_filtered, background_mean
)
surface_properties_mean_intensity["Ratio"] = surface_properties_mean_intensity[
    "Gradient_2"
]
surface_properties_mean_intensity.to_csv(path_to_save_gradient)
surface_properties_mean_intensity[
    "no_of_erosions"
] = surface_properties_mean_intensity.apply(count_erosions, axis=1)
final_eroded_image = erosion_based_on_labels(
    label_mask_filtered, surface_properties_mean_intensity
)

print("Processing finished! Starting export of histograms")

#################################################################################
############################### HISTOGRAMS ######################################
# BULK HISTOGRAMS
Bulk_histograms = extract_histograms(
    label_mask_filtered, gray_scale_thresh, numb_threads
)

# INNER HISTOGRAM
Inner_volume_labels = final_eroded_image * label_mask_filtered
Inner_volume_histograms = extract_histograms(
    Inner_volume_labels, gray_scale_thresh, numb_threads
)
del Inner_volume_labels, final_eroded_image

Inner_volume_histograms = replace_extra_rows_with_zeros(
    Bulk_histograms, Inner_volume_histograms
)

# OUTTER HISTOGRAMS
Outer_volume_histograms = Bulk_histograms - Inner_volume_histograms
Outer_volume_histograms[Outer_volume_histograms < 0] = 0
convert_h5ad(Inner_volume_histograms, path_to_save_inner_volume_histograms)
convert_h5ad(Outer_volume_histograms, path_to_save_outer_volume_histograms)

# SURFACE MESH HISTOGRAM
# Gets the voxel layer at 1 voxel depth surface mesh and convert/save as h5ad
binary_surface_mesh_eroded2 = eroded_image_1 - eroded_image_2
binary_surface_mesh_eroded2_labels = binary_surface_mesh_eroded2 * label_mask_filtered
del binary_surface_mesh_eroded2
histograms_surface_mesh = extract_histograms(
    binary_surface_mesh_eroded2_labels, gray_scale_thresh, numb_threads
)
histograms_surface_mesh = replace_extra_rows_with_zeros(
    Bulk_histograms, histograms_surface_mesh
)

# Save the histograms
convert_h5ad(histograms_surface_mesh, path_to_save_surface_mesh_histograms)
convert_h5ad(Bulk_histograms, path_to_save_bulk_histogram)

##################################################################################################
############################################# PROPERTIES #########################################
# List of properties
# area; #bbox; #bbox_area; #centroid; #convex_image; #coords; #equivalent_diameter; #euler_number; #extent
# feret_diameter_max; #filled_area; #filled_image; #image; #inertia_tensor; #inertia_tensor_eigvals; #intensity_image
# label; #local_centroid; #major_axis_length; #max_intensity; #mean_intensity; #min_intensity; #minor_axis_length
# moments; #moments_central; #moments_normalized; #slice; #solidity; #weighted_centroid; #weighted_local_centroid
# weighted_moments; #weighted_moments_central; #weighted_moments_normalized

# From the list above, add to the list the properties to be calculated. Note: area is actually volume
#### link to properties
properties = args.properties_list.split(",")
# properties = ['label', 'area', 'min_intensity', 'max_intensity', 'equivalent_diameter', 'mean_intensity', 'bbox', 'centroid']

# Call the function with appropriate properties
properties_Bulk = calculate_properties(
    label_mask_filtered,
    gray_scale_thresh,
    properties,
    path_to_save_geometrical_properties,
    unique_labels,
    angle_spacing,
    voxel_size,
    surface_areas_df,
)
properties_Bulk.to_csv(path_to_save_geometrical_properties)
