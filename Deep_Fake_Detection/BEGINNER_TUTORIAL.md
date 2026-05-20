# 🎓 Complete Beginner's Guide to Deep Fake Detection Project

## 📚 Table of Contents
1. [What is This Project?](#what-is-this-project)
2. [How Does It Work? (Simple Explanation)](#how-does-it-work-simple-explanation)
3. [Project Structure Explained](#project-structure-explained)
4. [Understanding Django Framework](#understanding-django-framework)
5. [Code Explanation - Step by Step](#code-explanation-step-by-step)
6. [The AI Model Explained](#the-ai-model-explained)
7. [How Everything Connects](#how-everything-connects)

---

## 🎯 What is This Project?

This is a **web application** that can detect if a video or image has been manipulated (fake) or is real. Think of it like a lie detector, but for videos and images!

### Real-World Example:
- You upload a video of someone speaking
- The AI analyzes the video
- It tells you: "This is FAKE with 85% confidence" or "This is REAL with 92% confidence"

---

## 🔍 How Does It Work? (Simple Explanation)

### The Journey of Your Video/Image:

```
1. YOU → Upload video/image through website
2. SERVER → Saves the file
3. AI → Extracts faces from video/image
4. AI → Analyzes faces using trained model
5. AI → Makes prediction (REAL or FAKE)
6. YOU → See the result with confidence score
```

### Think of it like a Restaurant:

- **You (Customer)**: Upload video
- **Waiter (Django)**: Takes your order and brings it to kitchen
- **Chef (AI Model)**: Analyzes the video
- **Waiter (Django)**: Brings back the result
- **You**: Get your answer!

---

## 📁 Project Structure Explained

```
Deep_Fake_Detection/
│
├── manage.py                    # The "start button" for Django
├── requirements.txt             # List of all tools/libraries needed
├── db.sqlite3                   # Database (stores data)
│
├── project_settings/            # Main settings folder
│   ├── settings.py             # Configuration (like app settings)
│   ├── urls.py                 # Main traffic controller
│   └── wsgi.py                 # Server connector
│
├── ml_app/                      # The brain of the application
│   ├── views.py                # The logic (what happens when you click)
│   ├── urls.py                 # Page routes (which page goes where)
│   ├── forms.py                # Upload forms (input fields)
│   ├── models.py               # Database structure (empty here)
│   └── templates/              # HTML pages (what you see)
│       ├── landing.html        # Home page
│       ├── index.html          # Video upload page
│       ├── image_upload.html   # Image upload page
│       └── predict.html        # Results page
│
├── static/                      # CSS, JavaScript, Images
│   ├── css/                    # Styling files
│   ├── js/                     # Interactive scripts
│   └── images/                 # Pictures
│
├── models/                      # AI brain files (.pt files)
├── uploaded_videos/             # Where uploaded videos go
└── uploaded_images/             # Where uploaded images go
```

---

## 🌐 Understanding Django Framework

### What is Django?
Django is like a **construction kit** for building websites. It provides:
- Ready-made tools
- Security features
- Database management
- User interface handling

### Django Components (Think of a House):

1. **URLs (urls.py)** = Address/Doorbell
   - Decides which page to show when you visit a URL
   
2. **Views (views.py)** = Rooms/Functions
   - Contains the logic of what happens in each room
   
3. **Templates (HTML files)** = Decoration/Furniture
   - What you actually see on the page
   
4. **Models (models.py)** = Storage/Database
   - Where data is stored (not used much in this project)
   
5. **Settings (settings.py)** = House Rules
   - Configuration for the entire project

---

## 💻 Code Explanation - Step by Step

### 1️⃣ **manage.py** - The Starting Point

```python
#!/usr/bin/env python
import os
import sys

def main():
    # Tell Django where settings are
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings.settings')
    
    # Import Django's command runner
    from django.core.management import execute_from_command_line
    
    # Run the command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

**What it does:**
- This is like the "power button" of your application
- When you run `python manage.py runserver`, this file starts everything
- It loads settings and starts the web server

---

### 2️⃣ **settings.py** - Configuration File

```python
# Where is the project located?
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret key (like a password for Django)
SECRET_KEY = '@)0qp0!&-vht7k0wyuihr+nk-b8zrvb5j^1d@vl84cd1%)f=dz'

# Debug mode (shows errors clearly during development)
DEBUG = True

# Who can access this website?
ALLOWED_HOSTS = ["*"]  # Anyone can access

# Installed apps (features of your website)
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ml_app.apps.MlAppConfig'  # Our main app
]

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Using SQLite
        "NAME": os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

# Where static files (CSS, JS, images) are stored
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'uploaded_images'),
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(PROJECT_DIR, 'models'),
]

# Where uploaded videos are saved
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'uploaded_videos')

# Maximum upload size (100 MB)
MAX_UPLOAD_SIZE = "104857600"
```

**What it does:**
- Sets up the entire project
- Tells Django where files are
- Configures database
- Sets security settings

---

### 3️⃣ **urls.py** - Traffic Controller

#### Main URLs (project_settings/urls.py):
```python
from django.urls import path, include

urlpatterns = [
    path('', include('ml_app.urls')),  # Send all traffic to ml_app
]
```

#### App URLs (ml_app/urls.py):
```python
from . import views

urlpatterns = [
    path('', landing_page, name='landing'),              # Home: /
    path('video-detect/', index, name='home'),           # Video: /video-detect/
    path('image-detect/', image_upload, name='image_upload'),  # Image: /image-detect/
    path('predict/', predict_page, name='predict'),      # Results: /predict/
    path('image-predict/', image_predict_page, name='image_predict'),
]
```

**What it does:**
- Like a GPS for your website
- When you visit `http://localhost:8000/`, it shows landing page
- When you visit `http://localhost:8000/video-detect/`, it shows video upload page
- Each URL is connected to a function in views.py

---

### 4️⃣ **forms.py** - Input Forms

```python
from django import forms

# Form for uploading videos
class VideoUploadForm(forms.Form):
    # File input field
    upload_video_file = forms.FileField(
        label="Select Video",      # Label shown to user
        required=True,             # Must upload a file
        widget=forms.FileInput(attrs={"accept": "video/*"})  # Only videos
    )
    
    # Number input field
    sequence_length = forms.IntegerField(
        label="Sequence Length",   # How many frames to analyze
        required=True
    )

# Form for uploading images
class ImageUploadForm(forms.Form):
    upload_image_file = forms.FileField(
        label="Select Image",
        required=True,
        widget=forms.FileInput(attrs={'accept': 'image/*'})  # Only images
    )
```

**What it does:**
- Creates input fields for users
- Validates uploaded files
- Makes sure users upload correct file types

---

### 5️⃣ **views.py** - The Brain (Main Logic)

This is the MOST IMPORTANT file! It contains all the logic.

#### Part 1: Imports (Getting Tools)

```python
from django.shortcuts import render, redirect  # Page navigation
import torch                                    # AI framework
import cv2                                      # Video/image processing
import face_recognition                         # Face detection
import numpy as np                              # Math operations
from .forms import VideoUploadForm, ImageUploadForm  # Our forms
```

**Think of imports like:**
- Getting tools from a toolbox before starting work
- Each import brings a specific capability

---

#### Part 2: Configuration Variables

```python
# Image size for AI model
im_size = 112

# Color normalization values (makes images consistent)
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

# Check if GPU is available (faster processing)
if torch.cuda.is_available():
    device = 'cuda'  # Use GPU
else:
    device = 'cpu'   # Use CPU (slower)

# Image transformations (prepare images for AI)
train_transforms = transforms.Compose([
    transforms.ToPILImage(),              # Convert to image
    transforms.Resize((im_size, im_size)), # Resize to 112x112
    transforms.ToTensor(),                # Convert to numbers
    transforms.Normalize(mean, std)       # Normalize colors
])
```

**What it does:**
- Sets up constants used throughout the code
- Prepares image processing pipeline
- Checks if GPU is available for faster processing

---

#### Part 3: The AI Model Class

```python
class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1,
                 hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()

        # Use pre-trained ResNext50 model (already knows about images)
        model = models.resnext50_32x4d(pretrained=True)

        # Remove last layers (we'll add our own)
        self.model = nn.Sequential(*list(model.children())[:-2])

        # LSTM: Analyzes sequence of frames (like reading a story)
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)

        # Activation function (adds non-linearity)
        self.relu = nn.LeakyReLU()

        # Dropout: Prevents overfitting (like not memorizing answers)
        self.dp = nn.Dropout(0.4)

        # Final layer: Makes the decision (REAL or FAKE)
        self.linear1 = nn.Linear(2048, num_classes)

        # Pooling: Reduces image size
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        # x shape: [batch_size, sequence_length, channels, height, width]
        batch_size, seq_length, c, h, w = x.shape

        # Reshape to process all frames at once
        x = x.view(batch_size * seq_length, c, h, w)

        # Extract features from images
        fmap = self.model(x)

        # Pool features
        x = self.avgpool(fmap)

        # Reshape back to sequence
        x = x.view(batch_size, seq_length, 2048)

        # Process sequence with LSTM
        x_lstm, _ = self.lstm(x, None)

        # Make final prediction
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))
```

**Simple Explanation:**

Think of this model like a detective:

1. **ResNext50** (self.model): The detective's eyes
   - Looks at each frame and extracts important features
   - Pre-trained means it already knows what faces look like

2. **LSTM** (self.lstm): The detective's brain
   - Remembers what it saw in previous frames
   - Looks for patterns across time (important for videos!)

3. **Linear Layer** (self.linear1): The final decision
   - Takes all information and decides: REAL or FAKE

**Why LSTM?**
- Videos are sequences of frames
- LSTM can remember patterns across frames
- Deepfakes often have inconsistencies between frames
- LSTM catches these inconsistencies!

---

#### Part 4: Dataset Classes (Preparing Data)

```python
class validation_dataset(Dataset):
    """Prepares video data for the AI model"""

    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length  # How many frames to extract

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []

        # Extract frames from video
        for i, frame in enumerate(self.frame_extract(video_path)):
            # Detect faces in frame
            faces = face_recognition.face_locations(frame)

            try:
                # Crop to face region
                top, right, bottom, left = faces[0]
                frame = frame[top:bottom, left:right, :]
            except:
                pass  # If no face, use full frame

            # Transform frame (resize, normalize)
            frames.append(self.transform(frame))

            # Stop when we have enough frames
            if len(frames) == self.count:
                break

        # Stack frames into tensor
        frames = torch.stack(frames)
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        """Extract frames from video one by one"""
        vidObj = cv2.VideoCapture(path)
        success = 1
        while success:
            success, image = vidObj.read()
            if success:
                yield image  # Return one frame at a time
```

**Simple Explanation:**

This class is like a **video processor**:

1. Opens the video file
2. Extracts frames one by one
3. Detects faces in each frame
4. Crops to face region
5. Resizes and normalizes
6. Returns processed frames ready for AI

**Why crop faces?**
- Deepfakes usually manipulate faces
- Focusing on faces improves accuracy
- Removes background noise

---

#### Part 5: Image Dataset Class

```python
class ImageValidationDataset(Dataset):
    """Prepares single image for the AI model"""

    def __init__(self, image_path, sequence_length=20, transform=None):
        self.image_path = image_path
        self.transform = transform
        self.sequence_length = sequence_length

    def __getitem__(self, idx):
        # Load image
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        faces = face_recognition.face_locations(image)

        if len(faces) > 0:
            # Crop to face with padding
            top, right, bottom, left = faces[0]
            padding = 40

            top = max(0, top - padding)
            bottom = min(image.shape[0], bottom + padding)
            left = max(0, left - padding)
            right = min(image.shape[1], right + padding)

            face_image = image[top:bottom, left:right]
        else:
            face_image = image

        # Apply transformations
        if self.transform:
            face_image = self.transform(face_image)

        # Create sequence by repeating image
        # (LSTM needs sequence, so we repeat the same image)
        frames = []
        for _ in range(self.sequence_length):
            frames.append(face_image)

        frames = torch.stack(frames)
        return frames.unsqueeze(0)
```

**Why repeat the same image?**
- The model was trained on video sequences
- For images, we create a "fake sequence" by repeating
- This allows us to use the same model for both videos and images

---

#### Part 6: Prediction Functions

```python
def predict(model, img, path='./', video_file_name=""):
    """Make prediction on video frames"""

    # Pass image through model
    fmap, logits = model(img.to(device))

    # Apply softmax (converts to probabilities)
    logits = sm(logits)

    # Get prediction (0 or 1)
    _, prediction = torch.max(logits, 1)

    # Get confidence score
    confidence = logits[:, int(prediction.item())].item() * 100

    print('Confidence:', confidence)

    # Return [prediction, confidence]
    # prediction: 0 = FAKE, 1 = REAL
    return [int(prediction.item()), confidence]
```

**Simple Explanation:**

This function is like a **fortune teller**:

1. **Input**: Processed video frames
2. **Process**:
   - Runs frames through AI model
   - Gets raw scores (logits)
   - Converts to probabilities (softmax)
3. **Output**:
   - Prediction (0 or 1)
   - Confidence (0-100%)

**What is Softmax?**
- Converts raw numbers to probabilities
- Example: [-2.3, 1.5] → [0.12, 0.88]
- Makes results easier to understand

---

#### Part 7: Helper Functions

```python
def get_accurate_model(sequence_length):
    """Find the best model for given sequence length"""

    # Get all model files
    list_models = glob.glob(os.path.join(settings.PROJECT_DIR, "models", "*.pt"))

    # Model naming: model_87_acc_20_frames_final_data.pt
    #                      ^^      ^^
    #                   accuracy  frames

    sequence_model = []

    # Find models matching sequence length
    for model_path in list_models:
        model_filename = os.path.basename(model_path)
        try:
            # Extract frame count from filename
            seq = model_filename.split("_")[3]
            if int(seq) == sequence_length:
                sequence_model.append(model_filename)
        except IndexError:
            pass

    # If multiple models, choose highest accuracy
    if len(sequence_model) > 1:
        accuracy = []
        for filename in sequence_model:
            acc = filename.split("_")[1]
            accuracy.append(acc)
        max_index = accuracy.index(max(accuracy))
        final_model = sequence_model[max_index]
    elif len(sequence_model) == 1:
        final_model = sequence_model[0]
    else:
        print("No model found!")
        return None

    return os.path.join(settings.PROJECT_DIR, "models", final_model)
```

**What it does:**
- Finds the right AI model based on how many frames you want to analyze
- If multiple models exist, picks the most accurate one
- Model filename contains accuracy and frame count

---

#### Part 8: View Functions (The Controllers)

##### 8.1 Landing Page

```python
def landing_page(request):
    """Show the home page"""
    return render(request, 'landing.html')
```

**Simple!** Just shows the landing page.

---

##### 8.2 Video Upload Page

```python
def index(request):
    """Handle video upload page"""

    if request.method == 'GET':
        # User is visiting the page
        video_upload_form = VideoUploadForm()

        # Clear old session data
        if 'file_name' in request.session:
            del request.session['file_name']

        return render(request, 'index.html', {"form": video_upload_form})

    else:
        # User submitted the form (POST request)
        video_upload_form = VideoUploadForm(request.POST, request.FILES)

        if video_upload_form.is_valid():
            # Get uploaded file
            video_file = video_upload_form.cleaned_data['upload_video_file']
            sequence_length = video_upload_form.cleaned_data['sequence_length']

            # Validate file type
            if not allowed_video_file(video_file.name):
                video_upload_form.add_error("upload_video_file",
                                           "Only video files allowed")
                return render(request, 'index.html', {"form": video_upload_form})

            # Validate file size (max 100MB)
            if video_file.size > int(settings.MAX_UPLOAD_SIZE):
                video_upload_form.add_error("upload_video_file",
                                           "Maximum file size 100 MB")
                return render(request, 'index.html', {"form": video_upload_form})

            # Save uploaded file
            saved_video_file = 'uploaded_file_' + str(int(time.time())) + ".mp4"
            file_path = os.path.join(settings.PROJECT_DIR, 'uploaded_videos',
                                    saved_video_file)

            with open(file_path, 'wb') as vFile:
                shutil.copyfileobj(video_file, vFile)

            # Store in session (temporary storage)
            request.session['file_name'] = file_path
            request.session['sequence_length'] = sequence_length

            # Redirect to prediction page
            return redirect('ml_app:predict')

        else:
            # Form has errors
            return render(request, 'index.html', {"form": video_upload_form})
```

**Flow Explanation:**

```
User visits page (GET)
    ↓
Show upload form
    ↓
User uploads video (POST)
    ↓
Validate file (type, size)
    ↓
Save file to server
    ↓
Store file path in session
    ↓
Redirect to prediction page
```

**What is a session?**
- Temporary storage for each user
- Like a shopping cart
- Stores data between page visits
- Automatically cleared when browser closes

---

##### 8.3 Video Prediction Page (The Magic Happens Here!)

```python
def predict_page(request):
    """Analyze video and show results"""

    if request.method == "GET":
        # Get file from session
        if 'file_name' not in request.session:
            return redirect("ml_app:home")

        video_file = request.session['file_name']
        sequence_length = request.session['sequence_length']

        # Step 1: Load the AI model
        model_path = get_accurate_model(sequence_length)

        if device == "cuda":
            model = Model(2).cuda()  # Use GPU
        else:
            model = Model(2).cpu()   # Use CPU

        # Load trained weights
        model.load_state_dict(torch.load(model_path,
                                        map_location=torch.device('cpu')))
        model.eval()  # Set to evaluation mode

        # Step 2: Extract and process frames
        print("Extracting frames...")
        cap = cv2.VideoCapture(video_file)
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                break
        cap.release()

        # Step 3: Detect and crop faces
        print("Detecting faces...")
        preprocessed_images = []
        faces_cropped_images = []

        for i in range(sequence_length):
            if i >= len(frames):
                break

            frame = frames[i]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Save preprocessed frame
            image_name = f"preprocessed_{i+1}.png"
            image_path = os.path.join(settings.PROJECT_DIR,
                                     'uploaded_images', image_name)
            cv2.imwrite(image_path, rgb_frame)
            preprocessed_images.append(image_name)

            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame)

            if len(face_locations) > 0:
                top, right, bottom, left = face_locations[0]
                face_image = frame[top:bottom, left:right]

                # Save cropped face
                face_name = f"face_{i+1}.png"
                face_path = os.path.join(settings.PROJECT_DIR,
                                        'uploaded_images', face_name)
                cv2.imwrite(face_path, face_image)
                faces_cropped_images.append(face_name)

        # Step 4: Make prediction
        print("Making prediction...")
        video_dataset = validation_dataset([video_file],
                                          sequence_length=sequence_length,
                                          transform=train_transforms)

        prediction = predict(model, video_dataset[0], './', 'video')

        confidence = round(prediction[1], 1)
        output = "REAL" if prediction[0] == 1 else "FAKE"

        print(f"Result: {output} with {confidence}% confidence")

        # Step 5: Prepare results for display
        context = {
            'preprocessed_images': preprocessed_images,
            'faces_cropped_images': faces_cropped_images,
            'original_video': video_file,
            'output': output,
            'confidence': confidence
        }

        return render(request, 'predict.html', context)
```

**Step-by-Step Breakdown:**

1. **Get Video**: Retrieve uploaded video from session
2. **Load Model**: Load the trained AI model
3. **Extract Frames**: Split video into individual frames
4. **Detect Faces**: Find faces in each frame
5. **Crop Faces**: Cut out face regions
6. **Preprocess**: Resize and normalize images
7. **Predict**: Run through AI model
8. **Display Results**: Show REAL/FAKE with confidence

---

## 🧠 The AI Model Explained

### What is the Model File (.pt)?

The `.pt` file is like a **trained brain**:
- Contains millions of learned parameters
- Trained on thousands of real and fake videos
- Learned to recognize patterns of manipulation

### Model Architecture Breakdown

```
INPUT: Video Frames (20 frames of 112x112 pixels)
    ↓
┌─────────────────────────────────────┐
│  ResNext50 (Feature Extractor)      │
│  - Looks at each frame               │
│  - Extracts 2048 features per frame  │
│  - Like finding fingerprints         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  LSTM (Sequence Analyzer)            │
│  - Analyzes sequence of features     │
│  - Remembers patterns across frames  │
│  - Detects temporal inconsistencies  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Linear Layer (Decision Maker)       │
│  - Combines all information          │
│  - Outputs 2 scores: [FAKE, REAL]   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Softmax (Probability Converter)     │
│  - Converts scores to probabilities  │
│  - Example: [0.15, 0.85] = 85% REAL │
└─────────────────────────────────────┘
    ↓
OUTPUT: Prediction + Confidence
```

### Why This Architecture Works

1. **ResNext50**:
   - Pre-trained on ImageNet (millions of images)
   - Already knows about faces, textures, lighting
   - Extracts high-level features

2. **LSTM (Long Short-Term Memory)**:
   - Designed for sequences
   - Remembers information across frames
   - Catches inconsistencies like:
     - Blinking patterns
     - Facial movements
     - Lighting changes
     - Edge artifacts

3. **Why Sequence Matters**:
   - Single frame might look perfect
   - But across frames, deepfakes show inconsistencies
   - LSTM catches these temporal anomalies

### Training Process (How the Model Learned)

```
1. Collect Data:
   - Thousands of REAL videos
   - Thousands of FAKE videos (deepfakes)

2. Label Data:
   - REAL videos labeled as 1
   - FAKE videos labeled as 0

3. Training Loop:
   For each video:
     a. Extract frames
     b. Feed to model
     c. Model makes prediction
     d. Compare with true label
     e. Calculate error
     f. Adjust model weights
     g. Repeat thousands of times

4. Result:
   - Model learns patterns
   - Gets better at distinguishing real from fake
   - Achieves 87% accuracy (from filename)
```

### Model Naming Convention

```
model_87_acc_20_frames_final_data.pt
      ^^      ^^
      |       |
   Accuracy  Frames per sequence

87 = 87% accuracy on test data
20 = Trained on 20-frame sequences
```

---

## 🔗 How Everything Connects

### Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  1. User visits: http://localhost:8000/                      │
│     → urls.py routes to landing_page()                       │
│     → views.py renders landing.html                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. User clicks "Start Video Detection"                      │
│     → Navigates to /video-detect/                            │
│     → urls.py routes to index()                              │
│     → views.py renders index.html with VideoUploadForm       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. User uploads video and sets sequence length              │
│     → Form data sent via POST                                │
│     → forms.py validates input                               │
│     → views.py (index function):                             │
│         - Validates file type and size                       │
│         - Saves file to uploaded_videos/                     │
│         - Stores path in session                             │
│         - Redirects to /predict/                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Prediction Process (predict_page function)               │
│                                                               │
│  Step 1: Load Model                                          │
│    - get_accurate_model() finds right .pt file               │
│    - Model class initialized                                 │
│    - Weights loaded from .pt file                            │
│                                                               │
│  Step 2: Extract Frames                                      │
│    - cv2.VideoCapture opens video                            │
│    - Reads frames one by one                                 │
│    - Stores in list                                          │
│                                                               │
│  Step 3: Detect Faces                                        │
│    - face_recognition.face_locations() finds faces           │
│    - Crops to face region                                    │
│    - Saves preprocessed images                               │
│                                                               │
│  Step 4: Prepare Data                                        │
│    - validation_dataset class processes frames               │
│    - Applies transformations (resize, normalize)             │
│    - Creates tensor [1, 20, 3, 112, 112]                     │
│                                                               │
│  Step 5: Make Prediction                                     │
│    - predict() function:                                     │
│      • Passes tensor through model                           │
│      • Gets logits (raw scores)                              │
│      • Applies softmax (probabilities)                       │
│      • Returns prediction and confidence                     │
│                                                               │
│  Step 6: Render Results                                      │
│    - Prepares context dictionary                             │
│    - Renders predict.html                                    │
│    - Shows REAL/FAKE with confidence                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. User sees results                                        │
│     - Original video                                         │
│     - Extracted frames                                       │
│     - Cropped faces                                          │
│     - Prediction: REAL or FAKE                               │
│     - Confidence score                                       │
└─────────────────────────────────────────────────────────────┘
```

### File Interaction Map

```
User Request
    ↓
manage.py (starts Django)
    ↓
project_settings/urls.py (main router)
    ↓
ml_app/urls.py (app router)
    ↓
ml_app/views.py (logic)
    ├→ ml_app/forms.py (validation)
    ├→ ml_app/templates/*.html (display)
    ├→ models/*.pt (AI brain)
    ├→ uploaded_videos/ (storage)
    └→ uploaded_images/ (storage)
```

### Data Flow

```
Video File (MP4)
    ↓
Frames (Images)
    ↓
Face Detection
    ↓
Cropped Faces
    ↓
Preprocessing (Resize, Normalize)
    ↓
Tensor [1, 20, 3, 112, 112]
    ↓
ResNext50 Feature Extraction
    ↓
Features [1, 20, 2048]
    ↓
LSTM Processing
    ↓
Final Features [1, 2048]
    ↓
Linear Layer
    ↓
Logits [1, 2]
    ↓
Softmax
    ↓
Probabilities [FAKE_prob, REAL_prob]
    ↓
Prediction (0 or 1) + Confidence (%)
```

---

## 📊 Key Concepts Explained

### 1. What is a Tensor?

A **tensor** is a multi-dimensional array of numbers.

```python
# 1D Tensor (Vector)
[1, 2, 3, 4]

# 2D Tensor (Matrix)
[[1, 2, 3],
 [4, 5, 6]]

# 3D Tensor (Image)
[[[R, G, B],  # Pixel 1
  [R, G, B]], # Pixel 2
 ...]

# 5D Tensor (Video Batch)
[batch, sequence, channels, height, width]
[1, 20, 3, 112, 112]
 ↑   ↑  ↑   ↑    ↑
 |   |  |   |    Width: 112 pixels
 |   |  |   Height: 112 pixels
 |   |  Channels: RGB (3 colors)
 |   Sequence: 20 frames
 Batch: 1 video
```

### 2. What is Normalization?

**Normalization** makes all images consistent.

```python
# Before normalization
Pixel values: 0-255 (different ranges)

# After normalization
Pixel values: -1 to 1 (standard range)

# Why?
- AI models work better with consistent input
- Prevents some features from dominating
- Speeds up training
```

### 3. What is Softmax?

**Softmax** converts scores to probabilities.

```python
# Raw scores (logits)
[2.5, -1.3]

# After softmax
[0.95, 0.05]  # Adds up to 1.0

# Interpretation
95% REAL, 5% FAKE
```

### 4. What is CUDA/GPU?

**GPU** (Graphics Processing Unit) is like having 1000 workers instead of 1.

```
CPU (1 worker):
Task 1 → Task 2 → Task 3 → ... (Sequential)

GPU (1000 workers):
Task 1 ↘
Task 2 → All at once! (Parallel)
Task 3 ↗

Result: 10-100x faster for AI!
```

---

## 🎨 HTML Templates Explained

### landing.html - Home Page

**Purpose**: Welcome page with navigation

**Key Elements**:
- Hero section with title
- Feature cards
- Buttons to video/image detection
- Animations and styling

### index.html - Video Upload

**Purpose**: Upload video for analysis

**Key Elements**:
- File upload input
- Sequence length slider (10-100 frames)
- Video preview
- Submit button

**JavaScript Features**:
- Drag and drop upload
- Real-time video preview
- Slider with visual feedback
- Form validation

### predict.html - Results Display

**Purpose**: Show analysis results

**Key Elements**:
- Original video player
- Extracted frames gallery
- Cropped faces gallery
- Result (REAL/FAKE)
- Confidence score
- Face detection overlay (using face-api.js)

**JavaScript Features**:
- Real-time face detection on video
- Bounding boxes around faces
- Color-coded results (green=REAL, red=FAKE)

---

## 🛠️ Practical Examples

### Example 1: Following a Request Through the Code

**User Action**: Upload a video

```
1. User clicks "Start Video Detection"
   File: ml_app/urls.py
   Line: path('video-detect/', index, name='home')
   → Calls index() function

2. index() function executes
   File: ml_app/views.py
   Line: def index(request):
   → Shows upload form

3. User uploads video.mp4 and sets sequence=20
   → Form submitted via POST

4. index() validates and saves
   File: ml_app/views.py
   Lines: 307-336
   → Saves to uploaded_videos/uploaded_file_1234567890.mp4
   → Stores in session
   → Redirects to predict

5. predict_page() executes
   File: ml_app/views.py
   Lines: 340-451
   → Loads model
   → Extracts frames
   → Makes prediction
   → Shows results
```

### Example 2: Understanding a Prediction

**Input**: Video with 20 frames

```python
# Step 1: Video loaded
video_path = "uploaded_videos/uploaded_file_1234567890.mp4"

# Step 2: Dataset created
dataset = validation_dataset([video_path], sequence_length=20)

# Step 3: Frames extracted and processed
# Output shape: [1, 20, 3, 112, 112]
#               ↑  ↑   ↑   ↑    ↑
#               |  |   |   |    Width
#               |  |   |   Height
#               |  |   RGB channels
#               |  20 frames
#               1 video

# Step 4: Model processes
fmap, logits = model(frames)
# fmap: Feature maps from ResNext50
# logits: Raw scores [FAKE_score, REAL_score]

# Step 5: Softmax applied
probabilities = softmax(logits)
# Example: [0.15, 0.85]
#          FAKE  REAL

# Step 6: Prediction made
prediction = argmax(probabilities)  # 1 (REAL)
confidence = probabilities[1] * 100  # 85%

# Step 7: Result
output = "REAL"
confidence = 85.0
```

### Example 3: How Face Detection Works

```python
# Load image
image = cv2.imread("video_frame.jpg")

# Convert to RGB (face_recognition needs RGB)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect faces
face_locations = face_recognition.face_locations(rgb_image)
# Returns: [(top, right, bottom, left), ...]

# Example output
# [(142, 617, 409, 350)]
#   ↑    ↑    ↑    ↑
#   top  right bottom left

# Crop to face
top, right, bottom, left = face_locations[0]
face_image = image[top:bottom, left:right]

# Now face_image contains only the face!
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "No module named 'torch'"

**Problem**: PyTorch not installed

**Solution**:
```bash
pip install torch torchvision
```

### Issue 2: "CUDA out of memory"

**Problem**: GPU doesn't have enough memory

**Solution**:
```python
# In views.py, force CPU usage
device = 'cpu'  # Change from 'cuda' to 'cpu'
```

### Issue 3: "No faces detected"

**Problem**: Face detection failed

**Reasons**:
- Face too small in video
- Face at extreme angle
- Poor lighting
- Face partially hidden

**Solution**:
- Use videos with clear, front-facing faces
- Ensure good lighting
- Face should be at least 100x100 pixels

### Issue 4: Model file not found

**Problem**: .pt file missing

**Solution**:
1. Download model from Google Drive (see README)
2. Place in `models/` folder
3. Ensure filename format: `model_XX_acc_YY_frames_final_data.pt`

### Issue 5: Slow prediction

**Problem**: Processing takes too long

**Solutions**:
- Reduce sequence_length (use 10 or 20 instead of 100)
- Use GPU if available
- Use smaller video files
- Reduce video resolution before upload

---

## 📝 Code Modification Examples

### Example 1: Change Maximum Upload Size

**File**: `project_settings/settings.py`

```python
# Current: 100 MB
MAX_UPLOAD_SIZE = "104857600"

# Change to 200 MB
MAX_UPLOAD_SIZE = "209715200"
```

### Example 2: Add New Video Format

**File**: `ml_app/views.py`

```python
# Current
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv'])

# Add 'mov'
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv', 'mov'])
```

### Example 3: Change Default Sequence Length

**File**: `ml_app/templates/index.html`

```javascript
// Current: Default is 20
var sliderSequenceNumbers = [10, 20, 40, 60, 80, 100];
var slider = $("div#slider").slider({
    value: 1,  // Index 1 = 20 frames
    ...
});

// Change default to 40
var slider = $("div#slider").slider({
    value: 2,  // Index 2 = 40 frames
    ...
});
```

### Example 4: Add Logging

**File**: `ml_app/views.py`

```python
def predict_page(request):
    # Add at the beginning
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Starting prediction for video: {video_file}")

    # ... rest of code ...

    logger.info(f"Prediction complete: {output} with {confidence}%")
```

---

## 🎓 Learning Path

### For Complete Beginners:

1. **Week 1**: Learn Python basics
   - Variables, functions, loops
   - File handling
   - Basic libraries (os, time)

2. **Week 2**: Learn Web Basics
   - HTML structure
   - CSS styling
   - JavaScript basics

3. **Week 3**: Learn Django
   - Django tutorial (official docs)
   - URLs, Views, Templates
   - Forms and file uploads

4. **Week 4**: Learn AI Basics
   - What is machine learning?
   - Neural networks basics
   - PyTorch fundamentals

5. **Week 5**: Understand This Project
   - Read this tutorial
   - Run the project
   - Modify small things
   - Experiment!

### Recommended Resources:

**Python**:
- Python.org tutorial
- "Automate the Boring Stuff with Python" (free book)

**Django**:
- Official Django tutorial
- "Django for Beginners" book

**AI/ML**:
- Fast.ai course (free)
- PyTorch tutorials
- 3Blue1Brown neural network videos (YouTube)

**Computer Vision**:
- OpenCV tutorials
- Face recognition library docs

---

## 🔬 Advanced Topics

### How Deepfakes Are Created

1. **Face Swap**: Replace one person's face with another
2. **Face Reenactment**: Transfer expressions from one person to another
3. **Audio Synthesis**: Generate fake voice
4. **Full Body**: Manipulate entire body movements

### How This Model Detects Them

1. **Temporal Inconsistencies**:
   - Deepfakes often have frame-to-frame inconsistencies
   - LSTM catches these patterns

2. **Artifacts**:
   - Blending artifacts around face edges
   - Unnatural lighting
   - Weird eye movements

3. **Biological Signals**:
   - Abnormal blinking patterns
   - Unnatural facial muscle movements
   - Inconsistent skin texture

### Model Improvements You Could Make

1. **Data Augmentation**:
   - Train on more diverse data
   - Include different lighting conditions
   - Various face angles

2. **Architecture Changes**:
   - Try different backbone (EfficientNet, Vision Transformer)
   - Add attention mechanisms
   - Use 3D convolutions

3. **Ensemble Methods**:
   - Combine multiple models
   - Vote on final prediction
   - Improves accuracy

4. **Multi-Modal**:
   - Analyze audio too
   - Check for audio-visual sync
   - Detect voice deepfakes

---

## 🎯 Summary

### What You Learned:

1. **Project Structure**: How files are organized
2. **Django Framework**: How web apps work
3. **AI Model**: How deepfake detection works
4. **Data Flow**: How video becomes prediction
5. **Code Logic**: What each function does

### Key Takeaways:

- **Django** handles web requests and responses
- **PyTorch** runs the AI model
- **OpenCV** processes videos and images
- **Face Recognition** detects faces
- **LSTM** analyzes temporal patterns
- **Everything connects** through views.py

### Next Steps:

1. **Run the project** yourself
2. **Upload test videos** (real and fake)
3. **Modify the code** (change colors, text, etc.)
4. **Read Django docs** to understand more
5. **Learn PyTorch** to understand AI better
6. **Experiment** and have fun!

---

## 📚 Glossary

**API**: Application Programming Interface - how programs talk to each other

**Backend**: Server-side code (Python, Django)

**CNN**: Convolutional Neural Network - AI for images

**CUDA**: Nvidia's parallel computing platform for GPUs

**Dataset**: Collection of data for training/testing

**Django**: Python web framework

**Epoch**: One complete pass through training data

**Frontend**: Client-side code (HTML, CSS, JavaScript)

**GPU**: Graphics Processing Unit - fast parallel processor

**LSTM**: Long Short-Term Memory - AI for sequences

**Model**: Trained AI brain

**Normalization**: Scaling data to standard range

**PyTorch**: AI/ML framework by Facebook

**Session**: Temporary storage for user data

**Softmax**: Converts scores to probabilities

**Tensor**: Multi-dimensional array

**Training**: Teaching AI by showing examples

**URL**: Web address

**View**: Django function that handles requests

**Weights**: Learned parameters in AI model

---

## 🎉 Congratulations!

You now understand how a complete AI-powered web application works!

This knowledge applies to many other projects:
- Image classification apps
- Object detection systems
- Text analysis tools
- Recommendation systems
- And much more!

Keep learning, keep coding, and keep building amazing things! 🚀

---

**Questions?**
- Read Django documentation
- Check PyTorch tutorials
- Search Stack Overflow
- Experiment with the code!

**Remember**: Every expert was once a beginner. Keep practicing! 💪

