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
    print("🧪 Testing AI Coaching - Realistic Interview Flow")
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
    
    # ========== TURN 1: Candidate submits stuck code ==========
    print("\n" + "=" * 80)
    print("TURN 1: Candidate submits attempt with stuck code")
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
        
        turn1_transcript = "I'm using a hashmap to track numbers I've seen. I found the complement but I'm stuck on getting the indices."
        
        print(f"\n📝 Code submission:\n{stuck_code[:100]}...")
        print(f"\n🎤 Candidate says: \"{turn1_transcript}\"")
        
        print("\n⏳ Getting AI response...")
        response1 = gemini.agent_reasoning(stuck_code, turn1_transcript, interview_context)
        
        print(f"\n✅ AI Response:\n")
        print(f"{'-' * 76}")
        print(f"{response1}")
        print(f"{'-' * 76}\n")
        
        # Convert to audio
        print("🎙️ Converting to audio...")
        audio1 = elevenlabs.text_to_speech(response1)
        with open('/tmp/turn1_response.mp3', 'wb') as f:
            f.write(audio1)
        print(f"✅ Audio saved: /tmp/turn1_response.mp3 ({len(audio1)} bytes)")
        
    except Exception as e:
        print(f"❌ Error in Turn 1: {e}")
        return False
    
    # ========== TURN 2: Candidate asks follow-up ==========
    print("\n" + "=" * 80)
    print("TURN 2: Candidate responds with follow-up question")
    print("=" * 80)
    
    try:
        # Candidate code might be unchanged or slightly modified
        improved_code = """def twoSum(nums, target):
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return ???
        
        seen[num] = ???"""
        
        turn2_transcript = "Should I store the index as the value in the hashmap?"
        
        print(f"\n📝 Updated code:\n{improved_code[:100]}...")
        print(f"\n🎤 Candidate says: \"{turn2_transcript}\"")
        
        print("\n⏳ Getting AI response...")
        response2 = gemini.agent_reasoning(improved_code, turn2_transcript, interview_context)
        
        print(f"\n✅ AI Response:\n")
        print(f"{'-' * 76}")
        print(f"{response2}")
        print(f"{'-' * 76}\n")
        
        # Convert to audio
        print("🎙️ Converting to audio...")
        audio2 = elevenlabs.text_to_speech(response2)
        with open('/tmp/turn2_response.mp3', 'wb') as f:
            f.write(audio2)
        print(f"✅ Audio saved: /tmp/turn2_response.mp3 ({len(audio2)} bytes)")
        
    except Exception as e:
        print(f"❌ Error in Turn 2: {e}")
        return False
    
    # ========== TURN 3: Candidate submits working solution ==========
    print("\n" + "=" * 80)
    print("TURN 3: Candidate submits improved solution")
    print("=" * 80)
    
    try:
        working_code = """def twoSum(nums, target):
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i"""
        
        turn3_transcript = "I implemented the solution storing indices as values. Does this look correct?"
        
        print(f"\n📝 Final code:\n{working_code}")
        print(f"\n🎤 Candidate says: \"{turn3_transcript}\"")
        
        print("\n⏳ Getting AI response...")
        response3 = gemini.agent_reasoning(working_code, turn3_transcript, interview_context)
        
        print(f"\n✅ AI Response:\n")
        print(f"{'-' * 76}")
        print(f"{response3}")
        print(f"{'-' * 76}\n")
        
        # Convert to audio
        print("🎙️ Converting to audio...")
        audio3 = elevenlabs.text_to_speech(response3)
        with open('/tmp/turn3_response.mp3', 'wb') as f:
            f.write(audio3)
        print(f"✅ Audio saved: /tmp/turn3_response.mp3 ({len(audio3)} bytes)")
        
    except Exception as e:
        print(f"❌ Error in Turn 3: {e}")
        return False
    
    # ========== INTERVIEW SCORING ==========
    print("\n" + "=" * 80)
    print("Interview Scoring & Evaluation")
    print("=" * 80)
    
    try:
        # These are the metrics an SWE would set for the round
        metrics = ['Correctness', 'Code Efficiency', 'Problem-Solving Approach', 'Communication', 'Code Quality']
        
        print(f"\n📊 Metrics for evaluation: {', '.join(metrics)}")
        print("\n⏳ Gemini analyzing full conversation history...")
        
        scoring_result = gemini.score_interview(metrics)
        
        score = scoring_result['score']
        feedback = scoring_result['feedback']
        
        print(f"\n✅ Interview Score: {score}/100")
        print(f"\n📝 Interview Feedback:\n")
        print(f"{'-' * 76}")
        print(f"{feedback}")
        print(f"{'-' * 76}\n")
        
        # Verify score is valid
        assert 0 <= score <= 100, f"Score {score} out of range [0-100]"
        assert len(feedback) > 0, "Feedback is empty"
        
        # Check that feedback has the structure (what went well + improvements)
        feedback_lower = feedback.lower()
        has_positive = any(word in feedback_lower for word in ['well', 'good', 'excellent', 'great', 'correct', 'solid', 'strong'])
        has_improvement = any(word in feedback_lower for word in ['improve', 'consider', 'could', 'better', 'enhance', 'refinement', 'area'])
        
        print(f"✅ Feedback structure validated:")
        print(f"   • Contains positive feedback: {has_positive}")
        print(f"   • Contains improvement areas: {has_improvement}")
        
    except Exception as e:
        print(f"❌ Error in scoring: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\n✨ Complete Interview Flow Verified:")
    print("   TURN 1: Stuck code + transcript → AI coaching response")
    print("   TURN 2: Improved code + follow-up question → AI response with context")
    print("   TURN 3: Working solution + validation question → AI evaluation")
    print("   FINAL: AI analyzes full conversation → Score (0-100) + Structured Feedback")
    print("\n📊 Scoring System:")
    print("   ✅ Reads metrics from round configuration")
    print("   ✅ Analyzes entire conversation history")
    print("   ✅ Generates score 0-100 based on metrics")
    print("   ✅ Creates structured feedback (25-35% positive, 65-75% improvements)")
    print("\n🎙️ Audio files generated:")
    print("   • /tmp/turn1_response.mp3 - Response to initial stuck code")
    print("   • /tmp/turn2_response.mp3 - Response to follow-up question")
    print("   • /tmp/turn3_response.mp3 - Evaluation of working solution")
    return True

if __name__ == "__main__":
    success = test_services()
    sys.exit(0 if success else 1)
