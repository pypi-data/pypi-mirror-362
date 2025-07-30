import gc
import glob
import os
import time
from tkinter.filedialog import askdirectory

import anndata
import nibabel as nib
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import ndimage
from skimage import io, measure, morphology
from skimage.measure import marching_cubes, mesh_surface_area
from tqdm import tqdm

startTime = time.time()

##################################################################################
############################### Inputs ###########################################
### link to inputs
# Size threshold in number of voxels, default 1000
Size_threshold = 800
# Defines the number of logical processors used in paralel. -1 is default (uses all)
# Only change if it crashes.
numberTreads = -1
# Stepsize for creating mesh (called mesh size in window - resolution of mesh)
Stepsize = 1
# Voxel spacing for creating mesh (keep constant)
voxel_spacing = (1, 1, 1)
# Enter angle spacing for calculationg Feret dia
Angle_spacing = 10
# voxel size in micron
Voxel_size = 16
Background_mean = 6600
# To load only part of the data
start_slice = None  # If loading all data set to: None
end_slice = None
# prompt to choose the directory. Must have folders with names 'binary','grey','data'
def directory():
    path = askdirectory(title="select folder")
    return path


#################################################################################
############################### Load-Save Paths #################################
### it reads tif, tiff, nii.gz and nii

path = directory()
# Load binary image with particle mask
Binary_image_path = os.path.join(path, r"mask\*")
# Load non binary image (grey-scale 16bit)
Non_binary_image_path = os.path.join(path, r"grey\*")
# save geometrical properties
Path_to_save_geometrical_properties = os.path.join(path, r"data\Properties.csv")
# save inner histograms (inside the particle without the eroded voxels)
Path_to_save_inner_volume_histograms = os.path.join(path, r"data\Inner_histograms.h5ad")
# save outer (surface layers consisting of all voxels eroded) volume histograms
Path_to_save_outer_volume_histograms = os.path.join(path, r"data\Outer_histograms.h5ad")
# save bulk histograms (= Inner + Outer)
Path_to_save_bulk_histogram = os.path.join(path, r"data\Bulk_histograms.h5ad")
# save mesh histograms
Path_to_save_surface_mesh_histograms = os.path.join(
    path, r"data\Surface_histogram.h5ad"
)
# save bulk histograms obtained sfter sobel and smoothening
Path_to_save_bulk_eroded_histogram = os.path.join(path, r"data\Eroded_histograms.h5ad")
# save gradient
Path_to_save_gradient = os.path.join(path, r"data\Gradient.csv")
print("loading from:", path)
###################################################################################
########################### load the images from stacks ###########################

# upload image. Enter the starting slice and end slice. In case of whole sample at once start_slice = 0 and end slice = number of slices -1. If 100 slices then end slice will be 99
# No need to metion tiff or tiff if its 2D stack or 3D image also decides dtype automatically based on number of labels. It can be more than 65535.
def Upload_images(Binary_image_path, start_slice, end_slice):
    # Detect all TIFF files in the provided path
    tiff_files = sorted(
        glob.glob(Binary_image_path + "*.tif") + glob.glob(Binary_image_path + "*.tiff")
    )
    nifti_files = glob.glob(Binary_image_path + "*.nii") + glob.glob(
        Binary_image_path + "*.nii.gz"
    )
    if len(tiff_files) > 1:
        # Multiple TIFF files - treat as 2D stack
        cv_img = []
        for img in tiff_files:
            n = io.imread(img, as_gray=True)
            cv_img.append(n)
        images = np.dstack(cv_img)
        images = np.rollaxis(images, -1)
        del cv_img
        del n
    elif len(tiff_files) == 1:
        # Single TIFF file - treat as 3D image
        images = io.imread(tiff_files[0])
    elif len(nifti_files) == 1:
        # Single NIfTI file - treat as 3D image
        images = nib.load(nifti_files[0]).get_fdata()
    else:
        raise ValueError("No compatible image files found in the specified directory.")
    if start_slice is not None and end_slice is not None:
        if start_slice == end_slice:
            raise ValueError("Start and end slice cannot be the same.")
        if images.ndim == 3:
            if start_slice >= 0 and end_slice < images.shape[0]:
                images = images[start_slice : end_slice + 1, :, :]
            else:
                raise ValueError("Invalid slice range for the 3D image stack.")
        else:
            raise ValueError("Slice range can only be specified for 3D image stacks.")
    # Calculate the maximum grey value
    max_grey_value = np.max(images)
    # Decide which unit type image should be based on the max grey value
    if max_grey_value <= 255:
        # Convert to uint8
        images = images.astype(np.uint8)
    elif max_grey_value <= 65535:
        # Convert to uint16
        images = images.astype(np.uint16)
    else:
        images = images.astype(np.uint32)
    gc.collect()
    return images


