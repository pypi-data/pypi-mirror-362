---
title: doteval
hide:
  - navigation
  - toc
  - feedback
---

#

<figure markdown>
  ![doteval](assets/images/dottxt.png){ width="300" }
</figure>

<center>
    <h1 class="title">Enhanced Evaluation Suite for LLMs</h1>
    <p class="subtitle">Simple, powerful, and extensible evaluation framework for Large Language Models</p>
    [:fontawesome-solid-rocket: Get started](welcome.md){ .md-button .md-button--primary }
    [:fontawesome-brands-github: View on GitHub](https://github.com/dottxt-ai/doteval){ .md-button }

<div class="index-pre-code">
```bash
pip install doteval
```
</div>
</center>

---

## Why doteval?

<div class="grid cards" markdown>

-   :material-code-tags: **Simple API**

    ---

    Define evaluations with just a decorator. No complex setup required.

    ```python
    @foreach("question,answer", dataset)
    def eval_model(question, answer, model):
        response = model.generate(question)
        return exact_match(response, answer)
    ```

-   :material-test-tube: **pytest Integration**

    ---

    Run evaluations as tests with full pytest ecosystem support.

    ```bash
    pytest eval_gsm8k.py --session my_eval
    ```

-   :material-play: **Session Management**

    ---

    Resume interrupted evaluations automatically. Track progress across runs.

    ```bash
    doteval list
    doteval show my_eval_session
    ```

-   :material-rocket-launch: **Async & Concurrent**

    ---

    Scale evaluations with built-in async support and concurrency control.

    ```python
    @foreach("prompt,expected", dataset)
    async def eval_async(prompt, expected, model):
        return await model.generate_async(prompt)
    ```

</div>

## Quick Example

Evaluate your model on the GSM8K math dataset in just a few lines:

```python title="eval_gsm8k.py"
import functools
from doteval import foreach
from doteval.evaluators import exact_match

@foreach("question,answer", gsm8k_dataset("test"))
def eval_gsm8k(question, answer, generator, template):
    """Evaluate model performance on GSM8K math problems."""
    prompt = template(question=question)
    result = generator(prompt, max_tokens=100)
    return exact_match(result, answer)
```

Run it with pytest:

```bash
pytest eval_gsm8k.py::eval_gsm8k --session gsm8k_eval
```

View results:

```bash
doteval show gsm8k_eval
```

---

<div class="footer-info" markdown>

Built with ❤️ by [dottxt](https://dottxt.co) • [GitHub](https://github.com/dottxt-ai/doteval) • [PyPI](https://pypi.org/project/doteval/)

</div>
