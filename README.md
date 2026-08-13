# 📧 Email Intent Parser

**Turns unstructured customer emails into structured triage data — intent, urgency, tone, and next action — in under 2 seconds.**

Built as a proof-of-concept for the kind of layer a support or sales team could plug in front of an inbox to auto-route tickets, instead of a human reading and tagging every email manually.

🔗 **[Live Demo](https://email-intent-parser-2026.streamlit.app/)**
🎥 **60-sec walkthrough:** [Loom link here](#)

---

## The problem this solves

Support and sales inboxes are full of unstructured text that still needs to answer four questions before anyone can act on it:
- What does this person actually want? (intent)
- How fast do we need to respond? (urgency)
- Are they about to churn or escalate? (tone)
- What's the next concrete step? (action)

Right now that triage is manual. This project shows how an LLM with a **strict output schema** — not a chatbot, not free text — can do that first pass reliably enough to plug into a real workflow.

## Example

**Input:**
> "I've been charged twice this month and support hasn't replied in 3 days. This is the second time this has happened. I'm about done with this product."

**Output:**
```json
{
  "sender_intent": "billing",
  "urgency_score": 4,
  "tone": "frustrated",
  "action_required": "Escalate to billing team for duplicate charge refund and flag account for retention follow-up"
}
```

## How it works

1. Raw email text goes in via a Streamlit UI
2. A structured prompt + **JSON Schema (strict mode)** — not regex, not "please respond in JSON" — constrains the model to return exactly four fields, every time
3. Output renders as a clean triage card: intent, urgency (color-coded), tone, and the recommended next action

## Design decisions

**Why strict JSON schema instead of prompting for JSON and parsing it:**
Free-text-then-parse breaks in production — models occasionally add a preamble, rename a key, or return malformed JSON. Schema-enforced structured output (`response_format` in JSON mode) removes that failure class entirely. This is the same pattern used across every project in this sprint, applied here to a different problem — the point is a repeatable approach to reliability, not a one-off script.

**Why low temperature (0.3):**
This is extraction, not creative generation. Lower temperature keeps intent/urgency classification consistent across near-identical inputs — important if this were ever compared or audited.

**Why a request cap on the public demo:**
The live demo runs on a real API key. A session-based limit (5 requests) plus an input length cap protects against cost/rate-limit abuse from public traffic, without affecting normal evaluation use.

## Tech stack

- **LLM:** Groq API with structured output (JSON mode)
- **Frontend:** Streamlit
- **Language:** Python 3.11
- **Deployment:** Streamlit Community Cloud

## Run it locally

```bash
git clone https://github.com/codewith-krishh/email-intent-parser.git
cd email-intent-parser
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Run:
```bash
streamlit run app.py
```

## What I'd add for production

- Confidence scores per field, with human-in-the-loop review below a threshold
- Structured logging of every classification for accuracy auditing over time
- Webhook/API endpoint version (not just UI) so it can plug directly into a CRM or helpdesk tool
- Batch mode for processing an inbox export rather than one email at a time

---

**Part of a 4-week applied prompt engineering sprint** — building toward production-ready AI tooling for SaaS support and sales workflows.

Built by [Krish Manji](https://github.com/codewith-krishh) · [LinkedIn](https://linkedin.com/in/krish-manji011) · [X](https://x.com/Born_TechK)