# 🎨 Visual Guide to Deep Fake Detection Project

## 📊 Architecture Diagrams

### 1. Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Landing Page │  │ Upload Page  │  │ Results Page │          │
│  │ (HTML/CSS/JS)│  │ (HTML/CSS/JS)│  │ (HTML/CSS/JS)│          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │ HTTP Requests    │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO WEB SERVER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    URL Router (urls.py)                   │  │
│  │  /              →  landing_page()                         │  │
│  │  /video-detect/ →  index()                                │  │
│  │  /predict/      →  predict_page()                         │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │              Views (views.py) - Business Logic           │  │
│  │  • Handle requests                                        │  │
│  │  • Process uploads                                        │  │
│  │  • Call AI model                                          │  │
│  │  • Return responses                                       │  │
│  └────────┬──────────────────────────────────┬──────────────┘  │
│           │                                   │                 │
│  ┌────────▼────────┐                 ┌───────▼──────────┐      │
│  │ Forms (forms.py)│                 │ Templates (HTML) │      │
│  │ • Validate input│                 │ • Render pages   │      │
│  │ • Handle files  │                 │ • Show results   │      │
│  └─────────────────┘                 └──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
          │                                   │
          │ File I/O                          │ Model Loading
          ▼                                   ▼
┌─────────────────────────┐    ┌──────────────────────────────┐
│   File System           │    │   AI Model (.pt files)       │
│  • uploaded_videos/     │    │  • ResNext50 + LSTM          │
│  • uploaded_images/     │    │  • Trained weights           │
│  • static/              │    │  • 87% accuracy              │
└─────────────────────────┘    └──────────────────────────────┘
```

---

### 2. Request-Response Flow

```
USER                    DJANGO                      AI MODEL
 │                        │                            │
 │  1. Visit website      │                            │
 ├───────────────────────>│                            │
 │                        │                            │
 │  2. Show landing page  │                            │
 │<───────────────────────┤                            │
 │                        │                            │
 │  3. Click "Video"      │                            │
 ├───────────────────────>│                            │
 │                        │                            │
 │  4. Show upload form   │                            │
 │<───────────────────────┤                            │
 │                        │                            │
 │  5. Upload video.mp4   │                            │
 ├───────────────────────>│                            │
 │                        │                            │
 │                        │  6. Save file              │
 │                        │  7. Extract frames         │
 │                        │  8. Detect faces           │
 │                        │  9. Preprocess             │
 │                        │                            │
 │                        │  10. Load model            │
 │                        ├───────────────────────────>│
 │                        │                            │
 │                        │  11. Make prediction       │
 │                        │<───────────────────────────┤
 │                        │     (REAL, 85%)            │
 │                        │                            │
 │  12. Show results      │                            │
 │<───────────────────────┤                            │
 │   REAL - 85%           │                            │
 │                        │                            │
```

---

### 3. Video Processing Pipeline

```
INPUT: video.mp4 (30 seconds, 900 frames)
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: Frame Extraction           │
│  • Open video with cv2.VideoCapture │
│  • Read frames one by one           │
│  • Store in memory                  │
└─────────────┬───────────────────────┘
              │ Output: 900 frames
              ▼
┌─────────────────────────────────────┐
│  Step 2: Frame Selection            │
│  • Select N frames (e.g., 20)       │
│  • Evenly distributed               │
│  • Frames: [0, 45, 90, ..., 855]    │
└─────────────┬───────────────────────┘
              │ Output: 20 frames
              ▼
┌─────────────────────────────────────┐
│  Step 3: Face Detection             │
│  • For each frame:                  │
│    - Convert BGR → RGB              │
│    - face_recognition.face_locations│
│    - Get coordinates (top,r,b,l)    │
└─────────────┬───────────────────────┘
              │ Output: 20 face locations
              ▼
┌─────────────────────────────────────┐
│  Step 4: Face Cropping              │
│  • Crop each frame to face region   │
│  • Add padding (40 pixels)          │
│  • Save cropped images              │
└─────────────┬───────────────────────┘
              │ Output: 20 face images
              ▼
