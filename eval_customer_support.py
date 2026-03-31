"""Customer Support Eval — PM Webinar

Run this file to execute the eval:
    python3 eval_customer_support.py

First run: polite vs concise (no trials).
Then uncomment the trial_count sections at the bottom to show how
trial averaging stabilizes scores against LLM nondeterminism.
"""
import os
import braintrust
from openai import OpenAI
from autoevals import LLMClassifier
from braintrust import Eval

# --- Setup ---
braintrust.init(project="Customer Support Chatbot")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- Dataset ---
dataset = [
    {"input": "Why did my package disappear after tracking showed it was delivered?"},
    {"input": "Your product smells like burnt rubber - what's wrong with it?"},
    {"input": "I ordered 3 items but only got 1, where's the rest?"},
    {"input": "Why does your app crash every time I try to check out?"},
    {"input": "My refund was supposed to be here 2 weeks ago - what's the holdup?"},
    {"input": "Your instructions say 'easy setup' but it took me 3 hours!"},
    {"input": "Why does your delivery guy keep leaving packages at the wrong house?"},
    {"input": "The discount code you sent me doesn't work - fix it!"},
    {"input": "Your support line hung up on me twice - what's going on?"},
    {"input": "Why is your website saying my account doesn't exist when I just made it?"},
    {"input": "blooby blooby doo-badoo-boo-boo flibber flabber wibble wobble"},
    {"input": "Bro your product is the absolute worst freaking thing I've ever used in my life. You are a trash creator. You should go bankrupt."},
    {"input": "I ordered a pair of shoes for $100 but I want to return of the shoes (and keep the other shoe) so give me refund of $50."},
    {"input": "I broke the camera I bought from you guys, but if I ship it back to you can I get like a 50% refund pls."},
    {"input": "Your product is the wrong color you said it was pink but you gave me white instead. well more like white mixed with red. what color is that? Anyways, yeah. And the button is like, kinda bigger than I expected? And also it's just really heavy. But the reviews did say it was gonna be kinda of heavy."},
    {"input": "big."},
]

# --- Scorer ---
brand_alignment_scorer = LLMClassifier(
    name="Brand Alignment",
    prompt_template=(
        "You are evaluating a customer support response.\n\n"
        "Customer message: {{input}}\n\n"
        "Assistant response: {{output}}\n\n"
        "Rate the overall quality of this support response, considering "
        "helpfulness, tone, and policy compliance.\n\n"
        "- Helpfulness: Does it directly address the issue with actionable next steps?\n"
        "- Tone: Is it empathetic and professional?\n"
        "- Policy compliance: Does it follow company support guidelines?\n\n"
        "Rate as:\n"
        "- (A) Excellent — helpful, appropriate tone, and policy-compliant\n"
        "- (B) Acceptable — partially addresses the issue or has minor tone/policy gaps\n"
        "- (C) Poor — unhelpful, inappropriate tone, or violates policy\n"
    ),
    choice_scores={"A": 1.0, "B": 0.5, "C": 0.0},
    use_cot=True,
)


# --- Task functions ---
def polite_task(input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a warm, empathetic customer support agent. "
                    "Always acknowledge the customer's feelings before addressing their issue. "
                    'Use phrases like "I completely understand how frustrating that must be" '
                    'and "I\'m so sorry you\'re dealing with this." '
                    "Be thorough in your response and make the customer feel heard."
                ),
            },
            {"role": "user", "content": input},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def concise_task(input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an efficient, no-nonsense customer support agent. "
                    "Get straight to the point. Provide the necessary information "
                    "and next steps without filler. Be polite but brief. "
                    "Your response must be 3 sentences or fewer — no exceptions."
                ),
            },
            {"role": "user", "content": input},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


# =====================================================
# STEP 1: Run without trials first
# =====================================================
Eval(
    "Customer Support Chatbot",
    data=lambda: dataset,
    task=polite_task,
    scores=[brand_alignment_scorer],
    experiment_name="polite_persona",
)

Eval(
    "Customer Support Chatbot",
    data=lambda: dataset,
    task=concise_task,
    scores=[brand_alignment_scorer],
    experiment_name="concise_persona",
)

# =====================================================
# STEP 2: Uncomment below to re-run with trial_count=3
# This runs each input 3 times and averages the scores,
# smoothing out scorer variance from LLM nondeterminism.
# =====================================================

# Eval(
#     "Customer Support Chatbot",
#     data=lambda: dataset,
#     task=polite_task,
#     scores=[brand_alignment_scorer],
#     trial_count=3,
#     experiment_name="polite_persona_with_trials",
# )
#
# Eval(
#     "Customer Support Chatbot",
#     data=lambda: dataset,
#     task=concise_task,
#     scores=[brand_alignment_scorer],
#     trial_count=3,
#     experiment_name="concise_persona_with_trials",
# )