# Upload binary image
def Upload_and_process_labelled_image(Binary_image_path):
    labels = Upload_images(Binary_image_path, start_slice, end_slice)
    if (
        len(np.unique(labels)) < 3
    ):  # if mask was exported from Dragonfly the particles have greyvalue 255, from Avizo or ImageJ change to 1.
        labels = measure.label(labels)
    else:
        labels = labels
    binary = np.where(labels > 1, 1, 0)
    binary = binary.astype(np.uint8)
    print("Number of particles before processing", labels.max())
    print("Image size", labels.shape)
    return labels, binary


labels1, binary = Upload_and_process_labelled_image(Binary_image_path)
print("mask loaded")
# Upload non binary image
def Upload_non_binary_images(Non_binary_image_path):
    non_binary = Upload_images(Non_binary_image_path, start_slice, end_slice)
    non_binary = non_binary.astype(np.uint16)
    return non_binary


non_binary = Upload_non_binary_images(Non_binary_image_path)
print("grey loaded")
# Get labels that are not pn the edges of the slice or cut of lables
def get_unique_labels(labels):
    unique = np.unique(labels)
    unique1 = np.unique(labels[0])
    unique2 = np.unique(labels[-1])
    unique3 = np.unique(labels[:, 0, :])
    unique4 = np.unique(labels[:, -1, :])
    unique5 = np.unique(labels[:, :, 0])
    unique6 = np.unique(labels[:, :, -1])
    particles_to_delete = np.concatenate(
        [unique1, unique2, unique3, unique4, unique5, unique6]
    )
    unique_filtered = np.array([i for i in unique if i not in particles_to_delete])
    return np.delete(unique_filtered, np.where(unique_filtered == 0))


unique_labels = get_unique_labels(labels1)
print("image labeled")
###################################################################################
########################### Image processing ######################################
# Remove the particles smaller than 'Size_threshold'
def delete_small_particles(labels, binary, non_binary, Size_threshold):
    binary = np.array(binary, dtype=bool)
    binary = morphology.remove_small_objects(binary, Size_threshold, connectivity=1)
    binary = binary.astype(int)
    labels = labels * binary
    binary = binary.astype(np.uint8)
    li_thresholded = binary * non_binary
    return labels, binary, li_thresholded


labels1, binary, li_thresholded = delete_small_particles(
    labels1, binary, non_binary, Size_threshold
)

# Keeping only the unique labesls in labelled image and turing rest to 0
def process_slice(slice_data, unique_labels):
    slice_data = slice_data.copy()  # Make a copy to ensure it is modifiable
    for label in np.unique(slice_data):
        if label not in unique_labels:
            slice_data[slice_data == label] = 0  # Set label to background
    return slice_data


# parallelization
def process_3d_image(image, unique_labels, n_jobs=-1):
    result = Parallel(n_jobs=n_jobs)(
        delayed(process_slice)(image[:, :, i], unique_labels)
        for i in tqdm(range(image.shape[2]), desc="Processing slices")
    )
    return np.stack(result, axis=2)


# Assuming 'labels' and 'unique_labels' are already defined
labels = process_3d_image(labels1, unique_labels)
del labels1
unique_labels = np.unique(labels)
unique_labels = unique_labels[unique_labels != 0]
print("Number of particles afer processing", len(unique_labels))

# Calculation of surfacearea
def calculate_surface_area(label, labels, spacing=voxel_spacing, step_size=Stepsize):
    non_zero_indices = np.argwhere(labels == label)
    if non_zero_indices.shape[0] < 2:
        return 0
    min_indices = non_zero_indices.min(axis=0) - 2
    max_indices = non_zero_indices.max(axis=0) + 2
    min_indices = np.maximum(min_indices, 0)
    max_indices = np.minimum(max_indices, np.array(labels.shape) - 1)
    isolated_region = labels[
        min_indices[0] : max_indices[0] + 1,
        min_indices[1] : max_indices[1] + 1,
        min_indices[2] : max_indices[2] + 1,
    ]
    label_mask = (isolated_region == label).astype(np.uint8)
    label_mask[label_mask != 1] = 0
    if np.any(np.array(label_mask.shape) < 2) or label_mask.sum() == 0:
        return 0
    verts, faces, _, _ = marching_cubes(
        label_mask, level=0, spacing=spacing, step_size=step_size
    )
    surface_area = mesh_surface_area(verts, faces)
    del isolated_region, verts, faces, non_zero_indices, min_indices, max_indices
    return surface_area


