import librosa
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from fastapi import UploadFile, File

# Load model & processor
def transcribe_audio(file: str):
    model_name = "openai/whisper-base"
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)

    # Load audio (force 16kHz for Whisper)
    waveform, sr = librosa.load(file, sr=16000)

    # Define chunk size (30s = 30 * 16000 samples)
    chunk_size = 30 * sr  
    chunks = [waveform[i:i+chunk_size] for i in range(0, len(waveform), chunk_size)]

    # Transcribe each chunk
    full_transcript = []
    for i, chunk in enumerate(chunks):
        inputs = processor(chunk, sampling_rate=sr, return_tensors="pt")
        predicted_ids = model.generate(inputs.input_features)
        text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        full_transcript.append(text)

    # Join all parts
    transcript = " ".join(full_transcript)
    return transcript
