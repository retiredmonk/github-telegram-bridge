def build_message(latest):
    return (
        f"Latest commit:\n\n"
        f"Message: {latest['commit']['message']}\n"
        f"Author: {latest['commit']['author']['name']}\n"
        f"URL: {latest['html_url']}"
    )