# Parallelizing the process to save time
def calculate_surface_areas(
    labels, unique_labels, spacing=voxel_spacing, step_size=Stepsize
):
    results = Parallel(n_jobs=-1)(
        delayed(calculate_surface_area)(
            label, labels, spacing=spacing, step_size=step_size
        )
        for label in tqdm(
            unique_labels, desc="Processing Labels", total=len(unique_labels)
        )
    )
    df = pd.DataFrame({"label": unique_labels, "Surface Area": results})
    return df


surface_areas_df = calculate_surface_areas(
    labels, unique_labels, spacing=voxel_spacing, step_size=Stepsize
)

# Calculate PVE gradients and eroded_image_1 image after 1 eorion and eroded_image_2 after 2 erosions
def PVE_gradient(binary, li_thresholded, labels, Background_mean):
    surface_properties_list = []
    eroded_image = binary.astype(int)
    eroded_image_1 = None
    eroded_image_2 = None
    for i in range(1, 7):
        eroded_image = morphology.binary_erosion(eroded_image).astype(np.uint8)
        if i == 1:  # Store the image after 1 voxel erosion
            eroded_image_1 = eroded_image.copy()
            eroded_image_1 = eroded_image_1.astype(np.uint8)
        if i == 2:  # Store the image after 2 voxel erosions
            eroded_image_2 = eroded_image.copy()
            eroded_image_2 = eroded_image_2.astype(np.uint8)
        surface_diff = binary - eroded_image
        surface_diff = surface_diff.astype(np.uint8)
        surface_non_binary = li_thresholded * surface_diff
        surface_non_binary = surface_non_binary.astype(np.uint16)
        surface_mesh_properties = pd.DataFrame(
            measure.regionprops_table(
                labels, surface_non_binary, properties=["label", "mean_intensity"]
            )
        ).set_index("label")
        surface_mesh_properties = surface_mesh_properties.rename(
            columns={"mean_intensity": f"mean_intensity{i}"}
        )
        surface_properties_list.append(surface_mesh_properties)
        del surface_diff, surface_non_binary, surface_mesh_properties
        gc.collect()
    surface_properties = pd.concat(surface_properties_list, axis=1)
    cols = [f"mean_intensity{i}" for i in range(1, 7)]
    surface_properties = surface_properties[cols]
    gradient_columns = []
    max_mean_intensity = surface_properties.max(axis=1)
    for i in range(1, 7):
        gradient_col_name = f"Gradient_{i}"
        surface_properties[gradient_col_name] = (
            surface_properties[f"mean_intensity{i}"] - Background_mean
        ) / (max_mean_intensity - Background_mean)
        gradient_columns.append(gradient_col_name)
    return surface_properties, eroded_image_1, eroded_image_2


surface_properties_mean_intensity, eroded_image_1, eroded_image_2 = PVE_gradient(
    binary, li_thresholded, labels, Background_mean
)
surface_properties_mean_intensity["Ratio"] = surface_properties_mean_intensity[
    "Gradient_2"
]
surface_properties_mean_intensity.to_csv(Path_to_save_gradient)

# Getting the number of erosions needed for each particle as a new column. Erossion will be done util gradient is greater than 0.9
def count_erosions(row):
    gradient_cols = row.filter(like="Gradient")
    return sum(1 for value in gradient_cols if value < 0.9 or value > 1)
    del gradient_cols


surface_properties_mean_intensity[
    "no_of_erosions"
] = surface_properties_mean_intensity.apply(count_erosions, axis=1)

# Create image after erosion based on Number od ersions calculated
def erosion_based_on_labels(labels, surface_properties_mean_intensity):
    eroded_images = []
    unique_erosions = surface_properties_mean_intensity["no_of_erosions"].unique()
    for no_of_erosions in unique_erosions:
        labels_with_erosions = surface_properties_mean_intensity.index[
            surface_properties_mean_intensity["no_of_erosions"] == no_of_erosions
        ].values
        labels_with_erosions
        group_mask = np.isin(labels, labels_with_erosions)
        eroded_mask = ndimage.binary_erosion(group_mask, iterations=no_of_erosions)
        eroded_images.append(
            eroded_mask.astype(np.uint8)
        )  # Convert to uint16 to save memory
    final_eroded_image = np.sum(eroded_images, axis=0)
    final_eroded_image = (final_eroded_image > 0).astype(np.int8)
    del labels_with_erosions, group_mask, eroded_mask
    return final_eroded_image


