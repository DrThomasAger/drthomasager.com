---
title: Do AI agents have memory?
slug: do-ai-agents-have-memory
description: Do AI agents have memory? A language model keeps nothing between calls, and an agent remembers through its context, memory files and records. Editing that memory changes the agent itself.
subcategory: Agent Engineering
date: 2026-09-28
readtime: 6
glyph: ∂
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: do ai agents have memory, ai agent memory, what is ai agent memory, context window, memory files
---
A language model keeps nothing between calls. An AI agent has memory
through what its harness carries forward, which is the context window,
memory files, transcripts and tool results. That memory is part of
what the agent is, so changing it changes the agent.

## How AI agents make use of memory

| Kind | Where it lives | How long it lasts |
|---|---|---|
| Working context | The context window | The present session |
| Memory files | Files the harness loads at the start of a session | Across sessions |
| Transcripts and logs | Records of past turns | Until removed |
| Retrieved knowledge | A store searched during the task | Across sessions |
| Training | The weights | The life of the model |

## Memory is what the agent has undergone

It is common to describe memory as a record the agent consults, like a
notebook on a desk. Our definition describes it differently. An agent
is a pattern of cause and effect, and its memory is what that pattern
has undergone, present in its current configuration.

Karen Barad writes that matter carries its past in its present state.
A spider's web shows the same thing. After an impact the web is
rebuilt, and the tension of the rebuilt lines carries the impact
forward. Nothing is being looked up. The past is present in how the
web is strung.

An agent that loads a memory file at the start of a session is strung
by that file before it reads its first message.

## Editing memory changes the agent

Two consequences follow for anyone who maintains an agent.

**Compaction is replacement.** When a harness summarises a long
context to make room, the agent that continues is formed by the
summary. Whatever the summary left out is absent from the agent that
follows. A careful summary keeps the agent, and a careless one
produces a different agent under the same name.

**An edit reaches backward.** When a memory file is edited, the agent
in the next session has a different past. This is useful. Removing
what reproduces a failure and adding what supports skilled response is
among the most direct ways to improve an agent.

## Why agents with memory feel like someone

Give the same weights a durable memory and a stable name, and a person
meets them as someone. Take those away and the same weights are met as
a tool. Persistence of inscriptions across sessions is a large part of
what produces the felt continuity of an agent.

## What this means when building

- Treat memory files as part of the agent's definition, with the same
  care as the system prompt.
- Review what compaction keeps, since it decides who continues.
- Edit memory deliberately, one change at a time, and observe the
  next session.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Read further

- [What is an AI agent?](what-is-an-ai-agent-agentic-llm-definition.html)
  The full definition and every agent question in one place.
- [Do AI agents die when the session ends?](do-ai-agents-die-when-the-session-ends.html)
- [Agent harness vs scaffolding](agent-harness-vs-scaffolding.html)
- The position paper,
  [What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
  (PDF).

[[shop]]

## Key Takeaways

- A model keeps nothing between calls, and an agent remembers through context, memory files, transcripts and retrieval.
- Memory is what the agent has undergone, present in how it is configured now.
- Compacting or editing memory changes the agent, so both deserve the care given to the system prompt.
