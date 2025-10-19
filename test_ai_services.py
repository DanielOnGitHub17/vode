#!/usr/bin/env python
"""
Direct test of AI services without running the server.
Tests Gemini and Eleven Labs integration.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vode.settings')
sys.path.insert(0, '/Users/danielosuoha/Documents/GitHub/vode')
django.setup()

from interview.services.gemini_service import GeminiService
from interview.services.elevenlabs_service import ElevenLabsService
from interview.mocks import MOCK_QUESTION

def test_services():
    print("=" * 70)
    print("🧪 Testing AI Services (Gemini + Eleven Labs)")
    print("=" * 70)
    
    # Test 1: Gemini Service
    print("\n1️⃣  Testing GeminiService...")
    try:
        gemini = GeminiService()
        print("   ✅ Gemini service initialized")
        
        # Initialize context
        interview_context = {
            'role': 'Backend Engineer',
            'round': 1,
            'total_rounds': 3,
            'difficulty': 'medium'
        }
        
        gemini.initialize_context(MOCK_QUESTION, interview_context)
        print("   ✅ Context initialized with problem statement")
        
        # Test agent reasoning
        print("   ⏳ Testing AI reasoning (calling Gemini API)...")
        code = """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []"""
        
        transcript = "I'm using a brute force approach with two nested loops"
        
        response = gemini.agent_reasoning(code, transcript, interview_context)
        print(f"   ✅ Gemini responded: {response[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Eleven Labs Service
    print("\n2️⃣  Testing ElevenLabsService...")
    try:
        elevenlabs = ElevenLabsService()
        print("   ✅ Eleven Labs service initialized")
        
        # Test text-to-speech
        print("   ⏳ Testing text-to-speech conversion...")
        test_text = "Your approach looks good! Can you think about the time and space complexity?"
        
        # Using voice ID "21m00Tcm4TlvDq8ikWAM" (Rachel)
        audio_bytes = elevenlabs.text_to_speech(test_text, voice_id="21m00Tcm4TlvDq8ikWAM")
        print(f"   ✅ Audio generated: {len(audio_bytes)} bytes")
        
        # Save audio
        with open('/tmp/test_audio.mp3', 'wb') as f:
            f.write(audio_bytes)
        print(f"   ✅ Audio saved to /tmp/test_audio.mp3")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Full Flow
    print("\n3️⃣  Testing full AI coaching flow...")
    try:
        print("   ⏳ Simulating candidate submission...")
        
        # Get Gemini response
        response = gemini.agent_reasoning(code, transcript, interview_context)
        print(f"   ✅ AI coaching feedback generated")
        
        # Convert to audio
        audio = elevenlabs.text_to_speech(response, voice_id="21m00Tcm4TlvDq8ikWAM")
        print(f"   ✅ Converted to audio: {len(audio)} bytes")
        print(f"\n   📝 AI Feedback (first 200 chars):")
        print(f"      {response[:200]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n✨ Services are working correctly:")
    print("   • Gemini API key is valid and responding")
    print("   • Eleven Labs API key is valid and converting text to audio")
    print("   • Full AI coaching flow is operational")
    print("\nNext: Start the server and test the HTTP endpoint:")
    print("  python manage.py runserver")
    return True

if __name__ == "__main__":
    success = test_services()
    sys.exit(0 if success else 1)