final_eroded_image = erosion_based_on_labels(labels, surface_properties_mean_intensity)

print("processing finished, start exporting histograms")
#################################################################################
############################### HISTOGRAMS ######################################
# BULK HISTOGRAMS
# Get the histogram of each particle # parallelized loop
def extract_histograms(labels, li_thresholded):
    def get_histogram(label, li_thresholded):
        hist, bins = np.histogram(li_thresholded[labels == label], bins=range(65537))
        return hist, label

    unique_labels = np.unique(labels)
    results = Parallel(n_jobs=numberTreads, prefer="threads")(
        delayed(get_histogram)(label, li_thresholded)
        for label in tqdm(unique_labels)
        if label != 0
    )  # tqdm added here
    histograms = [result[0] for result in results]
    index = [result[1] for result in results]
    histograms_df = pd.DataFrame(tqdm(histograms))
    histograms_df.index = index
    return histograms_df


Bulk_histograms = extract_histograms(labels, li_thresholded)

# INNER HISTOGRAM
Inner_volume_labels = final_eroded_image * labels
Inner_volume_histograms = extract_histograms(Inner_volume_labels, li_thresholded)
del Inner_volume_labels, final_eroded_image
# If after erosion the particle disappers a rows of 0s are added
def replace_extra_rows_with_zeros(data1, data2):
    # Find indices in data1 but not in data2
    missing_indices = data1.index.difference(data2.index)
    # Create a DataFrame with missing indices filled with zeros
    missing_rows = pd.DataFrame(0, index=missing_indices, columns=data2.columns)
    # Append the missing rows to data2
    data2_updated = pd.concat([data2, missing_rows])
    # Sort data2_updated by index to maintain order (optional)
    data2_updated = data2_updated.sort_index()
    return data2_updated


Inner_volume_histograms = replace_extra_rows_with_zeros(
    Bulk_histograms, Inner_volume_histograms
)

# OUTTER HISTOGRAMS
Outer_volume_histograms = Bulk_histograms - Inner_volume_histograms
Outer_volume_histograms[Outer_volume_histograms < 0] = 0

# Convert histograms to h5ad and save it
def convert_h5ad(histograms_df, Path_to_save_histograms):
    histograms_df.index = histograms_df.index.astype(str)
    histograms_df.columns = histograms_df.columns.astype(str)
    histograms_df.columns = ["bin_" + str(col) for col in histograms_df.columns]
    obs = pd.DataFrame(index=histograms_df.index)
    var = pd.DataFrame(index=histograms_df.columns)
    adata = anndata.AnnData(X=histograms_df, obs=obs, var=var)
    adata.write(Path_to_save_histograms)
    return histograms_df


Inner_volume_histograms = convert_h5ad(
    Inner_volume_histograms, Path_to_save_inner_volume_histograms
)
Outer_volume_histograms = convert_h5ad(
    Outer_volume_histograms, Path_to_save_outer_volume_histograms
)

# SURFACE MESH HISTOGRAM
# Gets the voxel layer at 1 voxel depth surface mesh and convert/save as h5ad
binary_surface_mesh_eroded2 = eroded_image_1 - eroded_image_2
binary_surface_mesh_eroded2_labels = binary_surface_mesh_eroded2 * labels
del binary_surface_mesh_eroded2
histograms_surface_mesh = extract_histograms(
    binary_surface_mesh_eroded2_labels, li_thresholded
)
histograms_surface_mesh = replace_extra_rows_with_zeros(
    Bulk_histograms, histograms_surface_mesh
)
histograms_surface_mesh = convert_h5ad(
    histograms_surface_mesh, Path_to_save_surface_mesh_histograms
)
Bulk_histograms = convert_h5ad(Bulk_histograms, Path_to_save_bulk_histogram)

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
Properties = [
    "label",
    "area",
    "min_intensity",
    "max_intensity",
    "equivalent_diameter",
    "mean_intensity",
    "bbox",
    "centroid",
]

