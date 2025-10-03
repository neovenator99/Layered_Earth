import requests
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
import time
import threading
import random
from shapely.geometry import Point

class RealTimeData:
    def __init__(self):
        self.active_feeds = {}
        self.update_callbacks = []
    
    def add_earthquake_feed(self, layer_name="Earthquakes"):
        """Add real-time earthquake data from USGS"""
        try:
            response = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson', timeout=10)
            data = response.json()
            
            features = []
            for feature in data['features']:
                props = feature['properties']
                geom = feature['geometry']
                
                features.append({
                    'magnitude': props['mag'],
                    'place': props['place'],
                    'time': datetime.fromtimestamp(props['time'] / 1000),
                    'geometry': Point(geom['coordinates'][0], geom['coordinates'][1])
                })
            
            gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")
            self.active_feeds[layer_name] = {
                'type': 'earthquake',
                'data': gdf,
                'update_interval': 60,
                'last_update': datetime.now()
            }
            return gdf
            
        except Exception as e:
            print(f"Error fetching earthquake data: {e}")
            return self._create_sample_earthquakes()
    
    def _create_sample_earthquakes(self):
        """Create sample earthquake data for demo"""
        features = []
        for i in range(10):
            features.append({
                'magnitude': random.uniform(1.0, 5.0),
                'place': f"Sample Location {i}",
                'time': datetime.now(),
                'geometry': Point(random.uniform(-180, 180), random.uniform(-90, 90))
            })
        
        return gpd.GeoDataFrame(features, crs="EPSG:4326")
    
    def add_weather_stations(self, layer_name="Weather Stations"):
        """Add simulated weather station data"""
        stations = []
        for i in range(20):
            stations.append({
                'station_id': f"ST{i:03d}",
                'temperature': random.uniform(-10, 35),
                'humidity': random.uniform(30, 100),
                'geometry': Point(random.uniform(-180, 180), random.uniform(-90, 90))
            })
        
        gdf = gpd.GeoDataFrame(stations, crs="EPSG:4326")
        self.active_feeds[layer_name] = {
            'type': 'weather',
            'data': gdf,
            'update_interval': 300,
            'last_update': datetime.now()
        }
        return gdf
    
    def start_real_time_updates(self):
        """Start background thread for real-time data updates"""
        def update_loop():
            while True:
                for layer_name, feed in self.active_feeds.items():
                    if (datetime.now() - feed['last_update']).seconds > feed['update_interval']:
                        if feed['type'] == 'earthquake':
                            self.add_earthquake_feed(layer_name)
                        self.simulate_data_update(layer_name)
                
                time.sleep(30)
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def simulate_data_update(self, layer_name):
        """Simulate real-time data updates"""
        feed = self.active_feeds[layer_name]
        feed['last_update'] = datetime.now()
        
        for callback in self.update_callbacks:
            callback(layer_name, feed['data'])
    
    def register_update_callback(self, callback):
        """Register callback for real-time updates"""
        self.update_callbacks.append(callback)