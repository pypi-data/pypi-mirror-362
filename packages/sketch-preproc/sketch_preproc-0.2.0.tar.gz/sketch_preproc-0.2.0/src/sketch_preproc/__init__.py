"""Sketch preprocessing package with V3 and V4 pipelines.

Note: V4 pipeline is deprecated as of v0.1.0 and will be removed in v1.0.0.
Please use V3 pipeline (default) for all new projects.
"""

from typing import Union, Optional, Dict, Any
from pathlib import Path
import numpy as np
import yaml
import warnings

from .common.io import load_image
from .common.config import PreprocCfg, PreprocCfgV4


# Preset mappings for numeric convenience
SPECTRUM_PRESETS = {
    1: "spectrum_01_bare_bones",
    2: "spectrum_02_minimal", 
    3: "spectrum_03_fine",
    4: "spectrum_04_balanced_fine",
    5: "spectrum_05_balanced",
    6: "spectrum_06_balanced_detailed",
    7: "spectrum_07_detailed",
    8: "spectrum_08_very_detailed",
    9: "spectrum_09_comprehensive",
    10: "spectrum_10_maximal"
}

SPECTRUM_DESCRIPTIONS = {
    1: "Bare bones - absolute minimal, only strongest edges",
    2: "Minimal - very fine lines, architectural/technical",
    3: "Fine - clean sketches with fine lines",
    4: "Balanced fine - good for simple subjects",
    5: "Balanced - general purpose default",
    6: "Balanced detailed - good for complex subjects",
    7: "Detailed - captures interior details",
    8: "Very detailed - includes subtle features",
    9: "Comprehensive - captures almost everything",
    10: "Maximal - maximum detail, may include noise"
}


def preprocess(
    ref_image: Union[str, Path, np.ndarray, bytes],
    user_image: Union[str, Path, np.ndarray, bytes],
    pipeline: str = "v3",
    preset: Optional[Union[str, int]] = None,
    config: Optional[PreprocCfg] = None,
    device: str = "cpu",
) -> Dict[str, Any]:
    """
    Preprocess sketch images using V3 or V4 pipeline.
    
    Args:
        ref_image: Reference image (path, array, or bytes)
        user_image: User sketch image (path, array, or bytes)
        pipeline: Pipeline version ("v3" or "v4"). Default is "v3".
                  Note: V4 is deprecated and will be removed in v1.0.0
        preset: Preset name or number (1-10) to load from presets/ directory
        config: Custom configuration (overrides preset)
        device: Device for processing ("cpu" or "cuda")
    
    Returns:
        Dictionary with keys:
            - primary_mask: Primary edge mask (uint8)
            - detail_mask: Detail edge mask (uint8)
            - shade_mask: Shade mask (uint8, None for V3)
            - debug: Debug information dict
            
    Example:
        # Use preset 5 (balanced) for V3 pipeline (recommended)
        result = preprocess(ref_img, user_img, preset=5)
        
        # Use preset 1 (bare bones) for minimal edges
        result = preprocess(ref_img, user_img, preset=1)
        
        # Use named preset
        result = preprocess(ref_img, user_img, preset="spectrum_07_detailed")
    """
    # Validate pipeline
    if pipeline not in ["v3", "v4"]:
        raise ValueError(f"Unknown pipeline: {pipeline}. Use 'v3' or 'v4'")
    
    # Show deprecation warning for V4
    if pipeline == "v4":
        warnings.warn(
            "V4 pipeline is deprecated and will be removed in v1.0.0. "
            "Please use V3 pipeline (default) which provides better performance "
            "and cleaner results. The shade_mask output will be None when using V3.",
            DeprecationWarning,
            stacklevel=2
        )
    
    # Load images
    ref_img = load_image(ref_image)
    user_img = load_image(user_image)
    
    # Load configuration
    if config is None:
        # Handle numeric presets
        if isinstance(preset, int):
            if preset not in SPECTRUM_PRESETS:
                raise ValueError(
                    f"Invalid numeric preset: {preset}. "
                    f"Valid options are 1-10:\n" + 
                    "\n".join(f"  {k}: {SPECTRUM_DESCRIPTIONS[k]}" 
                              for k in sorted(SPECTRUM_PRESETS.keys()))
                )
            preset_name = SPECTRUM_PRESETS[preset]
            # Add pipeline suffix if using numeric preset and V4
            if pipeline == "v4":
                preset = f"{preset_name}_v4"
            else:
                preset = preset_name
        elif preset is None:
            preset = f"default_{pipeline}"
        
        # Load preset from YAML
        preset_path = Path(__file__).parent / "presets" / f"{preset}.yml"
        if not preset_path.exists():
            # Try without pipeline suffix
            preset_path = Path(__file__).parent / "presets" / f"{preset.replace(f'_{pipeline}', '')}.yml"
            
        if not preset_path.exists():
            available_presets = list((Path(__file__).parent / "presets").glob("*.yml"))
            preset_names = [p.stem for p in available_presets]
            raise FileNotFoundError(
                f"Preset not found: {preset}\n"
                f"Available presets: {', '.join(sorted(preset_names))}"
            )
        
        with open(preset_path, "r") as f:
            config_dict = yaml.safe_load(f)
        
        # Remove tau_shade from V3 configs if present
        if pipeline == "v3" and "tau_shade" in config_dict:
            config_dict.pop("tau_shade")
            if "tau_lo_shade" in config_dict:
                config_dict.pop("tau_lo_shade")
        
        # Create appropriate config class
        if pipeline == "v4":
            config = PreprocCfgV4(**config_dict)
        else:
            config = PreprocCfg(**config_dict)
    
    # Import and run appropriate pipeline
    if pipeline == "v3":
        from .v3.pipeline import process
    else:
        from .v4.pipeline import process
    
    # Process images
    result = process(ref_img, user_img, config, device)
    
    # Ensure consistent output format
    output = {
        "primary_mask": result["edges_primary"],
        "detail_mask": result["edges_detail"],
        "shade_mask": result.get("edges_shade", None),
        "debug": {
            k: v for k, v in result.items() 
            if k not in ["edges_primary", "edges_detail", "edges_shade"]
        }
    }
    
    return output


def list_presets(pipeline: Optional[str] = None) -> Dict[Union[int, str], str]:
    """
    List available presets.
    
    Args:
        pipeline: Filter by pipeline ("v3", "v4", or None for all)
        
    Returns:
        Dictionary mapping preset identifiers to descriptions
    """
    presets = {}
    
    # Add numeric presets
    for num, desc in SPECTRUM_DESCRIPTIONS.items():
        if pipeline is None:
            presets[num] = desc
        else:
            presets[f"{num} ({pipeline})"] = desc
    
    # Add named presets from files
    preset_dir = Path(__file__).parent / "presets"
    for preset_file in preset_dir.glob("*.yml"):
        name = preset_file.stem
        if pipeline is None or name.endswith(f"_{pipeline}") or f"_{pipeline}" not in name:
            # Try to load description from file
            try:
                with open(preset_file, "r") as f:
                    lines = f.readlines()
                    for line in lines[:5]:  # Check first 5 lines
                        if line.strip().startswith("#") and ":" in line:
                            desc = line.strip("#").split(":", 1)[1].strip()
                            presets[name] = desc
                            break
                    else:
                        presets[name] = name.replace("_", " ").title()
            except:
                presets[name] = name.replace("_", " ").title()
    
    return presets


__all__ = ["preprocess", "list_presets", "SPECTRUM_PRESETS", "SPECTRUM_DESCRIPTIONS"]