# Calculate addl geomtrical properties with ferets
def calculate_properties(
    labels,
    li_thresholded,
    Properties,
    Path_to_save_geometrical_properties,
    unique_labels,
    Angle_spacing,
):
    Bulk_properties = (
        pd.DataFrame(
            measure.regionprops_table(labels, li_thresholded, properties=Properties)
        )
        .set_index("label")
        .rename(columns={"area": "Volume"})
    )
    Properties_Bulk = surface_areas_df.merge(Bulk_properties, how="left", on="label")
    Properties_Bulk["Volume"] = (
        Properties_Bulk["Volume"] * Voxel_size * Voxel_size * Voxel_size
    )
    Properties_Bulk["Surface Area"] = (
        Properties_Bulk["Surface Area"] * Voxel_size * Voxel_size
    )
    Properties_Bulk["equivalent_diameter"] = (
        Properties_Bulk["equivalent_diameter"] * Voxel_size
    )
    Properties_Bulk["Sphericity"] = (
        np.pi ** (1 / 3) * (6 * Properties_Bulk["Volume"]) ** (2 / 3)
    ) / (Properties_Bulk["Surface Area"])

    def process_angles(coords, angle1, angle2, angle3):
        theta1 = np.radians(angle1)
        theta2 = np.radians(angle2)
        theta3 = np.radians(angle3)
        rotation_matrix1 = np.array(
            [
                [np.cos(theta1), -np.sin(theta1), 0],
                [np.sin(theta1), np.cos(theta1), 0],
                [0, 0, 1],
            ]
        )
        rotation_matrix2 = np.array(
            [
                [np.cos(theta2), 0, -np.sin(theta2)],
                [0, 1, 0],
                [np.sin(theta2), 0, np.cos(theta2)],
            ]
        )
        rotation_matrix3 = np.array(
            [
                [1, 0, 0],
                [0, np.cos(theta3), -np.sin(theta3)],
                [0, np.sin(theta3), np.cos(theta3)],
            ]
        )
        rotated_coords = np.dot(coords, rotation_matrix1)
        rotated_coords = np.dot(rotated_coords, rotation_matrix2)
        rotated_coords = np.dot(rotated_coords, rotation_matrix3)
        max_distance = np.max(rotated_coords[:, 0]) - np.min(rotated_coords[:, 0])
        min_distance = np.max(rotated_coords[:, 1]) - np.min(rotated_coords[:, 1])
        depth_distance = np.max(rotated_coords[:, 2]) - np.min(rotated_coords[:, 2])
        return max_distance, min_distance, depth_distance

    def calculate_feret_diameters(label, coords, Angle_spacing):
        max_feret_diameter = 0
        min_feret_diameter = np.inf
        angle_combinations = [
            (angle1, angle2, angle3)
            for angle1 in range(0, 180, Angle_spacing)
            for angle2 in range(0, 180, Angle_spacing)
            for angle3 in range(0, 180, Angle_spacing)
        ]
        results = Parallel(n_jobs=-1)(
            delayed(process_angles)(coords, angle1, angle2, angle3)
            for angle1, angle2, angle3 in tqdm(
                angle_combinations, desc=f"Processing label {label}"
            )
        )
        for max_distance, min_distance, depth_distance in results:
            if max_distance > max_feret_diameter:
                max_feret_diameter = max_distance
            if min_distance < min_feret_diameter:
                min_feret_diameter = min_distance
            if depth_distance < min_feret_diameter:
                min_feret_diameter = depth_distance
        return label, max_feret_diameter, min_feret_diameter

    # Filter region_coords to include only labels in unique_labels
    #### link to ferets
    # region_coords_filtered = [(region.label, region.coords) for region in measure.regionprops(labels, intensity_image=li_thresholded, cache=False, extra_properties=None) if region.label in unique_labels]
    # results = Parallel(n_jobs=-1)(delayed(calculate_feret_diameters)(label, coords,Angle_spacing) for label, coords in tqdm(region_coords_filtered, desc="Calculating Feret diameters"))
    # feret_df = pd.DataFrame(results, columns=['label', 'Max_Feret_Diameter', 'Min_Feret_Diameter']).set_index('label')
    # Properties_Bulk = Properties_Bulk.merge(feret_df, how='left', on='label')
    # Properties_Bulk['Feret_ratio'] = Properties_Bulk['Min_Feret_Diameter'] / Properties_Bulk['Max_Feret_Diameter']
    Properties_Bulk.to_csv(Path_to_save_geometrical_properties)
    return Properties_Bulk


# Call the function with appropriate properties
Properties_Bulk = calculate_properties(
    labels,
    li_thresholded,
    Properties,
    Path_to_save_geometrical_properties,
    unique_labels,
    Angle_spacing,
)

#### link to save labels thick box
# label_image_path = os.path.join(path,'labels\*')
# labels = labels.astype(np.uint16)
# io.imsave(label_image_path\labels.tiff",labels)
finishTime = time.time()
print("Elapsed time:", finishTime - startTime)
