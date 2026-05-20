# 🛡️ Deep Fake Detection System (DFD_SYS)

A premium, production-grade web application designed to detect facial manipulation and deepfakes in both **videos** and **images**. Powered by state-of-the-art Deep Learning models, this system extracts facial regions, analyzes frame-to-frame inconsistencies, and provides predictions with highly accurate confidence metrics.

---

## 👨‍💻 Developer Information
* **Developer Name:** Darshan Naidu
* **Contact Email:** [darshannaidu696@gmail.com](mailto:darshannaidu696@gmail.com)
* **GitHub Profile:** [darshannaidu696](https://github.com/darshannaidu696)
* **Project Role:** Lead Backend & AI Integration Engineer

---

## ⚡ Quick Start: How to Run the Project

Your system is already fully configured with all necessary Python and Deep Learning libraries. Follow these simple steps to run the application:

### Step 1: Open Your Terminal
Open PowerShell, Command Prompt, or your integrated IDE terminal.

### Step 2: Navigate to the Project Directory
Ensure you are in the `Deep_Fake_Detection` folder:
```powershell
cd "c:\Users\Darshan Naidu\OneDrive\Desktop\all file\DFD_SYS\Deep_Fake_Detection"
```

### Step 3: Run the Development Server
Execute the Django management command to launch the web application:
```powershell
python manage.py runserver
```

### Step 4: Open Your Browser
Navigate to the local address to use the system:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## ⚙️ Core Technology Stack

* **Backend Framework:** Django 5.0.6 (Python 3.10+)
* **Deep Learning Engine:** PyTorch 2.3.1
* **Computer Vision:** OpenCV (`opencv-python` v4.10) & `face-recognition` (with `dlib`)
* **Mathematical Operations:** NumPy & Pandas
* **Frontend Design:** HTML5, Bootstrap 5, Stitch UI Design System (Premium Cobalt Blue Structural Grid & Off-White Canvas Cards with floating, interactive tilted components, Outfit & Space Grotesk Google Fonts)

---

## 🧠 Deep Learning Architecture & Pipeline

The system uses a **Hybrid Neural Network Architecture** that combines spatial and temporal modeling for maximum detection accuracy:

```
[ Uploaded Video ] 
        ↓
[ Frame Extraction ] (OpenCV splits video into N consecutive frames)
        ↓
[ Face Detection & Cropping ] (dlib extracts and aligns exact face coordinates)
        ↓
[ Spatial Feature Extraction ] (ResNext50 CNN extracts 2048-dim feature maps per face)
        ↓
[ Temporal Analysis ] (LSTM Network tracks inconsistencies between frames over time)
        ↓
[ Softmax Classification ] (Final Linear Layer outputs probability: REAL or FAKE)
```

1. **Spatial Features (ResNext50):** A deep Convolutional Neural Network pre-trained on millions of faces to recognize minute visual anomalies, texture inconsistencies, and blending artifacts.
2. **Temporal Features (LSTM):** Long Short-Term Memory recurrent networks analyze changes across frames. Deepfakes often have frame-wise jitter or facial movement artifacts that static classifiers miss. The LSTM catches these temporal patterns.

---

## 📁 Project Directory Structure

```
DFD_SYS/
│
└── Deep_Fake_Detection/
    ├── manage.py                    # Django management CLI ("Start Button")
    ├── requirements.txt             # Project library dependencies
    ├── db.sqlite3                   # SQLite database file
    │
    ├── ml_app/                      # Core Application Logic
    │   ├── views.py                 # Views handling preprocessing, face-cropping, and model inference
    │   ├── urls.py                  # Page routing & entry endpoints
    │   ├── forms.py                 # Safe image & video upload validation forms
    │   └── templates/               # User Interface HTML pages
    │       ├── landing.html         # Portal home page
    │       ├── index.html           # Video upload dashboard
    │       ├── image_upload.html    # Static image upload dashboard
    │       ├── predict.html         # Video prediction & frame analysis portal
    │       └── image_predict.html   # Image prediction portal
    │
    ├── project_settings/            # Django Global Configuration
    │   ├── settings.py              # Application environment & storage settings
    │   └── urls.py                  # Master routing routing-table
    │
    ├── models/                      # Pre-trained Neural Network Weights (.pt files)
    │   └── model_87_acc_20_frames_final_data.pt (Trained ResNext50+LSTM Weights)
    │
    ├── static/                      # Static Assets
    │   ├── css/                     # Sleek modern typography and layouts
    │   ├── js/                      # Page transitions & real-time upload progress scripts
    │   └── images/                  # Project logos & background illustrations
    │
    ├── uploaded_videos/             # Secure directory for runtime video analysis (Auto-cleared)
    └── uploaded_images/             # Secure directory for frame-splitting and face-cropping
```

---

## 🎯 Key Features

* **🎥 Dual-Mode Detection Engine:** Detect manipulations in single-frame images or temporal video sequences.
* **🧬 Face-Cropping Visualization Dashboard:** The results page shows you exactly which frames and face crops the neural network analyzed, giving the model high interpretability.
* **📈 High Accuracy Model:** Ships with a production-grade weight set (`model_87_acc_20_frames_final_data.pt`) yielding **87% validation accuracy** over 20-frame temporal analysis.
* **🎨 Award-Winning Stitch UI:** Beautiful minimalist and structured geometric design utilizing high-contrast cobalt-blue accents, structural grid backgrounds, and off-white custom rounded cards with floating, interactive, slightly tilted elements.
* **🛡️ Upload Safeguards:** Restricts file sizes to 100MB and strictly checks MIME types to ensure secure operations.

---

## 🎓 Educational Pathway & Skill Requirements

To help students, researchers, and developers understand the underlying mechanics of this project, we have created a highly detailed, step-by-step documentation file in the repository root:
👉 **[SKILL_REQUIREMENTS.txt](file:///c:/Users/Darshan%20Naidu/OneDrive/Desktop/all%20file/DFD_SYS/Deep_Fake_Detection/SKILL_REQUIREMENTS.txt)**

This document provides:
1. **Core Skills & Languages Needed:** Detailed concepts to master in Python, JavaScript/jQuery, and modern responsive CSS3/HTML5.
2. **Deep Learning Stack Details:** Under-the-hood analysis of PyTorch tensor operations, ResNeXt spatial feature maps, and recurrent LSTM sequencing.
3. **Step-by-Step Functional Workflow:** Trace logs showing how an uploaded media file travels from drag-and-drop triggers through dlib cropping coordinates to neural activation classes.
4. **Line-by-Line Code Breakdown:** Comprehensive breakdown explaining every class and function in `ml_app/views.py`.

---

## 🧼 System Maintenance & Optimization
To prevent disk bloat, this project contains a cleaning script that automatically manages storage. When running local tests, the system stores temporary face-cropped frames in the `uploaded_images` folder. 
* To manually purge old cached files and keep the repository light, use the cleanup workflow:
```powershell
Remove-Item -Path ".\uploaded_videos\*" -Exclude "Readme.txt" -Force
Remove-Item -Path ".\uploaded_images\*" -Exclude "Readme.txt" -Force
```
