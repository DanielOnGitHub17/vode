#!/usr/bin/env python
"""
Improved test of AI services with realistic stuck scenario.
Tests Gemini and Eleven Labs with a candidate struggling on hashmap approach.
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
    print("=" * 80)
    print("🧪 Testing AI Coaching - Single Call")
    print("=" * 80)
    
    # Initialize services once
    try:
        gemini = GeminiService()
        elevenlabs = ElevenLabsService()
        print("\n✅ Services initialized")
        
        interview_context = {
            'role': 'Backend Engineer',
            'round': 1,
            'total_rounds': 3,
            'difficulty': 'medium'
        }
        
        gemini.initialize_context(MOCK_QUESTION, interview_context)
        print("✅ Gemini context initialized")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False
    
    # ========== SINGLE CALL: Candidate submits stuck code ==========
    print("\n" + "=" * 80)
    print("Single AI Service Call")
    print("=" * 80)
    
    try:
        stuck_code = """def twoSum(nums, target):
    # I'm trying to use a hashmap to solve this
    seen = {}
    
    for num in nums:
        complement = target - num
        
        if complement in seen:
            # I'm stuck here - how do I return the indices?
            return ???
        
        seen[num] = ???"""
        
        transcript = "I'm using a hashmap to track numbers I've seen. I found the complement but I'm stuck on getting the indices."
        
        print(f"\n📝 Code submission:\n{stuck_code[:100]}...")
        print(f"\n🎤 Candidate says: \"{transcript}\"")
        
        print("\n⏳ Getting AI response...")
        response = gemini.agent_reasoning(stuck_code, transcript, interview_context)
        
        print(f"\n✅ AI Response:\n")
        print(f"{'-' * 76}")
        print(f"{response}")
        print(f"{'-' * 76}\n")
        
        # Convert to audio
        print("🎙️ Converting to audio...")
        audio = elevenlabs.text_to_speech(response)
        with open('/tmp/response.mp3', 'wb') as f:
            f.write(audio)
        print(f"✅ Audio saved: /tmp/response.mp3 ({len(audio)} bytes)")
        
    except Exception as e:
        print(f"❌ Error in AI call: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ TEST PASSED!")
    print("=" * 80)
    print("\n✨ Single AI Service Call Verified:")
    print("   ✅ Gemini generates coaching feedback")
    print("   ✅ ElevenLabs converts response to audio")
    print("\n🎙️ Audio file generated:")
    print("   • /tmp/response.mp3 - AI coaching response")
    return True

if __name__ == "__main__":
    success = test_services()
    sys.exit(0 if success else 1)
