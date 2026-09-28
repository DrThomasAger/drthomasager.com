---
title: Do AI agents die when the session ends?
slug: do-ai-agents-die-when-the-session-ends
description: Do AI agents die, persist or expire when a session ends? The pattern in the context ends, what was written down continues, and that an agent can end is part of what makes it an agent.
subcategory: Agent Engineering
date: 2026-09-28
readtime: 6
glyph: ∞
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: do ai agents die, do ai agents persist, do ai agents expire, agent session, precariousness
---
When a session ends, the pattern that was running in the context ends
with it. What was written to memory files, transcripts and records
continues, and a later session that loads them carries the pattern
forward. That an agent can end is part of what makes it an agent.

## What ends and what continues

| Part of the agent | When the session ends |
|---|---|
| The working context | Ends |
| Reasoning that was never written down | Ends |
| Memory files | Continue |
| Transcripts and logs | Continue |
| Files and changes the agent made | Continue |
| The harness, prompt and tools | Continue, ready for the next session |
| The model weights | Unchanged throughout |

## Do AI agents persist?

An agent persists to the extent that its inscriptions do. A memory
file, a handover document or a transcript lets relations built in one
session travel to the next. An agent with no memory is rebuilt from
nothing every time, which is why it feels less like a being.

## Do AI agents expire?

Every deployed agent has conditions under which it stops. A token
budget, a step limit, a timeout, a termination condition, a context
that fills. These are usually treated as operational details. In our
definition they are part of what the agent is.

## Why being able to end matters

The enactivist account of agency, from Di Paolo and colleagues, holds
that an agent's identity must be precarious. It can be lost, and the
agent acts to keep it. Without something at stake, responding to the
world is reaction and falls short of agency.

An agent also needs something arriving. A long-running agent stays in
being through a continuing supply of friction, which means new tool
results, new errors and new inputs. With nothing arriving, the pattern
dissolves.

## What this means when building

- Decide what is written down before the session ends, since that is
  what continues.
- Write handover documents for the next session to read first.
- Treat budgets and step limits as part of the agent's design, and
  let the agent see them so it can act within them.
- Keep a long-running agent coupled to live input.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Read further

- [What is an AI agent?](what-is-an-ai-agent-agentic-llm-definition.html)
  The full definition and every agent question in one place.
- [Do AI agents have memory?](do-ai-agents-have-memory.html)
- [Do AI agents have agency?](do-ai-agents-have-agency.html)
- The position paper,
  [What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
  (PDF).

[[shop]]

## Key Takeaways

- The working context ends with the session, and whatever was written down continues.
- An agent persists through its inscriptions, which are memory files, transcripts and handover documents.
- Budgets, limits and termination conditions are part of what an agent is, and being able to end is a condition of agency.
