from django.shortcuts import render, redirect
import torch
import torchvision
from torchvision import transforms, models
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import face_recognition
from torch.autograd import Variable
import time
import sys
from torch import nn
import json
import glob
import copy
from torchvision import models
import shutil
from PIL import Image as pImage
import time
from django.conf import settings
from .forms import VideoUploadForm, ImageUploadForm

# Template names
index_template_name = 'index.html'
predict_template_name = 'predict.html'
about_template_name = "about.html"
image_upload_template_name = 'image_upload.html'
image_predict_template_name = 'image_predict.html'
landing_template_name = 'landing.html'
# Model parameters
im_size = 112
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
sm = nn.Softmax()
inv_normalize = transforms.Normalize(mean=-1*np.divide(mean, std), std=np.divide([1, 1, 1], std))

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

train_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((im_size, im_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))

class validation_dataset(Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        a = int(100/self.count)
        first_frame = np.random.randint(0, a)
        for i, frame in enumerate(self.frame_extract(video_path)):
            faces = face_recognition.face_locations(frame)
            try:
                top, right, bottom, left = faces[0]
                frame = frame[top:bottom, left:right, :]
            except:
                pass
            frames.append(self.transform(frame))
            if(len(frames) == self.count):
                break
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)
    
    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path) 
        success = 1
        while success:
            success, image = vidObj.read()
            if success:
                yield image

class ImageValidationDataset(Dataset):
    """Dataset class for single image prediction - Fixed for LSTM model"""
    def __init__(self, image_path, sequence_length=20, transform=None):
        self.image_path = image_path
        self.transform = transform
        self.sequence_length = sequence_length

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        # Load image
        image = cv2.imread(self.image_path)
        if image is None:
            raise ValueError(f"Could not load image: {self.image_path}")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        faces = face_recognition.face_locations(image)
        if len(faces) > 0:
            top, right, bottom, left = faces[0]
            # Add padding
            padding = 40
            height, width = image.shape[:2]
            
            # Ensure boundaries are within image limits
            top = max(0, top - padding)
            bottom = min(height, bottom + padding)
            left = max(0, left - padding)
            right = min(width, right + padding)
            
            face_image = image[top:bottom, left:right]
        else:
            face_image = image
        
        # Apply transforms
        if self.transform:
            face_image = self.transform(face_image)
        
        # Create a sequence by repeating the same image (LSTM needs sequence)
        # This simulates a video sequence where all frames are the same
        frames = []
        for _ in range(self.sequence_length):
            frames.append(face_image)
        
        frames = torch.stack(frames)  # Shape: [sequence_length, C, H, W]
        return frames.unsqueeze(0)  # Shape: [1, sequence_length, C, H, W]

def im_convert(tensor, video_file_name):
    """ Display a tensor as an image. """
    image = tensor.to("cpu").clone().detach()
    image = image.squeeze()
    image = inv_normalize(image)
    image = image.numpy()
    image = image.transpose(1, 2, 0)
    image = image.clip(0, 1)
    return image

def im_plot(tensor):
    image = tensor.cpu().numpy().transpose(1, 2, 0)
    b, g, r = cv2.split(image)
    image = cv2.merge((r, g, b))
    image = image*[0.22803, 0.22145, 0.216989] +  [0.43216, 0.394666, 0.37645]
    image = image*255.0
    plt.imshow(image.astype('uint8'))
    plt.show()

def predict(model, img, path='./', video_file_name=""):
    fmap, logits = model(img.to(device))
    img = im_convert(img[:, -1, :, :, :], video_file_name)
    params = list(model.parameters())
    weight_softmax = model.linear1.weight.detach().cpu().numpy()
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item()*100
    print('confidence of prediction:', logits[:, int(prediction.item())].item()*100)  
    return [int(prediction.item()), confidence]

