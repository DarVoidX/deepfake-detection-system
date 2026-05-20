# 🛡️ NeuralTrace — Deep Fake Detection System

A production-grade web application for detecting facial manipulation and deepfakes in **videos** and **images**. Powered by a hybrid **ResNeXt50 + LSTM** neural architecture, the system extracts facial regions, analyzes spatial and temporal inconsistencies across frames, and outputs classification with confidence metrics.

---

## 👨‍💻 Developer Information
* **Developer:** Darshan Naidu
* **Email:** [darshannaidu696@gmail.com](mailto:darshannaidu696@gmail.com)
* **GitHub:** [darshannaidu696](https://github.com/darshannaidu696)

---

## ⚡ Quick Start

### 1. Navigate to the project
```powershell
cd "c:\Users\Darshan Naidu\OneDrive\Desktop\all file\DFD_SYS\Deep_Fake_Detection"
```

### 2. Run the server
```powershell
python manage.py runserver
```

### 3. Open in browser
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## ⚙️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | Django 5.0.6 (Python 3.10+) |
| Deep Learning | PyTorch 2.3.1 (with GPU/CUDA Acceleration support) |
| Spatial CNN | ResNeXt50 (32×4d) via `torchvision.models` |
| Temporal RNN | LSTM (2048 hidden units, 1 layer) |
| Face Detection | `face-recognition` + `dlib` (HOG-based) |
| Computer Vision | OpenCV (`opencv-python` 4.10) |
| Client-Side Face Tracking | face-api.js (SSD MobileNet V1) |
| Frontend | HTML5, Bootstrap 5, Custom CSS (Inter + JetBrains Mono fonts) |

---

## ⚡ GPU Acceleration & Performance Optimizations

To deliver fast, production-grade deepfake inferences, the backend has been optimized with two major speedup mechanisms:

1. **GPU/CUDA Acceleration (Automatic)**
   - The system automatically detects and targets your GPU (e.g., **NVIDIA GeForce RTX 2050**).
   - Both the deep learning model and the frame tensors are pushed to the GPU's memory for maximum execution speed, bypassing high-latency CPU operations.
   
2. **Global Model In-Memory Caching**
   - The ResNeXt50 + LSTM architecture weights (~100MB+) are loaded **exactly once** upon the first request and cached globally in memory.
   - Subsequent prediction requests bypass the disk-read bottleneck completely, bringing the model loading time down to **0 milliseconds**.
   - Model instantiations are optimized with a `pretrained=False` bypass to eliminate needless ImageNet default weights download checking.

---

## 🧠 Neural Architecture

The model is defined as `class Model(nn.Module)` in `ml_app/views.py` (line 52). It combines two neural components:

### Spatial Encoder — ResNeXt50
- Pre-trained `torchvision.models.resnext50_32x4d` (ImageNet weights)
- Final 2 layers stripped (`nn.Sequential(*list(model.children())[:-2])`)
- Outputs 2048-dimensional feature maps per face crop
- Adaptive average pooling reduces spatial dimensions to `[batch, 2048]`

### Temporal Analyzer — LSTM
- `nn.LSTM(input_size=2048, hidden_size=2048, num_layers=1)`
- Processes the sequence of spatial features across N video frames
- Captures frame-to-frame temporal inconsistencies (facial jitter, blending artifacts)
- For single images: the face crop is replicated 20× to fill the sequence tensor

### Classification Head
- Dropout (0.4) for regularization
- `nn.Linear(2048, 2)` maps to binary output
- Softmax converts to probability: Class 0 = FAKE, Class 1 = REAL
- Trained weight file: `models/model_87_acc_20_frames_final_data.pt` (87% validation accuracy, 20-frame sequences)

### Full Pipeline
```
Upload → Frame Extraction (OpenCV) → Face Detection (dlib) → Face Crop + Padding
   → Resize 112×112 → Normalize → ResNeXt50 → LSTM → Linear → Softmax → REAL/FAKE
```

---

## 📁 Project Structure

```
Deep_Fake_Detection/
├── manage.py                         # Django CLI entry point
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Container deployment config
├── SKILL_REQUIREMENTS.txt            # Detailed skills & architecture guide
│
├── ml_app/                           # Core application
│   ├── views.py                      # Model definition, preprocessing, inference
│   ├── urls.py                       # Route definitions
│   ├── forms.py                      # File upload validation
│   └── templates/                    # HTML templates
│       ├── landing.html              # Home page
│       ├── index.html                # Video upload
│       ├── image_upload.html         # Image upload
│       ├── predict.html              # Video results
│       └── image_predict.html        # Image results
│
├── project_settings/                 # Django configuration
│   ├── settings.py                   # App settings
│   └── urls.py                       # Root URL router
│
├── models/                           # Pre-trained weights (.pt)
│   └── model_87_acc_20_frames_final_data.pt
│
├── static/                           # Static assets
│   ├── css/styles.css                # NeuralTrace design system
│   ├── js/face-api.min.js            # Client-side face detection
│   └── json/                         # face-api model weights
│
├── uploaded_videos/                  # Runtime video storage
└── uploaded_images/                  # Runtime face crops
```

---

## 🎯 Key Features

* **Dual-Mode Detection:** Supports both video (temporal) and image (spatial) deepfake analysis
* **GPU & Cache Boost:** Powered by NVIDIA GPU acceleration and an in-memory model cache for blistering-fast, zero-overhead inferences
* **Face Visualization:** Results page shows extracted frames and isolated face crops for model interpretability
* **87% Accuracy:** Ships with production-grade weights trained on 20-frame temporal sequences
* **Real-Time Bounding Boxes:** face-api.js draws detection overlays on video playback in the browser
* **Upload Safeguards:** 100MB file size limit with MIME type validation

---

## 🧼 Maintenance

Clear cached uploads:
```powershell
Remove-Item -Path ".\uploaded_videos\*" -Exclude "Readme.txt" -Force
Remove-Item -Path ".\uploaded_images\*" -Exclude "Readme.txt" -Force
```
