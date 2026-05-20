# 🎯 Hands-On Exercises for Beginners

## 📚 Introduction

This document contains practical exercises to help you understand the code by actually modifying it. Start with Exercise 1 and work your way up!

---

## 🟢 Level 1: Basic Modifications (Easy)

### Exercise 1.1: Change the Website Title

**Goal**: Change the title on the landing page

**File**: `ml_app/templates/landing.html`

**Find this line** (around line 232):
```html
<h1 class="hero-title">True Vision - DeepFake Detection</h1>
```

**Change to**:
```html
<h1 class="hero-title">My Awesome DeepFake Detector</h1>
```

**Test**: Visit http://localhost:8000/ and see your new title!

---

### Exercise 1.2: Change Button Colors

**Goal**: Make the upload button a different color

**File**: `ml_app/templates/index.html`

**Find this CSS** (around line 257):
```css
.submit-btn {
    background: var(--primary-gradient);
    ...
}
```

**Change to**:
```css
.submit-btn {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    ...
}
```

**Test**: The button should now be red/orange!

---

### Exercise 1.3: Add a Welcome Message

**Goal**: Add a custom message on the upload page

**File**: `ml_app/templates/index.html`

**Find** (around line 415):
```html
<h1 class="logo-text">DeepFake Detection</h1>
```

**Add below it**:
```html
<p style="text-align: center; color: #00e5cc; font-size: 1.2rem;">
    Welcome! Upload your video to check if it's real or fake.
</p>
```

**Test**: You should see your welcome message!

---

### Exercise 1.4: Change Maximum File Size

**Goal**: Allow larger video uploads

**File**: `project_settings/settings.py`

**Find** (line 108):
```python
MAX_UPLOAD_SIZE = "104857600"  # 100 MB
```

**Change to**:
```python
MAX_UPLOAD_SIZE = "209715200"  # 200 MB
```

**Test**: Try uploading a larger video!

---

## 🟡 Level 2: Functional Changes (Medium)

### Exercise 2.1: Add a New Allowed Video Format

**Goal**: Allow .mov files to be uploaded

**File**: `ml_app/views.py`

**Find** (line 280):
```python
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv'])
```

**Change to**:
```python
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv', 'mov'])
```

**Test**: Try uploading a .mov file!

---

### Exercise 2.2: Add Logging to Track Predictions

**Goal**: Print information about each prediction

**File**: `ml_app/views.py`

**Find the `predict` function** (around line 176):
```python
def predict(model, img, path='./', video_file_name=""):
    fmap, logits = model(img.to(device))
    # ... rest of code
```

**Add at the beginning**:
```python
def predict(model, img, path='./', video_file_name=""):
    import datetime
    print(f"\n{'='*50}")
    print(f"PREDICTION STARTED: {datetime.datetime.now()}")
    print(f"Video file: {video_file_name}")
    print(f"{'='*50}\n")
    
    fmap, logits = model(img.to(device))
    # ... rest of code
```

**Add before return**:
```python
    print(f"\n{'='*50}")
    print(f"PREDICTION COMPLETE")
    print(f"Result: {'REAL' if prediction.item() == 1 else 'FAKE'}")
    print(f"Confidence: {confidence:.2f}%")
    print(f"{'='*50}\n")
    
    return [int(prediction.item()), confidence]
```

**Test**: Check the terminal output when making predictions!

---

### Exercise 2.3: Change Default Sequence Length

**Goal**: Make the default sequence length 40 instead of 20

**File**: `ml_app/templates/index.html`

**Find** (around line 492):
```javascript
var slider = $("div#slider").slider({
    value: 1,  // This is index 1 = 20 frames
    ...
});
```

**Change to**:
```javascript
var slider = $("div#slider").slider({
    value: 2,  // This is index 2 = 40 frames
    ...
});
```

**Also update the display** (around line 458):
```html
<span id="slider-value">20</span>
```

**Change to**:
```html
<span id="slider-value">40</span>
```

**Test**: The slider should now default to 40!

---

### Exercise 2.4: Add a Processing Time Display

**Goal**: Show how long the prediction took

**File**: `ml_app/views.py`

**In `predict_page` function**, find (around line 368):
```python
start_time = time.time()
```

**Before rendering the template** (around line 434):
```python
context = {
    'preprocessed_images': preprocessed_images,
    'faces_cropped_images': faces_cropped_images,
    'heatmap_images': heatmap_images,
    'original_video': production_video_name,
    'models_location': os.path.join(settings.PROJECT_DIR, 'models'),
    'output': output,
    'confidence': confidence
}
```

**Add processing time**:
```python
processing_time = round(time.time() - start_time, 2)

context = {
    'preprocessed_images': preprocessed_images,
    'faces_cropped_images': faces_cropped_images,
    'heatmap_images': heatmap_images,
    'original_video': production_video_name,
    'models_location': os.path.join(settings.PROJECT_DIR, 'models'),
    'output': output,
    'confidence': confidence,
    'processing_time': processing_time  # Add this line
}
```

**File**: `ml_app/templates/predict.html`

**Add after the result** (around line 48):
```html
<h4 class="mx-auto">Result: <span style="color:green">{{output}}</span>
    <img src="{% static 'images/thumpup.png'%}" alt="real" height="100px" width=auto>
</h4>
<p style="text-align: center; color: #666;">
    Processing time: {{processing_time}} seconds
</p>
```

**Test**: You'll see how long the prediction took!

---

## 🔴 Level 3: Advanced Modifications (Hard)

### Exercise 3.1: Add a Prediction History

**Goal**: Keep track of all predictions made

**File**: `ml_app/views.py`

**Add at the top** (after imports):
```python
# Global list to store prediction history
prediction_history = []
```

