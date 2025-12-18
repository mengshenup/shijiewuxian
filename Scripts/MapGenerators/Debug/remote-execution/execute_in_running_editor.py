"""
Execute map generation in already-running UE5 Editor
This script uses UE5's remote execution feature to send Python commands to the running editor.
"""

import socket
import json
import sys


def send_command_to_editor(command, host='127.0.0.1', port=6776):
    """
    Send Python command to running UE5 Editor via remote execution
    
    Args:
        command: Python command string to execute
        host: Editor host (default: localhost)
        port: Remote execution port (default: 6776)
    
    Returns:
        Response from editor
    """
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        
        print(f"Connecting to editor at {host}:{port}...")
        sock.connect((host, port))
        print("✓ Connected to editor")
        
        # Prepare command packet
        packet = {
            'command': 'exec',
            'data': command
        }
        
        # Send command
        message = json.dumps(packet) + '\n'
        sock.sendall(message.encode('utf-8'))
        print("✓ Command sent")
        
        # Receive response
        response = sock.recv(4096).decode('utf-8')
        sock.close()
        
        print("✓ Response received")
        return response
        
    except socket.timeout:
        print("✗ Connection timeout - is Remote Execution enabled in editor?")
        return None
    except ConnectionRefusedError:
        print("✗ Connection refused - is Remote Execution enabled in editor?")
        print("\nTo enable Remote Execution:")
        print("1. In UE5 Editor: Edit → Project Settings")
        print("2. Search for 'Python'")
        print("3. Enable 'Enable Remote Execution'")
        print("4. Restart editor")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None


def generate_map_in_running_editor():
    """Generate map in the currently running editor"""
    
    print("\n" + "="*60)
    print("Execute Map Generation in Running Editor")
    print("="*60 + "\n")
    
    # Python command to execute in editor
    command = """
import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')
import generate_cosmos_002_training_world
result = generate_cosmos_002_training_world.main()
print(f"Map generation result: {result}")
"""
    
    print("Sending map generation command to editor...")
    print("-" * 60)
    
    response = send_command_to_editor(command)
    
    if response:
        print("-" * 60)
        print("Editor Response:")
        print(response)
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("Failed to communicate with editor")
        print("="*60)
        print("\nAlternative: Use editor Python console manually")
        print("1. In editor: Window → Developer Tools → Output Log")
        print("2. Switch to Python tab")
        print("3. Execute:")
        print(command)
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(generate_map_in_running_editor())
