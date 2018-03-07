import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from pcl_helper import *

#########
# NOTE: #
#########
# Copy this into your sensor_stick package to recreate the feature extraction used for this project.

def rgb_to_hsv(rgb_list):
    rgb_normalized = [1.0*rgb_list[0]/255, 1.0*rgb_list[1]/255, 1.0*rgb_list[2]/255]
    hsv_normalized = matplotlib.colors.rgb_to_hsv([[rgb_normalized]])[0][0]
    return hsv_normalized


def compute_color_histograms(cloud, using_hsv=False):

    # Compute histograms for the clusters
    point_colors_list = []

    # Step through each point in the point cloud
    for point in pc2.read_points(cloud, skip_nans=True):
        rgb_list = float_to_rgb(point[3])
        if using_hsv:
            point_colors_list.append(rgb_to_hsv(rgb_list) * 255)
        else:
            point_colors_list.append(rgb_list)

    # Populate lists with color values
    channel_1_vals = []
    channel_2_vals = []
    channel_3_vals = []

    for color in point_colors_list:
        channel_1_vals.append(color[0])
        channel_2_vals.append(color[1])
        channel_3_vals.append(color[2])

    # Compute histograms
    nbins = 25;
    bins_range = (0,256);
    hist_c1 = np.histogram(channel_1_vals,bins=nbins,range=bins_range)
    hist_c2 = np.histogram(channel_2_vals,bins=nbins,range=bins_range)
    hist_c3 = np.histogram(channel_3_vals,bins=nbins,range=bins_range)

    # Concatenate and normalize the histograms
    features = np.concatenate((hist_c1[0],hist_c2[0],hist_c3[0])).astype(np.float64);
    normed_features = features / np.sum(features);

    return normed_features 


def compute_normal_histograms(normal_cloud):
    norm_x_vals = []
    norm_y_vals = []
    norm_z_vals = []

    for norm_component in pc2.read_points(normal_cloud,
                                          field_names = ('normal_x', 'normal_y', 'normal_z'),
                                          skip_nans=True):
        norm_x_vals.append(norm_component[0])
        norm_y_vals.append(norm_component[1])
        norm_z_vals.append(norm_component[2])

    # Compute histograms of normal values (just like with color)
    nbins = 5;
    bins_range = (-1,1);
    #hist_nx = np.histogram(norm_x_vals,bins=nbins,range=bins_range)
    #hist_ny = np.histogram(norm_y_vals,bins=nbins,range=bins_range)
    hist_nz = np.histogram(norm_z_vals,bins=nbins,range=bins_range)

    # Concatenate and normalize the histograms
    #features = np.concatenate((hist_nx[0],hist_ny[0],hist_nz[0])).astype(np.float64);
    features = hist_nz[0].astype(np.float64);
    normed_features = features / np.sum(features);

    return normed_features
