# Nano Banana Pro Integration

**Status: Implemented and Ready for Testing**

This document describes the Nano Banana Pro (Gemini 3 Pro Image) integration added to `amplifier-module-image-generation`.

---

## What's New

### New Provider: `nano-banana-pro`

Adds support for Google's Gemini 3 Pro Image model (codenamed "Nano Banana Pro") with:

- **High-fidelity image generation** - Studio-quality output up to 4K resolution
- **Multi-turn conversational editing** - Iterate on images through natural conversation
- **Advanced reasoning (Thinking mode)** - Better understanding of complex UI/UX instructions
- **Google Search grounding** - Generate images with accurate, current information
- **Professional text rendering** - Clear, legible text in images (perfect for UI mockups)
- **Multiple aspect ratios** - 1:1, 16:9, 9:16, 4:3, 3:4

---

## Usage Examples

### Single-Shot Generation

```python
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator

generator = ImageGenerator()

# Generate with Nano Banana Pro
result = await generator.generate(
    prompt="A modern mobile app dashboard in portrait orientation with stat cards",
    output_path=Path("output/dashboard.png"),
    preferred_api="nano-banana-pro",
    params={
        "aspect_ratio": "9:16",  # Mobile portrait
        "resolution": "2K",       # High quality
        "use_thinking": True,     # Enable reasoning
        "use_search": False,      # No grounding needed
    }
)

if result.success:
    print(f"Generated with {result.api_used} for ${result.cost:.3f}")
    print(f"Saved to: {result.local_path}")
```

### Multi-Turn Conversational Editing

```python
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator

generator = ImageGenerator()

# Create a conversation session
conversation_id = generator.create_conversation(
    preferred_api="nano-banana-pro",
    use_thinking=True,
    use_search=False
)

# Initial generation
result1 = await generator.generate(
    prompt="Create a fitness app dashboard with stat cards",
    output_path=Path("output/dashboard-v1.png"),
    preferred_api="nano-banana-pro",
    params={
        "conversation_id": conversation_id,
        "aspect_ratio": "9:16",
        "resolution": "2K",
    }
)

# Iterate on the same image
result2 = await generator.generate(
    prompt="Make the stat cards 50% larger and add a graph at the bottom",
    output_path=Path("output/dashboard-v2.png"),
    preferred_api="nano-banana-pro",
    params={
        "conversation_id": conversation_id,  # Continue conversation
        "aspect_ratio": "9:16",
        "resolution": "2K",
    }
)

# Further refinement
result3 = await generator.generate(
    prompt="Change the color scheme to use blues and greens",
    output_path=Path("output/dashboard-v3.png"),
    preferred_api="nano-banana-pro",
    params={
        "conversation_id": conversation_id,
        "aspect_ratio": "9:16",
        "resolution": "2K",
    }
)

# Clean up when done
generator.close_conversation(conversation_id)
```

### With Google Search Grounding

```python
result = await generator.generate(
    prompt="Create a tech news article layout showing today's top AI stories",
    output_path=Path("output/news-layout.png"),
    preferred_api="nano-banana-pro",
    params={
        "use_thinking": True,
        "use_search": True,  # Enable search for current information
        "aspect_ratio": "16:9",
        "resolution": "2K",
    }
)
```

---

## API Parameters

### `preferred_api` Values

- `"nano-banana-pro"` - New! Gemini 3 Pro Image
- `"imagen"` - Imagen 4
- `"dalle"` - DALL-E 3
- `"gptimage"` - GPT-Image-1

### Nano Banana Pro Parameters

All passed via the `params` dict:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `conversation_id` | `str` | `None` | Continue existing conversation |
| `use_thinking` | `bool` | `True` | Enable reasoning mode for complex instructions |
| `use_search` | `bool` | `False` | Enable Google Search grounding |
| `aspect_ratio` | `str` | `"1:1"` | Image aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` |
| `resolution` | `str` | `"1K"` | Image resolution: `1K`, `2K`, `4K` |
| `reference_image` | `Path` | `None` | Optional reference image for editing |

---

## Conversation Management

### Create a Conversation

```python
conversation_id = generator.create_conversation(
    preferred_api="nano-banana-pro",
    use_thinking=True,
    use_search=False
)
```

Returns a `conversation_id` string for use in subsequent `generate()` calls.

### Close a Conversation

```python
generator.close_conversation(conversation_id)
```

Frees resources associated with the conversation.

---

## Cost Estimates

Nano Banana Pro pricing (approximate):

| Resolution | Cost per Image |
|------------|----------------|
| 1K | $0.035 |
| 2K | $0.050 |
| 4K | $0.080 |

**Note**: Multi-turn conversations count each generation as a separate image.

---

## Tool Protocol Support

The Nano Banana Pro provider is accessible through the Tool protocol:

```python
from amplifier_module_image_generation import ImageGenerationTool

