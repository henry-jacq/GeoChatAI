# 🌍 GeoChatAI

GeoChatAI is a simple web application that allows users to upload **aerial or satellite imagery** and automatically generates **high-quality natural language captions** describing the contents of the image.

This project leverages **Meta’s LLaMA Vision-Language model** fine-tuned on the **ChatEarthNet dataset** derived from Sentinel-2 satellite imagery.

---

## 🚀 Overview

* **Upload**: Provide an aerial or satellite image.
* **Generate**: The fine-tuned model generates a natural language caption.
* **Use Case**: Remote sensing, environmental monitoring, land-cover analysis, and geospatial research.

---

## 🔧 Model Details

* **Dataset**: [ChatEarthNet](https://zenodo.org/records/11003436)
* **Base Model**: [Meta-LLaMA 3.2 11B Vision Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision)
* **Fine-Tuned Model**: [henry-07/geochat\_finetuned](https://huggingface.co/henry-07/geochat_finetuned/tree/main)
* **Training Method**: Supervised fine-tuning with **LoRA (Low-Rank Adaptation)**

---

## 📚 Dataset – ChatEarthNet

**ChatEarthNet** is a global-scale image-text dataset created from **Sentinel-2 imagery** and enriched with semantic segmentation labels from ESA’s **WorldCover project**. Captions were generated using **ChatGPT-3.5 and GPT-4V**, followed by manual verification.

* **163,488** image-text pairs (ChatGPT-3.5)
* **10,000** image-text pairs (ChatGPT-4V)
* Global coverage with detailed, high-quality, and diverse descriptions

📖 Reference Paper: [ChatEarthNet (Yuan et al., 2024)](https://arxiv.org/abs/2402.11325)

---

## 🖥️ Installation & Usage

### 1. Clone Repository

```bash
git clone https://github.com/henry-jacq/GeoChatAI.git
cd GeoChatAI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
python run.py
```

### 4. Open in Browser

Navigate to `http://localhost:5000` (or the port specified in your config).

