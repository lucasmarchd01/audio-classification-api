import torch
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
from transformers import pipeline
import librosa
import numpy as np
import asyncio
import logging
from typing import Dict, Any, Optional
import io

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.feature_extractor = None
        self.pipeline = None
        
    async def load_model(self):
        """Load the model and feature extractor asynchronously"""
        try:
            logger.info(f"Loading model {self.model_name} on {self.device}")
            
            # Run model loading in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            def _load_model():
                # Use AutoFeatureExtractor for AST models
                feature_extractor = AutoFeatureExtractor.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                )
                model = AutoModelForAudioClassification.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                )
                model.to(self.device)
                
                # Create pipeline for easier inference
                pipe = pipeline(
                    "audio-classification",
                    model=model,
                    feature_extractor=feature_extractor,
                    device=0 if self.device == "cuda" else -1
                )
                return feature_extractor, model, pipe
            
            self.feature_extractor, self.model, self.pipeline = await loop.run_in_executor(
                None, _load_model
            )
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    async def predict(self, audio_data: bytes) -> Dict[str, Any]:
        """Perform inference on audio data"""
        if not self.pipeline:
            raise RuntimeError("Model not loaded")
        
        try:
            # Convert bytes to audio array
            # AST models typically expect 16kHz audio
            audio_array, sample_rate = librosa.load(
                io.BytesIO(audio_data), 
                sr=16000,  # AST models work best with 16kHz
                mono=True
            )
            
            # Ensure minimum length (AST models need at least ~1 second)
            min_length = 16000  # 1 second at 16kHz
            if len(audio_array) < min_length:
                # Pad with zeros if too short
                audio_array = np.pad(audio_array, (0, min_length - len(audio_array)))
            
            # Run inference in thread pool
            loop = asyncio.get_event_loop()
            
            def _predict():
                results = self.pipeline(audio_array)
                return results
            
            predictions = await loop.run_in_executor(None, _predict)
            
            # Format results
            formatted_results = {
                "predictions": predictions,
                "model_name": self.model_name,
                "sample_rate": sample_rate,
                "audio_duration": len(audio_array) / sample_rate,
                "model_type": "Audio Spectrogram Transformer (AST)"
            }
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def cleanup(self):
        """Clean up model resources"""
        if self.model:
            del self.model
        if self.feature_extractor:
            del self.feature_extractor
        if self.pipeline:
            del self.pipeline
        torch.cuda.empty_cache() if torch.cuda.is_available() else None