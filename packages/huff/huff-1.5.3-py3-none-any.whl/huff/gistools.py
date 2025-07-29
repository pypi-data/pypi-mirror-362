#-----------------------------------------------------------------------
# Name:        gistools (huff package)
# Purpose:     GIS tools
# Author:      Thomas Wieland 
#              ORCID: 0000-0001-5168-9846
#              mail: geowieland@googlemail.com              
# Version:     1.4.1
# Last update: 2025-06-16 17:44
# Copyright (c) 2025 Thomas Wieland
#-----------------------------------------------------------------------


import geopandas as gp
import pandas as pd
from pandas.api.types import is_numeric_dtype
from math import pi, sin, cos, acos


def distance_matrix(
    sources: list,
    destinations: list,
    unit: str = "m",
    ):

    def euclidean_distance (
        source: list,
        destination: list,
        unit: str = "m"
        ):

        lon1 = source[0]
        lat1 = source[1]
        lon2 = destination[0]
        lat2 = destination[1]

        lat1_r = lat1*pi/180
        lon1_r = lon1*pi/180
        lat2_r = lat2*pi/180
        lon2_r = lon2*pi/180

        distance = 6378 * (acos(sin(lat1_r) * sin(lat2_r) + cos(lat1_r) * cos(lat2_r) * cos(lon2_r - lon1_r)))
        if unit == "m": 
            distance = distance*1000
        if unit == "mile": 
            distance = distance/1.60934

        return distance

    matrix = []

    for source in sources:
        row = []
        for destination in destinations:
            dist = euclidean_distance(
                source, 
                destination, 
                unit
                )
            row.append(dist)
        matrix.append(row)

    return matrix


def buffers(
    point_gdf: gp.GeoDataFrame,
    unique_id_col: str,
    distances: list,
    donut: bool = True,
    save_output: bool = True,
    output_filepath: str = "buffers.shp",
    output_crs: str = "EPSG:4326"
    ):    
  
    all_buffers_gdf = gp.GeoDataFrame(columns=[unique_id_col, "segment", "geometry"])

    for idx, row in point_gdf.iterrows():

        point_buffers = []

        for distance in distances:

            point = row["geometry"] 
            point_buffer = point.buffer(distance)

            point_buffer_gdf = gp.GeoDataFrame(
            {
                unique_id_col: row[unique_id_col],
                "geometry": [point_buffer], 
                "segment": [distance]
                },
                crs=point_gdf.crs
            )
        
            point_buffers.append(point_buffer_gdf)

        point_buffers_gdf = pd.concat(
            point_buffers, 
            ignore_index = True
            )

        if donut:
            point_buffers_gdf = overlay_difference(
                polygon_gdf = point_buffers_gdf, 
                sort_col = "segment"
                )
 
        all_buffers_gdf = pd.concat(
            [
                all_buffers_gdf,
                point_buffers_gdf
                ], 
            ignore_index = True)

    all_buffers_gdf = all_buffers_gdf.to_crs(output_crs)

    if save_output:
        all_buffers_gdf.to_file(output_filepath)
        print ("Saved as", output_filepath)

    return all_buffers_gdf 


def overlay_difference(
    polygon_gdf: gp.GeoDataFrame, 
    sort_col: str = None,
    ):

    if sort_col is not None:
        polygon_gdf = polygon_gdf.sort_values(by=sort_col).reset_index(drop=True)
    else:
        polygon_gdf = polygon_gdf.reset_index(drop=True)

    new_geometries = []
    new_data = []

    for i in range(len(polygon_gdf) - 1, 0, -1):
        
        current_polygon = polygon_gdf.iloc[i].geometry
        previous_polygon = polygon_gdf.iloc[i - 1].geometry
        difference_polygon = current_polygon.difference(previous_polygon)

        if difference_polygon.is_empty or not difference_polygon.is_valid:
            continue

        new_geometries.append(difference_polygon)
        new_data.append(polygon_gdf.iloc[i].drop("geometry"))

    inner_most_polygon = polygon_gdf.iloc[0].geometry

    if inner_most_polygon.is_valid:

        new_geometries.append(inner_most_polygon)
        new_data.append(polygon_gdf.iloc[0].drop("geometry"))

    polygon_gdf_difference = gp.GeoDataFrame(
        new_data, geometry=new_geometries, crs=polygon_gdf.crs
    )

    return polygon_gdf_difference


def point_spatial_join(
    polygon_gdf: gp.GeoDataFrame,
    point_gdf: gp.GeoDataFrame,
    join_type: str = "inner",
    polygon_ref_cols: list = [],
    point_stat_col: str = None
    ):
    
    if polygon_gdf is None:
        raise ValueError("Parameter 'polygon_gdf' is None")
    if point_gdf is None:
        raise ValueError("Parameter 'point_gdf' is None")
    
    if polygon_gdf.crs != point_gdf.crs:
        raise ValueError(f"Coordinate reference systems of polygon and point data do not match. Polygons: {str(polygon_gdf.crs)}, points: {str(point_gdf.crs)}")
    
    if polygon_ref_cols != []:
        for polygon_ref_col in polygon_ref_cols:
            if polygon_ref_col not in polygon_gdf.columns:
                raise KeyError (f"Column {polygon_ref_col} not in polygon data")
        
    if point_stat_col is not None:
        if point_stat_col not in point_gdf.columns:
            raise KeyError (f"Column {point_stat_col} not in point data")
        if not is_numeric_dtype(point_gdf[point_stat_col]):
            raise TypeError (f"Column {point_stat_col} is not numeric")
               
    shp_points_gdf_join = point_gdf.sjoin(
        polygon_gdf, 
        how=join_type
        )

    spatial_join_stat = None

    if polygon_ref_cols != [] and point_stat_col is not None:
        shp_points_gdf_join_count = shp_points_gdf_join.groupby(polygon_ref_cols)[point_stat_col].count()
        shp_points_gdf_join_sum = shp_points_gdf_join.groupby(polygon_ref_cols)[point_stat_col].sum()
        shp_points_gdf_join_min = shp_points_gdf_join.groupby(polygon_ref_cols)[point_stat_col].min()
        shp_points_gdf_join_max = shp_points_gdf_join.groupby(polygon_ref_cols)[point_stat_col].max()
        shp_points_gdf_join_mean = shp_points_gdf_join.groupby(polygon_ref_cols)[point_stat_col].mean()
        
        shp_points_gdf_join_count = shp_points_gdf_join_count.rename("count").to_frame()
        shp_points_gdf_join_sum = shp_points_gdf_join_sum.rename("sum").to_frame()
        shp_points_gdf_join_min = shp_points_gdf_join_min.rename("min").to_frame()
        shp_points_gdf_join_max = shp_points_gdf_join_max.rename("max").to_frame()
        shp_points_gdf_join_mean = shp_points_gdf_join_mean.rename("mean").to_frame()
        spatial_join_stat = shp_points_gdf_join_count.join(
            [
                shp_points_gdf_join_sum, 
                shp_points_gdf_join_min, 
                shp_points_gdf_join_max,
                shp_points_gdf_join_mean
                ]
            )

    return [
        shp_points_gdf_join,
        spatial_join_stat
        ]