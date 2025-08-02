from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
import base64, os

# Step 1: Load, resize, and encode the image
image_path = "test.png"  # Replace with your image path

instruction = (
    "You are analyzing a satellite image. Provide a single cohesive paragraph that summarizes the visible features "
    "observed across six regions: Top Left, Top Right, Center, Bottom Left, Bottom Right, and General Observations. "
    "Describe land cover types (such as vegetation, urban areas), any visible water bodies, and notable patterns or structures, "
    "ensuring each region is addressed but integrated smoothly into a unified narrative."
)

title_prompt = (
    "You are analyzing a satellite image. Based on the scene described in the image, generate a short and descriptive title "
    "for the chat summarizing the content. Use 2 to 5 words only. The title should reflect the most notable or dominant features "
    "or regions, such as land types, urban activity, vegetation, or structures."
)

with Image.open(image_path) as img:
    img = img.convert("RGB")
    img.thumbnail((256, 256))  # Resize to reduce token load
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=60)  # Compress for smaller size
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    image_data_url = f"data:image/jpeg;base64,{encoded_image}"

# Step 2: Use the image in your chat completion
client = InferenceClient(
    provider="fireworks-ai",
    api_key=os.getenv('HF_TOKEN'),
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": title_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data_url
                    }
                }
            ]
        }
    ],
    max_tokens=512,
)

# Step 3: Print the response
print(completion.choices[0].message.content)
