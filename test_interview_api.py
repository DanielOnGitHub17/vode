#!/usr/bin/env python
"""
Test script for the Interview AI API endpoint.
Run: python test_interview_api.py
"""

import requests
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"
INTERVIEW_ID = 1

def test_api():
    """Test the /interview/api/get-response/ endpoint"""
    
    # Test data: Two Sum brute force solution
    payload = {
        "code": """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
        "audio_transcript": "I'm using brute force with two loops to find the pair that sums to target",
        "interview_id": INTERVIEW_ID
    }
    
    print("=" * 70)
    print("🧪 Testing Interview AI API Endpoint")
    print("=" * 70)
    print(f"\n📤 Request Details:")
    print(f"   URL: POST {BASE_URL}/interview/api/get-response/")
    print(f"   Interview ID: {payload['interview_id']}")
    print(f"   Code snippet: {payload['code'][:40]}...")
    print(f"   Transcript: {payload['audio_transcript']}\n")
    
    try:
        print("⏳ Sending request (this may take 10-30 seconds)...")
        response = requests.post(
            f"{BASE_URL}/interview/api/get-response/",
            json=payload,
            timeout=120  
        )
        
        print(f"\n✅ Response received!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   Content-Length: {len(response.content)} bytes\n")
        
        if response.status_code == 200:
            # Save audio response
            output_file = Path("ai_response.mp3")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            print(f"✅ SUCCESS! Audio response saved: {output_file}")
            print(f"   File size: {len(response.content)} bytes")
            print(f"\n💡 Next steps:")
            print(f"   1. Play the audio: open ai_response.mp3")
            print(f"   2. You should hear AI coaching feedback about your code")
            print(f"   3. Try different code submissions and transcripts")
            return True
            
        elif response.status_code == 404:
            print(f"❌ Interview ID {INTERVIEW_ID} not found")
            print(f"   Create sample data first (see TESTING_AI_SETUP.md)")
            return False
            
        elif response.status_code == 400:
            print(f"❌ Bad Request")
            print(f"   Response: {response.text}")
            return False
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {BASE_URL}")
        print(f"   Is Django running? Start it with:")
        print(f"   python manage.py runserver")
        return False
        
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out (120 seconds)")
        print(f"   API is taking too long. Check Gemini/Eleven Labs status")
        return False
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
