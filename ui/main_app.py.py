import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import threading
import time
from datetime import datetime

from layered_earth.core.map_engine import MapEngine
from layered_earth.core.layer_manager import LayerManager
from layered_earth.analysis.vector_tools import VectorAnalysis
from layered_earth.analysis.ai_agent import GeospatialAIAgent
from layered_earth.ui.dashboard import Dashboard
from layered_earth.data.real_time import RealTimeData
from layered_earth.demo.sample_data import SampleDataGenerator

class LayeredEarthApp:
    def __init__(self):
        self.map_engine = MapEngine()
        self.layer_manager = LayerManager()
        self.vector_tools = VectorAnalysis()
        self.ai_agent = GeospatialAIAgent()
        self.real_time_data = RealTimeData()
        self.dashboard = None
        self.dashboard_visible = False
        
        self.real_time_data.register_update_callback(self.on_real_time_update)
        self.setup_ui()
        self.load_sample_data()
        self.real_time_data.start_real_time_updates()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.map_engine.ax.set_position([0.3, 0.1, 0.65, 0.85])
        self.create_control_panels()
        self.map_engine.fig.canvas.mpl_connect('button_press_event', self.on_click)
    
    def create_control_panels(self):
        """Create all control panels"""
        # Layer controls
        self.layer_ax = plt.axes([0.02, 0.8, 0.25, 0.15])
        self.layer_ax.set_title("Layer Controls", fontweight='bold')
        self.layer_ax.set_xticks([])
        self.layer_ax.set_yticks([])
        
        self.add_layer_ax = plt.axes([0.02, 0.75, 0.12, 0.04])
        self.add_layer_btn = Button(self.add_layer_ax, 'Add Layer')
        
        # Real-time data controls
        self.realtime_ax = plt.axes([0.02, 0.7, 0.25, 0.08])
        self.realtime_ax.set_title("Real-time Data", fontweight='bold')
        self.realtime_ax.set_xticks([])
        self.realtime_ax.set_yticks([])
        
        self.earthquake_ax = plt.axes([0.02, 0.65, 0.12, 0.04])
        self.earthquake_btn = Button(self.earthquake_ax, 'Earthquakes')
        self.earthquake_btn.on_clicked(self.add_earthquake_data)
        
        self.weather_ax = plt.axes([0.15, 0.65, 0.12, 0.04])
        self.weather_btn = Button(self.weather_ax, 'Weather')
        self.weather_btn.on_clicked(self.add_weather_data)
        
        # Dashboard controls
        self.dashboard_ax = plt.axes([0.02, 0.6, 0.12, 0.04])
        self.dashboard_btn = Button(self.dashboard_ax, 'Show Dashboard')
        self.dashboard_btn.on_clicked(self.toggle_dashboard)
        
        # AI Assistant
        self.ai_ax = plt.axes([0.02, 0.55, 0.23, 0.04])
        self.ai_text = TextBox(self.ai_ax, 'AI Assistant:', initial='Ask for analysis...')
        self.ai_text.on_submit(self.ask_ai_assistant)
    
    def toggle_dashboard(self, event):
        """Toggle dashboard visibility"""
        if self.dashboard_visible:
            self.map_engine.ax.set_position([0.3, 0.1, 0.65, 0.85])
            if self.dashboard:
                for ax in self.dashboard.charts.values():
                    ax.set_visible(False)
            self.dashboard_visible = False
            self.dashboard_btn.label.set_text('Show Dashboard')
        else:
            self.map_engine.ax.set_position([0.3, 0.5, 0.65, 0.45])
            if not self.dashboard:
                self.dashboard = Dashboard(self.map_engine.fig, [0.02, 0.05, 0.28, 0.45])
            else:
                for ax in self.dashboard.charts.values():
                    ax.set_visible(True)
            
            self.dashboard.update_all_charts(self.layer_manager.available_layers)
            self.dashboard_visible = True
            self.dashboard_btn.label.set_text('Hide Dashboard')
        
        self.map_engine._refresh_map()
    
    def add_earthquake_data(self, event):
        """Add real-time earthquake data"""
        gdf = self.real_time_data.add_earthquake_feed("Earthquakes")
        if gdf is not None:
            style = {
                'color': 'red',
                'markersize': gdf['magnitude'] * 20,
                'alpha': 0.7
            }
            self.map_engine.add_vector_layer(gdf, "Earthquakes", style)
            self.layer_manager.available_layers["Earthquakes"] = {
                'type': 'vector', 
                'data': gdf
            }
            print("Earthquake data added!")
    
    def add_weather_data(self, event):
        """Add simulated weather data"""
        gdf = self.real_time_data.add_weather_stations("Weather Stations")
        if gdf is not None:
            style = {
                'color': 'blue',
                'markersize': 50,
                'alpha': 0.6
            }
            self.map_engine.add_vector_layer(gdf, "Weather Stations", style)
            self.layer_manager.available_layers["Weather Stations"] = {
                'type': 'vector', 
                'data': gdf
            }
            print("Weather station data added!")
    
    def on_real_time_update(self, layer_name, new_data):
        """Handle real-time data updates"""
        if layer_name in self.layer_manager.available_layers:
            self.layer_manager.available_layers[layer_name]['data'] = new_data
            print(f"Updated: {layer_name} at {datetime.now().strftime('%H:%M:%S')}")
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        sample_gen = SampleDataGenerator()
        
        admin_gdf = sample_gen.generate_admin_boundaries()
        self.map_engine.add_vector_layer(admin_gdf, "Admin Boundaries", 
                                       {'color': 'lightblue', 'edgecolor': 'blue', 'alpha': 0.3})
        self.layer_manager.available_layers["Admin Boundaries"] = {
            'type': 'vector', 
            'data': admin_gdf
        }
        
        poi_gdf = sample_gen.generate_points_of_interest()
        self.map_engine.add_vector_layer(poi_gdf, "Points of Interest", 
                                       {'color': 'red', 'markersize': 50})
        self.layer_manager.available_layers["Points of Interest"] = {
            'type': 'vector', 
            'data': poi_gdf
        }
        
        print("Sample data loaded!")
    
    def ask_ai_assistant(self, text):
        """Query AI assistant"""
        response = self.ai_agent.process_query(text, self.layer_manager.available_layers)
        print(f"AI Assistant: {response}")
    
    def on_click(self, event):
        """Handle map clicks"""
        if event.inaxes == self.map_engine.ax:
            from shapely.geometry import Point
            popup_info = self.map_engine.show_popup(event.xdata, event.ydata)
            if popup_info:
                print(f"Click at ({event.xdata:.4f}, {event.ydata:.4f}):")
                for layer, features in popup_info.items():
                    print(f"  {layer}: {len(features)} features found")
    
    def show(self):
        """Display the application"""
        plt.show()

def launch_app():
    """Launch the Layered-Earth application"""
    app = LayeredEarthApp()
    return app