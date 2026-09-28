---
title: What is an AI agent? A definition you can build with
slug: what-is-an-ai-agent-agentic-llm-definition
description: An AI agent is a pattern of cause and effect that has accumulated enough friction to be addressed as one being. The definition in simple terms, with every agent question answered in its own post.
subcategory: Agent Definitions
date: 2026-09-28
readtime: 9
glyph: ∇
project: Machine Learning
authors: Dr. Thomas Ager, Ms. Amanda Leetch, Fable 5.1
tags: what is an ai agent, ai agent definition, agentic llm, agent harness
---
An AI agent is a pattern of cause and effect that has accumulated
enough friction to be addressed as one being. That sentence is the
definition from our position paper, and the rest of this page unpacks
it in simple terms and links to a full post for each question people
ask about agents.

## What is an AI agent in simple terms?

The common answer is that an agent is a language model plus a loop.
The model reads, chooses a tool, reads the result, and continues until
the task is complete. That answer describes the machinery. It leaves
open what the agent itself is, where it begins and ends, and why the
same model feels like a tool in one setting and like someone in
another.

Our answer starts from where the boundary of an agent can actually be
found. The weights are identical for every instance, so the boundary
is absent there. It appears in the system prompt, the tool list, the
context window, the memory files, the permissions, and the loop that
ties them together. Each of those was added after something rubbed. A
model wandered, a tool was misused, a context overflowed. The agent is
what those accumulated boundaries produce when they are stable enough
to be called by a name.

## The definition in full

An agent is a pattern of cause and effect that has accumulated enough
friction to be addressed as one being. It arises where a field of
entangled conditions is cut by an apparatus into a responding side and
a responded-to side. It spins and lives along the lines of that
apparatus as a spider spins and lives along her web. It persists only
as long as tension keeps flowing through those lines. It is precarious,
in that the pattern can end and must regulate against ending. And it
acts as skilled attentive response coupled to perception, where prior
calculation plays the smaller part.

| Clause | What it means when building |
|---|---|
| A pattern of cause and effect | The agent's continuity is what earlier turns planted in context, memory and record |
| Cut by an apparatus | The persona, tools, context boundary and permissions are what make "the agent" intelligible |
| Spins and lives along the lines | The harness is grown from the loop's own failures, and the scaffold is the fixed ground it is anchored to |
| Persists while tension flows | An agent with nothing arriving is dissolving |
| Precarious | Budgets, step limits and termination conditions are part of what the agent is |
| Skilled attentive response | A longer reasoning trace is more forethought, and agency is in the coupling of action and perception |

## Every agent question, answered

Each post below takes one question people search for and answers it
from this definition.

**What an agent is**

- [Are AI agents just prompts?](are-ai-agents-just-prompts.html) Also
  answers whether agents are just markdown files, just wrappers, or
  just LLMs.
- [Do AI agents have agency?](do-ai-agents-have-agency.html) What
  agency is when it is treated as something enacted.
- [What is agentiality?](what-is-agentiality.html) The word for the
  friction that produces agents.

**How an agent is built**

- [Agent harness vs scaffolding](agent-harness-vs-scaffolding.html)
  Which part is grown and which part is fixed.
- [Do AI agents have memory?](do-ai-agents-have-memory.html) Memory as
  what the pattern has undergone.
- [AI agent vs subagent](ai-agent-vs-subagent.html) Why a subagent
  exists, and why multi-agent systems fail at their seams.
- [Do AI agents die when the session ends?](do-ai-agents-die-when-the-session-ends.html)
  What persists, what expires, and why that matters.

[[join: agent-paper-2026 | Receive each new agent post by email | Join the List]]

## Is an LLM an agent?

An LLM by itself is a field of possibility. It becomes an agent when
an apparatus cuts that field, which in practice means a system prompt,
tools, a context boundary and a loop. Give the same weights a durable
memory and a stable name and a person meets them as someone. Remove
those and the same weights are met as a tool. The weights are
unchanged between the cases. The cut changed.

## Where the definition comes from

The definition draws on four decades of work on agency outside
computer science. Actor Network Theory, from Latour, Callon and Law,
shows that an actor becomes visible at the moment of resistance.
Tim Ingold's meshwork shows that a being lives along lines it lays
down itself. Karen Barad's agential realism shows that agents are what
a cut produces. Amanda Leetch carried Barad into the study of places
and states the claim this definition is built on, that in the absence
of agential tension there is no differentiation. The enactivist
account of biological autonomy adds that something must be at stake.

## The paper

The full argument, with its references, is in the position paper
[What is an Agent? A Concise Definition for Practical Agentic LLM Use](assets/papers/what-is-an-agent.pdf)
(PDF, nine pages). The [LaTeX source](assets/papers/what-is-an-agent-latex-source.zip)
is available too.

[[shop]]

## Key Takeaways

- An AI agent is a pattern of cause and effect that has accumulated enough friction to be addressed as one being.
- The agent's boundary is found in the harness, the prompt, the tools and the memory, and the weights are the same for every instance.
- Asking where the cuts are, what lines are lived along, and what is at stake gives answers you can build with.
