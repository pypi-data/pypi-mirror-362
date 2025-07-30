"""Cross-platform wrapper for the antiword utility to extract text from MS Word documents."""
import os
import subprocess
import platform
from .text_optimizer import optimize_text

ANTIWORD_SHARE = os.path.join(os.path.dirname(__file__), "antiword_share")

def get_antiword_binary():
    """Get the appropriate antiword binary path for the current platform."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Map platform.system() and platform.machine() to our binary directories
    if system == "windows":
        binary_dir = "win-amd64"
        binary_name = "antiword.exe"
    elif system == "linux":
        binary_dir = "linux-amd64"
        binary_name = "antiword"
    elif system == "darwin":
        if machine in ["arm64", "aarch64"]:
            binary_dir = "darwin-arm64"
        else:
            # macOS Intel (x86_64) - no dedicated binary available
            raise RuntimeError(
                "macOS Intel (x86_64) is not currently supported. "
            )
        binary_name = "antiword"
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")

    binary_path = os.path.join(os.path.dirname(__file__), "bin", binary_dir, binary_name)

    if not os.path.exists(binary_path):
        raise RuntimeError(
            f"Antiword binary not found for platform {system} {machine}: {binary_path}"
        )

    return binary_path

def extract_text(doc_path, optimize_format=False):
    """Extract text from a Microsoft Word document using antiword.

    Args:
        doc_path (str): Path to the .doc file to extract text from.
        optimize_format (bool): Whether to optimize text formatting by merging
            lines without leading spaces. Defaults to False.

    Returns:
        str: The extracted text content from the document.

    Raises:
        RuntimeError: If the platform is not supported or binary is missing.
        subprocess.CalledProcessError: If antiword execution fails.
    """
    antiword_binary = get_antiword_binary()
    env = os.environ.copy()
    env["ANTIWORDHOME"] = ANTIWORD_SHARE
    result = subprocess.run(
        [antiword_binary, doc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        env=env
    )
    text = result.stdout.decode('utf-8')
    
    if optimize_format:
        text = optimize_text(text)
    
    return text
