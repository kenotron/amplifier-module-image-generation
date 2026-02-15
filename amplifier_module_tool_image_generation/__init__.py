"""Multi-provider AI image generation for Amplifier applications.

This module provides both a standalone library interface and an Amplifier Tool protocol interface.

Library Usage (Direct Import):
    >>> from amplifier_module_tool_image_generation import ImageGenerator
    >>> generator = ImageGenerator()
    >>> result = await generator.generate(
    ...     prompt="A serene landscape",
    ...     output_path=Path("output/image.png")
    ... )

Tool Usage (Via Amplifier):
    >>> from amplifier_module_tool_image_generation import ImageGenerationTool
    >>> tool = ImageGenerationTool()
    >>> result = await tool.execute({
    ...     "operation": "generate",
    ...     "prompt": "A serene landscape",
    ...     "output_path": "output/image.png"
    ... })
"""

from .generator import ImageGenerator
from .models import ImageGenerationError
from .models import ImageResult
from .tool import ImageGenerationTool

__version__ = "0.1.0"
__all__ = [
    "ImageGenerator",
    "ImageResult",
    "ImageGenerationError",
    "ImageGenerationTool",
    "mount",
]


async def mount(coordinator, config: dict | None = None) -> ImageGenerationTool:
    """Mount the image generation tool for Amplifier.
    
    This function is called by Amplifier's module loader to instantiate
    the tool when loaded via settings.yaml module configuration.
    
    Args:
        coordinator: The Amplifier coordinator instance
        config: Optional configuration dictionary (currently unused)
        
    Returns:
        ImageGenerationTool instance ready for use
    """
    return ImageGenerationTool()
