def build_message(commit: dict) -> str:
    sha = commit['sha'][:7]
    message = commit['commit']['message']
    author = commit['commit']['author']['name']
    url = commit['html_url']

    formatted_message = (
        f"🚀 *New Commit Detected*\n\n"
        f"👤 Author: {author}\n"
        f"📝 Message: {message}\n"
        f"🔑 SHA: `{sha}`\n"
        f"🔗 View Commit: {url}"
    )

    return formatted_message