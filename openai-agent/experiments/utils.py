import json

from agents import RunResult


def save_results(
    write_folder: str, stock_id: str, result: RunResult, elapsed_time: float
) -> None:
    usage = result.context_wrapper.usage
    nrequests = usage.requests
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    total_tokens = usage.total_tokens
    steps = [item.to_input_item() for item in result.new_items]

    with open(f"{write_folder}/{stock_id}.json", "w") as f:
        json.dump(
            {
                "steps": steps,
                "usage": {
                    "requests": nrequests,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                },
                "time": elapsed_time,
            },
            f,
            indent=4,
        )

    with open(f"{write_folder}/{stock_id}_output.json", "w") as f:
        json.dump(result.final_output.model_dump(), f, indent=4)