**In `predict_page` function**, before rendering:
```python
# Add to history
prediction_entry = {
    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'filename': video_file_name,
    'result': output,
    'confidence': confidence
}
prediction_history.append(prediction_entry)

# Keep only last 10 predictions
if len(prediction_history) > 10:
    prediction_history.pop(0)

context = {
    # ... existing context ...
    'history': prediction_history  # Add this
}
```

**File**: `ml_app/templates/predict.html`

**Add at the bottom**:
```html
<div class="container mt-5">
    <h3>Recent Predictions</h3>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Time</th>
                <th>File</th>
                <th>Result</th>
                <th>Confidence</th>
            </tr>
        </thead>
        <tbody>
            {% for entry in history %}
            <tr>
                <td>{{entry.timestamp}}</td>
                <td>{{entry.filename}}</td>
                <td>{{entry.result}}</td>
                <td>{{entry.confidence}}%</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

**Test**: Make multiple predictions and see the history!

---

### Exercise 3.2: Add Email Notification (Advanced)

**Goal**: Send an email when a fake video is detected

**File**: `project_settings/settings.py`

**Add email configuration**:
```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**File**: `ml_app/views.py`

**Add import**:
```python
from django.core.mail import send_mail
from django.conf import settings
```

**In `predict_page`, after prediction**:
```python
# Send email if fake detected
if output == "FAKE":
    subject = f"⚠️ Fake Video Detected!"
    message = f"""
    A fake video has been detected!
    
    Filename: {video_file_name}
    Confidence: {confidence}%
    Time: {datetime.datetime.now()}
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['recipient@example.com'],
            fail_silently=True,
        )
        print("Email notification sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")
```

**Note**: You need to set up Gmail app password for this to work!

---

### Exercise 3.3: Create a Statistics Dashboard

**Goal**: Show statistics about all predictions

**File**: `ml_app/views.py`

**Add a new view function**:
```python
def statistics(request):
    """Show prediction statistics"""
    
    # Calculate statistics
    total_predictions = len(prediction_history)
    
    if total_predictions > 0:
        fake_count = sum(1 for p in prediction_history if p['result'] == 'FAKE')
        real_count = total_predictions - fake_count
        avg_confidence = sum(p['confidence'] for p in prediction_history) / total_predictions
    else:
        fake_count = real_count = avg_confidence = 0
    
    context = {
        'total': total_predictions,
        'fake_count': fake_count,
        'real_count': real_count,
        'avg_confidence': round(avg_confidence, 2),
        'history': prediction_history
    }
    
    return render(request, 'statistics.html', context)
```

**File**: `ml_app/urls.py`

**Add URL pattern**:
```python
from .views import statistics

urlpatterns = [
    # ... existing patterns ...
    path('statistics/', statistics, name='statistics'),
]
```

**File**: `ml_app/templates/statistics.html` (create new file):
```html
{% extends 'base.html' %}
{% block content %}

<div class="container mt-5">
    <h1 class="text-center mb-4">Prediction Statistics</h1>
    
    <div class="row">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total Predictions</h5>
                    <h2>{{total}}</h2>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Real Videos</h5>
                    <h2 style="color: green;">{{real_count}}</h2>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Fake Videos</h5>
                    <h2 style="color: red;">{{fake_count}}</h2>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Avg Confidence</h5>
                    <h2>{{avg_confidence}}%</h2>
                </div>
            </div>
        </div>
    </div>
</div>

{% endblock %}
```

**Test**: Visit http://localhost:8000/statistics/

---

## 🎓 Challenge Projects

### Challenge 1: Add User Authentication
- Allow users to create accounts
- Track predictions per user
- Show personalized history

### Challenge 2: Batch Processing
- Allow uploading multiple videos at once
- Process them in parallel
- Show results in a table

### Challenge 3: API Endpoint
- Create a REST API
- Accept video uploads via API
- Return JSON results

### Challenge 4: Real-time Processing
- Use WebSockets
- Show progress bar during processing
- Update results in real-time

---

## ✅ Exercise Checklist

Track your progress:

- [ ] Exercise 1.1: Change website title
- [ ] Exercise 1.2: Change button colors
- [ ] Exercise 1.3: Add welcome message
- [ ] Exercise 1.4: Change max file size
- [ ] Exercise 2.1: Add new video format
- [ ] Exercise 2.2: Add logging
- [ ] Exercise 2.3: Change default sequence
- [ ] Exercise 2.4: Add processing time
- [ ] Exercise 3.1: Add prediction history
- [ ] Exercise 3.2: Email notifications
- [ ] Exercise 3.3: Statistics dashboard

---

## 💡 Tips for Success

1. **Always backup** before making changes
2. **Test after each change** - don't make multiple changes at once
3. **Read error messages** carefully - they tell you what's wrong
4. **Use print statements** to debug
5. **Google is your friend** - search for errors
6. **Ask for help** when stuck

---

## 🐛 Debugging Tips

### If something breaks:

1. **Check the terminal** for error messages
2. **Restart the server**: Ctrl+C, then `python manage.py runserver`
3. **Clear browser cache**: Ctrl+Shift+R
4. **Check file paths** - are they correct?
5. **Verify indentation** - Python is sensitive to spaces!

### Common Errors:

**TemplateDoesNotExist**: Check file name and location
**NameError**: Variable not defined - check spelling
**IndentationError**: Fix spacing/tabs
**ImportError**: Module not installed - run `pip install`

---

## 🎉 Congratulations!

By completing these exercises, you've learned:
- How to modify HTML templates
- How to change CSS styles
- How to modify Python code
- How to add new features
- How to debug issues

Keep experimenting and building! 🚀

