import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self, fig, position):
        self.fig = fig
        self.position = position
        self.charts = {}
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Initialize dashboard with multiple chart areas"""
        self.dashboard_gs = GridSpec(2, 2, left=self.position[0], 
                                   bottom=self.position[1], 
                                   right=self.position[2], 
                                   top=self.position[3])
        
        self.charts['stats'] = self.fig.add_subplot(self.dashboard_gs[0, 0])
        self.charts['timeline'] = self.fig.add_subplot(self.dashboard_gs[0, 1])
        self.charts['histogram'] = self.fig.add_subplot(self.dashboard_gs[1, 0])
        self.charts['pie'] = self.fig.add_subplot(self.dashboard_gs[1, 1])
        
        self.initialize_charts()
    
    def initialize_charts(self):
        """Initialize empty charts"""
        for name, ax in self.charts.items():
            ax.set_title(f"{name.title()} Chart", fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])
    
    def update_statistics(self, layers):
        """Update statistics chart with layer information"""
        ax = self.charts['stats']
        ax.clear()
        
        if layers:
            stats_data = []
            for name, layer in layers.items():
                if layer['type'] == 'vector':
                    gdf = layer['data']
                    stats_data.append({
                        'Layer': name,
                        'Features': len(gdf)
                    })
            
            if stats_data:
                df = pd.DataFrame(stats_data)
                ax.bar(df['Layer'], df['Features'], alpha=0.7)
                ax.set_title('Layer Statistics')
                ax.tick_params(axis='x', rotation=45)
        
        ax.grid(True, alpha=0.3)
    
    def update_all_charts(self, layers):
        """Update all dashboard charts"""
        self.update_statistics(layers)
        self.update_timeline()
        self.update_histogram()
        self.update_pie_chart()
        self.fig.canvas.draw_idle()
    
    def update_timeline(self):
        """Sample timeline update"""
        ax = self.charts['timeline']
        ax.clear()
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        values = np.cumsum(np.random.randn(30) + 100)
        ax.plot(dates, values)
        ax.set_title('Temporal Analysis')
        ax.grid(True, alpha=0.3)
    
    def update_histogram(self):
        """Sample histogram update"""
        ax = self.charts['histogram']
        ax.clear()
        data = np.random.normal(100, 15, 200)
        ax.hist(data, bins=20, alpha=0.7)
        ax.set_title('Distribution Analysis')
        ax.grid(True, alpha=0.3)
    
    def update_pie_chart(self):
        """Sample pie chart update"""
        ax = self.charts['pie']
        ax.clear()
        sizes = [45, 25, 15, 10, 5]
        labels = ['Residential', 'Commercial', 'Industrial', 'Agricultural', 'Other']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Category Distribution')