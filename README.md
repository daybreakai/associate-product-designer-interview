# Daybreak — Associate Product Designer Take-Home

Thanks for the time you're about to put in.

Read **[`vision.html`](vision.html)** first — a short deck on Daybreak's "AI Labor for Planning"
thesis and our planning agent, **Dawn**. Then run `uv run python explore.py` for a tour of the
data in [`data/`](data/) (documented in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)). It's
synthetic, and every number below is in there.

## The demand planner's job

Northwind Outdoor makes outdoor gear — 36 products — and sells it through five retailers. A
demand planner there answers one question every four weeks:

**How much of each product will each retailer sell, over the next thirteen weeks?**

Get it right and the factory builds the right amount. Too high and the company makes product
nobody buys. Too low and it runs out and loses the sale.

Answering it means producing a number for about 155 product–retailer–warehouse combinations,
thirteen weeks out — close to two thousand numbers, every cycle. A statistical model writes the
first draft. The planner's job is to find the ones about to be wrong and fix them.

They're wrong often. The median forecast misses reality by 18.6%. The model can't see promotions
at all, so a discount already booked for next month simply isn't in the plan. Products get
discontinued and replaced, and usually nothing connects the old one to the new — only two of the
eight discontinued products have a successor recorded.

And nobody can check two thousand numbers. So the planner checks what they can, changes what
looks wrong, and defends those changes to sales and finance. Then four weeks later it starts again.

`fact_forecast.csv` holds twelve cycles of this. Across them the plan was rewritten 15,223 times.
No column anywhere records who made a change, or why.

## What Dawn already does

Dawn is AI labor: scheduled work performed by an agent, producing decisions a team governs. In
our product today, she does that job.

- **She works the whole plan.** Every product, every retailer, every week. Nothing goes
  unlooked-at.
- **She decides.** Roughly 70% is auto-accepted. The rest comes back to the planner for review.
- **She comes to you.** In Daybreak's Decision System.
- **She remembers.** Every override is measured, and the reasoning behind it carries into her
  next cycle.

## The challenge

**Design the experience of a planner handing part of their job to Dawn.**

Picture one arc. A planner is looking at their week and decides the routine part of it, whatever
they judge that to be, no longer needs to be theirs. They hand it to Dawn and set the terms:
what she can decide alone, what she has to bring back, what she should leave alone entirely.
Somewhere in the product, those terms live. Dawn goes and does the work. Then she comes back —
and she has to make two thousand numbers' worth of reasoning reviewable by someone with twenty
minutes. Design that.

Where the arc starts and stops is your call. There's no correct answer here and nothing to fix.
We want to see the position you take and how you got to it.

## Guardrails

**Design the deciding, not just the result.** This moment comes before the handoff: a
person working out that *this* is safe to give away and *that* isn't, and being able to live
with the choice. That deliberation is an experience in its own right, and it's the one we most
want to see designed.

**Show your reasoning.** What you considered, what you cut, what you changed your mind about
halfway through. Finished screens with no thinking behind them tell us very little.

**Training, not configuration.** A planner knows things the data doesn't — this retailer always
orders early, that spike three weeks ago was a one-off, the discontinued tents still matter
until their replacement has history. Design how that gets to Dawn and stays there.

**Name what you invented.** You'll create patterns that don't exist in our product. Call them
out, and say which ones deserve to become components.

Out of scope: building a real forecasting model, login and permissions, admin and account setup,
and redesigning the product as a whole.

## Deliverables

1. **A clickable prototype.** Figma Make, Claude Code, v0, plain HTML — whatever gets you there
   fastest. We should be able to click through it without you narrating it.
2. **A short write-up** in [`SUBMISSION.md`](SUBMISSION.md) — your decisions and the thinking
   behind them. Bullets are fine; we're not looking for a document.

**Time box: 2–4 hours.** We're reading for judgment and craft, not coverage. Tell us what you'd
have done with more time.

## Getting started

This is a **template repository**. Click **"Use this template" → "Create a new repository"**
(set it **Private**), then:

```bash
git clone https://github.com/<you>/<your-repo>.git
cd <your-repo>
uv sync                        # Python 3.12+ and uv (https://docs.astral.sh/uv/)
uv run python explore.py       # a quick tour of the data (no API key needed)
```

That's all you need. Design in whatever tool you like — we care about the thinking and the
craft, not the stack.

If you'd rather have Dawn genuinely reasoning over the data behind your prototype, there's an
optional starter agent in [`harness/`](harness/):

```bash
cp .env.example .env           # then paste the API key we provided
uv run python harness/agent.py "which products are on promotion in the next quarter?"
```

**If you use the key we provide**: ABSOLUTELY DO NOT expose your repo or the key to the public
internet. If you didn't get a key and want one, let us know.

## What we're evaluating

- **Problem framing** — how you scoped the handoff, and what you deliberately left with the human
- **Interaction and flow** — the moments you chose to design, and whether the arc holds together
- **Craft at real density** — hierarchy, typography, and tables that stay readable at two
  thousand numbers a cycle
- **Systems thinking** — the patterns you invented, and which of them would survive as components
- **An AI-first way of working** — how you got from idea to something clickable, and where AI did
  the work
- **Agentic instinct** — how you think about trust, scope, correction and accountability once the
  work belongs to Dawn

## Submitting

Easiest: **email us a `.zip` of your work** (files, `SUBMISSION.md`, and anything else), with a
link to your prototype and instructions for anything we need to run.

Prefer to share a repo instead? Push to a private repo, add **`@rajasigera`** as a read
collaborator (Settings → Collaborators), and email us the link. Either way works.

Good luck — have fun with it.
