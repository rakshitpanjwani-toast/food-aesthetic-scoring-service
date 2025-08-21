# 🍽️ Food Aesthetics API

A FastAPI-based REST API that provides aesthetic scoring for food images using a pre-trained deep learning model. **Perfect for Hugging Face Spaces deployment and service-to-service integration!**

## 🚀 Quick Start

### 1. Start the API Server
```bash
./start_api.sh
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 2. Test the API
```bash
# Test base64 endpoints (recommended for production)
python test_base64_api.py

# Test legacy file upload endpoints
python test_api.py

# Run client example
python client_example.py
```

## 📚 API Endpoints

### 🔍 Health Check
**GET** `/health`

Check if the API and model are running properly.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Food Aesthetics model is ready"
}
```

### 🏠 Root Information
**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "message": "Food Aesthetics API",
  "version": "1.0.0",
  "endpoints": {
    "/score": "POST - Send image data and get aesthetic score",
    "/score-batch": "POST - Send multiple images for batch scoring",
    "/health": "GET - Check API health and model status"
  }
}
```

### 📸 Single Image Scoring (Base64) - **RECOMMENDED**
**POST** `/score`

Send image data as base64 string and get aesthetic score. **Perfect for Hugging Face Spaces and service integration.**

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_string",
  "image_format": "jpeg"
}
```

**Response:**
```json
{
  "aesthetic_score": 0.8542,
  "image_format": "jpeg",
  "image_size": "1920x1080",
  "message": "Image scored successfully"
}
```

**Python Example:**
```python
import requests
import base64

# Encode image to base64
with open('food_image.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Send to API
payload = {
    "image_data": image_base64,
    "image_format": "jpeg"
}

response = requests.post('http://localhost:8000/score', json=payload)
result = response.json()
print(f"Aesthetic Score: {result['aesthetic_score']:.4f}")
```

**cURL Example:**
```bash
# First encode image to base64
IMAGE_BASE64=$(base64 -i food_image.jpg)

# Send to API
curl -X POST "http://localhost:8000/score" \
     -H "Content-Type: application/json" \
     -d "{\"image_data\": \"$IMAGE_BASE64\", \"image_format\": \"jpeg\"}"
```

### 🖼️ Batch Image Scoring (Base64) - **RECOMMENDED**
**POST** `/score-batch`

Send multiple images as base64 strings for batch processing.

**Request Body:**
```json
[
  {
    "image_data": "base64_encoded_image_1",
    "image_format": "jpeg"
  },
  {
    "image_data": "base64_encoded_image_2",
    "image_format": "png"
  }
]
```

**Response:**
```json
{
  "results": [
    {
      "image_index": 0,
      "aesthetic_score": 0.8542,
      "image_format": "jpeg",
      "image_size": "1920x1080"
    },
    {
      "image_index": 1,
      "aesthetic_score": 0.7234,
      "image_format": "png",
      "image_size": "1280x720"
    }
  ],
  "total_images": 2,
  "successful_images": 2,
  "message": "Batch scoring completed"
}
```

### 📁 Legacy File Upload Endpoints

For backward compatibility, these endpoints are still available:

- **POST** `/score-file` - Upload single image file
- **POST** `/score-batch-file` - Upload multiple image files

## 🌐 Hugging Face Spaces Deployment

This API is designed to work perfectly with Hugging Face Spaces! Here's how to deploy it:

