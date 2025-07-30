"""Cross-platform clipboard access module with platform-specific fallback handling."""

import logging
import os
import platform
import subprocess
from typing import Optional

import pyperclip

from ._errors import ClipboardError
from ._validators import ValidationException, validate_clipboard_text

# Configure logging
logger = logging.getLogger(__name__)


def _get_platform_info() -> str:
    """Get detailed platform information for error messages."""
    system = platform.system()

    # Handle Linux variants
    if system == "Linux":
        # Check for WSL first
        if os.path.exists("/proc/version"):
            try:
                with open("/proc/version", "r", encoding="utf-8") as f:
                    version = f.read().strip()
                    if "Microsoft" in version or "WSL" in version:
                        return "WSL (Windows Subsystem for Linux)"
            except (IOError, OSError):
                pass

        # Check for Wayland environment
        if "WAYLAND_DISPLAY" in os.environ:
            return "Linux (Wayland)"

        # Check for headless or X11
        return "Linux (headless)" if "DISPLAY" not in os.environ else "Linux (X11)"

    # Handle other platforms
    platform_map = {
        "Darwin": "macOS",
        "Windows": "Windows",
    }

    return platform_map.get(system, f"{system} (unsupported)")


def _get_platform_guidance(error_msg: str) -> str:
    """Get platform-specific guidance for clipboard errors."""
    platform_info = _get_platform_info()

    # Check WSL first since it contains "Linux" but needs special handling
    if "WSL" in platform_info:
        return (
            "WSL clipboard access may be limited. Try: "
            "1. Use WSL2 with Windows 10 build 19041+ "
            "2. Install wslu package for clip.exe integration "
            "3. Use Windows Terminal or enable clipboard sharing"
        )

    # Handle Linux variants
    if "Linux" in platform_info:
        error_lower = error_msg.lower()

        # Platform-specific Linux guidance
        linux_guidance = {
            "headless": (
                "Clipboard access requires a display server. "
                "On headless Linux systems, clipboard operations are not supported."
            ),
            "Wayland": (
                "Wayland clipboard access requires wl-clipboard utilities. Install with: "
                "sudo apt-get install wl-clipboard (Ubuntu/Debian) or "
                "sudo dnf install wl-clipboard (Fedora) or "
                "sudo pacman -S wl-clipboard (Arch). "
                "If wl-clipboard is installed, ensure compositor supports clipboard sharing."
            ),
        }

        # Check for exact platform variant matches
        for variant, guidance in linux_guidance.items():
            if variant in platform_info:
                return guidance

        # Check for error-specific patterns
        if "xclip" in error_lower or "xsel" in error_lower:
            return (
                "Missing clipboard utilities. Install with: "
                "sudo apt-get install xclip xsel (Ubuntu/Debian) or "
                "sudo yum install xclip xsel (RHEL/CentOS) or "
                "sudo pacman -S xclip xsel (Arch)"
            )

        if "display" in error_lower:
            return (
                "No display available. Ensure DISPLAY environment variable is set "
                "or run in a desktop environment."
            )

    # Platform-specific guidance mapping
    guidance_map = {
        "macOS": (
            "macOS clipboard access failed. This may be due to: "
            "1. Security permissions (check System Preferences > Privacy) "
            "2. Running in a sandboxed environment "
            "3. Insufficient user privileges"
        ),
        "Windows": (
            "Windows clipboard access failed. This may be due to: "
            "1. Another application holding clipboard lock "
            "2. Insufficient user privileges "
            "3. Antivirus software blocking access"
        ),
    }

    for platform_name, guidance in guidance_map.items():
        if platform_name in platform_info:
            return guidance

    return f"Platform-specific guidance not available for {platform_info}"


def _try_wayland_clipboard_get() -> Optional[str]:
    """Try to get clipboard content using Wayland wl-clipboard tools."""
    try:
        result = subprocess.run(
            ["wl-paste"], capture_output=True, text=True, timeout=5, check=False
        )
        if result.returncode == 0:
            return result.stdout
        logger.debug(
            "wl-paste failed with return code %s: %s", result.returncode, result.stderr
        )
        return None
    except (
        subprocess.TimeoutExpired,
        FileNotFoundError,
        subprocess.SubprocessError,
    ) as e:
        logger.debug("Wayland clipboard get failed: %s", e)
        return None


def _try_wayland_clipboard_set(text: str) -> bool:
    """Try to set clipboard content using Wayland wl-clipboard tools."""
    try:
        result = subprocess.run(
            ["wl-copy"],
            input=text,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            logger.debug("Successfully set clipboard using wl-copy")
            return True
        logger.debug(
            "wl-copy failed with return code %s: %s", result.returncode, result.stderr
        )
        return False
    except (
        subprocess.TimeoutExpired,
        FileNotFoundError,
        subprocess.SubprocessError,
    ) as e:
        logger.debug("Wayland clipboard set failed: %s", e)
        return False


def get_clipboard() -> str:
    """
    Get the current contents of the system clipboard with platform-specific fallback handling.

    Returns:
        str: The clipboard contents as a string. Returns empty string if clipboard is empty
             or if clipboard access fails gracefully.

    Raises:
        ClipboardError: If clipboard access fails critically.
    """
    try:
        content = pyperclip.paste()
        return content if content is not None else ""
    except (OSError, RuntimeError, ImportError) as e:
        error_msg = str(e)
        platform_info = _get_platform_info()

        # Try Wayland fallback on Linux systems
        if "Linux" in platform_info and "WAYLAND_DISPLAY" in os.environ:
            logger.debug("Attempting Wayland clipboard fallback for get operation")
            wayland_content = _try_wayland_clipboard_get()
            if wayland_content is not None:
                logger.info(
                    "Successfully retrieved clipboard content using Wayland fallback"
                )
                return wayland_content

        guidance = _get_platform_guidance(error_msg)

        # Log detailed error information for debugging
        logger.error(
            "Clipboard read failed on %s: %s\nPlatform guidance: %s",
            platform_info,
            error_msg,
            guidance,
        )

        # For read operations, return empty string as per spec requirement
        # This allows the application to continue functioning gracefully
        logger.warning("Returning empty string due to clipboard read failure")
        return ""


def set_clipboard(text: str) -> None:
    """
    Set the system clipboard contents to the provided text with platform-specific fallback handling.

    Args:
        text: The text to copy to the clipboard.

    Raises:
        ClipboardError: If clipboard access fails.
        ValueError: If text validation fails.
    """
    try:
        # Use enhanced validation
        validate_clipboard_text(text)
    except ValidationException as e:
        # Convert ValidationException to ValueError for backward compatibility
        raise ValueError(str(e)) from e

    try:
        pyperclip.copy(text)
        logger.debug("Successfully set clipboard content: %s characters", len(text))
    except (OSError, RuntimeError, ImportError) as e:
        error_msg = str(e)
        platform_info = _get_platform_info()

        # Try Wayland fallback on Linux systems
        if "Linux" in platform_info and "WAYLAND_DISPLAY" in os.environ:
            logger.debug("Attempting Wayland clipboard fallback for set operation")
            if _try_wayland_clipboard_set(text):
                logger.info("Successfully set clipboard content using Wayland fallback")
                return

        guidance = _get_platform_guidance(error_msg)

        # Log detailed error information
        logger.error(
            "Clipboard write failed on %s: %s\nPlatform guidance: %s",
            platform_info,
            error_msg,
            guidance,
        )

        # For write operations, raise ClipboardError with enhanced message
        raise ClipboardError(
            f"Failed to write to clipboard on {platform_info}: {error_msg}. "
            f"Solution: {guidance}"
        ) from e
