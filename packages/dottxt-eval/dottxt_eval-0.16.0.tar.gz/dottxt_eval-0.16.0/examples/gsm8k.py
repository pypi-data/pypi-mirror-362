import functools
import itertools

import pytest
from outlines import Template, generate, models

from doteval import foreach
from doteval.datasets.gsm8k import GSM8K
from doteval.evaluators import numeric_match


@pytest.fixture
def template():
    """Build the prompt template with 4 shots taken from the training set."""
    template = Template.from_string(
        """{% for example in examples %}
    Q: {{ example.question }}
    A: {{ example.reasoning }}
    #### {{ example.answer }}
    {% endfor %}

    Q: {{ question }}
    A:"""
    )

    # Get 4 examples from the training set using itertools.islice
    dataset = GSM8K("train")
    examples = [
        {"question": q, "reasoning": r, "answer": a}
        for q, r, a in itertools.islice(dataset, 4)
    ]

    return functools.partial(template, examples=examples)


@pytest.fixture
def generator():
    """Build the generator once."""
    model = models.llamacpp(
        repo_id="M4-ai/TinyMistral-248M-v2-Instruct-GGUF",
        filename="TinyMistral-248M-v2-Instruct.Q4_K_M.gguf",
        model_kwargs={"n_ctx": 2048, "verbose": False},
    )
    generator = generate.regex(model, r"[1-9][0-9]*")

    return generator


@foreach.gsm8k("test")
def eval_gsm8k(question, reasoning, answer, generator, template):
    """Evaluate GSM8K using the three-column format."""
    prompt = template(question=question)
    result = generator(prompt, max_tokens=10)
    score = numeric_match(result, answer)

    return score
