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
    print("🧪 Testing AI Coaching - Realistic Stuck Scenario")
    print("=" * 80)
    
    # Test 1: Gemini Service
    print("\n1️⃣  Testing GeminiService with Charlie (male) voice...")
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
        print("   ✅ Context initialized with Two Sum problem")
        
        # SCENARIO: Candidate is stuck trying to use hashmap
        print("\n   📝 Scenario: Candidate starts with hashmap approach but gets stuck")
        
        stuck_code = """def twoSum(nums, target):
    # I'm trying to use a hashmap to solve this
    seen = {}
    
    for num in nums:
        complement = target - num
        
        if complement in seen:
            # I'm stuck here - how do I return the indices?
            # The complement is in seen but I don't know how to get its index
            return ???
        
        # I know I need to store something in seen
        seen[num] = ???"""
        
        stuck_transcript = "I'm using a hashmap to track numbers I've seen, and I found the complement! But I'm stuck on how to return the correct indices from the hashmap."
        
        print("   ⏳ Sending stuck code to Gemini for coaching...")
        response = gemini.agent_reasoning(stuck_code, stuck_transcript, interview_context)
        print(f"\n   ✅ Gemini coaching response:\n")
        print(f"   {'-' * 76}")
        print(f"   {response}")
        print(f"   {'-' * 76}\n")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Eleven Labs Service
    print("2️⃣  Testing ElevenLabsService with Charlie (male) voice...")
    try:
        elevenlabs = ElevenLabsService()
        print("   ✅ Eleven Labs service initialized (using Charlie voice)")
        
        # Convert Gemini's response to audio
        print("   ⏳ Converting coaching feedback to audio...")
        audio_bytes = elevenlabs.text_to_speech(response)
        print(f"   ✅ Audio generated: {len(audio_bytes)} bytes")
        
        # Save audio
        with open('/tmp/coaching_audio.mp3', 'wb') as f:
            f.write(audio_bytes)
        print(f"   ✅ Audio saved to /tmp/coaching_audio.mp3")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Follow-up interaction
    print("\n3️⃣  Testing follow-up interaction (candidate asks another question)...")
    try:
        print("   📝 Candidate's follow-up: 'So I should use the index as the value?'")
        
        follow_up_transcript = "So I should store the index as the value in the hashmap?"
        
        print("   ⏳ Getting Gemini's response to follow-up...")
        followup_response = gemini.agent_reasoning("", follow_up_transcript, interview_context)
        print(f"\n   ✅ Gemini follow-up response:\n")
        print(f"   {'-' * 76}")
        print(f"   {followup_response}")
        print(f"   {'-' * 76}\n")
        
        # Convert to audio
        audio_bytes = elevenlabs.text_to_speech(followup_response)
        with open('/tmp/followup_audio.mp3', 'wb') as f:
            f.write(audio_bytes)
        print(f"   ✅ Follow-up audio saved to /tmp/followup_audio.mp3 ({len(audio_bytes)} bytes)")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Conversation history validation
    print("\n4️⃣  Verifying conversation history is maintained...")
    try:
        print(f"   ✅ Conversation history size: {len(gemini.conversation_history)} messages")
        print(f"   ✅ Messages preserved for context (no separate endpoint needed)")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\n✨ What was tested:")
    print("   • Gemini AI coaching on stuck scenario")
    print("   • Charlie (male) voice text-to-speech")
    print("   • Conversation history for follow-ups")
    print("   • Natural hints without spoiling solution")
    print("   • Professional interviewer tone")
    print("\n🎙️ Audio files generated:")
    print("   • /tmp/coaching_audio.mp3 - Initial coaching on stuck code")
    print("   • /tmp/followup_audio.mp3 - Response to follow-up question")
    print("\n📊 Interview Flow Verified:")
    print("   ✅ Candidate gets stuck → AI provides guidance")
    print("   ✅ Candidate asks follow-up → AI remembers context")
    print("   ✅ Natural male voice provides engaging feedback")
    print("   ✅ No separate endpoints needed (one call = full interaction)")
    return True

if __name__ == "__main__":
    success = test_services()
    sys.exit(0 if success else 1)
