#!/usr/bin/env python3
"""
Client example for calling the Food Aesthetics API
Shows how to integrate with the API from your service
"""

import requests
import base64
import json
from pathlib import Path

class FoodAestheticsClient:
    """Client for the Food Aesthetics API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if the API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def score_image(self, image_path, image_format="jpeg"):
        """
        Score a single image
        
        Args:
            image_path: Path to the image file
            image_format: Image format (jpeg, png, etc.)
        
        Returns:
            Tuple of (success, result)
        """
        try:
            # Encode image to base64
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Prepare payload
            payload = {
                "image_data": image_base64,
                "image_format": image_format
            }
            
            # Make API call
            response = requests.post(f"{self.base_url}/score", json=payload)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            return False, {"error": str(e)}
    
    def score_images_batch(self, image_paths, image_format="jpeg"):
        """
        Score multiple images in batch
        
        Args:
            image_paths: List of image file paths
            image_format: Image format (jpeg, png, etc.)
        
        Returns:
            Tuple of (success, result)
        """
        try:
            # Prepare batch payload
            images_payload = []
            for img_path in image_paths:
                with open(img_path, 'rb') as f:
                    image_bytes = f.read()
                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                images_payload.append({
                    "image_data": image_base64,
                    "image_format": image_format
                })
            
            # Make API call
            response = requests.post(f"{self.base_url}/score-batch", json=images_payload)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            return False, {"error": str(e)}

def main():
    """Example usage of the client"""
    
    # Initialize client
    client = FoodAestheticsClient()
    
    print("🍽️ Food Aesthetics API Client Example")
    print("=" * 50)
    
    # Check API health
    print("1. Checking API health...")
    healthy, health_result = client.health_check()
    if healthy:
        print("✅ API is healthy!")
        print(f"   Status: {health_result['status']}")
        print(f"   Message: {health_result['message']}")
    else:
        print("❌ API health check failed")
        print(f"   Error: {health_result}")
        return
    
    print()
    
    # Score a single image
    print("2. Scoring a single image...")
    images_dir = Path("./images")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
        if image_files:
            test_image = image_files[0]
            print(f"   Using image: {test_image.name}")
            
            success, result = client.score_image(test_image)
            if success:
                print("✅ Image scored successfully!")
                print(f"   Aesthetic Score: {result['aesthetic_score']:.4f}")
                print(f"   Image Size: {result['image_size']}")
                print(f"   Format: {result['image_format']}")
                
                # Interpret the score
                score = result['aesthetic_score']
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
                print("❌ Failed to score image")
                print(f"   Error: {result}")
        else:
            print("❌ No test images found")
    else:
        print("❌ Images directory not found")
    
    print()
    
    # Score multiple images
    print("3. Scoring multiple images...")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
        if len(image_files) >= 2:
            test_images = image_files[:2]  # Use 2 images for batch testing
            print(f"   Using {len(test_images)} images for batch scoring")
            
            success, result = client.score_images_batch(test_images)
            if success:
                print("✅ Batch scoring completed!")
                print(f"   Processed: {result['successful_images']}/{result['total_images']} images")
                
                for item in result['results']:
                    if "error" not in item:
                        print(f"   - Image {item['image_index']}: {item['aesthetic_score']:.4f} ({item['image_size']})")
                    else:
                        print(f"   - Image {item['image_index']}: ❌ {item['error']}")
            else:
                print("❌ Batch scoring failed")
                print(f"   Error: {result}")
        else:
            print("❌ Not enough images for batch testing")
    else:
        print("❌ Images directory not found")
    
    print()
    print("🎉 Client example completed!")
    print()
    print("Integration tips:")
    print("- Use the client class in your service")
    print("- Handle errors gracefully")
    print("- Consider implementing retry logic")
    print("- Cache results if needed")
    print("- Monitor API response times")

if __name__ == "__main__":
    main()
