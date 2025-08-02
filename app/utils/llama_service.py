from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
import base64, os

# Prompts
SUMMARY_PROMPT = (
    "You are analyzing a satellite image. Provide a single cohesive paragraph that summarizes the visible features "
    "observed across six regions: Top Left, Top Right, Center, Bottom Left, Bottom Right, and General Observations. "
    "Describe land cover types (such as vegetation, urban areas), any visible water bodies, and notable patterns or structures, "
    "ensuring each region is addressed but integrated smoothly into a unified narrative."
)

TITLE_PROMPT = (
    "You are analyzing a satellite image. Based on the scene described in the image, generate a single, clear, and descriptive "
    "title for the chat summarizing the content. Use 2 to 5 words only. Do not include quotation marks or provide multiple options. "
    "The title should reflect the most prominent features or regions, such as land types, urban activity, vegetation, or structures."
)


provider = "fireworks-ai"
model = os.getenv("HF_MODEL")
key = os.getenv("HF_TOKEN")

# Initialize client
client = InferenceClient(
    provider=provider,
    api_key=key,
)

def encode_image_for_chat(path):
    """Opens, resizes, compresses, and encodes the image to base64."""
    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((256, 256))
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=60)
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"


def generate_title(image_path):
    image_data_url = encode_image_for_chat(image_path)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TITLE_PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ],
        max_tokens=512,
    )
    return completion.choices[0].message.content.strip()


def generate_summary(image_path):
    image_data_url = encode_image_for_chat(image_path)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SUMMARY_PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ],
        max_tokens=512,
    )
    return completion.choices[0].message.content.strip()
