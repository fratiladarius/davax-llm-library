import json
from prompts.recommender import SYSTEM_PROMPT
from utils.summary_tool import GET_SUMMARY_TOOL, get_summary_by_title

TOOL_NAME = 'get_summary_by_title'


def ask_recommend_with_summary(client, model, content, temperature: float = 0.4):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]

    first = client.chat.completions.create(
        model=model, messages=messages,
        tools=[GET_SUMMARY_TOOL], tool_choice="auto",
        temperature=temperature,
    )

    msg = first.choices[0].message
    tool_calls = getattr(msg, "tool_calls", None)

    if tool_calls:
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id, "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments or "{}"
                    },
                }
                for tc in tool_calls
            ],
        })

        for tc in tool_calls:
            if tc.type == "function" and tc.function.name == TOOL_NAME:
                args = json.loads(tc.function.arguments or "{}")
                title = (args.get("title") or "").strip()
                summary = get_summary_by_title(title)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": "get_summary_by_title",
                    "content": summary or "",
                })

        final = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        return _finalize(final.choices[0].message.content or "")

    return _finalize(msg.content or "")


def _finalize(text: str) -> str:
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]

    fields = {"title": "", "why": "", "summary": ""}
    for ln in lines:
        low = ln.lower()
        if low.startswith("title:") and not fields["title"]:
            fields["title"] = ln.split(":", 1)[1].strip()
        elif low.startswith("why:") and not fields["why"]:
            fields["why"] = ln.split(":", 1)[1].strip()
        elif low.startswith("summary:") and not fields["summary"]:
            fields["summary"] = ln.split(":", 1)[1].strip()

    if fields["title"] and not fields["summary"]:
        s = get_summary_by_title(fields["title"]) or ""
        fields["summary"] = s

    if fields["title"] and fields["why"] and fields["summary"]:
        return "\n".join([
            f"Title: {fields['title']}",
            f"Why: {fields['why']}",
            f"Summary: {fields['summary']}",
        ])

    return "\n".join(lines)
