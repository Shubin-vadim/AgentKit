---
name: facade-pattern
description: >-
  Generic Facade pattern: a single simplified entry point over a complex
  subsystem. Use when callers only need a narrow slice of a big subsystem's
  API and shouldn't have to wire several subsystem classes themselves, in any
  language or project.
---

# Facade Pattern (Portable Template)

## When to Use

Activate when:
- A subsystem has several classes that most callers must wire together the same way every time
- You want a stable, simple entry point that can absorb internal subsystem changes without breaking callers
- Onboarding new callers to the subsystem currently requires reading several classes just to do the common case

Do **not** use when:
- The subsystem is already simple enough that wiring it directly is one or two lines
- Some callers genuinely need fine-grained control over subsystem internals — don't hide the subsystem's classes entirely, keep them accessible for those callers

## Template

```python
class VideoConversionFacade:
    def __init__(self) -> None:
        self._demuxer = Demuxer()
        self._decoder = Decoder()
        self._encoder = Encoder()
        self._muxer = Muxer()

    def convert(self, input_path: str, output_path: str, codec: str) -> None:
        stream = self._demuxer.demux(input_path)
        frames = self._decoder.decode(stream)
        encoded = self._encoder.encode(frames, codec)
        self._muxer.mux(encoded, output_path)

VideoConversionFacade().convert("in.mov", "out.mp4", codec="h264")
```

Callers get a one-method surface for the common case. `Demuxer`, `Decoder`, `Encoder`, `Muxer` remain independently usable for callers that need more control — the facade doesn't replace them, it hides them for the 90% case.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Facade class | `XxxFacade`, or simply named for the operation it exposes (`VideoConverter`) |
| Facade methods | High-level verbs matching the caller's actual intent (`convert`, `checkout`), not the subsystem's internal step names |

## Anti-Patterns

- A "facade" that just re-exposes every subsystem method 1:1 with no simplification — that's a re-export, not a facade
- Business logic accumulating inside the facade instead of orchestration only — if branching/validation grows large, it belongs in a service the facade calls
- Making the wrapped subsystem classes private/unreachable, forcing power users through the simplified facade even when they need finer control

## Related Skills

- `design-patterns-catalog` — choosing Facade vs. Adapter vs. Mediator
- `codebase-design` — deep-module vocabulary; a good facade is a deep module (small interface, real behavior behind it)
