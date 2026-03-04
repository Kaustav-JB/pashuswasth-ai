import os
import torch
import torch.nn as nn
import librosa
import numpy as np
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# =========================
# MODEL DEFINITION
# =========================

class AudioCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.AdaptiveAvgPool2d((8,8))
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32*8*8, 64),
            nn.ReLU(),
            nn.Linear(64,1)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x


# =========================
# LOAD MODEL
# =========================

model = AudioCNN()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

print("Model loaded successfully")


# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(file_path):

    target_length = 5
    sr_target = 22050
    samples = sr_target * target_length

    y, sr = librosa.load(file_path, sr=sr_target)

    if len(y) < samples:
        y = np.pad(y, (0, samples - len(y)))
    else:
        y = y[:samples]

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr_target,
        n_mels=64
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-6)

    mel_db = np.expand_dims(mel_db, axis=0)
    mel_db = np.expand_dims(mel_db, axis=0)

    return torch.tensor(mel_db).float()


# =========================
# API ENDPOINT
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    file_path = f"{uuid.uuid4()}.wav"
    file.save(file_path)

    features = extract_features(file_path)

    with torch.no_grad():
        logits = model(features)
        prob = torch.sigmoid(logits).item()

    os.remove(file_path)

    label = "Unhealthy" if prob > 0.5 else "Healthy"

    return jsonify({
        "prediction": label,
        "risk_score": round(prob, 6)
    })


# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)