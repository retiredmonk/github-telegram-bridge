def build_message(latest):

    message = f"🚨 {len(latest)} New commit(s) Found\n\n"

    for i, commit in enumerate(latest, start=1):
        message += (
            f"{i}. Message: {latest['commit']['message']}"
            f" Author: {latest['commit']['author']['name']}\n"
            f"URL: {latest['html_url']}"
        )

    return message.strip()
