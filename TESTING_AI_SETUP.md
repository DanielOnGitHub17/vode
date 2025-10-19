# Testing the AI Interview System

## ✅ Checklist Before Testing

### 1. Dependencies Installed
```bash
/Users/danielosuoha/Documents/GitHub/vode/env/bin/pip install -r requirements.txt
```
Should have:
- `python-dotenv==1.0.0` ✅
- `google-generativeai==0.8.5` ✅
- `requests==2.31.0` ✅
- `Django==5.2.7` ✅

### 2. Environment Variables
Check `.env` file exists with:
```
GEMINI_API_KEY=AIzaSyCfXYmTJFQ8lI-dKMVcXmVNZDCO66qU9IY
ELEVENLABS_API_KEY=sk_8255f9aac656a1c9c16dfbab2ae93b2a1840965c94c78177
```

### 3. Django System Checks
```bash
cd /Users/danielosuoha/Documents/GitHub/vode
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python manage.py check
```

Expected: ✅ System check identified no issues

---

## 🧪 Testing Steps

### Step 1: Run Django System Check
```bash
cd /Users/danielosuoha/Documents/GitHub/vode
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python manage.py check
```

**Expected Output:**
```
System check identified no issues (0 silenced).
```

---

### Step 2: Start Django Server
```bash
cd /Users/danielosuoha/Documents/GitHub/vode
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python manage.py runserver
```

**Expected Output:**
```
Django version 5.2.7, using settings 'vode.settings'
Starting development server at http://127.0.0.1:8000/
```

---

### Step 3: Test the API Endpoint (in a new terminal)

#### Option A: Using curl (test with minimal data)
```bash
curl -X POST http://localhost:8000/interview/api/get-response/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def twoSum(nums, target):\n    # brute force\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []",
    "audio_transcript": "I am thinking of using a brute force approach with two nested loops",
    "interview_id": 1
  }' \
  --output response.mp3
```

#### Option B: Using Python (more detailed testing)
Create `test_interview_api.py`:
```python
import requests
import json

BASE_URL = "http://localhost:8000"
INTERVIEW_ID = 1

# Test data
payload = {
    "code": """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
    "audio_transcript": "I'm using brute force with two loops to find the pair",
    "interview_id": INTERVIEW_ID
}

print("📤 Sending request to /interview/api/get-response/...")
print(f"Code: {payload['code'][:50]}...")
print(f"Transcript: {payload['audio_transcript']}")
print(f"Interview ID: {payload['interview_id']}\n")

try:
    response = requests.post(
        f"{BASE_URL}/interview/api/get-response/",
        json=payload,
        timeout=60
    )
    
    print(f"✅ Response Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save audio response
        with open("ai_response.mp3", "wb") as f:
            f.write(response.content)
        print(f"✅ Audio response saved: ai_response.mp3 ({len(response.content)} bytes)")
        print("\n💡 Next: Play the audio file to hear AI coaching feedback")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:200])
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is Django running?")
except Exception as e:
    print(f"❌ Error: {e}")
```

Run it:
```bash
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python test_interview_api.py
```

---

## 🔍 What Each Test Validates

| Test | What It Checks | Success Indicator |
|------|---|---|
| **System Check** | Models, migrations, settings are valid | "0 issues" |
| **Server Start** | Django runs, .env loads correctly | Server listens on 8000 |
| **API Call** | Endpoint accepts request, returns audio | 200 status + audio bytes in response |
| **Gemini** | Can initialize context & call Gemini | Non-empty AI response |
| **Eleven Labs** | Can convert text to MP3 audio | Audio file generated |

---

## 🐛 Troubleshooting

### Server won't start (Exit Code 1)
```bash
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python manage.py check
```
This will show specific errors.

### "GEMINI_API_KEY not found"
- Verify `.env` file exists in `/Users/danielosuoha/Documents/GitHub/vode/.env`
- Check the key is not blank
- Restart Django server after adding .env

### "Connection refused" when calling API
- Ensure Django server is running (`python manage.py runserver`)
- Check it's listening on http://127.0.0.1:8000

### "No such interview_id: 1"
Create sample data first:
```bash
/Users/danielosuoha/Documents/GitHub/vode/env/bin/python manage.py shell
```
Then in Python shell:
```python
from recruit.models import Role, Round
from cand.models import Candidate
from interview.models import Interview

# Create role and round
role = Role.objects.first() or Role.objects.create(title="Backend Engineer")
round_obj = Round.objects.first() or Round.objects.create(
    role=role,
    round_number=1,
    total_rounds=3,
    difficulty="Medium"
)

# Create candidate
candidate = Candidate.objects.first() or Candidate.objects.create(user_id=1, name="Test Candidate")

# Create interview
interview = Interview.objects.create(
    candidate=candidate,
    round=round_obj,
)
print(f"Created interview with ID: {interview.id}")
```

### Audio plays but sounds robotic or wrong voice
- Check Eleven Labs voice_id in `elevenlabs_service.py` (default: "Rachel")
- Verify API key is correct

---

## 📊 Expected Flow

```
1. POST /interview/api/get-response/ (code + transcript + id)
   ↓
2. Django views.get_response() receives request
   ↓
3. orchestrator.agent_evaluate_submission() called
   ↓
4. Gemini analyzes code & transcript (using conversation history)
   ↓
5. Gemini returns coaching feedback text
   ↓
6. Eleven Labs converts text to MP3
   ↓
7. Binary audio returned (Content-Type: audio/mpeg)
   ↓
8. Frontend plays audio to candidate
```

---

## ✨ What Works If Tests Pass

✅ Gemini is receiving and processing submissions  
✅ Conversation history is maintained  
✅ Eleven Labs is converting text to audio  
✅ Django is serving binary audio correctly  
✅ API endpoint is accessible from frontend  

Now you're ready to build the **frontend** (code editor, audio recording, timer).