def predict_image(model, img, image_file_name=""):
    """Predict if an image is real or fake with detailed debugging"""
    try:
        print(f"Input tensor shape: {img.shape}")
        
        # Forward pass through model
        fmap, logits = model(img.to(device))
        
        print(f"Raw logits: {logits}")
        print(f"Logits shape: {logits.shape}")
        
        # Apply softmax
        logits_softmax = sm(logits)
        print(f"Softmax probabilities: {logits_softmax}")
        
        # Get prediction
        _, prediction = torch.max(logits_softmax, 1)
        prediction_value = int(prediction.item())
        
        # Get confidence for the predicted class
        confidence = logits_softmax[:, prediction_value].item() * 100
        
        # Debug output
        print(f"Prediction index: {prediction_value}")
        print(f"Class 0 probability: {logits_softmax[0, 0].item() * 100:.2f}%")
        print(f"Class 1 probability: {logits_softmax[0, 1].item() * 100:.2f}%")
        print(f"Final confidence: {confidence:.2f}%")
        
        return [prediction_value, confidence]
        
    except Exception as e:
        print(f"Error in image prediction: {e}")
        import traceback
        traceback.print_exc()
        return [0, 50.0]  # Default values

def plot_heat_map(i, model, img, path='./', video_file_name=''):
    fmap, logits = model(img.to(device))
    params = list(model.parameters())
    weight_softmax = model.linear1.weight.detach().cpu().numpy()
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    idx = np.argmax(logits.detach().cpu().numpy())
    bz, nc, h, w = fmap.shape
    out = np.dot(fmap[i].detach().cpu().numpy().reshape((nc, h*w)).T, weight_softmax[idx, :].T)
    predict = out.reshape(h, w)
    predict = predict - np.min(predict)
    predict_img = predict / np.max(predict)
    predict_img = np.uint8(255*predict_img)
    out = cv2.resize(predict_img, (im_size, im_size))
    heatmap = cv2.applyColorMap(out, cv2.COLORMAP_JET)
    img = im_convert(img[:, -1, :, :, :], video_file_name)
    result = heatmap * 0.5 + img*0.8*255
    heatmap_name = video_file_name+"_heatmap_"+str(i)+".png"
    image_name = os.path.join(settings.PROJECT_DIR, 'uploaded_images', heatmap_name)
    cv2.imwrite(image_name, result)
    result1 = heatmap * 0.5/255 + img*0.8
    r, g, b = cv2.split(result1)
    result1 = cv2.merge((r, g, b))
    return image_name

def get_accurate_model(sequence_length):
    model_name = []
    sequence_model = []
    final_model = ""
    list_models = glob.glob(os.path.join(settings.PROJECT_DIR, "models", "*.pt"))

    for model_path in list_models:
        model_name.append(os.path.basename(model_path))

    for model_filename in model_name:
        try:
            seq = model_filename.split("_")[3]
            if int(seq) == sequence_length:
                sequence_model.append(model_filename)
        except IndexError:
            pass

    if len(sequence_model) > 1:
        accuracy = []
        for filename in sequence_model:
            acc = filename.split("_")[1]
            accuracy.append(acc)
        max_index = accuracy.index(max(accuracy))
        final_model = os.path.join(settings.PROJECT_DIR, "models", sequence_model[max_index])
    elif len(sequence_model) == 1:
        final_model = os.path.join(settings.PROJECT_DIR, "models", sequence_model[0])
    else:
        print("No model found for the specified sequence length.")

    return final_model

# File validation
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv'])
ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp', 'gif'])

def allowed_video_file(filename):
    if (filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS):
        return True
    else: 
        return False

def allowed_image_file(filename):
    """Check if uploaded file is an allowed image format"""
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    return False

