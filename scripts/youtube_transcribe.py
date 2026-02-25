#!/usr/bin/env python3
"""
Transcribe YouTube videos using the trained Whisper model
"""
import os
import sys
import glob
import torch
import librosa
from yt_dlp import YoutubeDL
from transformers import pipeline
from config import OUTPUT_DIR, LANGUAGE, TASK, MODEL_NAME

def transcribe_youtube(youtube_url):
    """Download and transcribe YouTube video"""
    final_model_dir = os.path.join(OUTPUT_DIR, "final_model")
    
    model_path = final_model_dir
    if not os.path.exists(final_model_dir):
        print(f"WARNING: Custom model not found at {final_model_dir}")
        print(f"Using base model: {MODEL_NAME}")
        model_path = MODEL_NAME
    
    print("="*60)
    print("YOUTUBE VIDEO TRANSCRIPTION")
    print("="*60)
    print()
    print(f"Video URL: {youtube_url}")
    print()
    
    # Download audio
    print("Downloading audio from YouTube...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': 'video_audio',
        'quiet': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print("✅ Audio downloaded")
    except Exception as e:
        print(f"ERROR downloading video: {e}")
        return
    
    # Find audio file
    audio_files = glob.glob('video_audio.*')
    if not audio_files:
        print("ERROR: Audio file not found")
        return
    
    audio_file = audio_files[0]
    print(f"Audio file: {audio_file}")
    print()
    
    # Load model
    print("Loading model...")
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_path,
        device=0 if torch.cuda.is_available() else -1
    )
    print("✅ Model loaded")
    print()
    
    # Transcribe
    print("Transcribing...")
    audio, sr = librosa.load(audio_file, sr=16000)
    result = pipe(audio, generate_kwargs={"language": LANGUAGE, "task": TASK})
    
    transcription = result["text"]
    
    print()
    print("="*60)
    print("TRANSCRIPTION")
    print("="*60)
    print(transcription)
    print("="*60)
    print()
    
    # Save to file
    output_file = "transcription.txt"
    with open(output_file, "w") as f:
        f.write(transcription)
    print(f"✅ Saved to: {output_file}")
    
    # Cleanup
    try:
        os.remove(audio_file)
        print("✅ Cleaned up temporary files")
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcribe.py <youtube_url>")
        print("Example: python youtube_transcribe.py \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    transcribe_youtube(youtube_url)