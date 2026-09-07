import pytest
from rawhuman_engine.biomechanics import (
    BiomechanicalAnalyzer,
    generate_synthetic_bot_trajectory,
    generate_human_like_trajectory,
)
from rawhuman_engine.detector import SyntheticEventDetector, EventOrigin


def test_synthetic_os_flag_detection():
    detector = SyntheticEventDetector()
    
    # Test synthetic injection flag
    result = detector.inspect_event_metadata(event_flags=0x01)
    assert result.is_synthetic is True
    assert result.origin == EventOrigin.SYNTHETIC_API_INJECTED

    # Test physical HID event
    clean_result = detector.inspect_event_metadata(event_flags=0x00)
    assert clean_result.is_synthetic is False
    assert clean_result.origin == EventOrigin.HARDWARE_PHYSICAL


def test_biomechanical_bot_rejection():
    analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
    bot_points = generate_synthetic_bot_trajectory((10.0, 20.0), (500.0, 400.0), steps=20)
    for p in bot_points:
        analyzer.add_point(p.x, p.y, p.timestamp)

    report = analyzer.analyze()
    # A robotic constant-speed, flat-timer trajectory must fail
    assert report.is_human is False
    assert report.human_confidence < 0.60
    assert len(report.rejection_reasons) > 0


def test_biomechanical_human_verification():
    analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
    human_points = generate_human_like_trajectory((10.0, 20.0), (500.0, 400.0), steps=25)
    for p in human_points:
        analyzer.add_point(p.x, p.y, p.timestamp)

    report = analyzer.analyze()
    assert report.is_human is True
    assert report.human_confidence >= 0.60
    assert report.fitts_law_fit >= 0.40
    assert report.tremor_energy_score >= 0.30
