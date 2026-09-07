"""
RawHuman Engine: Synthetic Event & Low-Level OS Injection Detector.
Detects whether mouse/keyboard I/O was dispatched via synthetic APIs (e.g. SendInput, CGEventPost)
or originated from physical USB/Bluetooth HID controllers.
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
    Inspects OS-level input events for synthetic injection markers.
    """

    def __init__(self):
        self.os_type = platform.system()
        self._init_platform_hooks()

    def _init_platform_hooks(self):
        """Initializes platform-specific libraries if available."""
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
        Evaluates input event metadata across OS architectures.
        """
        # 1. Windows: Check LLMHF_INJECTED (0x01) or LLKHF_INJECTED (0x10)
        if self.os_type == "Windows":
            is_injected = bool(event_flags & 0x01 or event_flags & 0x10)
            if is_injected:
                return IODetectionResult(
                    origin=EventOrigin.SYNTHETIC_API_INJECTED,
                    is_synthetic=True,
                    platform_flag="LLMHF_INJECTED / LLKHF_INJECTED",
                    confidence=0.99,
                    details={"flags": hex(event_flags)},
                )

        # 2. macOS: Quartz CGEventSource state inspection
        elif self.os_type == "Darwin":
            # In macOS Quartz:
            # Source state 0 = Private/Synthetic source
            # Source state 1 = Combined session state (physical HID)
            # Source state 2 = HID event state
            if source_id is not None:
                if source_id == 0:  # kCGEventSourceStatePrivate / programmatic
                    return IODetectionResult(
                        origin=EventOrigin.SYNTHETIC_API_INJECTED,
                        is_synthetic=True,
                        platform_flag="kCGEventSourceStatePrivate",
                        source_pid=source_pid,
                        confidence=0.98,
                        details={"source_state_id": source_id, "source_pid": source_pid},
                    )

        # 3. Linux: Check Virtual Device Markers (uinput / xdotool)
        elif self.os_type == "Linux":
            if device_vendor_id and "uinput" in device_vendor_id.lower():
                return IODetectionResult(
                    origin=EventOrigin.VIRTUAL_DRIVER,
                    is_synthetic=True,
                    platform_flag="/dev/uinput-virtual",
                    confidence=0.99,
                    details={"device": device_vendor_id},
                )

        # Fallback: If synthetic flag was passed explicitly or detected
        if bool(event_flags & 0x01):
            return IODetectionResult(
                origin=EventOrigin.SYNTHETIC_API_INJECTED,
                is_synthetic=True,
                platform_flag="GENERIC_SYNTHETIC_FLAG",
                confidence=0.95,
                details={"event_flags": event_flags},
            )

        return IODetectionResult(
            origin=EventOrigin.HARDWARE_PHYSICAL,
            is_synthetic=False,
            platform_flag="PHYSICAL_HID_INTERRUPT",
            confidence=0.92,
            details={"device_vendor_id": device_vendor_id or "Apple/Standard HID"},
        )
