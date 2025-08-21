#!/usr/bin/env python3
"""
Test script for the Food Aesthetics API with base64 image data
Tests the new endpoints designed for Hugging Face Spaces and service-to-service calls
"""

import requests
import json
import base64
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def encode_image_to_base64(image_path):
    """Convert image file to base64 string"""
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
        return base64.b64encode(image_bytes).decode('utf-8')

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

def test_single_image_base64():
    """Test scoring a single image using base64 data"""
    print("\n📸 Testing single image scoring with base64...")
    
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
        # Encode image to base64
        image_base64 = encode_image_to_base64(test_image)
        
        # Prepare request payload
        payload = {
            "image_data": image_base64,
            "image_format": "jpeg"
        }
        
        # Make API call
        response = requests.post(f"{BASE_URL}/score", json=payload)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Aesthetic Score: {result['aesthetic_score']:.4f}")
            print(f"   Image Size: {result['image_size']}")
            print(f"   Format: {result['image_format']}")
            return True
        else:
            print(f"❌ Scoring failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_images_base64():
    """Test scoring multiple images using base64 data"""
    print("\n🖼️ Testing batch image scoring with base64...")
    
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
        # Prepare batch payload
        images_payload = []
        for img_path in test_images:
            image_base64 = encode_image_to_base64(img_path)
            images_payload.append({
                "image_data": image_base64,
                "image_format": "jpeg"
            })
        
        # Make API call
        response = requests.post(f"{BASE_URL}/score-batch", json=images_payload)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Processed {result['successful_images']}/{result['total_images']} images")
            for item in result['results']:
                if "error" not in item:
                    print(f"  - Image {item['image_index']}: {item['aesthetic_score']:.4f} ({item['image_size']})")
                else:
                    print(f"  - Image {item['image_index']}: ❌ {item['error']}")
            return True
        else:
            print(f"❌ Batch scoring failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_legacy_file_upload():
    """Test the legacy file upload endpoint for backward compatibility"""
    print("\n📁 Testing legacy file upload endpoint...")
    
    images_dir = Path("./images")
    if not images_dir.exists():
        print("❌ No images directory found")
        return False
    
    image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
    if not image_files:
        print("❌ No JPEG images found in images directory")
        return False
    
    test_image = image_files[0]
    print(f"Using test image: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/score-file", files=files)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Aesthetic Score: {result['aesthetic_score']:.4f}")
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Food Aesthetics API Test Suite (Base64 Endpoints)")
    print("=" * 60)
    
    # Make sure API is running
    print("⚠️  Make sure the API server is running (./start_api.sh)")
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Single Image Base64", test_single_image_base64),
        ("Batch Images Base64", test_batch_images_base64),
        ("Legacy File Upload", test_legacy_file_upload)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*25} {test_name} {'='*25}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 Test Results Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly with base64 endpoints.")
        print("\n🚀 Ready for Hugging Face Spaces deployment!")
    else:
        print("⚠️  Some tests failed. Check the API server and try again.")

if __name__ == "__main__":
    main()
