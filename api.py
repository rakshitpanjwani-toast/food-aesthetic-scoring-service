from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
from food_aesthetics.model import FoodAesthetics
import uvicorn
import base64
import io
from PIL import Image
import numpy as np

app = FastAPI(
    title="Food Aesthetics API",
    description="API for scoring food images based on aesthetic quality",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model globally
try:
    fa_model = FoodAesthetics()
    print("✅ Food Aesthetics model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    fa_model = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Food Aesthetics API",
        "version": "1.0.0",
        "endpoints": {
            "/score": "POST - Send image data and get aesthetic score",
            "/score-batch": "POST - Send multiple images for batch scoring",
            "/health": "GET - Check API health and model status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if fa_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "healthy",
        "model_loaded": True,
        "message": "Food Aesthetics model is ready"
    }

@app.post("/score")
async def score_image(
    image_data: str = Body(..., description="Base64 encoded image data"),
    image_format: str = Body("jpeg", description="Image format (jpeg, png, etc.)")
):
    """
    Send image data (base64 encoded) and get aesthetic score
    
    Args:
        image_data: Base64 encoded image string
        image_format: Image format (jpeg, png, etc.)
    
    Returns:
        JSON with aesthetic score
    """
    if fa_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Decode base64 image data
        image_bytes = base64.b64decode(image_data)
        
        # Create PIL Image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to temporary file for the model
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_format}") as temp_file:
            image.save(temp_file, format=image_format.upper())
            temp_file_path = temp_file.name
        
        # Get the aesthetic score
        score = fa_model.aesthetic_score(temp_file_path)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return JSONResponse({
            "aesthetic_score": float(score),
            "image_format": image_format,
            "image_size": f"{image.width}x{image.height}",
            "message": "Image scored successfully"
        })
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/score-batch")
async def score_batch_images(
    images: list = Body(..., description="List of base64 encoded images")
):
    """
    Send multiple images (base64 encoded) and get aesthetic scores
    
    Args:
        images: List of objects with 'image_data' and 'image_format' fields
    
    Returns:
        JSON with list of results for each image
    """
    if fa_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(images) == 0:
        raise HTTPException(status_code=400, detail="No images provided")
    
    if len(images) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed per batch")
    
    results = []
    temp_files = []
    
    try:
        for i, img_obj in enumerate(images):
            if not isinstance(img_obj, dict) or 'image_data' not in img_obj:
                continue  # Skip invalid image objects
            
            image_data = img_obj.get('image_data', '')
            image_format = img_obj.get('image_format', 'jpeg')
            
            try:
                # Decode base64 image data
                image_bytes = base64.b64decode(image_data)
                
                # Create PIL Image from bytes
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_format}") as temp_file:
                    image.save(temp_file, format=image_format.upper())
                    temp_file_path = temp_file.name
                    temp_files.append(temp_file_path)
                
                # Get aesthetic score
                score = fa_model.aesthetic_score(temp_file_path)
                
                results.append({
                    "image_index": i,
                    "aesthetic_score": float(score),
                    "image_format": image_format,
                    "image_size": f"{image.width}x{image.height}"
                })
                
            except Exception as e:
                results.append({
                    "image_index": i,
                    "error": f"Failed to process image: {str(e)}"
                })
        
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return JSONResponse({
            "results": results,
            "total_images": len(images),
            "successful_images": len([r for r in results if "error" not in r]),
            "message": "Batch scoring completed"
        })
        
    except Exception as e:
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error processing batch: {str(e)}")

# Keep the file upload endpoints for backward compatibility
@app.post("/score-file")
async def score_image_file(file: UploadFile = File(...)):
    """
    Upload an image file and get its aesthetic score (legacy endpoint)
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with image filename and aesthetic score
    """
    if fa_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Create a temporary file to save the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Get the aesthetic score
        score = fa_model.aesthetic_score(temp_file_path)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return JSONResponse({
            "filename": file.filename,
            "aesthetic_score": float(score),
            "message": "Image scored successfully"
        })
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
