#!/usr/bin/env python3
"""
Flightradar24 API Setup Assistant
=================================

This script helps you set up and test your FR24 API client.
"""

import os
import sys

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = ['requests', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_environment():
    """Help user set up environment variables"""
    print("\n🔧 Setting up environment...")
    
    # Check if token is already set
    token = os.getenv('FR24_API_TOKEN')
    if token:
        print(f"   ✅ FR24_API_TOKEN is set (length: {len(token)})")
        return True
    
    print("   ⚠️  FR24_API_TOKEN not found")
    print("\n💡 To set up your API token:")
    print("1. Subscribe to FR24 API: https://www.flightradar24.com/commercial-services/api")
    print("2. Get your API token from the dashboard")
    print("3. Set the environment variable:")
    print("   export FR24_API_TOKEN=your_token_here")
    print("   OR create a .env file with: FR24_API_TOKEN=your_token_here")
    
    # Offer to create .env file
    create_env = input("\n❓ Would you like to create a .env file now? (y/n): ").lower().strip()
    if create_env == 'y':
        token = input("🔑 Enter your FR24 API token: ").strip()
        if token:
            with open('.env', 'w') as f:
                f.write(f"FR24_API_TOKEN={token}\n")
            print("   ✅ .env file created successfully")
            return True
    
    return False

def test_client():
    """Test the FR24 client"""
    print("\n🧪 Testing FR24 client...")
    
    try:
        from flightradar24_api_client import FlightRadar24Client
        print("   ✅ Client import successful")
        
        # Try to initialize (will fail without token, but that's ok)
        try:
            client = FlightRadar24Client()
            print("   ✅ Client initialization successful")
            
            # Test connection (requires valid token)
            if client.test_connection():
                print("   ✅ API connection successful")
                return True
            else:
                print("   ⚠️  API connection failed (check your token)")
                return False
                
        except ValueError as e:
            print(f"   ⚠️  {e}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n🎯 Next Steps:")
    print("1. 📖 Read the documentation: FR24_API_DOCUMENTATION.md")
    print("2. 🎮 Run examples: python fr24_examples.py")
    print("3. 🚀 Start building with: python flightradar24_api_client.py")
    print("\n📁 Available files:")
    print("   - flightradar24_api_client.py  (Main API client)")
    print("   - fr24_examples.py             (Usage examples)")
    print("   - FR24_API_DOCUMENTATION.md    (Complete documentation)")
    print("   - FR24_API_SETUP_GUIDE.md      (Setup guide)")

def main():
    """Main setup function"""
    print("🛩️  FLIGHTRADAR24 API SETUP ASSISTANT")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install required packages first")
        return
    
    # Setup environment
    env_ok = setup_environment()
    
    # Test client
    client_ok = test_client()
    
    # Show results
    print("\n" + "=" * 50)
    print("📊 SETUP SUMMARY")
    print("=" * 50)
    print(f"Requirements: {'✅ OK' if True else '❌ Missing packages'}")
    print(f"Environment:  {'✅ OK' if env_ok else '⚠️  Token needed'}")
    print(f"API Client:   {'✅ OK' if client_ok else '⚠️  Check token'}")
    
    if env_ok and client_ok:
        print("\n🎉 SETUP COMPLETE!")
        print("Your FR24 API client is ready to use!")
    else:
        print("\n⚠️  SETUP INCOMPLETE")
        print("Please complete the steps above and run this script again")
    
    show_next_steps()

if __name__ == "__main__":
    main()