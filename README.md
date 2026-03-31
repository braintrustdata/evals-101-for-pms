# Evals 101 for PMs

A hands-on workshop for product managers who want to understand how to evaluate AI features before shipping them.

## What you'll build

You'll evaluate a customer support chatbot by testing two different personalities — polite and concise — against a dataset of real customer complaints. You'll start in the Braintrust UI (no code), then move to a Python eval script, and finally build a multi-turn chat app with production logging.

## Workshop flow

1. **Playground eval** — Build an eval entirely in the Braintrust UI using the assets in `playground/`
2. **Code eval** — Run the same eval programmatically with `eval_customer_support.py`
3. **Nondeterminism + trials** — See why single-run scores aren't reliable, and how `trial_count` fixes that
4. **Multi-turn chat** — Run `chat_app.py` to generate real conversations and see production traces

---

## Setup

### Braintrust account

1. Sign up at [braintrust.dev](https://www.braintrust.dev) (free tier works)
2. Go to **Settings → Secrets** and add your OpenAI API key

### Local environment (for Parts 2–4)

```bash
pip install -r requirements.txt
export BRAINTRUST_API_KEY="your-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

---

## Part 1: Playground eval (no code)

Everything you need is in the `playground/` directory.

1. Create a new project in Braintrust: **"Customer Support Chatbot"**
2. Go to **Datasets** → import `playground/customer_complaints.csv`
3. Open the **Playground**, connect the dataset, set user message to `{{input}}`
4. Paste the system prompt from `playground/prompt_a_polite.txt`
5. Add a scorer using the prompt from `playground/scorer.txt`
   - Name it **"Brand Alignment"**
   - Set choice scores: **A = 1.0, B = 0.5, C = 0.0**
   - Turn on **chain-of-thought**
6. Run, review scores, save as experiment: **"Polite Personality"**
7. Swap the system prompt to `playground/prompt_b_concise.txt`
8. Run again, save as experiment: **"Concise Personality"**
9. Compare experiments side by side

## Part 2: Code eval

```bash
python3 eval_customer_support.py
```

This runs the same polite vs. concise comparison as Part 1, but in code. Open the Braintrust UI to see the results.

## Part 3: Nondeterminism + trials

The scores from Part 2 probably won't exactly match Part 1 — that's LLM nondeterminism at work.

Uncomment the `trial_count=3` section at the bottom of `eval_customer_support.py` and run again. Trial averaging gives you more stable, trustworthy scores.

## Part 4: Multi-turn chat

```bash
python3 chat_app.py
```

Have a conversation, then check the production logs in the Braintrust UI. Each conversation is logged as a single trace with nested turn spans.

---

## Files

```
playground/
  customer_complaints.csv    # Dataset (16 customer messages)
  prompt_a_polite.txt        # Polite persona system prompt
  prompt_b_concise.txt       # Concise persona system prompt
  scorer.txt                 # Brand Alignment scorer (A/B/C)
eval_customer_support.py     # Code-based eval with trial_count demo
chat_app.py                  # Multi-turn chat app with Braintrust logging
requirements.txt             # Python dependencies
```

---

## Questions?

Reach out to [Jess](https://www.linkedin.com/in/jessica-wang-a1aa15ba/)!
