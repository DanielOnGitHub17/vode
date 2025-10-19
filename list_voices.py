#!/usr/bin/env python
"""
Get available Eleven Labs voices
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vode.settings')
sys.path.insert(0, '/Users/danielosuoha/Documents/GitHub/vode')
django.setup()

from interview.services.elevenlabs_service import ElevenLabsService

try:
    elevenlabs = ElevenLabsService()
    voices = elevenlabs.get_available_voices()
    
    print("Available Eleven Labs Voices:")
    print("=" * 60)
    for voice in voices.get('voices', []):
        print(f"  • {voice['name']:20} (ID: {voice['voice_id']})")
    
except Exception as e:
    print(f"Error: {e}")
