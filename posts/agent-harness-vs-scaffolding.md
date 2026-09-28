---
title: Agent harness vs scaffolding
slug: agent-harness-vs-scaffolding
description: Agent harness vs scaffolding, with a distinction you can build with. The scaffold is the fixed ground an agent is anchored to, and the harness is what the loop grows from its own failures.
subcategory: Agent Engineering
date: 2026-09-28
readtime: 7
glyph: Σ
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: agent harness vs scaffolding, what is an agent harness, harness engineering, agent scaffold
---
The scaffold is the fixed ground an agent is anchored to, which means
the model and the tool interfaces. The harness is what grows on that
ground, which means the control policy, skills and context that the
loop develops from its own failures. Many sources use the two words
for the same thing. Separating them tells you which parts of an agent
to keep fixed and which parts to let grow.

## What is an agent harness?

An agent harness is the software around a language model that lets it
operate as an agent. It manages tool use, memory, context, permissions
and the loop. A common shorthand is that an agent is a model plus a
harness.

## What is agent scaffolding?

Scaffolding is often used as another word for harness. Some writers
note that a scaffold suggests something temporary, to be taken down
when the model is capable enough, while a harness suggests something
the model keeps.

## The distinction we propose

The anthropologist Tim Ingold describes a spider. She extrudes her
silk from her own body and lays it down as she moves, and she
perceives and acts along those lines. She also anchors the silk to a
blade of grass or a twig that she did not make.

| Aspect | Scaffold | Harness |
|---|---|---|
| In the spider's world | Grass, post and twig | Silk |
| In an agent | The fixed model and tool interfaces | Control policy, skills, context and memory |
| Where it comes from | Given to the agent | Grown by the loop from its own failures |
| How to treat it | Keep it fixed, as the medium | Let it develop, and tend it |

Every rule in a working harness was added after something rubbed. A
model wandered, so a line was added to the prompt. A tool was misused,
so its schema was tightened. The harness is a record of past friction.

## Where agents break

The friction that produces an agent is concentrated at the knots where
harness meets scaffold. A rate limit fires. An interface changes. A
tool returns a format the policy did not expect. When the web's anchor
moves, the tension of the whole web shifts.

This is why the same model can behave as a capable agent in one
harness and an unreliable one in another. What is called agency in the
trace is an effect of the configuration staying stable.

## Agent harness vs agent loop, framework and MCP

| Term | Relation to the harness |
|---|---|
| Agent loop | The cycle of reading, acting and observing, which is one part of the harness |
| Agent framework | A library for building harnesses |
| MCP | A protocol for tool interfaces, which belongs to the scaffold |
| Orchestration | The harness of a system of several agents |

## What this means when building

- Hold the scaffold fixed during a piece of work, so that changes in
  behaviour can be traced to the harness.
- Let the harness be grown from observed failures, one boundary for
  each.
- When a benchmark score is reported, read it as a measurement of a
  model inside a harness, since the harness is part of what was
  measured.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Read further

- [What is an AI agent?](what-is-an-ai-agent-agentic-llm-definition.html)
  The full definition and every agent question in one place.
- [Are AI agents just prompts?](are-ai-agents-just-prompts.html)
- [Do AI agents have memory?](do-ai-agents-have-memory.html)
- The position paper,
  [What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
  (PDF).

[[shop]]

## Key Takeaways

- The scaffold is the fixed model and tool interfaces, and the harness is the control policy, skills and context grown on top of them.
- A harness is a record of past friction, with each rule added after something rubbed.
- Agents break at the knots where harness meets scaffold, so that is where to look first.