┌─────────────────────────────────────┐
│  Step 5: Preprocessing              │
│  • Resize to 112x112                │
│  • Convert to tensor                │
│  • Normalize (mean, std)            │
└─────────────┬───────────────────────┘
              │ Output: Tensor [20,3,112,112]
              ▼
┌─────────────────────────────────────┐
│  Step 6: Model Inference            │
│  • Pass through ResNext50           │
│  • Extract features                 │
│  • Process with LSTM                │
│  • Get prediction                   │
└─────────────┬───────────────────────┘
              │ Output: [prediction, confidence]
              ▼
┌─────────────────────────────────────┐
│  Step 7: Result Display             │
│  • REAL or FAKE                     │
│  • Confidence percentage            │
│  • Show processed images            │
└─────────────────────────────────────┘
```

---

### 4. AI Model Architecture (Detailed)

```
INPUT TENSOR: [1, 20, 3, 112, 112]
              (batch, frames, RGB, height, width)
    │
    ▼
┌──────────────────────────────────────────────────────┐
│              RESHAPE FOR BATCH PROCESSING             │
│  [1, 20, 3, 112, 112] → [20, 3, 112, 112]            │
│  Process all 20 frames together                       │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│                   ResNext50 CNN                       │
│  ┌────────────────────────────────────────────┐      │
│  │ Conv Layer 1: 3 → 64 channels              │      │
│  │ • Detects edges, colors                    │      │
│  └────────────────────────────────────────────┘      │
│  ┌────────────────────────────────────────────┐      │
│  │ Conv Layer 2: 64 → 128 channels            │      │
│  │ • Detects textures, patterns               │      │
│  └────────────────────────────────────────────┘      │
│  ┌────────────────────────────────────────────┐      │
│  │ Conv Layer 3: 128 → 256 channels           │      │
│  │ • Detects facial features                  │      │
│  └────────────────────────────────────────────┘      │
│  ┌────────────────────────────────────────────┐      │
│  │ Conv Layer 4: 256 → 512 channels           │      │
│  │ • Detects complex patterns                 │      │
│  └────────────────────────────────────────────┘      │
│  ┌────────────────────────────────────────────┐      │
│  │ Conv Layer 5: 512 → 2048 channels          │      │
│  │ • High-level feature extraction            │      │
│  └────────────────────────────────────────────┘      │
└────────────────────┬─────────────────────────────────┘
                     │ Output: [20, 2048, 4, 4]
                     ▼
┌──────────────────────────────────────────────────────┐
│              ADAPTIVE AVERAGE POOLING                 │
│  [20, 2048, 4, 4] → [20, 2048, 1, 1]                 │
│  Reduces spatial dimensions                           │
└────────────────────┬─────────────────────────────────┘
                     │ Output: [20, 2048]
                     ▼
┌──────────────────────────────────────────────────────┐
│              RESHAPE FOR SEQUENCE                     │
│  [20, 2048] → [1, 20, 2048]                          │
│  (batch, sequence, features)                          │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│                    LSTM LAYER                         │
│  ┌────────────────────────────────────────────┐      │
│  │ Frame 1 features → LSTM cell → hidden_1    │      │
│  │ Frame 2 features → LSTM cell → hidden_2    │      │
│  │ Frame 3 features → LSTM cell → hidden_3    │      │
│  │ ...                                         │      │
│  │ Frame 20 features → LSTM cell → hidden_20  │      │
│  │                                             │      │
│  │ Each cell remembers previous frames!       │      │
│  └────────────────────────────────────────────┘      │
│                                                        │
│  LSTM learns:                                         │
│  • Temporal patterns                                  │
│  • Frame-to-frame consistency                         │
│  • Motion patterns                                    │
│  • Blinking patterns                                  │
└────────────────────┬─────────────────────────────────┘
                     │ Output: [1, 2048]
                     ▼
