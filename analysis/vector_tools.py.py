import geopandas as gpd

class VectorAnalysis:
    def __init__(self):
        self.available_tools = {
            'buffer': self.buffer_analysis,
            'intersect': self.intersection_analysis,
            'clip': self.clip_analysis,
        }
    
    def buffer_analysis(self, gdf, distance):
        """Create buffer around features"""
        buffered = gdf.copy()
        buffered.geometry = buffered.geometry.buffer(distance)
        return buffered
    
    def intersection_analysis(self, gdf1, gdf2):
        """Find intersection between two layers"""
        return gpd.overlay(gdf1, gdf2, how='intersection')
    
    def clip_analysis(self, gdf_to_clip, gdf_clipper):
        """Clip one layer with another"""
        return gpd.clip(gdf_to_clip, gdf_clipper)