import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon

class SampleDataGenerator:
    def __init__(self):
        self.base_bounds = [-122.5, 37.5, -122.2, 37.8]  # San Francisco area
    
    def generate_admin_boundaries(self):
        """Generate sample administrative boundaries"""
        bounds = self.base_bounds
        polygons = []
        names = []
        
        for i in range(3):
            for j in range(3):
                left = bounds[0] + (i * (bounds[2]-bounds[0]) / 3)
                right = bounds[0] + ((i + 1) * (bounds[2]-bounds[0]) / 3)
                bottom = bounds[1] + (j * (bounds[3]-bounds[1]) / 3)
                top = bounds[1] + ((j + 1) * (bounds[3]-bounds[1]) / 3)
                
                polygon = Polygon([
                    (left, bottom), (right, bottom), 
                    (right, top), (left, top)
                ])
                
                polygons.append(polygon)
                names.append(f"District {i*3 + j + 1}")
        
        return gpd.GeoDataFrame({
            'name': names,
            'population': np.random.randint(1000, 50000, 9)
        }, geometry=polygons, crs="EPSG:4326")
    
    def generate_points_of_interest(self):
        """Generate sample points of interest"""
        bounds = self.base_bounds
        points = []
        
        for i in range(15):
            lon = np.random.uniform(bounds[0], bounds[2])
            lat = np.random.uniform(bounds[1], bounds[3])
            points.append(Point(lon, lat))
        
        return gpd.GeoDataFrame({
            'name': [f"POI {i+1}" for i in range(15)],
            'type': np.random.choice(['School', 'Hospital', 'Park', 'Mall'], 15)
        }, geometry=points, crs="EPSG:4326")