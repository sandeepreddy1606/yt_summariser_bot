#!/usr/bin/env python3
"""
Configuration settings for the training pipeline
"""
import os
from pathlib import Path
import torch

# Get project root (parent of this script's directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# ============================================
# PATHS CONFIGURATION
# ============================================

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
TRAIN_PATH = os.path.join(DATA_ROOT, 'train-clean-100')
TEST_PATH = os.path.join(DATA_ROOT, 'test-clean')
VAL_PATH = os.path.join(DATA_ROOT, 'dev-clean')

# Output directories
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "model_output")
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")

# Create directories if they don't exist
for directory in [OUTPUT_DIR, CACHE_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================
# MODEL CONFIGURATION
# ============================================

MODEL_NAME = "openai/whisper-small"  # tiny, base, small, medium, large
LANGUAGE = "en"
TASK = "transcribe"

# ============================================
# TRAINING HYPERPARAMETERS
# ============================================

BATCH_SIZE = 16                    # Reduce if OOM error
GRADIENT_ACCUMULATION_STEPS = 2   # Increase if reducing batch size
LEARNING_RATE = 1e-5
NUM_EPOCHS = 3
WARMUP_STEPS = 500
SAVE_STEPS = 500
EVAL_STEPS = 500
LOGGING_STEPS = 100
MAX_SAMPLES = None                # Set to 100 for quick test

# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    print("="*60)
    print("CONFIGURATION")
    print("="*60)
    print(f"\nPATHS:")
    print(f"  Data root: {DATA_ROOT}")
    print(f"  Train: {TRAIN_PATH}")
    print(f"  Test: {TEST_PATH}")
    print(f"  Val: {VAL_PATH}")
    print(f"\nOUTPUT:")
    print(f"  Model: {OUTPUT_DIR}")
    print(f"  Logs: {LOG_DIR}")
    print(f"\nMODEL:")
    print(f"  Name: {MODEL_NAME}")
    print(f"  Language: {LANGUAGE}")
    print(f"\nTRAINING:")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Effective batch: {BATCH_SIZE * GRADIENT_ACCUMULATION_STEPS}")
    print(f"  Epochs: {NUM_EPOCHS}")
    print(f"  Device: {DEVICE}")
    print("="*60)