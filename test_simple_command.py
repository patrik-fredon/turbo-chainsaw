#!/usr/bin/env python3
"""
Simple test command to verify menu closing
"""
import time
import sys

print("Test command started!")
print(f"Arguments: {sys.argv}")

# Simulate some work
for i in range(3):
    print(f"Working... {i+1}/3")
    time.sleep(0.5)

print("Test command completed!")
sys.exit(0)