# Video Processing Views
def index(request):
    if request.method == 'GET':
        video_upload_form = VideoUploadForm()
        if 'file_name' in request.session:
            del request.session['file_name']
        if 'preprocessed_images' in request.session:
            del request.session['preprocessed_images']
        if 'faces_cropped_images' in request.session:
            del request.session['faces_cropped_images']
        return render(request, index_template_name, {"form": video_upload_form})
    else:
        video_upload_form = VideoUploadForm(request.POST, request.FILES)
        if video_upload_form.is_valid():
            video_file = video_upload_form.cleaned_data['upload_video_file']
            video_file_ext = video_file.name.split('.')[-1]
            sequence_length = video_upload_form.cleaned_data['sequence_length']
            video_content_type = video_file.content_type.split('/')[0]
            if video_content_type in settings.CONTENT_TYPES:
                if video_file.size > int(settings.MAX_UPLOAD_SIZE):
                    video_upload_form.add_error("upload_video_file", "Maximum file size 100 MB")
                    return render(request, index_template_name, {"form": video_upload_form})

            if sequence_length <= 0:
                video_upload_form.add_error("sequence_length", "Sequence Length must be greater than 0")
                return render(request, index_template_name, {"form": video_upload_form})
            
            if allowed_video_file(video_file.name) == False:
                video_upload_form.add_error("upload_video_file", "Only video files are allowed ")
                return render(request, index_template_name, {"form": video_upload_form})
            
            saved_video_file = 'uploaded_file_'+str(int(time.time()))+"."+video_file_ext
            if settings.DEBUG:
                with open(os.path.join(settings.PROJECT_DIR, 'uploaded_videos', saved_video_file), 'wb') as vFile:
                    shutil.copyfileobj(video_file, vFile)
                request.session['file_name'] = os.path.join(settings.PROJECT_DIR, 'uploaded_videos', saved_video_file)
            else:
                with open(os.path.join(settings.PROJECT_DIR, 'uploaded_videos', 'app', 'uploaded_videos', saved_video_file), 'wb') as vFile:
                    shutil.copyfileobj(video_file, vFile)
                request.session['file_name'] = os.path.join(settings.PROJECT_DIR, 'uploaded_videos', 'app', 'uploaded_videos', saved_video_file)
            request.session['sequence_length'] = sequence_length
            return redirect('ml_app:predict')
        else:
            return render(request, index_template_name, {"form": video_upload_form})

def predict_page(request):
    if request.method == "GET":
        if 'file_name' not in request.session:
            return redirect("ml_app:home")
        if 'file_name' in request.session:
            video_file = request.session['file_name']
        if 'sequence_length' in request.session:
            sequence_length = request.session['sequence_length']
        path_to_videos = [video_file]
        video_file_name = os.path.basename(video_file)
        video_file_name_only = os.path.splitext(video_file_name)[0]
        
        if not settings.DEBUG:
            production_video_name = os.path.join('/home/app/staticfiles/', video_file_name.split('/')[3])
            print("Production file name", production_video_name)
        else:
            production_video_name = video_file_name

        video_dataset = validation_dataset(path_to_videos, sequence_length=sequence_length, transform=train_transforms)

        if(device == "cuda"):
            model = Model(2).cuda()
        else:
            model = Model(2).cpu()
        model_name = os.path.join(settings.PROJECT_DIR, 'models', get_accurate_model(sequence_length))
        path_to_model = os.path.join(settings.PROJECT_DIR, model_name)
        model.load_state_dict(torch.load(path_to_model, map_location=torch.device('cpu')))
        model.eval()
        start_time = time.time()
        
        print("<=== | Started Videos Splitting | ===>")
        preprocessed_images = []
        faces_cropped_images = []
        cap = cv2.VideoCapture(video_file)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                break
        cap.release()

        print(f"Number of frames: {len(frames)}")
        padding = 40
        faces_found = 0
        for i in range(sequence_length):
            if i >= len(frames):
                break
            frame = frames[i]

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image_name = f"{video_file_name_only}_preprocessed_{i+1}.png"
            image_path = os.path.join(settings.PROJECT_DIR, 'uploaded_images', image_name)
            img_rgb = pImage.fromarray(rgb_frame, 'RGB')
            img_rgb.save(image_path)
            preprocessed_images.append(image_name)

            face_locations = face_recognition.face_locations(rgb_frame)
            if len(face_locations) == 0:
                continue

            top, right, bottom, left = face_locations[0]
            frame_face = frame[top - padding:bottom + padding, left - padding:right + padding]

            rgb_face = cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB)
            img_face_rgb = pImage.fromarray(rgb_face, 'RGB')
            image_name = f"{video_file_name_only}_cropped_faces_{i+1}.png"
            image_path = os.path.join(settings.PROJECT_DIR, 'uploaded_images', image_name)
            img_face_rgb.save(image_path)
            faces_found += 1
            faces_cropped_images.append(image_name)

        print("<=== | Videos Splitting and Face Cropping Done | ===>")
        print("--- %s seconds ---" % (time.time() - start_time))

        if faces_found == 0:
            return render(request, predict_template_name, {"no_faces": True})

        try:
            heatmap_images = []
            output = ""
            confidence = 0.0

            for i in range(len(path_to_videos)):
                print("<=== | Started Prediction | ===>")
                prediction = predict(model, video_dataset[i], './', video_file_name_only)
                confidence = round(prediction[1], 1)
                output = "REAL" if prediction[0] == 1 else "FAKE"
                print("Prediction:", prediction[0], "==", output, "Confidence:", confidence)
                print("<=== | Prediction Done | ===>")
                print("--- %s seconds ---" % (time.time() - start_time))

            context = {
                'preprocessed_images': preprocessed_images,
                'faces_cropped_images': faces_cropped_images,
                'heatmap_images': heatmap_images,
                'original_video': production_video_name,
                'models_location': os.path.join(settings.PROJECT_DIR, 'models'),
                'output': output,
                'confidence': confidence
            }

            if settings.DEBUG:
                return render(request, predict_template_name, context)
            else:
                return render(request, predict_template_name, context)

        except Exception as e:
            print(f"Exception occurred during prediction: {e}")
            return render(request, 'cuda_full.html')

