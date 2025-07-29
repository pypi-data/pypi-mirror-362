# tests/test_presets.py
"""Tests for numeric preset functionality."""

import pytest
import numpy as np
import cv2
from pathlib import Path

from sketch_preproc import preprocess, list_presets, SPECTRUM_PRESETS, SPECTRUM_DESCRIPTIONS


@pytest.fixture
def sample_image():
    """Create a simple test image with various edge types."""
    img = np.ones((256, 256, 3), dtype=np.uint8) * 255
    
    # Strong edges (should appear in all presets)
    cv2.circle(img, (128, 128), 50, (0, 0, 0), 3)
    cv2.rectangle(img, (30, 30), (100, 100), (0, 0, 0), 3)
    
    # Medium edges (should appear in presets 5+)
    cv2.line(img, (0, 128), (256, 128), (50, 50, 50), 2)
    cv2.line(img, (128, 0), (128, 256), (50, 50, 50), 2)
    
    # Fine details (should appear in presets 7+)
    for i in range(10, 100, 20):
        cv2.circle(img, (200, i), 3, (100, 100, 100), 1)
    
    # Very fine details (should only appear in presets 9-10)
    for x in range(150, 250, 5):
        cv2.line(img, (x, 150), (x, 155), (150, 150, 150), 1)
    
    return img


def test_numeric_presets_basic(sample_image):
    """Test that all numeric presets work."""
    for preset_num in range(1, 11):
        result = preprocess(sample_image, sample_image, preset=preset_num)
        
        assert "primary_mask" in result
        assert "detail_mask" in result
        assert result["primary_mask"].shape == (256, 256)
        assert result["detail_mask"].shape == (256, 256)
        assert result["primary_mask"].dtype == np.uint8
        assert result["detail_mask"].dtype == np.uint8


def test_preset_progression(sample_image):
    """Test that edge density increases with preset number."""
    densities = []
    
    for preset_num in range(1, 11):
        result = preprocess(sample_image, sample_image, preset=preset_num)
        combined = cv2.bitwise_or(result["primary_mask"], result["detail_mask"])
        density = np.mean(combined > 0)
        densities.append(density)
    
    # Check that density generally increases
    # Allow some variation but overall trend should be increasing
    increases = sum(densities[i] <= densities[i+1] for i in range(9))
    assert increases >= 7, f"Density should generally increase with preset number, but only {increases}/9 increases found"
    
    # Check that preset 1 has minimum density and preset 10 has maximum
    assert densities[0] == min(densities), "Preset 1 should have minimum edge density"
    assert densities[9] == max(densities), "Preset 10 should have maximum edge density"


def test_preset_v3_v4_compatibility(sample_image):
    """Test that presets work with both V3 and V4 pipelines."""
    import warnings
    
    for preset_num in [1, 5, 10]:  # Test min, mid, max
        # V3 pipeline (default)
        result_v3 = preprocess(sample_image, sample_image, preset=preset_num)
        assert result_v3["shade_mask"] is None
        
        # V4 pipeline (deprecated) - suppress warning for test
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result_v4 = preprocess(sample_image, sample_image, pipeline="v4", preset=preset_num)
            assert result_v4["shade_mask"] is not None
            assert result_v4["shade_mask"].shape == (256, 256)


def test_preset_thresholds(sample_image):
    """Test that preset thresholds are correctly applied."""
    # Test extreme presets
    result_minimal = preprocess(sample_image, sample_image, preset=1)
    result_maximal = preprocess(sample_image, sample_image, preset=10)
    
    # Minimal should have much fewer edges
    edges_minimal = np.sum(result_minimal["primary_mask"] > 0)
    edges_maximal = np.sum(result_maximal["primary_mask"] > 0)
    
    assert edges_maximal > edges_minimal * 1.5, "Maximal preset should have significantly more edges than minimal"


