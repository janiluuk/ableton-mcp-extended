"""
Mock RVC Server for E2E Testing

Simulates the RVC API for voice conversion.
"""
from flask import Flask, request, jsonify, send_file
import os
import io

app = Flask(__name__)

# Mock models database
MODELS = {
    "test_model": {
        "name": "test_model",
        "version": "1.0",
        "description": "Test voice model"
    },
    "anime_character": {
        "name": "anime_character",
        "version": "1.0",
        "description": "Anime character voice"
    },
    "opera_singer": {
        "name": "opera_singer",
        "version": "1.0",
        "description": "Opera singer voice"
    }
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/models', methods=['GET'])
def list_models():
    """List available voice models"""
    models = [
        {"name": name, "info": info["description"]}
        for name, info in MODELS.items()
    ]
    return jsonify({"models": models}), 200

@app.route('/api/models/<model_name>', methods=['GET'])
def get_model_info(model_name):
    """Get information about a specific model"""
    if model_name not in MODELS:
        return jsonify({"error": "Model not found"}), 404
    
    return jsonify(MODELS[model_name]), 200

@app.route('/api/convert', methods=['POST'])
def convert_voice():
    """Convert voice using RVC model"""
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio_file']
    model_name = request.form.get('model_name')
    pitch_shift = int(request.form.get('pitch_shift', 0))
    
    if not model_name or model_name not in MODELS:
        return jsonify({"error": "Invalid model name"}), 400
    
    # Create mock converted audio
    mock_audio = b'MOCK_RVC_CONVERTED_AUDIO_' + os.urandom(200)
    
    return send_file(
        io.BytesIO(mock_audio),
        mimetype='audio/wav',
        as_attachment=True,
        download_name='converted.wav'
    )

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train a new RVC model"""
    if 'training_files' not in request.files:
        return jsonify({"error": "No training files provided"}), 400
    
    model_name = request.form.get('model_name')
    if not model_name:
        return jsonify({"error": "Model name required"}), 400
    
    # Simulate training job
    job_id = f"train_{model_name}"
    
    return jsonify({
        "job_id": job_id,
        "status": "training",
        "message": f"Training model {model_name}"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=False)
