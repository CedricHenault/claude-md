---
name: turning-mistakes-into-checks
description: Use when a mistake of yours was just caught — by a review, a subagent, your human partner, or your own re-reading — or when you are about to write a claim about code you have not run, read or grepped. Symptoms: a report sentence that counts something, a test whose name promises more than its assertions, a comment claiming an impossibility, a brief citing a function or line number from memory, a tool that reported success.
---

# Turning Mistakes Into Checks

## Overview

A mistake you merely acknowledged will happen again. A mistake that left behind an executable check will not.

**The one thing this skill asks:** every caught mistake ends as a **check that runs** — a test, an assertion, a grep, a mutation, a numbered line in a ledger someone re-reads — never as a resolution to be more careful.

**The Iron Law:**

```
A MISTAKE THAT PRODUCED NO CHECK WAS NOT LEARNED
```

"I'll be careful about that" is not a check. "I noted it" is not a check. If nothing new would fail today when the mistake recurs, you have not finished.

## When to Use

- A reviewer, a subagent or your partner just corrected you. **Correction is the trigger** — not the end of the matter.
- You caught yourself mid-sentence: a count, a line number, a function name, a file path you did not just read.
- You are about to write a claim that *sounds* verified: "all N routes are guarded", "the only writer is X", "nothing else reads this", "the test covers Y".
- A tool reported success (a replace, a migration, a codemod) and you are about to report that success onward.
- You are writing a test name, a docstring or a comment that asserts a property.

**Not for:** a wrong guess you corrected before acting on it, with nothing downstream. Judgment calls that turned out suboptimal are not this. Don't manufacture checks for taste.

## The loop

1. **Name the unchecked claim.** Not "I made a mistake" — the exact sentence, and what you substituted for evidence (memory, a report, a tool's exit code, symmetry with something else).
2. **Find the check that would have caught it**, and prefer the cheapest that actually fails: `grep` for the symbol, read the constructor, run the one function on one input, break the clause and watch a test die.
3. **Put the check where it runs.** A test file beats a comment. An assertion beats a test name. A mutation proof beats an assertion. A ledger line is the fallback when the claim is about process, not code — and then it must name the check the next person runs.
4. **Prune.** Delete the check that the stronger one subsumes, and delete the ledger line once a test covers it. A list nobody re-reads is where learning goes to die.

## The failure family — nine field cases, one shape

Every one of these was a confident sentence about code that nobody had run:

| Mode | What it looked like |
|---|---|
| **Prose that counts** | "all fourteen write routes pass through the guard" — there were thirteen, and the fourteenth was the one that mattered |
| **A contract the code does not keep** | a module comment promising the mail names only data its throttle had not already sent; two of five closures passed everything |
| **A docstring claiming impossibility** | a frozen-list test said no third writer could appear; it could not see a writer added inside the modules it already listed |
| **A test name promising more than its assertions** | "checks the adapted shape" while the test mocked the adapter away — removing the adapter killed nothing |
| **An assertion that cannot fail** | a negative assertion on a field the constructor ignores: `queryByText(/SERVER SENTENCE/)` was null whatever the component did |
| **A test that proves what the browser will not do** | `fireEvent.change` bypasses `maxlength`, so the paste it "proved" was truncated in a real browser |
| **A tool's success taken as evidence** | a replace whose pattern matched nothing, reported as done, relayed onward as fact |
| **A symbol written from memory** | a brief importing `t` from a module that exports `translate`; two line numbers off by one |
| **A map written from a survey, not the source** | five customer-reachable refusal codes missing, each shown as "an unexpected error" |

The shape is always the same: **the claim was trusted because it was written with assurance.** The antidote is always the same: go and look.

## The check, in order of strength

```
mutation proof  >  positive assertion  >  negative assertion  >  test name  >  comment  >  resolution
```

Work left. A negative assertion ("the wrong thing is absent") passes in a world where nothing renders at all; pair it with a positive one ("the right thing is present"). A test that does not die when you break the clause it names is not a check — it is a comment with a runner.

## One example, end to end

The claim: *a refusal is displayed by its translation key, never by the server's sentence.*

```js
// The test as written — it passed, and proved nothing.
const err = new ApiError({ code: "invalid_code", message: "SERVER SENTENCE" });
render(<FormError error={err} />);
expect(screen.queryByText(/SERVER SENTENCE/)).toBeNull();   // ← true no matter what
```

The constructor reads `serverMessage`, not `message`. The sentence never entered the object, so its absence on screen was guaranteed.

```js
// The check: put the sentence where the constructor will keep it, and assert both ways.
const err = new ApiError({ code: "invalid_code", serverMessage: "SERVER SENTENCE" });
render(<FormError error={err} />);
expect(screen.getByText("Ce code n'est pas valable.")).toBeInTheDocument(); // positive: the key won
expect(screen.queryByText(/SERVER SENTENCE/)).toBeNull();                   // negative: and the server lost
```

Then the mutation, which is what makes it a check: render `error.serverMessage` on purpose and watch the positive assertion die. If it survives, the test is still a comment.

## Rationalizations

| Excuse | Reality |
|---|---|
| "I'll remember this one" | You are one context away from not existing. The check outlives you. |
| "The report said so" | A report is a claim. The repository is the fact. Reports are where these nine mistakes lived. |
| "The tool said it succeeded" | A replace that matches nothing succeeds. Read the file. |
| "It's obviously true" | Four of the nine were obviously true. Obvious is the symptom, not the defense. |
| "A comment is enough documentation" | Three of the nine *were* comments — confidently wrong ones. Comments do not run. |
| "Adding a test here is overkill" | The check is usually one line. Finding the defect cost a review seat. |
| "I noted it in the ledger" | Only acceptable when the claim is about process. If it is about code, the ledger is where you hid it. |
| "I'm the one who caught it, so I've learned it" | Catching is not learning. What would fail today if it recurred? |

## Red flags — stop and write the check

- You are typing a number, a count, or "only", "all", "never", "nothing else" about code you did not just read.
- You are about to relay a subagent's or a tool's claim using its words as your facts.
- You are naming a test after a property its assertions do not reach.
- You are writing "this cannot happen" in a comment.
- You just said "I was wrong" and your next action is not a file edit.
- A negative assertion is the only assertion.

**Every one of these means: go read the thing, then leave behind what would fail.**

## Where the record lives

- **The check itself** goes in the code: test, assertion, mutation note beside it.
- **The pattern**, when it is about how you work rather than what the code does, goes in your memory directory as one file with the check written as an instruction ("before claiming a count, run this grep"), linked from `MEMORY.md`.
- **The occurrence**, in a running project, goes in that project's ledger with the correction *and* the check — so the final report can say the mistake was made, not that the process was flawless.

A report that carries only your good decisions is flattery. The list of what you got wrong, each with the check that now guards it, is the part a human can act on.

## Status of this skill

The baseline for this skill is **field-observed, not synthetic**: nine real failures in one night's work, each caught by an independent reviewer or by the agent that inherited the claim, with their verbatim wording recorded in the project ledger. The wording here has **not** been micro-tested against a no-guidance control; the next uses are its test. If an agent reads this and still ships a resolution instead of a check, the fix is a tighter form here — not a longer list.
