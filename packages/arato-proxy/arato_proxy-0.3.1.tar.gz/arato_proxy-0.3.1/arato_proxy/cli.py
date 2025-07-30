import subprocess
import sys
import os
import argparse
import importlib.resources
import shutil
import tempfile


def ensure_callback_files_available():
    """Ensure callback files are available in the current directory for LiteLLM to load"""
    # Check if arato_proxy directory already exists
    if os.path.exists('arato_proxy'):
        return
    
    # Create the arato_proxy directory
    os.makedirs('arato_proxy', exist_ok=True)
    
    # Copy the callback files from the installed package
    try:
        # Copy custom_callbacks.py
        callback_source = importlib.resources.files('arato_proxy') / 'custom_callbacks.py'
        with callback_source.open('rb') as src, open('arato_proxy/custom_callbacks.py', 'wb') as dst:
            shutil.copyfileobj(src, dst)
        
        # Create __init__.py to make it a proper package
        with open('arato_proxy/__init__.py', 'w', encoding='utf-8') as f:
            f.write('# Arato proxy package\n')
            
        print("Created arato_proxy directory with callback files")
        
    except (OSError, IOError) as e:
        print(f"Warning: Could not copy callback files: {e}")
        print("The callback may not work correctly.")


def main():
    """Main entry point for the arato-proxy CLI"""
    parser = argparse.ArgumentParser(
        description="Arato LiteLLM Proxy - Run LiteLLM proxy with Arato logging callbacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  arato-proxy                    # Run with default config.yaml
  arato-proxy --config custom.yaml --port 8080
  arato-proxy --init-config      # Create a template config file
  
Environment variables (required):
  ARATO_API_URL         # URL of the Arato API endpoint
  ARATO_API_KEY         # API key for authentication
  OPENAI_API_KEY        # OpenAI API key for the proxy
        """
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to LiteLLM config file (default: config.yaml)"
    )
    parser.add_argument(
        "--port",
        default="4000",
        help="Port to run the proxy on (default: 4000)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file (default: .env)"
    )
    parser.add_argument(
        "--init-config",
        action="store_true",
        help="Create a template config.yaml file in the current directory"
    )
    parser.add_argument(
        "--init-env",
        action="store_true",
        help="Create a template .env file in the current directory"
    )
    
    args = parser.parse_args()
    
    # Handle initialization commands
    if args.init_config:
        init_config_file()
        return
    
    if args.init_env:
        init_env_file()
        return
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(args.env_file)
    except ImportError:
        print("WARNING: python-dotenv not installed, skipping .env file loading")
    
    # Check for required environment variables
    required_env_vars = ["ARATO_API_URL", "ARATO_API_KEY"]
    missing_vars = []

    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment.")
        print(f"Expected .env file location: {args.env_file}")
        print("\nYou can create a template .env file by running: arato-proxy --init-env")
        sys.exit(1)

    # Resolve config path
    config_path = args.config
    if not os.path.isabs(config_path):
        # Try relative to current working directory first
        if os.path.exists(config_path):
            config_path = os.path.abspath(config_path)
        else:
            # Try to find bundled config as fallback
            try:
                bundled_config = str(importlib.resources.files('arato_proxy') / 'config.yaml')
                if os.path.exists(bundled_config):
                    config_path = bundled_config
                    print(f"Using bundled config: {config_path}")
                else:
                    print(f"Bundled config not found at {bundled_config}")
            except (ImportError, AttributeError):
                pass
    
    if not os.path.exists(config_path):
        print(f"ERROR: Config file not found at {config_path}")
        print("Please ensure the config file exists or specify a different path with --config")
        print("\nYou can create a template config file by running: arato-proxy --init-config")
        sys.exit(1)
    
    # Ensure callback files are available in the current directory
    ensure_callback_files_available()
    
    print("Starting Arato LiteLLM Proxy...")
    print(f"Config: {config_path}")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Arato API URL: {os.getenv('ARATO_API_URL')}")
    print()
    
    try:
        # Run litellm proxy directly
        subprocess.run([
            "litellm",
            "--config", config_path,
            "--port", args.port,
            "--host", args.host
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to start LiteLLM proxy: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
        sys.exit(0)


def init_config_file():
    """Create a template config.yaml file"""
    config_content = """model_list:
  - model_name: "*"             
    litellm_params:
      model: openai/*           
      api_key: os.environ/OPENAI_API_KEY
litellm_settings:
    callbacks: ["arato_proxy.custom_callbacks.proxy_handler_instance"]
"""
    
    if os.path.exists("config.yaml"):
        print("ERROR: config.yaml already exists. Remove it first if you want to recreate it.")
        sys.exit(1)
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("Created config.yaml template file.")
    print("Please review and modify it according to your needs.")


def init_env_file():
    """Create a template .env file"""
    env_content = """# Arato API Configuration
ARATO_API_URL=https://api.arato.com/v1/logs
ARATO_API_KEY=your-arato-api-key-here

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
"""
    
    if os.path.exists(".env"):
        print("ERROR: .env already exists. Remove it first if you want to recreate it.")
        sys.exit(1)
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("Created .env template file.")
    print("Please edit it and fill in your actual API keys.")
    print("WARNING: Do not commit this file to version control!")

if __name__ == "__main__":
    main()
