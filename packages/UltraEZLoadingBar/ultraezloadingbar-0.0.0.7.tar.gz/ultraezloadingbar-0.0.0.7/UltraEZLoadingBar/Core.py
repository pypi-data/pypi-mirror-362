import sys
import time
from cryptography.fernet import Fernet
from .__init__ import versionnumber


# Color Stuff
def loading_bar(steps=50, bar_length=50, delay_per_step=0.1, message="Loading... ", color=None):
    """
    Displays a horizontal loading bar in the console.

    Args:
        steps (int): Total number of steps.
        bar_length (int): The length of the loading bar in characters.
        delay_per_step (float): The delay between each step (in seconds).
        message (str): The message to display before the loading bar.
        color (str): Optional. Adds color to the loading bar using ANSI escape codes. Examples: "r", "g", "b", etc.
    """
    # Define basic ANSI color codes
    colors = {
        "r": "\033[91m",
        "g": "\033[92m",
        "y": "\033[93m",
        "b": "\033[94m",
        "m": "\033[95m",
        "c": "\033[96m",
        "w": "\033[97m",
        "refresh": "\033[0m"
    }
    
    # Apply color if specified
    start_color = colors.get(color, "")  # Get the color code or empty string if invalid
    reset_color = colors["refresh"]

    try:
        if steps <= 0 or bar_length <= 0:
            raise ValueError("steps and bar_length must be positive integers.")
        if delay_per_step < 0:
            raise ValueError("delay_per_step must be non-negative.")
        for current_step in range(steps + 1):
            # Calculate progress
            filled_length = int((current_step / steps) * bar_length)
            bar = f"[{'=' * filled_length}{' ' * (bar_length - filled_length)}]"
            # Print the bar on the same line without adding extra lines
            sys.stdout.write(f"\r{start_color}{message}{bar} {current_step}/{steps}{reset_color}")
            sys.stdout.flush()
            time.sleep(delay_per_step)
        # Clear and overwrite the bar with a "Complete!" message
        sys.stdout.write("\n")
    except Exception as e:
        print(f"Error in loading_bar: {e}")


def enhancedloading_bar(steps=50, bar_length=50, delay_per_step=0.1, message="Loading...", color=None):
    """
    Displays a horizontal loading bar in the console with estimated time remaining.

    Args:
        steps (int): Total number of steps.
        bar_length (int): The length of the loading bar in characters.
        delay_per_step (float): The delay between each step (in seconds).
        message (str): The message to display before the loading bar.
        color (str): Optional. Adds color to the loading bar using ANSI escape codes. Examples: "r", "g", "b", etc.
    """
    # Define basic ANSI color codes
    colors = {
        "r": "\033[91m",
        "g": "\033[92m",
        "y": "\033[93m",
        "b": "\033[94m",
        "m": "\033[95m",
        "c": "\033[96m",
        "w": "\033[97m",
        "refresh": "\033[0m"
    }

    # Apply color if specified
    start_color = colors.get(color, "")  # Get the color code or empty string if invalid
    reset_color = colors["refresh"]

    try:
        if steps <= 0 or bar_length <= 0:
            raise ValueError("steps and bar_length must be positive integers.")
        if delay_per_step < 0:
            raise ValueError("delay_per_step must be non-negative.")
        start_time = time.time()
        for current_step in range(steps + 1):
            # Calculate progress
            filled_length = int((current_step / steps) * bar_length)
            bar = f"[{'=' * filled_length}{' ' * (bar_length - filled_length)}]"
            elapsed_time = time.time() - start_time
            eta = (elapsed_time / (current_step + 1)) * (steps - current_step) if current_step > 0 else 0
            # Print the bar with ETA
            sys.stdout.write(f"\r{start_color}{message}{bar} {current_step}/{steps} ETA: {eta:.1f}s{reset_color}")
            sys.stdout.flush()
            time.sleep(delay_per_step)
        sys.stdout.write("\nDone!\n")
    except Exception as e:
        print(f"Error in enhancedloading_bar: {e}")

def new_line():
    """
    Makes a new line
    """
    print("\n")

# Function to print colored text
def colored_text(text, color):
    """
    Prints the given text in the specified color.
    
    Args:
        text (str): The text to be printed.
        color (str): The color of the text. Available colors: red, green, blue, etc.
    """
    # Define basic ANSI color codes
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    
    try:
        # Get the color code, default to white if invalid color is provided
        color_code = colors.get(color.lower(), colors["white"])
        # Print the text with the chosen color
        print(f"{color_code}{text}{colors['reset']}")
    except Exception as e:
        print(f"Error in colored_text: {e}")


def cls():
    """
    Clears the console screen.
    """
    print("\033[H\033[J")


def generatekey():
    """
    Generates A Random Key Using Fernet-Cryptography

    Returns:
    <Key>

    Usage:
    <Varible> = generatekey()

    Output:
    <Key>

    Code Usage:
    Key = generatekey()
    print(key)

    Output: (Can Vary)
    179hf938je8329ht923j92e392ht9
    """
    try:
        a = Fernet.generate_key()
        return a.decode()
    except Exception as e:
        print(f"Error in generatekey: {e}")
        return None

def enhancedloading_bar(steps=50, bar_length=50, delay_per_step=0.1, message="Loading...", color=None):
    """
    Displays a horizontal loading bar with estimated time remaining.
    """
    # Define basic ANSI color codes
    colors = {
        "r": "\033[91m",
        "g": "\033[92m",
        "y": "\033[93m",
        "b": "\033[94m",
        "m": "\033[95m",
        "c": "\033[96m",
        "w": "\033[97m",
        "refresh": "\033[0m"
    }

    # Apply color if specified
    start_color = colors.get(color, "")
    reset_color = colors["refresh"]

    start_time = time.time()

    for current_step in range(steps + 1):
        # Calculate progress
        filled_length = int((current_step / steps) * bar_length)
        bar = f"[{'=' * filled_length}{' ' * (bar_length - filled_length)}]"

        elapsed_time = time.time() - start_time
        eta = (elapsed_time / (current_step + 1)) * (steps - current_step) if current_step > 0 else 0

        # Print the bar with ETA
        sys.stdout.write(f"\r{start_color}{message}{bar} {current_step}/{steps} ETA: {eta:.1f}s{reset_color}")
        sys.stdout.flush()
        time.sleep(delay_per_step)

def version():
    """
    Returns the version of the UltraEZLoadingBar module.
    
    Returns:
        str: The version of the module.
    """
    
    print(f"UltraEZLoadingBar Version: {versionnumber}")

