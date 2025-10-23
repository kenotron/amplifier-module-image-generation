# How This Module Was Made

**Migration from scenarios/article_illustrator to reusable Amplifier module**

---

## The Problem

The article_illustrator scenario tool had a sophisticated image generation system supporting multiple AI providers (DALL-E, Imagen, GPT-Image-1), but it was:
- Locked inside a single-purpose tool
- Not reusable by other applications
- Missing amplifier-dev integration patterns
- Valuable functionality inaccessible to ecosystem

Other content creation apps (blog writers, documentation generators, presentation creators) all need image generation but had to implement it from scratch.

---

## The Solution: Extract as Reusable Module

### What We Extracted

The image generation orchestration system from article_illustrator:
- Multi-API client implementations (DALL-E, Imagen, GPT-Image-1)
- Provider protocol for extensibility
- Automatic fallback when providers fail
- Cost tracking and budget limits
- Parallel generation for alternatives

### What We Left Behind

App-specific logic stayed in blog-creator app:
- Image prompt generation (content-aware)
- Markdown integration
- User interaction and review
- Session state management

---

## Migration Process

### Step 1: Analyzed Source Code

From `scenarios/article_illustrator/image_generation/`:
- `core.py`: ImageGenerator orchestrator (~180 LOC)
- `clients.py`: Three API client implementations (~390 LOC)
- `models.py`: Data models for images and prompts

**Total**: ~570 LOC of production-tested code

### Step 2: Defined Module Boundary

**Clear Interface ("Studs")**:
```python
ImageGenerator.generate(prompt, output_path, ...) -> ImageResult
```

**Key Decision**: Orchestrator as primary interface
- Consumers don't choose providers
- Automatic fallback handling
- Single entry point

### Step 3: Set Up Git Sources

**Critical Pattern from MODULE_DEVELOPMENT_LESSONS.md**:
- Use git sources, NOT path dependencies
- Enables standalone installation
- Points to microsoft/amplifier-core (kernel)
- This module lives in robotdad/amplifier-dev

```toml
[tool.uv.sources.amplifier-core]
git = "https://github.com/microsoft/amplifier-dev"
subdirectory = "amplifier-core"
branch = "main"
```

### Step 4: Added Amplifier Patterns

**Capability Registry Integration**:
```python
# Register for cooperation with other modules
coordinator.register_capability("image_generation.orchestrator", self)
coordinator.register_capability("image_generation.providers", self.clients)
```

**Path Expansion** (from MODULE_DEVELOPMENT_LESSONS.md:177-192):
```python
# ALWAYS use .expanduser() for paths from config
output_dir = Path(config.get("output_dir", "~/.images")).expanduser()
```

### Step 5: Maintained Simplicity

**What We Kept Simple**:
- Direct API client calls (no complex retry frameworks)
- Simple cost estimation (fixed prices per model)
- Basic error handling (log and raise)
- Minimal configuration (sensible defaults)

**What We Avoided**:
- Complex provider routing logic
- Advanced caching systems
- Elaborate error recovery strategies
- Over-abstracted client interfaces

---

## Architecture Decisions

### Decision 1: Protocol vs Abstract Base Class

**Chose**: `ImageProviderProtocol` (typing.Protocol)
**Why**: More flexible, runtime type checking, easier to add providers
**Alternative**: ABC would enforce inheritance, more rigid

### Decision 2: Async Interface

**Chose**: Fully async API
**Why**: All image generation involves network I/O, async prevents blocking
**Alternative**: Sync would be simpler but blocks event loop

### Decision 3: Single vs Multiple Results

**Chose**: Return single ImageResult, support multiple via separate calls
**Why**: Simpler interface, parallel calls if needed
**Alternative**: Return list of results - more complex contract

### Decision 4: Cost Tracking in Contract

**Chose**: Include cost in ImageResult
**Why**: Users care about costs, should be visible
**Alternative**: Separate cost tracking - less convenient

---

## Key Learnings

### From Original Implementation

1. **Multi-API support is valuable** - Different APIs excel at different image types
2. **Automatic fallback reduces friction** - Users don't handle provider failures
3. **Cost visibility matters** - Helps users make informed decisions
4. **Base64 vs URL handling differs** - GPT-Image-1 returns base64, others return URLs

### From Migration Process

1. **Git sources are mandatory** - Path dependencies break standalone installation
2. **Capability registry enables cooperation** - Modules share resources without tight coupling
3. **Path expansion is critical** - Always `.expanduser()` for paths from config
4. **Module boundaries should be clear** - Image generation is mechanism, prompt creation is policy

### From Agent Consultation

1. **api-contract-designer validated interface** - Single entry point with minimal surface area
2. **integration-specialist confirmed patterns** - Git sources and capability registry correct
3. **zen-architect challenged extraction** - Suggested pushing to core, but we can't modify microsoft repos

---

## Testing Strategy

### Unit Tests

- Each API client tested independently
- Orchestrator logic (provider selection, fallback)
- Cost calculation accuracy
- Error handling paths

### Integration Tests

- Real API calls (with test API keys)
- Capability registry cooperation
- Standalone mode fallback
- Multi-provider parallel generation

### Manual Acceptance

- Generate images with each provider
- Verify file output and format
- Validate cost estimates
- Test with missing API keys

---

## Reusability

This module is designed for any Amplifier app needing image generation:

**Use Cases**:
- Blog post illustration
- Documentation diagrams
- Social media content
- Presentation slides
- Marketing materials
- Technical documentation

**Integration**: Import and use, or leverage via capability registry

---

## What's Next

### For This Module

- Add more providers (Stability AI, Midjourney when APIs available)
- Support batch generation optimization
- Add image quality assessment
- Support more output formats

### For Other Developers

Use this module in your apps:
1. Add to dependencies (git source)
2. Import ImageGenerator
3. Generate images with simple async call

See [README.md](./README.md) for usage examples.

---

## References

**Source Material**:
- Original: `scenarios/article_illustrator/image_generation/`
- Migration Guide: `ai_working/SCENARIO_MIGRATION_GUIDE.md`
- Module Lessons: `ai_working/MODULE_DEVELOPMENT_LESSONS.md`

**Philosophy Alignment**:
- Ruthless Simplicity: Minimal interface, clear purpose
- Modular Design: Self-contained brick with stable studs
- Bricks & Studs: Regeneratable from specification

**Agent Consultation**:
- zen-architect: Validated design approach
- api-contract-designer: Designed clean interface
- integration-specialist: Confirmed git source patterns

---

**Created**: 2025-10-22
**Migration From**: scenarios/article_illustrator (production-tested)
**Status**: Active development
