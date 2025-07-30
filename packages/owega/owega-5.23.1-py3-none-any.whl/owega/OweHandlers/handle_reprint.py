"""Handle /reprint."""
from ..conversation import Conversation
from ..utils import markdown_print


# reprints chat history
def handle_reprint(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /reprint.

    Command description:
        Reprints (fancy) the conversation history.

    Usage:
        /reprint
    """
    # removes linter warning about unused arguments
    _, _, _ = temp_file, given, temp_is_temp

    if not silent:
        for i, message in enumerate(messages.get_messages()):
            ind = i-1
            ind_str = f' [ \033[90m{ind}\033[0m ]'
            if ind < 0:
                ind_str = ' [ \033[90mCONTEXT\033[0m ]'

            print()

            if message['role'] == 'system':
                print("[ \033[92mSYSTEM\033[0m ]", end="")
            elif message['role'] == 'user':
                print("[ \033[96mUSER\033[0m ]", end="")
            elif message['role'] == 'assistant':
                print("[ \033[95mOWEGA\033[0m ]", end="")
            else:
                print("[ \033[95mFUNCTION\033[0m ]", end="")
            print(ind_str)
            markdown_print(
                message['content']
                .encode('utf16', 'surrogatepass')
                .decode('utf16')
            )

    return messages


item_reprint = {
    "fun": handle_reprint,
    "help": "reprints the conversation history with fancy markdown support",
    "commands": ["reprint"],
}
