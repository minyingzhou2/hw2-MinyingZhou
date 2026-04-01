import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_INSTRUCTIONS = (
    "You summarize meeting notes into a concise JSON object. "
    "Be careful with uncertainty. Only include owners and deadlines when they are explicitly stated. "
    "If no action item is clearly assigned, return an empty action_items list."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize meeting notes into action items with the OpenAI Responses API."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a text file containing meeting notes or a meeting transcript.",
    )
    parser.add_argument(
        "--output",
        default="output/meeting_summary.json",
        help="Where to save the structured JSON output.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use for the API call. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--instructions",
        default=DEFAULT_INSTRUCTIONS,
        help="System instructions for the summarization step.",
    )
    parser.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable that stores the OpenAI API key.",
    )
    return parser.parse_args()


def load_input_text(path_str: str) -> str:
    input_path = Path(path_str)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Input file is empty: {input_path}")
    return text


def build_request_payload(model: str, instructions: str, meeting_notes: str) -> dict:
    return {
        "model": model,
        "instructions": instructions,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Summarize these meeting notes into structured JSON.\n\n"
                            f"Meeting notes:\n{meeting_notes}"
                        ),
                    }
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "meeting_summary",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "action_items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "task": {"type": "string"},
                                    "owner": {"type": ["string", "null"]},
                                    "deadline": {"type": ["string", "null"]},
                                },
                                "required": ["task", "owner", "deadline"],
                                "additionalProperties": False,
                            },
                        },
                        "risks_or_uncertainties": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["summary", "action_items", "risks_or_uncertainties"],
                    "additionalProperties": False,
                },
            }
        },
    }


def call_openai_api(payload: dict, api_key: str) -> dict:
    request = urllib.request.Request(
        url="https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_json_output(response_data: dict) -> dict:
    for item in response_data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return json.loads(content["text"])
    raise ValueError("Could not find JSON output in the API response.")


def save_output(output_path_str: str, result: dict) -> Path:
    output_path = Path(output_path_str)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return output_path


def print_sections(result: dict, output_path: Path) -> None:
    print("=== Summary ===")
    print(result["summary"])
    print()

    print("=== Action Items ===")
    if result["action_items"]:
        for index, item in enumerate(result["action_items"], start=1):
            owner = item["owner"] or "Unassigned"
            deadline = item["deadline"] or "No deadline"
            print(f"{index}. Task: {item['task']}")
            print(f"   Owner: {owner}")
            print(f"   Deadline: {deadline}")
    else:
        print("No clear action items.")
    print()

    print("=== Risks / Uncertainties ===")
    if result["risks_or_uncertainties"]:
        for note in result["risks_or_uncertainties"]:
            print(f"- {note}")
    else:
        print("None identified.")
    print()

    print(f"Saved structured output to: {output_path}")


def main() -> int:
    args = parse_args()
    api_key = os.getenv(args.api_key_env)
    if not api_key:
        print(
            f"Missing API key. Set the {args.api_key_env} environment variable and try again.",
            file=sys.stderr,
        )
        return 1

    try:
        meeting_notes = load_input_text(args.input)
        payload = build_request_payload(args.model, args.instructions, meeting_notes)
        response_data = call_openai_api(payload, api_key)
        result = extract_json_output(response_data)
        output_path = save_output(args.output, result)
        print_sections(result, output_path)
        return 0
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(f"OpenAI API request failed: {exc.code} {exc.reason}", file=sys.stderr)
        print(error_body, file=sys.stderr)
    except urllib.error.URLError as exc:
        print(f"Network error while calling OpenAI API: {exc.reason}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
