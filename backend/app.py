import torch
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
app.logger.info("CPU-based API server starting...")

base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "rifukawa/ucrg-tinyllama-finetuned"
app.logger.info(f"Loading base model: {base_model_name}")
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float32, # Use standard precision for CPU
    device_map="auto",
)
app.logger.info(f"Loading LoRA adapter: {adapter_path}")
model = PeftModel.from_pretrained(base_model, adapter_path)
app.logger.info("Model loaded successfully!")

@app.route('/')
def home():
    return "CPU API server is up and running. TinyLlama model is loaded."

@app.route('/generate-report', methods=['POST'])
def generate_report():
    app.logger.info("Received a request for /generate-report")
    data = request.get_json()
    if not data or 'incident_type' not in data:
        app.logger.error("Invalid or missing JSON data")
        return jsonify({"error": "Invalid request: No JSON data or missing 'incident_type' field"}), 400
    prompt = f"""<|system|>
Generate a compliance report summary from the following structured data.</s>
<|user|>
{data}</s>
<|assistant|>
"""
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
    try:
        outputs = model.generate(**inputs, max_new_tokens=150)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_text = generated_text.split("<|assistant|>")[1].strip()
        app.logger.info(f"Successfully generated report: {response_text}")
        return jsonify({"report_text": response_text})
    except Exception as e:
        app.logger.error(f"Model generation failed: {e}")
        return jsonify({"error": "Failed to generate report"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)