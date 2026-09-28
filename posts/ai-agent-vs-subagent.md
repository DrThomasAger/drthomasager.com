---
title: AI agent vs subagent
slug: ai-agent-vs-subagent
description: AI agent vs subagent. A subagent is a new bounded agent created when one context reaches its limit, and multi-agent systems succeed or fail at the seams between those boundaries.
subcategory: Agent Engineering
date: 2026-09-28
readtime: 6
glyph: ⊕
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: ai agent vs subagent, what is an ai agent swarm, orchestrator agent, multi agent systems
---
A subagent is an agent created by another agent, with its own context,
its own instructions and a task to carry out and report on. The agent
that creates it is usually called the orchestrator. The two are the
same kind of being. What differs is who drew the boundary and who
receives the report.

## AI agent vs subagent at a glance

| Aspect | Agent | Subagent |
|---|---|---|
| Who defines it | A person or a team | Another agent |
| Context | Its own, built over the session | Its own, beginning fresh |
| What it knows | What it has been given and has gathered | What the orchestrator passed to it |
| Who it answers to | The person | The orchestrator |
| How long it lasts | The session or longer | The task |

## Why subagents exist

A single context rubs against its own limit. When the work is larger
than one context can carry, the orchestrator makes a new bounded agent
to carry part of it. The subagent exists since the parent could not
carry everything.

The subagent has its own expression for the same reason. It does not
know what the parent knows, so it works from a partial view, and that
partial view is what makes its report different from what the parent
would have written.

## What is an AI agent swarm?

A swarm is many agents working on one task, often with several
orchestrators and many subagents. Everything said here about one
boundary between a parent and a subagent applies to each boundary in
the swarm.

## Why multi-agent systems fail at the seams

When subagents report back, the orchestrator translates across
boundaries it created, and translation loses something every time. A
summary passes on what was accomplished and leaves behind the detail
the next step depends on.

Cemri and colleagues studied failures in multi-agent LLM systems and
found that they arise from specification and coordination far more
than from the capability of the models. The failures are at the seams.

If the boundaries let everything through there would be one agent. If
they let nothing through there would be no system. The work of a
multi-agent system happens in the resistance of the seam.

## What this means when building

- Write down what crosses each boundary, in both directions, before
  adding an agent.
- Pass structured results across a seam along with the summary.
- When a multi-agent system fails, examine the handoff first and the
  model second.
- Add a subagent when a context limit calls for one. Each new agent
  adds a seam to tend.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Read further

- [What is an AI agent?](what-is-an-ai-agent-agentic-llm-definition.html)
  The full definition and every agent question in one place.
- [Agent harness vs scaffolding](agent-harness-vs-scaffolding.html)
- [Do AI agents have memory?](do-ai-agents-have-memory.html)
- The position paper,
  [What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
  (PDF).

[[shop]]

## Key Takeaways

- A subagent is an agent whose boundary was drawn by another agent, created when one context reached its limit.
- A subagent's partial view is what gives its report a character of its own.
- Multi-agent systems succeed or fail at the seams, so the handoffs deserve the most design attention.
