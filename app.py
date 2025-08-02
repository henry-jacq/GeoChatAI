from app.utils.chat_db import get_chat, get_all_chats, update_chat_response
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, current_app
from flask_cors import CORS
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO
import torch
import logging
import os
import sys


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeoChatInference")

MODEL_NAME = os.getenv("GEOCHAT_MODEL", "henry-07/geochat_finetuned")
USE_GPU = torch.cuda.is_available()
DEVICE = 0 if USE_GPU else -1

logger.info(
    f"Loading model '{MODEL_NAME}' on {'GPU' if USE_GPU else 'CPU'}...")


try:
    pipe = pipeline(
        "image-text-to-text",
        model=MODEL_NAME,
        device=DEVICE
    )
    logger.info("Model pipeline loaded successfully.")
except Exception as e:
    logger.error("Failed to load model pipeline: %s", e)
    pipe = None


app = Flask(__name__)
CORS(app)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_url = data.get('image_url')
    prompt = data.get('prompt', '')

    if not image_url:
        return jsonify({'error': 'No image URL provided.'}), 400

    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert('RGB')
        messages = [
            {"role": "user", "content": prompt},
            {"role": "user", "content": image}
        ]
        result = pipe(messages)
        return jsonify({'generated_text': result[0]['generated_text']})
    except Exception as e:
        logger.exception("Error during prediction:")
        return jsonify({'error': str(e)}), 500



@app.route('/')
def root():
    return redirect(url_for('home'))


@app.route('/c/new')
def home():
    chats = get_all_chats()
    return render_template('home.html', chats=chats)


@app.route('/c/<cid>')
def chatBox(cid):
    chats = get_all_chats()
    chat = get_chat(cid)
    if chat:
        return render_template(
            'chat.html',
            cid=cid,
            title=chat[1],
            image=chat[2],
            message=chat[3],
            chats=chats,
            is_streamed=chat[4]
        )
    return redirect(url_for('home'))


@app.route('/mark_streamed/<chat_id>')
def mark_streamed(chat_id):
    chat = get_chat(chat_id)
    if chat:
        update_chat_response(chat_id, chat[3], is_streamed=True)
        return 'OK'
    return 'Not found', 404


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    return send_from_directory(upload_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