def test_invalid_preset_number():
    """Test error handling for invalid preset numbers."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    
    with pytest.raises(ValueError, match="Invalid numeric preset"):
        preprocess(img, img, preset=0)
    
    with pytest.raises(ValueError, match="Invalid numeric preset"):
        preprocess(img, img, preset=11)
    
    with pytest.raises(ValueError, match="Invalid numeric preset"):
        preprocess(img, img, preset=-1)


def test_list_presets():
    """Test listing available presets."""
    # List all presets
    all_presets = list_presets()
    
    # Should include numeric presets
    for i in range(1, 11):
        assert i in all_presets
        assert all_presets[i] == SPECTRUM_DESCRIPTIONS[i]
    
    # List V4 presets
    v4_presets = list_presets(pipeline="v4")
    assert len(v4_presets) > 0
    
    # List V3 presets
    v3_presets = list_presets(pipeline="v3")
    assert len(v3_presets) > 0


def test_preset_constants():
    """Test that preset constants are properly defined."""
    assert len(SPECTRUM_PRESETS) == 10
    assert len(SPECTRUM_DESCRIPTIONS) == 10
    
    for i in range(1, 11):
        assert i in SPECTRUM_PRESETS
        assert i in SPECTRUM_DESCRIPTIONS
        assert SPECTRUM_PRESETS[i].startswith("spectrum_")


def test_preset_edge_characteristics(sample_image):
    """Test that different presets capture appropriate edge types."""
    # Add specific test patterns
    test_img = sample_image.copy()
    
    # Very strong edge (should appear in all presets)
    cv2.rectangle(test_img, (10, 10), (50, 50), (0, 0, 0), 5)
    strong_roi = (10, 10, 50, 50)
    
    # Medium edge (should appear in presets 4+)
    cv2.circle(test_img, (200, 50), 20, (80, 80, 80), 2)
    medium_roi = (180, 30, 220, 70)
    
    # Fine edge (should appear in presets 7+)
    cv2.ellipse(test_img, (200, 200), (30, 20), 0, 0, 360, (120, 120, 120), 1)
    fine_roi = (170, 180, 230, 220)
    
    # Test different presets
    for preset_num, expected_edges in [
        (1, ["strong"]),
        (5, ["strong", "medium"]),
        (8, ["strong", "medium", "fine"])
    ]:
        result = preprocess(test_img, test_img, preset=preset_num)
        combined = cv2.bitwise_or(result["primary_mask"], result["detail_mask"])
        
        # Check strong edges (should always be present)
        if "strong" in expected_edges:
            strong_edges = combined[strong_roi[1]:strong_roi[3], strong_roi[0]:strong_roi[2]]
            assert np.sum(strong_edges > 0) > 100, f"Preset {preset_num} should capture strong edges"
        
        # Check medium edges
        medium_edges = combined[medium_roi[1]:medium_roi[3], medium_roi[0]:medium_roi[2]]
        if "medium" in expected_edges:
            assert np.sum(medium_edges > 0) > 50, f"Preset {preset_num} should capture medium edges"
        else:
            assert np.sum(medium_edges > 0) < 20, f"Preset {preset_num} should not capture many medium edges"
        
        # Check fine edges
        fine_edges = combined[fine_roi[1]:fine_roi[3], fine_roi[0]:fine_roi[2]]
        if "fine" in expected_edges:
            assert np.sum(fine_edges > 0) > 30, f"Preset {preset_num} should capture fine edges"
        else:
            assert np.sum(fine_edges > 0) < 10, f"Preset {preset_num} should not capture many fine edges"


def test_preset_performance_scaling(sample_image):
    """Test that processing time is reasonable across presets."""
    import time
    
    # Use smaller image for faster tests
    small_image = cv2.resize(sample_image, (256, 256))
    
    times = []
    for preset_num in [1, 5, 10]:
        start = time.perf_counter()
        preprocess(small_image, small_image, preset=preset_num)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    # All presets should complete in reasonable time
    assert all(t < 5.0 for t in times), "All presets should process in under 5 seconds"
    
    # More detailed presets might take slightly longer, but not dramatically
    assert times[2] < times[0] * 5, "Maximal preset shouldn't take more than 5x the minimal preset"