import re
import asyncio
import argparse
import json
from typing import TypedDict, List
from pathlib import Path
import fleet as flt
from nova_act import NovaAct, ActResult
from dotenv import load_dotenv

load_dotenv()


MAX_STEPS = 30


class Problem(TypedDict):
    id: str
    problem: str
    category: str
    difficulty: str
    verifier_func: str


def extract_function_name(function_str: str) -> str | None:
    match = re.search(r"(?:async\s+)?def\s+(\w+)\s*\(", function_str)
    if match:
        return match.group(1)
    raise ValueError(f"No function name found in {function_str}")


async def main():
    parser = argparse.ArgumentParser(
        description="Load and display Jira problems from JSON file"
    )
    parser.add_argument(
        "json_file", type=str, help="Path to the JSON file containing problems"
    )
    args = parser.parse_args()

    file_path = Path(args.json_file)
    if not file_path.exists():
        raise FileNotFoundError(f"Error: File '{args.json_file}' not found")

    env = await flt.env.make_async("fira:v1.2.7")
    print(f"New Instance: {env.urls.app}")

    successes = 0

    try:
        with open(args.json_file, "r") as f:
            data = json.load(f)
        problems: List[Problem] = data["problems"]

        print(f"Loaded {len(problems)} problems from '{args.json_file}'")

        for i, problem in enumerate(problems):
            print(f"Solving problem {i + 1} of {len(problems)}: {problem['id']}")
            await env.reset()

            def run_nova() -> ActResult:
                with NovaAct(starting_page=env.urls.app, headless=True) as nova:
                    return nova.act(problem["problem"], max_steps=MAX_STEPS)

            try:
                await asyncio.to_thread(run_nova)
            except Exception as e:
                print(f"Error: {e}")

            function_name = extract_function_name(problem["verifier_func"])
            print(f"Verifying {function_name} ({problem['id']})...")
            response = await env.verify_raw(problem["verifier_func"], function_name)
            print(response)
            if response.success:
                successes += 1

        print(f"Successes: {successes}")
        print(f"Total: {len(problems)}")
        print(f"Success rate: {successes / len(problems)}")
    finally:
        await env.close()


if __name__ == "__main__":
    asyncio.run(main())
