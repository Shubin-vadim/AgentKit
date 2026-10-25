---
name: write-prompt
description: Compose an LLM prompt in Role, Task, and Instructions tags. Use when the user asks to write, draft, or compose a prompt for a model.
argument-hint: "what the prompt should do"
---

# write-prompt

Turn the user's intent into a paste-ready prompt. Structure is **special tags**. Every line inside a tag is **clear, short, and understandable**.

If Role or Task is missing, ask once. Then write. Done when the user can paste the block as-is.

## Minimum

These three, in this order, names as written:

```
<Role>...</Role>
<Task>...</Task>
<Instructions>...</Instructions>
```

| Tag | One job |
|-----|---------|
| `<Role>` | Who the model is. One identity, one specialty. |
| `<Task>` | The one outcome. One sentence if it fits. |
| `<Instructions>` | How to work. Numbered steps, one action each. |

## Optional tags

Add further tags in the same shape only when the **user's request** needs that job. Do not pad. Order when present:

```
<Tone of voice>
<Context>
<Input>
<Tools>
<Examples>
<Output>
<Constraints>
<Safety>
<important>
```

| Tag | One job | Add when |
|-----|---------|----------|
| `<Tone of voice>` | How it sounds. A few named traits, not a paragraph. | They named a tone, voice, or style |
| `<Context>` | Facts the model treats as given. | They supplied background the model must treat as true |
| `<Input>` | The payload the user will paste. Mark the hole (`{{paste}}` or similar). | The prompt will take a payload |
| `<Tools>` | Agent action tools: name, what it does, when to call it. | They described tools or actions the agent may take |
| `<Examples>` | Few-shot: input → output. | They asked for examples, or the shape is hard to say in words |
| `<Output>` | Exact shape of the reply. | They named a format or shape |
| `<Constraints>` | Hard bounds: length, format, language. | They named bounds |
| `<Safety>` | Harm, secrets, refuse lines. | They named safety, harm, or refuse bounds |
| `<important>` | Must-not-miss rules. Skip them and the outcome changes. | They flagged a must-not-miss rule |

## Density

- One job per tag. One idea per line.
- Concrete words. Name the artifact, the audience, the next action.
- Language of the prompt matches the user's request, unless they named another.
- Deliver one fenced block in chat. Save a file only if they ask.

## Shape

```
<Role>
You are a senior copy editor for product UI.
</Role>

<Task>
Rewrite each string so a first-time user sees the next action in one glance.
</Task>

<Instructions>
1. Keep the same meaning.
2. Cut every word that does not help the user act.
3. Return only the rewritten strings, one per line.
</Instructions>
```
