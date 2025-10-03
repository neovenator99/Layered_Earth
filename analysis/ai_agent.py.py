import re

class GeospatialAIAgent:
    def __init__(self):
        self.analysis_patterns = {
            'buffer': r'\b(buffer|distance|proximity)\b',
            'intersection': r'\b(intersect|overlap|cross)\b',
            'cluster': r'\b(cluster|group|pattern)\b',
            'optimal': r'\b(optimal|best|suitable)\b',
        }
    
    def process_query(self, query, available_layers):
        """Process natural language query and suggest analysis"""
        query_lower = query.lower()
        
        suggested_analyses = []
        for analysis_type, pattern in self.analysis_patterns.items():
            if re.search(pattern, query_lower):
                suggested_analyses.append(analysis_type)
        
        if not suggested_analyses:
            return "I can help with buffer analysis, intersection, clustering, and optimal location finding. Please specify what you'd like to do."
        
        response = f"Based on your query, I suggest: {', '.join(suggested_analyses)} analysis.\n"
        
        return response