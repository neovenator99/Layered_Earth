import geopandas as gpd
import pandas as pd
from pathlib import Path

class LayerManager:
    def __init__(self):
        self.available_layers = {}
        self.symbology_settings = {}
    
    def load_file(self, file_path, layer_name=None):
        """Load various geospatial file formats"""
        file_path = Path(file_path)
        
        if not layer_name:
            layer_name = file_path.stem
        
        try:
            if file_path.suffix.lower() in ['.shp', '.geojson', '.json']:
                gdf = gpd.read_file(file_path)
                self.available_layers[layer_name] = {
                    'type': 'vector',
                    'data': gdf,
                    'crs': gdf.crs
                }
                return gdf
                
            elif file_path.suffix.lower() in ['.csv']:
                df = pd.read_csv(file_path)
                
                lat_col = next((col for col in df.columns if 'lat' in col.lower()), None)
                lon_col = next((col for col in df.columns if 'lon' in col.lower()), None)
                
                if lat_col and lon_col:
                    gdf = gpd.GeoDataFrame(
                        df, 
                        geometry=gpd.points_from_xy(df[lon_col], df[lat_col])
                    )
                else:
                    raise ValueError("No lat/lon columns found")
                
                self.available_layers[layer_name] = {
                    'type': 'vector',
                    'data': gdf,
                    'crs': gdf.crs if hasattr(gdf, 'crs') else 'EPSG:4326'
                }
                return gdf
                
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            raise
    
    def set_symbology(self, layer_name, style_dict):
        """Set symbology for a layer"""
        self.symbology_settings[layer_name] = style_dict
    
    def get_layer(self, layer_name):
        """Get layer data by name"""
        return self.available_layers.get(layer_name)
    
    def remove_layer(self, layer_name):
        """Remove layer from manager"""
        if layer_name in self.available_layers:
            del self.available_layers[layer_name]