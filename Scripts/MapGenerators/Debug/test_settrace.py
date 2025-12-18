"""
Test if sys.settrace() works in UE5 Python environment
"""

import unreal
import sys

print("="*60)
print("Testing sys.settrace() in UE5")
print("="*60)

# Test 1: Basic print
print("[TEST 1] Basic print works")
unreal.log("[TEST 1] Basic unreal.log works")

# Test 2: sys.settrace setup
def trace_func(frame, event, arg):
    if event == 'line':
        line_no = frame.f_lineno
        print(f"[TRACE] Line {line_no}", flush=True)
        unreal.log(f"[TRACE] Line {line_no}")
    return trace_func

print("[TEST 2] Setting up sys.settrace...")
sys.settrace(trace_func)
print("[TEST 2] sys.settrace() called")

# Test 3: Execute some code that should be traced
print("[TEST 3] Executing traced code...")
x = 1
y = 2
z = x + y
print(f"[TEST 3] Result: {z}")

# Test 4: Disable tracing
sys.settrace(None)
print("[TEST 4] Tracing disabled")

print("="*60)
print("Test complete")
print("="*60)
