import os
import torch
import torch.nn as nn
import librosa
import numpy as np
from flask import Flask, request, jsonify
import uuid, boto3, json

bedrock = boto3.client(
    'bedrock-runtime',
    region_name = 'us-east-1'
)

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

# LLM Analysis
def generate_ai_report(prediction, score):

    prompt = f"""
You are a livestock veterinarian assistant.

An AI acoustic model analyzed a chicken vocalization.

Prediction: {prediction}
Risk Score: {score}

Risk interpretation:
0.0–0.25 → Healthy
0.25–0.5 → Mild symptoms
0.5–0.75 → Possible respiratory illness
0.75–1.0 → Severe respiratory distress

Explain the condition and give simple advice for farmers.
Keep the answer under 100 words.
"""

    response = bedrock.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ]
    )

    return response["output"]["message"]["content"][0]["text"]

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

    ai_report = generate_ai_report(label, prob)

    return jsonify({
        "prediction": label,
        "risk_score": round(prob, 6),
        "ai_report": ai_report
    })


# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)