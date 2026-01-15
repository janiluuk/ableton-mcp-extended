"""
Mock UVR5 Server for E2E Testing

Simulates the UVR5 API for vocal/instrumental separation.
"""
from flask import Flask, request, jsonify, send_file
import os
import time
import uuid
import io

app = Flask(__name__)

# In-memory storage for jobs
jobs = {}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/models', methods=['GET'])
def list_models():
    """List available separation models"""
    models = [
        "UVR-MDX-NET-Inst_HQ_3",
        "UVR-MDX-NET-Voc_FT",
        "UVR-MDX-NET-1",
        "UVR-MDX-NET-2"
    ]
    return jsonify({"models": models}), 200

@app.route('/api/separate', methods=['POST'])
def separate_audio():
    """Separate audio into stems"""
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio_file']
    model_name = request.form.get('model_name', 'UVR-MDX-NET-Inst_HQ_3')
    output_format = request.form.get('output_format', 'wav')
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Create mock audio data
    mock_vocals = b'MOCK_VOCALS_DATA_' + os.urandom(100)
    mock_instrumental = b'MOCK_INSTRUMENTAL_DATA_' + os.urandom(100)
    
    # Store job results
    jobs[job_id] = {
        "status": "completed",
        "stems": {
            "vocals": mock_vocals,
            "instrumental": mock_instrumental
        },
        "model": model_name,
        "format": output_format
    }
    
    return jsonify({
        "job_id": job_id,
        "status": "completed",
        "stems": {
            "vocals": "available",
            "instrumental": "available"
        }
    }), 200

@app.route('/api/result/<job_id>', methods=['GET'])
def get_result(job_id):
    """Get separation result"""
    if job_id not in jobs:
        return jsonify({"status": "error", "message": "Job not found"}), 404
    
    job = jobs[job_id]
    return jsonify({
        "status": job["status"],
        "stems": {
            "vocals": "available",
            "instrumental": "available"
        }
    }), 200

@app.route('/api/download/<job_id>/<stem_type>', methods=['GET'])
def download_stem(job_id, stem_type):
    """Download a separated stem"""
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = jobs[job_id]
    if stem_type not in job["stems"]:
        return jsonify({"error": "Stem not found"}), 404
    
    stem_data = job["stems"][stem_type]
    return send_file(
        io.BytesIO(stem_data),
        mimetype='audio/wav',
        as_attachment=True,
        download_name=f'{stem_type}.{job["format"]}'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
