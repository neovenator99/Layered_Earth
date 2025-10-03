import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
from shapely.geometry import Point

class MapEngine:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.layers = {}
        self.current_bounds = None
        self.setup_map()
    
    def setup_map(self):
        """Initialize the map canvas"""
        self.ax.set_title("Layered-Earth Geospatial System", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        self.ax.grid(True, alpha=0.3)
        
        self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)
        plt.ion()
    
    def add_vector_layer(self, gdf, layer_name, style=None):
        """Add vector layer to map"""
        if layer_name in self.layers:
            print(f"Layer '{layer_name}' already exists")
            return
        
        self.layers[layer_name] = {
            'type': 'vector',
            'data': gdf,
            'style': style or {'color': 'blue', 'alpha': 0.5}
        }
        
        gdf.plot(ax=self.ax, **self.layers[layer_name]['style'])
        self._update_bounds()
        self._refresh_map()
    
    def _update_bounds(self):
        """Update map bounds based on all layers"""
        all_bounds = []
        for layer in self.layers.values():
            if layer['type'] == 'vector':
                bounds = layer['data'].total_bounds
                all_bounds.append(bounds)
        
        if all_bounds:
            all_bounds = np.array(all_bounds)
            total_bounds = [
                all_bounds[:, 0].min(), all_bounds[:, 1].min(),
                all_bounds[:, 2].max(), all_bounds[:, 3].max()
            ]
            self.ax.set_xlim(total_bounds[0], total_bounds[2])
            self.ax.set_ylim(total_bounds[1], total_bounds[3])
            self.current_bounds = total_bounds
    
    def _refresh_map(self):
        """Refresh the map display"""
        self.ax.figure.canvas.draw_idle()
    
    def show_popup(self, x, y, tolerance=0.01):
        """Show popup information for features at clicked location"""
        popup_info = {}
        
        for layer_name, layer in self.layers.items():
            if layer['type'] == 'vector':
                gdf = layer['data']
                for idx, row in gdf.iterrows():
                    if hasattr(row.geometry, 'contains'):
                        if row.geometry.contains(Point(x, y)):
                            if layer_name not in popup_info:
                                popup_info[layer_name] = []
                            popup_info[layer_name].append(dict(row))
        
        return popup_info
    
    def get_layer_names(self):
        """Get list of all layer names"""
        return list(self.layers.keys())