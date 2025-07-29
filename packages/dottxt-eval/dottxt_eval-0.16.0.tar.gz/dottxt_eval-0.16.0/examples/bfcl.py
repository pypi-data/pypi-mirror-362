"""Example of using the BFCL dataset for function calling evaluation."""

import json

import doteval


@doteval.eval
def evaluate_function_calling(question, schema, answer):
    """Evaluate a model's function calling capabilities.

    This function tests whether a model can correctly:
    1. Select the appropriate function(s) from available schemas
    2. Extract the right parameters from the user query
    3. Format the function call correctly

    Args:
        question: The user's natural language query
        schema: JSON string containing available function definitions
        answer: JSON string containing expected function call(s)

    Returns:
        Score indicating whether the model made the correct function call
    """
    # Parse the available functions
    available_functions = json.loads(schema)

    # In a real implementation, you would use your model here
    # For example:
    # response = model.generate_function_call(
    #     user_query=question,
    #     functions=available_functions,
    #     system_prompt="You are a helpful assistant that calls functions..."
    # )

    # For demonstration, return a dummy response
    response = []

    # Parse the expected answer
    expected_calls = json.loads(answer)

    # Compare the response with expected calls
    if response == expected_calls:
        return doteval.Score(value=1.0, passed=True)
    else:
        return doteval.Score(value=0.0, passed=False)


# Example: Evaluate on simple function calling
if __name__ == "__main__":
    # Run on simple variant (single function selection)
    print("Evaluating simple function calling...")
    simple_results = doteval.run(
        evaluate_function_calling, dataset="bfcl", variant="simple"
    )
    print(f"Simple accuracy: {simple_results['accuracy']:.2%}")

    # Run on multiple variant (select from multiple functions)
    print("\nEvaluating multiple function selection...")
    multiple_results = doteval.run(
        evaluate_function_calling, dataset="bfcl", variant="multiple"
    )
    print(f"Multiple accuracy: {multiple_results['accuracy']:.2%}")

    # Run on parallel variant (multiple function calls)
    print("\nEvaluating parallel function calling...")
    parallel_results = doteval.run(
        evaluate_function_calling, dataset="bfcl", variant="parallel"
    )
    print(f"Parallel accuracy: {parallel_results['accuracy']:.2%}")


# Advanced example with custom evaluation logic
@doteval.eval
def evaluate_with_partial_credit(question, schema, answer):
    """Evaluate function calling with partial credit for correct function selection."""
    available_functions = json.loads(schema)
    expected_calls = json.loads(answer)

    # Mock model response
    # In practice: response = your_model.generate(question, available_functions)
    response = []

    score = 0.0

    # Give partial credit for:
    # - Correct function name selection (0.5 points)
    # - Correct parameters (0.5 points)

    if len(response) > 0 and len(expected_calls) > 0:
        # Check if function names match
        response_func_names = [list(call.keys())[0] for call in response]
        expected_func_names = [list(call.keys())[0] for call in expected_calls]

        if set(response_func_names) == set(expected_func_names):
            score += 0.5

            # Check if parameters match
            if response == expected_calls:
                score += 0.5

    return doteval.Score(value=score, passed=(score == 1.0))
