"""
Simple test script to verify UE5 Python execution
"""
import unreal

print("="*60)
print("TEST: Python script is executing!")
print("="*60)

unreal.log("TEST: unreal.log() is working!")
unreal.log_warning("TEST: unreal.log_warning() is working!")
unreal.log_error("TEST: unreal.log_error() is working!")

print("TEST: Script completed successfully")
