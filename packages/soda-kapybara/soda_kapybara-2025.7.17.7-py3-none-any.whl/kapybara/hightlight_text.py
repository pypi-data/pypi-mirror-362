
def highlight_text(text: str) -> str:
    if len(text) >= 50:
        return text
    remaining_len = 50 - len(text)
    if remaining_len % 2 == 0:
        left_padding = remaining_len // 2
        right_padding = remaining_len // 2
    else:
        left_padding = remaining_len // 2
        right_padding = remaining_len // 2 + 1
    return f'{"-" * left_padding}{text}{"-" * right_padding}'