tool = ImageGenerationTool()

# Generate via tool
result = await tool.execute({
    "operation": "generate",
    "prompt": "A modern UI mockup",
    "output_path": "output/mockup.png",
    "preferred_api": "nano-banana-pro",
    "params": {
        "aspect_ratio": "16:9",
        "resolution": "2K",
        "use_thinking": True,
    }
})
```

---

## Configuration

Set your Google API key:

```bash
export GOOGLE_API_KEY=your_gemini_api_key
```

The provider will be automatically available when the key is configured.

---

## Implementation Details

### Files Added

- `src/amplifier_module_image_generation/nano_banana_client.py` - Nano Banana Pro client implementation

### Files Modified

- `src/amplifier_module_image_generation/generator.py`:
  - Added `NanaBananaProClient` to provider list
  - Added `create_conversation()` method
  - Added `close_conversation()` method
  
- `src/amplifier_module_image_generation/models.py`:
  - Updated `GeneratedImage.api` type to include `"nano-banana-pro"`

### Provider Priority

The default fallback order is now:
1. `nano-banana-pro` (new default for best quality)
2. `gptimage`
3. `imagen`
4. `dalle`

---

## Next Steps for UI Mockup Bundle

This enhanced module will serve as the foundation for a specialized UI mockup bundle:

```
amplifier-bundle-ui-mockup/
├── bundle.md
├── agents/
│   ├── mockup-generator.md      # Generates initial mockups
│   ├── mockup-editor.md         # Conversational refinement
│   └── prototype-builder.md     # Creates clickable prototypes
├── context/
│   ├── ui-prompt-patterns.md    # UI-specific prompt engineering
│   └── nano-banana-tips.md      # Best practices for mockups
└── recipes/
    ├── generate-mockup.yaml     # Single mockup workflow
    ├── iterative-refinement.yaml # Multi-turn editing
    └── mockup-to-prototype.yaml  # Full mockup → prototype flow
```

The bundle will:
1. Use this module's `nano-banana-pro` provider for generation
2. Apply UI/UX prompt engineering patterns
3. Support conversational mockup refinement
4. Generate clickable prototype HTML from mockups

---

## Testing

To test the integration:

```bash
# Install dependencies (if not already installed)
cd amplifier-module-image-generation
uv sync

# Run quality checks
uv run python -m ruff check src/
uv run python -m pyright src/

# Test with a simple script
cat > test_nano_banana.py << 'EOF'
import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator

async def test():
    generator = ImageGenerator()
    
    # Check availability
    client = generator.clients["nano-banana-pro"]
    available = await client.check_availability()
    print(f"Nano Banana Pro available: {available}")
    
    if available:
        # Test single-shot generation
        result = await generator.generate(
            prompt="A simple blue square on white background",
            output_path=Path("test_output.png"),
            preferred_api="nano-banana-pro",
            params={"resolution": "1K"}
        )
        print(f"Success: {result.success}")
        print(f"Cost: ${result.cost:.3f}")
        print(f"Path: {result.local_path}")

asyncio.run(test())
EOF

uv run python test_nano_banana.py
```

---

## Contributing Back

To contribute this back to the original repository:

1. **Create a branch** in your fork
2. **Test thoroughly** with your Google API key
3. **Update README.md** to document Nano Banana Pro
4. **Submit a PR** to @robotdad's repository with:
   - Clear description of the new provider
   - Example usage
   - Benefits for UI mockup generation

---

## Questions?

For technical questions about this integration, see the implementation in:
- `nano_banana_client.py` - Client implementation
- `generator.py` - Integration and conversation management
- `models.py` - Type definitions
