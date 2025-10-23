# amplifier-module-image-generation

**Multi-provider AI image generation for Amplifier applications**

Generate images using DALL-E, Imagen, or GPT-Image-1 through a unified interface with automatic fallback, cost tracking, and parallel generation support.

---

## Installation

```bash
pip install git+https://github.com/robotdad/amplifier-dev#subdirectory=amplifier-module-image-generation
```

Or add to your `pyproject.toml`:

```toml
[tool.uv.sources]
amplifier-module-image-generation = {
    git = "https://github.com/robotdad/amplifier-dev",
    subdirectory = "amplifier-module-image-generation",
    branch = "main"
}
```

---

## Quick Start

```python
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator

# Initialize generator
generator = ImageGenerator()

# Generate image
result = await generator.generate(
    prompt="A serene mountain landscape at sunset",
    output_path=Path("output/mountain.png")
)

if result.success:
    print(f"Generated with {result.api_used} for ${result.cost:.2f}")
    print(f"Saved to: {result.local_path}")
```

---

## Features

- **Multi-Provider Support**: DALL-E 3, Imagen 4, GPT-Image-1
- **Automatic Fallback**: Tries other providers if preferred fails
- **Cost Tracking**: Estimates and tracks generation costs
- **Parallel Generation**: Create alternatives with multiple APIs simultaneously
- **Availability Checking**: Validates API keys and connectivity
- **Type Safety**: Full type hints and Pydantic models

---

## API Reference

### ImageGenerator

Primary interface for image generation.

```python
class ImageGenerator:
    async def generate(
        self,
        prompt: str,
        output_path: Path,
        *,
        preferred_api: str | None = None,
        params: dict | None = None,
    ) -> ImageResult:
        """Generate image using best available provider.

        Args:
            prompt: Text description of image to generate
            output_path: Where to save the generated image
            preferred_api: Optional API preference (imagen, dalle, gptimage)
            params: Optional provider-specific parameters

        Returns:
            ImageResult with status, cost, and path information

        Raises:
            ImageGenerationError: When no providers available or all fail
        """
```

### ImageResult

Result of image generation operation.

```python
@dataclass
class ImageResult:
    success: bool          # Whether generation succeeded
    api_used: str          # Which provider was used (imagen, dalle, gptimage)
    cost: float            # Estimated cost in USD
    local_path: Path       # Where image was saved
    error: str | None      # Error message if failed
```

---

## Usage Examples

### Basic Generation

```python
from amplifier_module_image_generation import ImageGenerator

generator = ImageGenerator()

result = await generator.generate(
    "A minimalist technical diagram of a microservices architecture",
    Path("diagrams/architecture.png")
)
```

### Specify Preferred API

```python
# Prefer Imagen for quality
result = await generator.generate(
    prompt="Professional headshot photo",
    output_path=Path("images/headshot.png"),
    preferred_api="imagen"
)
```

### Custom Parameters

```python
# High quality with DALL-E
result = await generator.generate(
    prompt="Detailed technical illustration",
    output_path=Path("output/detailed.png"),
    preferred_api="dalle",
    params={"quality": "hd", "size": "1024x1792"}
)
```

### Handle Errors Gracefully

```python
result = await generator.generate(prompt, output_path)

if result.success:
    print(f"Success! Cost: ${result.cost:.2f}")
else:
    print(f"Failed: {result.error}")
    # Fallback or retry logic here
```

---

## Configuration

### API Keys

Set environment variables for the providers you want to use:

```bash
# OpenAI (for DALL-E 3 and GPT-Image-1)
export OPENAI_API_KEY=your_openai_key

# Google (for Imagen 4)
export GOOGLE_API_KEY=your_google_key
```

The module automatically detects which APIs are configured and uses them.

### Default Behavior

- **Preferred API**: GPT-Image-1 (best quality/cost ratio)
- **Fallback Order**: gptimage → imagen → dalle
- **Quality**: Standard (medium for GPT-Image-1)
- **Size**: 1024x1024

---

## Supported Providers

### GPT-Image-1 (OpenAI)

- **Model**: gpt-image-1
- **Cost**: $0.02-$0.08 per image (quality-dependent)
- **Quality**: low, medium, high, auto
- **Sizes**: 1024x1024, 1024x1792, 1792x1024
- **Format**: Base64-encoded PNG

### DALL-E 3 (OpenAI)

- **Model**: dall-e-3
- **Cost**: $0.04-$0.08 per image (quality-dependent)
- **Quality**: standard, hd
- **Sizes**: 1024x1024, 1024x1792, 1792x1024
- **Format**: URL download

### Imagen 4 (Google)

- **Model**: imagen-4.0-generate-001
- **Cost**: ~$0.03-$0.04 per image
- **Aspect Ratios**: 1:1, 16:9, 9:16, 4:3, 3:4
- **Format**: Binary bytes

---

## Integration with Amplifier

### Capability Registry Pattern

When used in Amplifier apps, register with coordinator:

```python
# In your module initialization
coordinator.register_capability("image_generation.orchestrator", generator)

# In consuming code - use capability first
generator = coordinator.get_capability("image_generation.orchestrator")
if not generator:
    from amplifier_module_image_generation import ImageGenerator
    generator = ImageGenerator()  # Standalone fallback
```

This allows multiple modules to share the same generator instance and configuration.

---

## Error Handling

The module handles common failures gracefully:

- **Missing API keys**: Skips unconfigured providers
- **API failures**: Falls back to other providers automatically
- **Network errors**: Retries with exponential backoff
- **Invalid prompts**: Returns descriptive error messages

```python
# Example error handling
result = await generator.generate(prompt, output_path)

if not result.success:
    if "API key" in result.error:
        print("Configure API keys in environment")
    elif "rate limit" in result.error:
        print("Wait before retrying")
    else:
        print(f"Unexpected error: {result.error}")
```

---

## Cost Management

Track costs to stay within budget:

```python
total_cost = 0.0

for prompt in prompts:
    result = await generator.generate(prompt, output_path)
    total_cost += result.cost

    if total_cost > budget_limit:
        print(f"Budget limit reached: ${total_cost:.2f}")
        break
```

**Current Pricing** (as of 2025):
- GPT-Image-1: $0.02-$0.08 per image
- DALL-E 3: $0.04-$0.08 per image
- Imagen 4: $0.03-$0.04 per image

---

## Development

### Setup

```bash
cd amplifier-module-image-generation
uv sync --dev
```

### Run Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run pyright
```

---

## Contributing

See the main [Amplifier contributing guide](https://github.com/microsoft/amplifier-dev/blob/main/CONTRIBUTING.md).

This module follows the [Amplifier module development patterns](https://github.com/microsoft/amplifier-dev/blob/main/docs/MODULE_DEVELOPMENT.md).

---

## License

MIT License - See [LICENSE](https://github.com/robotdad/amplifier-dev/blob/main/LICENSE) file.

---

## Learn More

- [HOW_THIS_MODULE_WAS_MADE.md](./HOW_THIS_MODULE_WAS_MADE.md) - Creation story and patterns
- [examples/](./examples/) - Additional usage examples
- [Amplifier Documentation](https://github.com/microsoft/amplifier-dev/blob/main/docs/)
