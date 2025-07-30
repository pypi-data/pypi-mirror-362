#!/usr/bin/env python3
"""
Setup script for Form Automation MCP Server
This script installs dependencies and configures the MCP server for use with Claude Desktop
"""

import subprocess
import sys
import os
import json
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_claude_desktop_config():
    """Set up Claude Desktop configuration."""
    print("🔧 Configuring Claude Desktop...")
    
    # Claude Desktop config paths
    if os.name == 'nt':  # Windows
        config_dir = Path.home() / "AppData" / "Roaming" / "Claude"
    else:  # macOS/Linux
        config_dir = Path.home() / "Library" / "Application Support" / "Claude"
    
    config_file = config_dir / "claude_desktop_config.json"
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Find the job-automator-mcp executable
    mcp_command = None
    
    # Method 1: Try to find using shutil.which (works for global installs)
    mcp_command = shutil.which("job-automator-mcp")
    
    if not mcp_command:
        # Method 2: Check in same directory as current Python executable
        python_dir = Path(sys.executable).parent
        if os.name == 'nt':  # Windows
            potential_path = python_dir / "job-automator-mcp.exe"
        else:  # macOS/Linux
            potential_path = python_dir / "job-automator-mcp"
        
        if potential_path.exists():
            mcp_command = str(potential_path)
    
    if not mcp_command:
        # Method 3: Check in Scripts subdirectory (Windows virtual env)
        scripts_dir = Path(sys.executable).parent / "Scripts"
        if scripts_dir.exists():
            if os.name == 'nt':
                potential_path = scripts_dir / "job-automator-mcp.exe"
            else:
                potential_path = scripts_dir / "job-automator-mcp"
            
            if potential_path.exists():
                mcp_command = str(potential_path)
    
    if not mcp_command:
        # Fallback: use just the command name and hope it's in PATH
        mcp_command = "job-automator-mcp"
        print("⚠️  Could not find job-automator-mcp executable, using command name only")
    else:
        print(f"✅ Found job-automator-mcp at: {mcp_command}")
    
    # Prepare the configuration
    new_config = {
        "mcpServers": {
            "job-automator": {
                "command": mcp_command
            }
        }
    }
    
    # Read existing config if it exists
    existing_config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Existing Claude config file is invalid, creating new one")
    
    # Merge configurations
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}
    
    existing_config["mcpServers"]["job-automator"] = new_config["mcpServers"]["job-automator"]
    
    # Write the updated config
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2)
        print(f"✅ Claude Desktop config updated: {config_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to update Claude Desktop config: {e}")
        return False

def test_mcp_server():
    """Test the MCP server installation."""
    print("🧪 Testing MCP server...")
    
    server_path = Path(__file__).parent / "form_automation_server.py"
    
    # Test that the server can be imported
    try:
        # Add the project directory to Python path for testing
        project_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(project_dir))
        
        # Try to import the server modules
        from simple_form_extractor import SimpleFormExtractor
        from simple_form_filler import SimpleFormFiller
        print("✅ Form automation modules imported successfully")
        
        # Validate server exists
        try:
            import job_application_automator.mcp_server
            print("✅ MCP server module found")
        except ImportError:
            print("❌ MCP server module not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False
    
    # Setup Claude Desktop config
    if not setup_claude_desktop_config():
        print("❌ Claude Desktop configuration failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart Claude Desktop application")
    print("2. Look for the form automation tools in Claude Desktop")
    print("3. Test with: 'Extract form data from [URL]'")
    print("\n🔧 Available tools:")
    print("- simple_form_extraction: Extract form fields from any URL")
    print("- simple_form_filling: Fill forms with provided data")
    print("- health_check: Check server status")
    
    print(f"\n📁 Server location: {Path(__file__).parent / 'form_automation_server.py'}")
    print(f"📁 Config location: {Path.home() / 'Library/Application Support/Claude/claude_desktop_config.json' if os.name != 'nt' else Path.home() / 'AppData/Roaming/Claude/claude_desktop_config.json'}")

def main():
    """Main entry point for Claude Desktop setup."""
    print("🚀 Job Application Automator - Claude Desktop Setup")
    print("=" * 60)
    
    # Install playwright browsers if needed
    print("🎭 Installing Playwright browsers...")
    try:
        run_command("playwright install chromium", "Installing Playwright browser")
    except:
        print("⚠️  Playwright browser installation skipped (may already be installed)")
    
    # Setup Claude Desktop config
    if not setup_claude_desktop_config():
        print("❌ Claude Desktop configuration failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart Claude Desktop application")
    print("2. Look for the job automation tools in Claude Desktop")
    print("3. Test with: 'Extract form data from [job posting URL]'")
    print("\n🔧 Available tools:")
    print("- simple_form_extraction: Extract form fields from job posting URLs")
    print("- simple_form_filling: Fill forms with your information")
    print("- create_cover_letter: Generate personalized cover letters")
    print("- get_applied_jobs: View your application dashboard")
    print("- health_check: Check server status")
    
    config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json" if os.name == 'nt' else Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    print(f"\n📁 Config location: {config_path}")

if __name__ == "__main__":
    main()
