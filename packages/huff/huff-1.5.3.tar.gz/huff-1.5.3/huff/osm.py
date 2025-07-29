#-----------------------------------------------------------------------
# Name:        osm (huff package)
# Purpose:     Helper functions for OpenStreetMap API
# Author:      Thomas Wieland 
#              ORCID: 0000-0001-5168-9846
#              mail: geowieland@googlemail.com              
# Version:     1.4.1
# Last update: 2025-06-16 17:44
# Copyright (c) 2025 Thomas Wieland
#-----------------------------------------------------------------------


import pandas as pd
import geopandas as gpd
import math
import requests
import tempfile
import time
import os
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import contextily as cx
from shapely.geometry import box


class Client:

    def __init__(
        self,
        server = "http://a.tile.openstreetmap.org/",
        headers = {
           'User-Agent': 'huff.osm/1.0.0 (your_name@your_email_provider.com)'
           }
        ):
        
        self.server = server
        self.headers = headers

    def download_tile(
        self,
        zoom, 
        x, 
        y,
        timeout = 10
        ):

        osm_url = self.server + f"{zoom}/{x}/{y}.png"
       
        response = requests.get(
            osm_url, 
            headers = self.headers,
            timeout = timeout
            )

        if response.status_code == 200:

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
            return Image.open(tmp_file_path)
        
        else:

            print(f"Error while accessing OSM server. Status code: {response.status_code} - {response.reason}")

            return None
    

def get_basemap(
    sw_lat, 
    sw_lon, 
    ne_lat, 
    ne_lon, 
    zoom = 15
    ):

    def lat_lon_to_tile(
        lat, 
        lon, 
        zoom
        ):

        n = 2 ** zoom
        x = int(n * ((lon + 180) / 360))
        y = int(n * (1 - (math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi)) / 2)
        return x, y

    def stitch_tiles(
        zoom, 
        sw_lat, 
        sw_lon, 
        ne_lat, 
        ne_lon,
        delay = 0.1
        ):

        osm_client = Client(
            server = "http://a.tile.openstreetmap.org/"
            )
        
        sw_x_tile, sw_y_tile = lat_lon_to_tile(sw_lat, sw_lon, zoom)
        ne_x_tile, ne_y_tile = lat_lon_to_tile(ne_lat, ne_lon, zoom)

        tile_size = 256
        width = (ne_x_tile - sw_x_tile + 1) * tile_size
        height = (sw_y_tile - ne_y_tile + 1) * tile_size

        stitched_image = Image.new('RGB', (width, height))
        
        for x in range(sw_x_tile, ne_x_tile + 1):
            for y in range(ne_y_tile, sw_y_tile + 1):
                tile = osm_client.download_tile(
                    zoom = zoom, 
                    x = x, 
                    y = y
                    )
                if tile:
                    
                    stitched_image.paste(tile, ((x - sw_x_tile) * tile_size, (sw_y_tile - y) * tile_size))
                else:
                    print(f"Error while retrieving tile {x}, {y}.")

                time.sleep(delay)
        
        return stitched_image
    
    stitched_image = stitch_tiles(zoom, sw_lat, sw_lon, ne_lat, ne_lon)

    if stitched_image:

        stitched_image_path = "osm_map.png"
        stitched_image.save(stitched_image_path)

    else:
        print("Error while building stitched images")


def map_with_basemap(
    layers: list,
    osm_basemap: bool = True,
    zoom: int = 15,
    styles: dict = {},
    save_output: bool = True,
    output_filepath: str = "osm_map_with_basemap.png",
    output_dpi=300,
    legend: bool = True
):
    if not layers:
        raise ValueError("List layers is empty")

    combined = gpd.GeoDataFrame(
        pd.concat(layers, ignore_index=True),
        crs=layers[0].crs
    )

    combined_wgs84 = combined.to_crs(epsg=4326)
    bounds = combined_wgs84.total_bounds

    sw_lon, sw_lat, ne_lon, ne_lat = bounds[0]*0.9999, bounds[1]*0.9999, bounds[2]*1.0001, bounds[3]*1.0001

    if osm_basemap:
        get_basemap(sw_lat, sw_lon, ne_lat, ne_lon, zoom=zoom)

    fig, ax = plt.subplots(figsize=(10, 10))

    if osm_basemap:
        img = Image.open("osm_map.png")
        extent_img = [sw_lon, ne_lon, sw_lat, ne_lat]
        ax.imshow(img, extent=extent_img, origin="upper")

    i = 0
    legend_handles = []

    for layer in layers:
        layer_3857 = layer.to_crs(epsg=3857)

        if styles != {}:
            layer_style = styles[i]
            layer_color = layer_style["color"]
            layer_alpha = layer_style["alpha"]
            layer_name = layer_style["name"]           

            if isinstance(layer_color, str):
                layer_3857.plot(
                    ax=ax,
                    color=layer_color,
                    alpha=layer_alpha,
                    label=layer_name                    
                )
                if legend:
                    patch = Patch(
                        facecolor=layer_color, 
                        alpha=layer_alpha, 
                        label=layer_name
                        )
                    legend_handles.append(patch)

            elif isinstance(layer_color, dict):
                color_key = list(layer_color.keys())[0]
                color_mapping = layer_color[color_key]

                if color_key not in layer_3857.columns:
                    raise KeyError("Column " + color_key + " not in layer.")

                for value, color in color_mapping.items():
                    
                    subset = layer_3857[layer_3857[color_key].astype(str) == str(value)]
                    
                    if not subset.empty:
                        
                        subset.plot(
                            ax=ax,
                            color=color,
                            alpha=layer_alpha,
                            label=str(value)
                        )
                        
                        if legend:
                            patch = Patch(facecolor=color, alpha=layer_alpha, label=str(value))
                            legend_handles.append(patch)

        else:
            
            layer_3857.plot(ax=ax, alpha=0.6, label=f"Layer {i+1}")
            
            if legend:
                
                patch = Patch(
                    facecolor="gray", 
                    alpha=0.6, 
                    label=f"Layer {i+1}"
                    )
                
                legend_handles.append(patch)

        i += 1

    bbox = box(sw_lon, sw_lat, ne_lon, ne_lat)
    extent_geom = gpd.GeoSeries([bbox], crs=4326).to_crs(epsg=3857).total_bounds
    ax.set_xlim(extent_geom[0], extent_geom[2])
    ax.set_ylim(extent_geom[1], extent_geom[3])

    if osm_basemap:
        cx.add_basemap(
            ax,
            source=cx.providers.OpenStreetMap.Mapnik,
            zoom=zoom
        )

    plt.axis('off')

    if legend and legend_handles:
        ax.legend(handles=legend_handles, loc='lower right', fontsize='small', frameon=True)

    plt.show()

    if save_output:
        plt.savefig(
            output_filepath,
            dpi=output_dpi,
            bbox_inches="tight"
        )
        plt.close()

    if os.path.exists("osm_map.png"):
        os.remove("osm_map.png")