import socket
import os
import sys
import subprocess
import platform

def check_port(port=8000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"✅ Port {port} is open - something is already running there")
        else:
            print(f"ℹ️ Port {port} is closed/available")
        sock.close()
    except Exception as e:
        print(f"❌ Error checking port {port}: {e}")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"Error executing command: {e}"

def main():
    print("=" * 50)
    print("Network Diagnostics for Plant Care Assistant API")
    print("=" * 50)
    
    # Check if we can create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("✅ Socket creation successful")
        s.close()
    except socket.error as e:
        print(f"❌ Socket creation error: {e}")
    
    # Check localhost resolution
    try:
        localhost_ip = socket.gethostbyname('localhost')
        print(f"✅ 'localhost' resolves to: {localhost_ip}")
    except socket.gaierror:
        print("❌ Cannot resolve 'localhost'")
    
    # Check if port 8000 is available
    check_port(8000)
    
    # Check firewall status (platform specific)
    os_name = platform.system()
    if os_name == "Windows":
        print("\nWindows Firewall Status:")
        firewall_status = run_command("netsh advfirewall show allprofiles state")
        print(firewall_status)
    elif os_name == "Linux":
        print("\nLinux Firewall Status:")
        firewall_status = run_command("sudo ufw status")
        print(firewall_status)
    
    # Suggest solutions
    print("\n" + "=" * 50)
    print("Troubleshooting Tips:")
    print("=" * 50)
    print("1. Access the API using: http://localhost:8000 or http://127.0.0.1:8000")
    print("2. Make sure no firewall is blocking the connection")
    print("3. Try running the server with a different port: --port 8080")
    print("4. Check if uvicorn is installed correctly: pip install uvicorn[standard]")
    print("5. Make sure you're accessing from the same machine where the server is running")
    
    # How to run the API server
    print("\n" + "=" * 50)
    print("To start the API server properly:")
    print("=" * 50)
    print("python main.py")
    print("or")
    print("uvicorn main:app --host 127.0.0.1 --port 8000 --reload")

if __name__ == "__main__":
    main()
