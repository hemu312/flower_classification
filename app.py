import json
import torch
from huggingface_hub import hf_hub_download
import torchvision.transforms as transforms
from PIL import Image
import io
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# import uvicorn

# Download your model from Hugging Face Hub
model_id = "hemu312/flower-classification_convnext"
model_path = hf_hub_download(repo_id=model_id, filename="flower-classification_convnext.pt")
# Load model
device = torch.device('cpu')
model = torch.jit.load(model_path, map_location=device)

# Load class names from file
with open('class_names.json', 'r') as f:
    class_names = json.load(f)

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route for POST method /predict
@app.post("/predict")
async def predict(imgFile: UploadFile = File(...)):
    data = await imgFile.read()
    img = Image.open(io.BytesIO(data))
    # get model 
    try:
        input_tensor = transform(img).unsqueeze(0)
        
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.softmax(output, dim=1)
        
        top_probs, top_indices = torch.topk(probabilities, k=5)
        
        results = {}
        for prob, idx in zip(top_probs[0], top_indices[0]):
            class_name = class_names[idx.item()]
            results[class_name] = float(prob.item())
        
        return results
        
    except Exception as e:
        return {"Error": str(e)}
    
# Mount frontend directory
frontend = Path("frontend")
app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=7860)