┌──────────────────────────────────────────────────────┐
│                   DROPOUT (0.4)                       │
│  Randomly drop 40% of connections                     │
│  Prevents overfitting                                 │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│              LINEAR LAYER (2048 → 2)                  │
│  [1, 2048] → [1, 2]                                  │
│  Output: [FAKE_score, REAL_score]                    │
│  Example: [-1.5, 2.3]                                │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│                    SOFTMAX                            │
│  Converts scores to probabilities                     │
│  [-1.5, 2.3] → [0.15, 0.85]                          │
│                 FAKE  REAL                            │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
OUTPUT: Prediction = 1 (REAL), Confidence = 85%
```

---

### 5. File Structure Tree

```
Deep_Fake_Detection/
│
├── 📄 manage.py                    ← Django's command center
├── 📄 requirements.txt             ← List of dependencies
├── 📄 db.sqlite3                   ← Database file
│
├── 📁 project_settings/            ← Main configuration
│   ├── __init__.py
│   ├── settings.py                 ← App settings
│   ├── urls.py                     ← Main URL router
│   └── wsgi.py                     ← Server interface
│
├── 📁 ml_app/                      ← Main application
│   ├── __init__.py
│   ├── admin.py                    ← Admin interface (unused)
│   ├── apps.py                     ← App configuration
│   ├── forms.py                    ← Upload forms
│   ├── models.py                   ← Database models (empty)
│   ├── urls.py                     ← App URL routes
│   ├── views.py                    ← ⭐ MAIN LOGIC HERE
│   │
│   └── 📁 templates/               ← HTML files
│       ├── landing.html            ← Home page
│       ├── index.html              ← Video upload
│       ├── image_upload.html       ← Image upload
│       ├── predict.html            ← Video results
│       ├── image_predict.html      ← Image results
│       └── about.html              ← About page
│
├── 📁 templates/                   ← Shared templates
│   ├── base.html                   ← Base template
│   ├── nav-bar.html                ← Navigation
│   └── footer.html                 ← Footer
│
├── 📁 static/                      ← Static files
│   ├── 📁 css/                     ← Stylesheets
│   ├── 📁 js/                      ← JavaScript
│   │   ├── script.js               ← Main scripts
│   │   └── face-api.min.js         ← Face detection
│   ├── 📁 images/                  ← Images
│   └── 📁 json/                    ← Face-api models
│
├── 📁 models/                      ← ⭐ AI MODEL FILES
│   └── model_87_acc_20_frames_final_data.pt
│
├── 📁 uploaded_videos/             ← User uploads
│   └── uploaded_file_*.mp4
│
└── 📁 uploaded_images/             ← Processed images
    ├── *_preprocessed_*.png
    └── *_face_*.png
```

---

### 6. Data Transformation Journey

```
ORIGINAL VIDEO
┌─────────────────────┐
│  1920x1080 pixels   │
│  30 fps             │
│  10 seconds         │
│  300 frames total   │
└──────────┬──────────┘
           │
           ▼
FRAME EXTRACTION
┌─────────────────────┐
│  Select 20 frames   │
│  Evenly spaced      │
│  1920x1080 each     │
└──────────┬──────────┘
           │
           ▼
FACE DETECTION
┌─────────────────────┐
│  Detect face box    │
│  (top, right,       │
│   bottom, left)     │
└──────────┬──────────┘
           │
           ▼
FACE CROPPING
┌─────────────────────┐
│  Crop to face       │
│  ~400x400 pixels    │
│  Add 40px padding   │
└──────────┬──────────┘
           │
           ▼
RESIZE
┌─────────────────────┐
│  Resize to 112x112  │
│  Maintain aspect    │
└──────────┬──────────┘
           │
           ▼
NORMALIZE
┌─────────────────────┐
│  RGB values:        │
│  0-255 → -1 to 1    │
│  Apply mean & std   │
└──────────┬──────────┘
           │
           ▼
TENSORIZE
┌─────────────────────┐
│  Convert to tensor  │
│  [20, 3, 112, 112]  │
│  20 frames          │
│  3 channels (RGB)   │
│  112x112 pixels     │
└──────────┬──────────┘
           │
           ▼
ADD BATCH DIMENSION
┌─────────────────────┐
│  [1,20,3,112,112]   │
│  Ready for model!   │
└─────────────────────┘
```

---

This visual guide helps you understand the flow and structure of the entire project!

