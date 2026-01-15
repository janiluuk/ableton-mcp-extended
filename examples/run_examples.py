"""
Run All AI Audio Integration Examples

This script demonstrates all available integrations and their usage.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("""
╔════════════════════════════════════════════════════════════╗
║     AI Audio Integrations - Interactive Examples          ║
╚════════════════════════════════════════════════════════════╝
""")

print("Select an integration to explore:\n")
print("1. LocalAI - Text-to-Speech, Speech-to-Text, Audio Generation")
print("2. ComfyUI - Workflow-based Audio Generation")
print("3. UVR5 - Vocal/Instrumental Separation")
print("4. RVC - Voice Conversion")
print("5. Run all examples (sequential)")
print("0. Exit\n")

choice = input("Enter your choice (0-5): ").strip()

if choice == "1":
    print("\n" + "=" * 60)
    print("Running LocalAI Examples")
    print("=" * 60)
    import localai_examples
    
elif choice == "2":
    print("\n" + "=" * 60)
    print("Running ComfyUI Examples")
    print("=" * 60)
    import comfyui_examples
    
elif choice == "3":
    print("\n" + "=" * 60)
    print("Running UVR5 Examples")
    print("=" * 60)
    import uvr5_examples
    
elif choice == "4":
    print("\n" + "=" * 60)
    print("Running RVC Examples")
    print("=" * 60)
    import rvc_examples
    
elif choice == "5":
    print("\n" + "=" * 60)
    print("Running All Examples")
    print("=" * 60)
    
    print("\n### LocalAI ###")
    import localai_examples
    
    print("\n### ComfyUI ###")
    import comfyui_examples
    
    print("\n### UVR5 ###")
    import uvr5_examples
    
    print("\n### RVC ###")
    import rvc_examples
    
elif choice == "0":
    print("Exiting...")
    sys.exit(0)
    
else:
    print("Invalid choice. Exiting...")
    sys.exit(1)

print("\n" + "=" * 60)
print("Example run complete!")
print("\nNext steps:")
print("1. Check output files in your User Library folders")
print("2. Review USAGE_EXAMPLES.md for more detailed examples")
print("3. Try using the AI assistant with natural language commands")
print("=" * 60)
