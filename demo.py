#!/usr/bin/env python3
"""
Simple demo script for the Food Aesthetics API
Shows basic usage examples
"""

import requests
import json
from pathlib import Path

def demo_api():
    """Demonstrate the API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🍽️ Food Aesthetics API Demo")
    print("=" * 40)
    print("Make sure the API server is running with: ./start_api.sh")
    print()
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API is healthy and ready!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Start it with: ./start_api.sh")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print()
    
    # Test root endpoint
    print("2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   API Version: {response.json()['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test single image scoring
    print("3. Testing single image scoring...")
    images_dir = Path("./images")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
        if image_files:
            test_image = image_files[0]
            print(f"   Using test image: {test_image.name}")
            
            try:
                with open(test_image, 'rb') as f:
                    files = {'file': (test_image.name, f, 'image/jpeg')}
                    response = requests.post(f"{base_url}/score", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    score = result['aesthetic_score']
                    print(f"✅ Success! Aesthetic Score: {score:.4f}")
                    
                    # Interpret the score
                    if score < 0.2:
                        quality = "Low"
                    elif score < 0.4:
                        quality = "Below Average"
                    elif score < 0.6:
                        quality = "Average"
                    elif score < 0.8:
                        quality = "Above Average"
                    else:
                        quality = "High"
                    
                    print(f"   Quality Level: {quality}")
                else:
                    print(f"❌ Scoring failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ No test images found in ./images directory")
    else:
        print("❌ Images directory not found")
    
    print()
    print("🎉 Demo completed!")
    print()
    print("Next steps:")
    print("1. Start the API server: ./start_api.sh")
    print("2. Open interactive docs: http://localhost:8000/docs")
    print("3. Run full tests: python test_api.py")
    print("4. Make your own API calls!")

if __name__ == "__main__":
    demo_api()
