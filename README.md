# 🍽️ Food Aesthetic Scoring Service

A machine learning service that automatically scores food images based on their aesthetic quality using a pre-trained MobileNet model.

## 🌟 Features

- **AI-Powered Scoring**: Uses a fine-tuned MobileNet model to evaluate food aesthetics
- **RESTful API**: FastAPI-based service with multiple endpoints
- **Batch Processing**: Score multiple images at once
- **Multiple Input Formats**: Support for file uploads and base64 encoded images
- **Real-time Scoring**: Get aesthetic scores in milliseconds
- **CORS Enabled**: Ready for web applications

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- TensorFlow 2.9
- 4GB+ RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd food-aesthetic-scoring-service
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API server**
   ```bash
   ./start_api.sh
   ```
   
   Or manually:
   ```bash
   python api.py
   ```

4. **Test the service**
   ```bash
   python demo.py
   ```

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Check if the model is loaded and ready.

### Score Single Image
```http
POST /score
```
Score a single food image. Accepts both file uploads and base64 encoded data.

**File Upload:**
```bash
curl -X POST "http://localhost:8000/score" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_food_image.jpg"
```

**Base64 Data:**
```bash
curl -X POST "http://localhost:8000/score" \
     -H "Content-Type: application/json" \
     -d '{"image_data": "base64_encoded_string", "image_format": "jpeg"}'
```

### Batch Scoring
```http
POST /score-batch
```
Score multiple images at once for efficient processing.

### API Information
```http
GET /
```
Get API version and available endpoints.

## 🧠 Model Details

The service uses a **MobileNet-based neural network** that has been specifically trained on food images to predict aesthetic quality. The model:

- Takes 224x224 RGB images as input
- Outputs scores between 0 and 1 (higher = more aesthetic)
- Uses temperature scaling for calibrated predictions
- Processes images with aspect ratio preservation

### Score Interpretation

| Score Range | Quality Level |
|-------------|---------------|
| 0.0 - 0.2  | Low          |
| 0.2 - 0.4  | Below Average|
| 0.4 - 0.6  | Average      |
| 0.6 - 0.8  | Above Average|
| 0.8 - 1.0  | High         |

## 💻 Usage Examples

### Python Client

```python
import requests
from PIL import Image
import base64
import io

# Initialize client
base_url = "http://localhost:8000"

# Score an image file
with open("food_image.jpg", "rb") as f:
    files = {"file": ("image.jpg", f, "image/jpeg")}
    response = requests.post(f"{base_url}/score", files=files)
    
if response.status_code == 200:
    score = response.json()["aesthetic_score"]
    print(f"Aesthetic Score: {score:.4f}")
```

### Base64 Encoding

```python
# Convert image to base64
with open("food_image.jpg", "rb") as f:
    image_bytes = f.read()
    base64_data = base64.b64encode(image_bytes).decode()

# Send to API
data = {
    "image_data": base64_data,
    "image_format": "jpeg"
}
response = requests.post(f"{base_url}/score", json=data)
```

## 🛠️ Development

### Project Structure

```
food-aesthetic-scoring-service/
├── api.py                 # FastAPI server
├── food_aesthetics/       # Core ML model
│   ├── model.py          # FoodAesthetics class
│   └── trained_weights.h5 # Pre-trained model weights
├── images/               # Sample images for testing
├── requirements.txt      # Python dependencies
├── demo.py              # Usage examples
└── start_api.sh         # Server startup script
```

### Running Tests

```bash
# Test the API endpoints
python test_api.py

# Test base64 functionality
python test_base64_api.py
```

### Model Training

The model is pre-trained and ready to use. If you need to retrain:

1. Prepare your food image dataset
2. Modify the `FoodAesthetics` class in `model.py`
3. Train using TensorFlow/Keras
4. Save weights to `trained_weights.h5`

## 🔧 Configuration

### Environment Variables

- `PORT`: API server port (default: 8000)
- `HOST`: API server host (default: 0.0.0.0)

### Model Parameters

- **Input Size**: 224x224 pixels
- **Batch Size**: 1 (configurable in model.py)
- **Temperature**: 1.537 (for score calibration)

## 📊 Performance

- **Inference Time**: ~50-100ms per image
- **Memory Usage**: ~2-3GB RAM
- **Concurrent Requests**: Supports multiple simultaneous users
- **Model Loading**: ~5-10 seconds on first startup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with TensorFlow and FastAPI
- Model architecture based on MobileNet
- Food aesthetics dataset for training

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the [API documentation](API_README.md)
- Review the demo scripts for usage examples

---

**Happy Food Aesthetic Scoring! 🍕🍜🍰**
