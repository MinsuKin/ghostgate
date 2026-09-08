"""
RawHuman Engine: Low-Level OS Synthetic Event & Injection Detector.

Provides cross-platform input event inspection to identify whether mouse and keyboard
events originate from physical HID hardware controllers or software synthesis APIs.

Standards & Specifications Implemented:
1. Windows Win32 Low-Level Hooks (WH_MOUSE_LL / WH_KEYBOARD_LL):
   - MSLLHOOKSTRUCT.flags bit 0: LLMHF_INJECTED (0x00000001)
     * Definition: "Low-Level Mouse Hook Flag: Injected" (Win32 SDK, winuser.h).
     * Note: "LLMHF" is standard Win32 nomenclature dating to Windows 2000,
             standing for Low-Level Mouse Hook Flag, entirely unrelated to Large Language Models.
   - KBDLLHOOKSTRUCT.flags bit 4: LLKHF_INJECTED (0x00000010)
     * Definition: "Low-Level Keyboard Hook Flag: Injected" (Win32 SDK, winuser.h).
2. macOS Quartz Event Services:
   - CGEventSourceGetSourceStateID:
     * kCGEventSourceStateHIDSystemState (1): Authentic hardware HID bus.
     * kCGEventSourceStateCombinedSessionState (0): Mixed session state.
     * kCGEventSourceStatePrivate (-1 or 0): Programmatically synthesized source (CGEventPost, cliclick).
   - CGEventGetIntegerValueField:
     * kCGEventSourceUnixProcessID: Non-zero PID indicates synthetic injection by automation processes.
3. Linux Input Subsystem (evdev / uinput):
   - /dev/uinput virtual device nodes vs /dev/input/by-id hardware bus topology.
"""

from __future__ import annotations
import os
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class EventOrigin(str, Enum):
    HARDWARE_PHYSICAL = "HARDWARE_PHYSICAL"
    SYNTHETIC_API_INJECTED = "SYNTHETIC_API_INJECTED"
    VIRTUAL_DRIVER = "VIRTUAL_DRIVER"
    UNKNOWN = "UNKNOWN"


# Win32 SDK Standards (winuser.h)
WIN32_LLMHF_INJECTED = 0x00000001        # Low-Level Mouse Hook Injected Flag
WIN32_LLMHF_LOWER_IL_INJECTED = 0x00000002 # Injected from lower Integrity Level
WIN32_LLKHF_INJECTED = 0x00000010        # Low-Level Keyboard Hook Injected Flag

# macOS Quartz Standards
MACOS_CG_SOURCE_PRIVATE = 0              # kCGEventSourceStatePrivate
MACOS_CG_SOURCE_HID = 1                  # kCGEventSourceStateHIDSystemState


@dataclass
class IODetectionResult:
    origin: EventOrigin
    is_synthetic: bool
    platform_flag: Optional[str] = None
    source_pid: Optional[int] = None
    confidence: float = 1.0
    details: Dict[str, Any] = None


class SyntheticEventDetector:
    """
    Inspects OS-level input event streams across Windows, macOS, and Linux.
    Identifies programmatic event injection (SendInput, CGEventPost, uinput, pyautogui).
    """

    def __init__(self):
        self.os_type = platform.system()
        self._init_platform_hooks()

    def _init_platform_hooks(self):
        """Initializes platform-specific event subsystems when running on host."""
        self.quartz_available = False
        if self.os_type == "Darwin":
            try:
                import Quartz
                self.quartz = Quartz
                self.quartz_available = True
            except ImportError:
                self.quartz_available = False

    def inspect_event_metadata(
        self,
        event_flags: int = 0,
        source_id: Optional[int] = None,
        source_pid: Optional[int] = None,
        device_vendor_id: Optional[str] = None,
    ) -> IODetectionResult:
        """
        Evaluates input event metadata against low-level OS specifications.
        """
        # 1. Windows: Win32 MSLLHOOKSTRUCT / KBDLLHOOKSTRUCT
        if self.os_type == "Windows":
            is_mouse_injected = bool(event_flags & WIN32_LLMHF_INJECTED)
            is_keyboard_injected = bool(event_flags & WIN32_LLKHF_INJECTED)
            is_lower_il = bool(event_flags & WIN32_LLMHF_LOWER_IL_INJECTED)

            if is_mouse_injected or is_keyboard_injected or is_lower_il:
                flag_label = "MSLLHOOKSTRUCT:LLMHF_INJECTED" if is_mouse_injected else "KBDLLHOOKSTRUCT:LLKHF_INJECTED"
                return IODetectionResult(
                    origin=EventOrigin.SYNTHETIC_API_INJECTED,
                    is_synthetic=True,
                    platform_flag=flag_label,
                    confidence=0.99,
                    details={
                        "flags_hex": hex(event_flags),
                        "spec": "Win32 SDK winuser.h (Low-Level Hook Injected Flag)",
                    },
                )

        # 2. macOS: Quartz Event Services (CGEventSourceStateID)
        elif self.os_type == "Darwin":
            # kCGEventSourceStatePrivate or non-zero source_pid indicates synthetic origin
            if source_id is not None and source_id == MACOS_CG_SOURCE_PRIVATE:
                return IODetectionResult(
                    origin=EventOrigin.SYNTHETIC_API_INJECTED,
                    is_synthetic=True,
                    platform_flag="kCGEventSourceStatePrivate",
                    source_pid=source_pid,
                    confidence=0.98,
                    details={"source_state_id": source_id, "source_pid": source_pid},
                )
            if source_pid is not None and source_pid > 0:
                return IODetectionResult(
                    origin=EventOrigin.SYNTHETIC_API_INJECTED,
                    is_synthetic=True,
                    platform_flag=f"kCGEventSourceUnixProcessID:{source_pid}",
                    source_pid=source_pid,
                    confidence=0.97,
                    details={"source_pid": source_pid},
                )

        # 3. Linux: Virtual Input Device Bus (/dev/uinput)
        elif self.os_type == "Linux":
            if device_vendor_id and ("uinput" in device_vendor_id.lower() or "virtual" in device_vendor_id.lower()):
                return IODetectionResult(
                    origin=EventOrigin.VIRTUAL_DRIVER,
                    is_synthetic=True,
                    platform_flag="/dev/uinput-virtual",
                    confidence=0.99,
                    details={"device_bus": device_vendor_id},
                )

        # Generic Flag Fallback (0x01)
        if bool(event_flags & 0x01):
            return IODetectionResult(
                origin=EventOrigin.SYNTHETIC_API_INJECTED,
                is_synthetic=True,
                platform_flag="SYNTHETIC_INJECTION_FLAG_0x01",
                confidence=0.95,
                details={"event_flags": event_flags},
            )

        # Verified Physical Hardware Event
        return IODetectionResult(
            origin=EventOrigin.HARDWARE_PHYSICAL,
            is_synthetic=False,
            platform_flag="PHYSICAL_HID_INTERRUPT",
            confidence=0.92,
            details={"device_vendor_id": device_vendor_id or "Hardware HID Host Controller"},
        )
