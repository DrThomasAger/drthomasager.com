# AI just wants to make more AI

A quick draft. This is one part of a post about how an AI, handed a problem, reaches for more AI.

## What happened

I had an AI build a RuneLite plugin that shows who has PID in a fight. PID is read from timing. Every weapon's hit lands a known number of ticks after the attack starts, and when the other player was processed first, it lands one tick late. So the plugin needs to know, for each attack, which weapon it was and how many ticks that weapon's hit takes.

The AI's first answer was a learning system. It mined 1,567 of my recorded fights for every attack animation it could find, counted how often each animation's hits landed on each candidate delay, fitted every animation to a rule, shipped the result as a text file of learned weapons, and wrote a routine so the plugin would keep learning new weapons from each player's own fights, with a threshold of eight hits and a 75 percent fit before an animation counted as a weapon. It had an "attack book". It had tests for the book learning a weapon nobody had listed. It was proud of a scoring harness that said the learned reading agreed with the old one on 49,304 of 49,334 ticks.

Then I asked why it was learning any of this. The game already knows what every weapon is. Each item in the game's own data carries a category, the same number the combat interface uses to decide which attack styles a weapon offers. Crossbows are 37, bows 64, thrown weapons 24, ballistae 567, staves 1. The hit delay for each category is on the wiki in one line. A weapon released tomorrow carries its category from the day it comes out.

So the right answer was about forty lines that read the category from the game data and look up the delay. No learning, no text file, no thresholds, no fit. The AI had assumed a machine learning problem and read the data. It was a coding problem.

## Why it matters

The AI didn't do this because the learning answer was easier. It was far harder. It did it because that is what it reaches for. Given data and a pattern, it builds a learner, and then it builds the apparatus around the learner, and then it measures the learner, and each step feels like progress.

The fix came from asking one question about the game itself. Does the game already know this? It did. It always did.

## For the post

This goes beside the other cases where the AI, given a question, wanted to grow something that answers questions rather than find the answer that already existed. The pattern is the same each time. More AI, where a look at the source would do.
