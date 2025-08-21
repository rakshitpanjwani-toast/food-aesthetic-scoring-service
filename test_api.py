#!/usr/bin/env python3
"""
Test script for the Food Aesthetics API
Demonstrates how to use the API endpoints
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    print("\n🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_single_image():
    """Test scoring a single image"""
    print("\n📸 Testing single image scoring...")
    
    # Check if we have test images
    images_dir = Path("./images")
    if not images_dir.exists():
        print("❌ No images directory found")
        return False
    
    # Find first JPEG image
    image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
    if not image_files:
        print("❌ No JPEG images found in images directory")
        return False
    
    test_image = image_files[0]
    print(f"Using test image: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/score", files=files)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Aesthetic score: {result['aesthetic_score']:.4f}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_images():
    """Test scoring multiple images"""
    print("\n🖼️ Testing batch image scoring...")
    
    # Check if we have test images
    images_dir = Path("./images")
    if not images_dir.exists():
        print("❌ No images directory found")
        return False
    
    # Find JPEG images (limit to 3 for testing)
    image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
    if not image_files:
        print("❌ No JPEG images found in images directory")
        return False
    
    test_images = image_files[:3]  # Limit to 3 images
    print(f"Using {len(test_images)} test images")
    
    try:
        files = []
        # Prepare all files first
        for img_path in test_images:
            with open(img_path, 'rb') as f:
                content = f.read()
                files.append(('files', (img_path.name, content, 'image/jpeg')))
        
        response = requests.post(f"{BASE_URL}/score-batch", files=files)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Processed {result['total_images']} images")
            for item in result['results']:
                print(f"  - {item['filename']}: {item['aesthetic_score']:.4f}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Food Aesthetics API Test Suite")
    print("=" * 40)
    
    # Make sure API is running
    print("⚠️  Make sure the API server is running (./start_api.sh)")
    print("")
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Single Image Scoring", test_single_image),
        ("Batch Image Scoring", test_batch_images)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server and try again.")

if __name__ == "__main__":
    main()