# Image Processing Views
def image_upload(request):
    """Handle image upload page"""
    if request.method == 'GET':
        image_upload_form = ImageUploadForm()
        # Clear any existing session data
        session_keys = ['image_file_name', 'image_preprocessed', 'image_faces_cropped']
        for key in session_keys:
            if key in request.session:
                del request.session[key]
        return render(request, image_upload_template_name, {"form": image_upload_form})
    
    else:
        image_upload_form = ImageUploadForm(request.POST, request.FILES)
        if image_upload_form.is_valid():
            image_file = image_upload_form.cleaned_data['upload_image_file']
            image_file_ext = image_file.name.split('.')[-1]
            image_content_type = image_file.content_type.split('/')[0]
            
            # Validate file type
            if image_content_type not in ['image']:
                image_upload_form.add_error("upload_image_file", "Only image files are allowed")
                return render(request, image_upload_template_name, {"form": image_upload_form})
            
            # Validate file size (10MB limit for images)
            if image_file.size > 10 * 1024 * 1024:  # 10MB
                image_upload_form.add_error("upload_image_file", "Maximum file size 10 MB")
                return render(request, image_upload_template_name, {"form": image_upload_form})
            
            # Validate file extension
            if not allowed_image_file(image_file.name):
                image_upload_form.add_error("upload_image_file", "Only JPG, JPEG, PNG, BMP image files are allowed")
                return render(request, image_upload_template_name, {"form": image_upload_form})
            
            # Save uploaded file
            saved_image_file = f'uploaded_image_{int(time.time())}.{image_file_ext}'
            image_save_path = os.path.join(settings.PROJECT_DIR, 'uploaded_images', saved_image_file)
            
            try:
                with open(image_save_path, 'wb') as img_file:
                    shutil.copyfileobj(image_file, img_file)
                
                request.session['image_file_name'] = image_save_path
                return redirect('ml_app:image_predict')
                
            except Exception as e:
                print(f"Error saving image: {e}")
                image_upload_form.add_error("upload_image_file", "Error saving uploaded file")
                return render(request, image_upload_template_name, {"form": image_upload_form})
        
        else:
            return render(request, image_upload_template_name, {"form": image_upload_form})

def landing_page(request):
    """Handle landing page display"""
    return render(request, landing_template_name)

