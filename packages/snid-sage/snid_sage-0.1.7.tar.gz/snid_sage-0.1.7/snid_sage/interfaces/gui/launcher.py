"""
SNID SAGE GUI Launcher Entry Point
==================================

Simplified entry point for the SNID SAGE GUI when installed via pip.
This directly uses the FastGUILauncher without complex import fallbacks.
"""

import sys
import os
import argparse

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="SNID SAGE GUI")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    parser.add_argument("--silent", "-s", action="store_true", help="Silent mode")
    
    # Check environment variables for defaults
    args = parser.parse_args()
    
    if os.environ.get('SNID_DEBUG', '').lower() in ('1', 'true', 'yes'):
        args.debug = True
        args.verbose = True
    elif os.environ.get('SNID_VERBOSE', '').lower() in ('1', 'true', 'yes'):
        args.verbose = True
    elif os.environ.get('SNID_QUIET', '').lower() in ('1', 'true', 'yes'):
        args.quiet = True
    
    return args

def main():
    """
    Main entry point for snid-sage and snid-gui commands
    """
    try:
        # Import the fast launcher directly
        from snid_sage.interfaces.gui.fast_launcher import main as fast_main
        return fast_main()
        
    except ImportError as e:
        print(f"❌ Error importing fast launcher: {e}")
        
        # Try fallback to direct GUI launch
        try:
            print("🔄 Attempting fallback launch...")
            from snid_sage.interfaces.gui.sage_gui import main as sage_main
            return sage_main()
        except Exception as fallback_error:
            print(f"❌ Fallback launch also failed: {fallback_error}")
            print("💡 Try running: pip install --upgrade snid-sage")
            return 1
            
    except Exception as e:
        print(f"❌ Error launching SNID SAGE GUI: {e}")
        return 1

def main_with_args():
    """
    Alternative entry point that accepts command line arguments
    """
    try:
        args = parse_arguments()
        
        # Import and use FastGUILauncher with parsed args
        from snid_sage.interfaces.gui.fast_launcher import FastGUILauncher
        
        launcher = FastGUILauncher(args)
        return launcher.run()
        
    except ImportError as e:
        print(f"❌ Error importing fast launcher: {e}")
        # Fallback to direct GUI launch
        try:
            from snid_sage.interfaces.gui.sage_gui import main as sage_main
            return sage_main()
        except Exception as fallback_error:
            print(f"❌ Fallback launch also failed: {fallback_error}")
            return 1
            
    except Exception as e:
        print(f"❌ Error launching SNID SAGE GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 