### 1. Create a Hugging Face Space
- Go to [huggingface.co/spaces](https://huggingface.co/spaces)
- Create a new Space
- Choose "Gradio" or "Streamlit" as the SDK

### 2. Add the API Files
Upload these files to your Space:
- `api.py` - Main API application
- `food_aesthetics/` - Model package
- `requirements.txt` - Dependencies

### 3. Configure the Space
Create a `README.md` in your Space:

```markdown
---
title: Food Aesthetics API
emoji: 🍽️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 3.50.2
app_file: app.py
pinned: false
---

# Food Aesthetics API

Aesthetic scoring for food images using deep learning.

## API Endpoints

- `POST /score` - Score single image (base64)
- `POST /score-batch` - Score multiple images (base64)
- `GET /health` - Health check
- `GET /docs` - Interactive documentation

## Usage

```python
import requests
import base64

# Encode image
with open('image.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Score image
response = requests.post(
    "https://your-space-name.hf.space/score",
    json={"image_data": image_base64, "image_format": "jpeg"}
)

score = response.json()['aesthetic_score']
print(f"Aesthetic Score: {score:.4f}")
```
```

### 4. Create the Space App
Create `app.py` for your Space:

```python
import gradio as gr
import requests
import base64
from PIL import Image
import io

# Your Space's API URL
API_URL = "https://your-space-name.hf.space"

def score_image(image):
    """Score an image using the API"""
    try:
        # Convert PIL image to base64
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Send to API
        payload = {
            "image_data": image_base64,
            "image_format": "jpeg"
        }
        
        response = requests.post(f"{API_URL}/score", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result['aesthetic_score']
            
            # Interpret score
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
            
            return f"Aesthetic Score: {score:.4f}\nQuality Level: {quality}"
        else:
            return f"Error: {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=score_image,
    inputs=gr.Image(type="pil"),
    outputs=gr.Textbox(label="Result"),
    title="Food Aesthetics Scorer",
    description="Upload a food image to get its aesthetic score"
)

iface.launch()
```

## 🔧 Service Integration

### Using the Client Class
```python
from client_example import FoodAestheticsClient

# Initialize client
client = FoodAestheticsClient("https://your-api-url.com")

# Score single image
success, result = client.score_image("food_image.jpg")
if success:
    print(f"Score: {result['aesthetic_score']:.4f}")

# Score multiple images
success, result = client.score_images_batch(["img1.jpg", "img2.jpg"])
if success:
    for item in result['results']:
        print(f"Image {item['image_index']}: {item['aesthetic_score']:.4f}")
```

### Direct HTTP Calls
```python
import requests
import base64

def score_image_direct(image_path, api_url):
    """Direct API call without client class"""
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "image_data": image_base64,
        "image_format": "jpeg"
    }
    
    response = requests.post(f"{api_url}/score", json=payload)
    return response.json()
```

## 🎯 Aesthetic Score Interpretation

The aesthetic score ranges from **0.0 to 1.0**:

- **0.0 - 0.2**: Low aesthetic quality
- **0.2 - 0.4**: Below average aesthetic quality
- **0.4 - 0.6**: Average aesthetic quality
- **0.6 - 0.8**: Above average aesthetic quality
- **0.8 - 1.0**: High aesthetic quality

## 🔧 Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- Other common image formats supported by PIL/Pillow

## ⚠️ Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid image data, no images provided)
- **500**: Internal Server Error (model processing error)
- **503**: Service Unavailable (model not loaded)

## 🛠️ Development

### Project Structure
```
food-aesthetics/
├── api.py                 # Main FastAPI application
├── start_api.sh          # API startup script
├── test_base64_api.py    # Test base64 endpoints
├── test_api.py           # Test legacy endpoints
├── client_example.py     # Client integration example
├── food_aesthetics/      # Model package
│   ├── model.py          # Core model implementation
│   └── trained_weights.h5
├── images/               # Sample images
└── requirements.txt      # Python dependencies
```

### Running in Development
```bash
# Terminal 1: Start the API
./start_api.sh

# Terminal 2: Test base64 endpoints
python test_base64_api.py

# Terminal 3: Test client integration
python client_example.py
```

## 🌐 Production Deployment

### Hugging Face Spaces (Recommended)
- Automatic scaling
- Free hosting
- Easy integration
- Built-in monitoring

### Self-Hosted
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# For production deployment
export HOST="0.0.0.0"
export PORT="8000"
export WORKERS="4"
```

## 📊 Performance

- **Model Loading**: ~2-3 seconds on first startup
- **Single Image Processing**: ~0.5-1 second per image
- **Batch Processing**: ~0.3-0.8 seconds per image (optimized)
- **Memory Usage**: ~500MB-1GB (depends on image sizes)
- **Base64 Processing**: Minimal overhead compared to file uploads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the API health endpoint: `GET /health`
2. Review the server logs for error messages
3. Ensure the model weights file exists
4. Verify Python environment compatibility
5. For Hugging Face Spaces: Check Space logs and configuration

---

**Ready for Hugging Face Spaces deployment! 🚀✨**

**Happy Food Aesthetics Scoring! 🍕📸✨**
