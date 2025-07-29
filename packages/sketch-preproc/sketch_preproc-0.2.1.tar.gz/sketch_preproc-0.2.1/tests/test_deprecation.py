# tests/test_deprecation.py
"""Tests for V4 pipeline deprecation."""

import pytest
import warnings
import numpy as np

from sketch_preproc import preprocess


@pytest.fixture
def sample_image():
    """Create a simple test image."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


def test_v4_deprecation_warning(sample_image):
    """Test that V4 pipeline shows deprecation warning."""
    with pytest.warns(DeprecationWarning, match="V4 pipeline is deprecated"):
        result = preprocess(sample_image, sample_image, pipeline="v4")
    
    # Should still work despite warning
    assert result is not None
    assert "primary_mask" in result
    assert "shade_mask" in result
    assert result["shade_mask"] is not None


def test_v3_no_deprecation_warning(sample_image):
    """Test that V3 pipeline shows no deprecation warning."""
    # Should not raise any warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # Turn warnings into errors
        result = preprocess(sample_image, sample_image, pipeline="v3")
    
    assert result is not None
    assert "primary_mask" in result
    assert result["shade_mask"] is None


def test_default_pipeline_is_v3(sample_image):
    """Test that default pipeline is V3."""
    # Should not raise deprecation warning
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # Turn warnings into errors
        result = preprocess(sample_image, sample_image)  # No pipeline specified
    
    assert result is not None
    assert result["shade_mask"] is None  # V3 characteristic


def test_numeric_presets_default_to_v3(sample_image):
    """Test that numeric presets use V3 by default."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # Turn warnings into errors
        result = preprocess(sample_image, sample_image, preset=5)
    
    assert result is not None
    assert result["shade_mask"] is None  # V3 characteristic


def test_v4_functionality_still_works(sample_image):
    """Test that V4 still functions correctly despite deprecation."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        
        # Test with various presets
        for preset in [1, 5, 10]:
            result = preprocess(sample_image, sample_image, pipeline="v4", preset=preset)
            
            assert "primary_mask" in result
            assert "detail_mask" in result
            assert "shade_mask" in result
            assert result["shade_mask"] is not None
            assert isinstance(result["shade_mask"], np.ndarray)
            assert result["shade_mask"].shape == (100, 100)