#!/usr/bin/env python3
"""
Layered-Earth Demo Runner
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("🚀 Starting Layered-Earth: Geospatial Special Support System")
    print("=" * 60)
    
    try:
        from layered_earth import launch
        
        print("✅ Successfully imported Layered-Earth")
        print("📊 Loading sample data...")
        print("🌐 Initializing real-time data feeds...")
        print("📈 Setting up dashboard...")
        print("\n💡 Tips:")
        print("   - Click 'Show Dashboard' to see analytics")
        print("   - Click 'Earthquakes' for real-time data")
        print("   - Click 'Weather' for simulated weather stations")
        print("   - Click on map features for popup information")
        print("   - Use the AI Assistant for analysis suggestions")
        print("\n🖱️  The application will open in a new window...")
        
        app = launch()
        app.show()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure all files are in the correct folders")
        print("2. Run: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()