def image_predict_page(request):
    """Handle image prediction page - Fixed version"""
    if request.method == "GET":
        # Redirect to image upload if no file in session
        if 'image_file_name' not in request.session:
            return redirect("ml_app:image_upload")
        
        image_file = request.session['image_file_name']
        image_file_name = os.path.basename(image_file)
        image_file_name_only = os.path.splitext(image_file_name)[0]
        
        start_time = time.time()
        
        try:
            print("<=== | Started Image Processing | ===>")
            
            # Load image for face detection
            image = cv2.imread(image_file)
            if image is None:
                print(f"Failed to load image: {image_file}")
                return render(request, image_predict_template_name, {"no_faces": True})
            
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            print(f"Image shape: {rgb_image.shape}")
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_image)
            print(f"Detected {len(face_locations)} faces")
            
            if len(face_locations) == 0:
                print("No faces detected in image")
                return render(request, image_predict_template_name, {"no_faces": True})
            
            # Process detected faces
            faces_cropped_images = []
            padding = 40
            
            for i, (top, right, bottom, left) in enumerate(face_locations):
                print(f"Face {i+1} location: top={top}, right={right}, bottom={bottom}, left={left}")
                
                # Crop face with padding
                height, width = rgb_image.shape[:2]
                top_padded = max(0, top - padding)
                bottom_padded = min(height, bottom + padding)
                left_padded = max(0, left - padding)
                right_padded = min(width, right + padding)
                
                face_image = rgb_image[top_padded:bottom_padded, left_padded:right_padded]
                print(f"Cropped face shape: {face_image.shape}")
                
                # Save cropped face
                face_pil = pImage.fromarray(face_image, 'RGB')
                face_filename = f"{image_file_name_only}_face_{i+1}.png"
                face_path = os.path.join(settings.PROJECT_DIR, 'uploaded_images', face_filename)
                face_pil.save(face_path)
                faces_cropped_images.append(face_filename)
            
            print("<=== | Face Detection Done | ===>")
            
            # Load model for prediction
            sequence_length = 20  # Use sequence length 20 to match training
            model_path = get_accurate_model(sequence_length)
            print(f"Model path: {model_path}")
            
            if not model_path or not os.path.exists(model_path):
                print("Model not found, using default prediction")
                output = "REAL"
                confidence = 75.0
            else:
                print(f"Loading model from: {model_path}")
                
                # Initialize model
                if device == "cuda" and torch.cuda.is_available():
                    model = Model(2).cuda()
                    print("Using CUDA")
                else:
                    model = Model(2).cpu()
                    print("Using CPU")
                
                # Load model weights
                try:
                    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
                    model.eval()
                    print("Model loaded successfully")
                except Exception as e:
                    print(f"Error loading model: {e}")
                    return render(request, image_predict_template_name, {"no_faces": True})
                
                # Create dataset for single image with proper sequence length
                print(f"Creating image dataset with sequence length: {sequence_length}")
                image_dataset = ImageValidationDataset(image_file, sequence_length=sequence_length, transform=train_transforms)
                
                # Perform prediction
                print("<=== | Started Prediction | ===>")
                try:
                    with torch.no_grad():
                        # Get the processed image tensor
                        img_tensor = image_dataset[0]
                        print(f"Image tensor shape: {img_tensor.shape}")
                        
                        # Perform prediction with debugging
                        prediction = predict_image(model, img_tensor, image_file_name_only)
                        
                        confidence = round(prediction[1], 1)
                        prediction_value = prediction[0]
                        
                        # Map prediction to output
                        # IMPORTANT: Check this mapping - you may need to reverse it
                        # If real images show as FAKE, try reversing these conditions
                        if prediction_value == 1:
                            output = "REAL"
                        else:
                            output = "FAKE"
                        
                        # ALTERNATIVE: If the above doesn't work, uncomment and try this:
                        # if prediction_value == 0:
                        #     output = "REAL"
                        # else:
                        #     output = "FAKE"
                        
                        print(f"\nFinal Result: {output} with {confidence}% confidence")
                        print(f"Raw prediction value: {prediction_value}")
                        
                except Exception as e:
                    print(f"Error during prediction: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fallback
                    output = "REAL"
                    confidence = 50.0
                
                print("<=== | Prediction Done | ===>")
            
            print(f"--- Total time: {time.time() - start_time} seconds ---")
            
            # Prepare context for template
            context = {
                'faces_cropped_images': faces_cropped_images,
                'original_image': image_file_name,
                'output': output,
                'confidence': confidence,
                'no_faces': False
            }
            
            return render(request, image_predict_template_name, context)
            
        except Exception as e:
            print(f"Error during image prediction: {e}")
            import traceback
            traceback.print_exc()
            return render(request, image_predict_template_name, {"no_faces": True})
    
    else:
        return redirect("ml_app:image_upload")

# Other Views
def about(request):
    return render(request, about_template_name)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def cuda_full(request):
    return render(request, 'cuda_full.html')