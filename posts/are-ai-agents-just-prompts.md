---
title: Are AI agents just prompts?
slug: are-ai-agents-just-prompts
description: Are AI agents just prompts, just markdown files, just wrappers, or just LLMs? The prompt is one of the cuts that produces an agent, and the agent is what all the cuts produce together.
subcategory: Agent Definitions
date: 2026-09-28
readtime: 6
glyph: λ
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: are ai agents just prompts, are ai agents just markdown files, are ai agents just wrappers, system prompt
---
An AI agent is more than a prompt, and the prompt is a real part of
it. The prompt is one of the boundaries that produces the agent. The
agent is what all of the boundaries produce together, which includes
the tools, the context window, the memory, the permissions and the
loop.

## Why it looks like agents are just prompts

Open the folder of a working agent and most of what is there is text.
A system prompt. A file of instructions. Skill files in markdown. It
is reasonable to look at that and conclude the agent is a prompt with
a name.

The observation is accurate about where the agent's character is
written. Nobody can find the agent in the weights, since the weights
are identical for every instance. What differs from one agent to the
next is the text and configuration around the model.

## What the prompt does

A system prompt says "you are X and you will do Y in this way". That
sentence is a boundary. It divides the field of everything the model
could be into the part that is this agent and the part that is
excluded. In our definition this is a cut, and an agent arises where
a field is cut into a responding side and a responded-to side.

The prompt is one cut among several.

| Boundary | What it divides |
|---|---|
| System prompt | Who the agent is from everything else the model could be |
| Tool schema | The ways the agent may touch the world from all other ways |
| Context window | What the agent presently perceives from what is beyond it |
| Memory files | What carries forward from what ends with the session |
| Permissions | What the agent may do alone from what needs a person |
| The loop | Continuing from stopping |

## Are AI agents just markdown files?

Markdown files are where many of these boundaries are written, so an
agent's definition can live in markdown. The agent itself is the
pattern that runs when a model reads those files inside a loop, with
tools answering and results returning. The file is the inscription.
The agent is what the inscription makes possible each time it is
read.

## Are AI agents just wrappers, or just LLMs?

"Wrapper" suggests a thin layer around the part that matters. The
harness is where most of an agent's behaviour is decided, and the same
model behaves as a different agent inside a different harness. "Just
an LLM" has the same difficulty in the other direction. An LLM with
no boundary around it is a field of possibility, and it becomes an
agent when it is cut.

## What this means when building

- Write the prompt as a boundary. Say what the agent is, and the
  exclusions follow.
- Design the cuts first and choose the model second.
- When an agent behaves unexpectedly, look at which boundary was
  active. The cause is usually found there.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Read further

- [What is an AI agent?](what-is-an-ai-agent-agentic-llm-definition.html)
  The full definition and every agent question in one place.
- [Agent harness vs scaffolding](agent-harness-vs-scaffolding.html)
- The position paper,
  [What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
  (PDF).

[[shop]]

## Key Takeaways

- The prompt is one of the boundaries that produces an agent, alongside tools, context, memory, permissions and the loop.
- Markdown files carry the agent's inscription, and the agent is the pattern that runs when they are read in a loop.
- The same model inside a different harness is a different agent.
