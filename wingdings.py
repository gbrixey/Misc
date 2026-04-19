text_to_wingdings_dict = {
'A': '✌',
'B': '👌',
'C': '👍',
'D': '👎',
'E': '👈',
'F': '👉',
'G': '☝',
'H': '👇',
'I': '✋',
'J': '🙂',
'K': '😐',
'L': '☹',
'M': '💣',
'N': '☠',
'O': '🏳️',
'P': '🚩',
'Q': '✈',
'R': '☀️',
'S': '💧',
'T': '❄',
'U': '✝️',
'V': '🤞',
'W': '🎯',
'X': '🙏',
'Y': '✡',
'Z': '☪',
'1': '📂',
'2': '📄',
'3': '📝',
'4': '📑',
'5': '🗄',
'6': '⌛',
'7': '⌨️',
'8': '🖱️',
'9': '🖲',
'0': '📁',
'!': '✏',
'@': '🙌',
'#': '⚔️',
'$': '👓',
'%': '🔔',
'^': '♈',
'&': '📖',
'*': '✉️',
'(': '☎️',
')': '📞',
'-': '📫',
'_': '♉',
'=': '💿',
'+': '📨',
'[': '☯',
']': '☸',
'{': '🌼',
'}': '➿',
'\\': '🕉️',
'|': '🌸',
';': '💽',
':': '🖥️',
'\'': '7️⃣',
'‘': '7️⃣',
'’': '7️⃣',
'"': '9️⃣',
'“': '9️⃣',
'”': '9️⃣',
',': '📪',
'.': '📬',
'<': '💾',
'>': '📼',
'/': '📭',
'?': '✍',
' ': ' '
}

wingdings_to_text_dict = {
'✌': 'A',
'👌': 'B',
'👍': 'C',
'👎': 'D',
'👈': 'E',
'👉': 'F',
'☝': 'G',
'☝️': 'G',
'👇': 'H',
'✋': 'I',
'🙂': 'J',
'😐': 'K',
'☹': 'L',
'💣': 'M',
'☠': 'N',
'🏳️': 'O',
'🚩': 'P',
'✈': 'Q',
'☀️': 'R',
'💧': 'S',
'❄': 'T',
'✝️': 'U',
'🤞': 'V',
'🎯': 'W',
'🙏': 'X',
'✡': 'Y',
'☪': 'Z',
'📂': '1',
'📄': '2',
'📝': '3',
'📑': '4',
'🗄': '5',
'⌛': '6',
'⌨️': '7',
'🖱️': '8',
'🖲': '9',
'📁': '0',
'✏': '!',
'🙌': '@',
'⚔️': '#',
'👓': '$',
'🔔': '%',
'♈': '^',
'📖': '&',
'✉️': '*',
'☎️': '(',
'📞': ')',
'📫': '-',
'♉': '_',
'💿': '=',
'📨': '+',
'☯': '[',
'☸': ']',
'🌼': '{',
'➿': '}',
'🕉️': '\\',
'🌸': '|',
'💽': ';',
'🖥️': ':',
'7️⃣': '\'',
'9️⃣': '"',
'📪': ',',
'📬': '.',
'💾': '<',
'📼': '>',
'📭': '/',
'✍': '?',
'✍️': '?',
' ': ' ',
'️': '',
}

# For 34 of these 66 characters, I replaced the original wingding with a different emoji to improve the appearance of the output text.
# Usually I chose an emoji that looks similar to the wingding or has a similar theme, but in some cases they are completely unrelated.
# The replacements are as follows:

# Used 👈 instead of ☜ for 'E' 
# Used 👉 instead of ☞ for 'F'
# Used 👇 instead of ☟ for 'H'
# Used 🙂 instead of ☺ for 'J'
# Used 🏳️ instead of ⚐ for 'O'
# Used 🚩 instead of 🏱 for 'P'
# Used ☀️ instead of ☼ for 'R'
# Used ✝️ instead of 🕆 for 'U'
# Used 🤞 instead of ✞ for 'V': The crossed fingers gesture is thematically related to the Christian cross.
# Used 🎯 instead of 🕈 for 'W': The Celtic cross looks similar to crosshairs, so the bullseye is tangentially related.
# Used 🙏 instead of ✠ for 'X': The praying hands are thematically related to the Maltese cross.
# Used 📝 instead of 🗏 for '3'
# Used 📑 instead of 🗐 for '4'
# Used ⌨️ instead of 🖮 for '7'
# Used 🖱️ instead of 🖰 for '8'
# Used 🙌 instead of @ for '@': Unrelated. For some reason the @ character does not have a separate wingding.
# Used ⚔️ instead of ✁ for '#': The crossed swords look similar to scissors.
# Used 🔔 instead of 🕭 for '%'
# Used 📖 instead of 🕮 for '&'
# Used ✉️ instead of 🖂 for '*'
# Used ☎️ instead of 🕿 for '('
# Used 📞 instead of ✆ for ')'
# Used 💿 instead of 🖬 for '=': The CD is thematically related to the 5.25-inch floppy disk.
# Used 📨 instead of 🖃 for '+'
# Used 🌼 instead of ❀ for '{'
# Used ➿ instead of ❝ for '}': The double loop bears a slight resemblance to a double quotation mark.
# Used 🕉️ instead of ॐ for '\'
# Used 🌸 instead of 🏶 for '|'
# Used 💽 instead of 🖴 for ';'
# Used 🖥️ instead of 🖳 for ':'
# Used 7️⃣ instead of ❼ for '
# Used 9️⃣ instead of ❾ for "
# Used 💾 instead of 🖫 for '<'
# Used 📼 instead of ✇ for '>': The VHS tape is thematically related to the tape drive.

def to_wingdings(text):
    '''Translates the given string to a string of wingding-like emojis.'''
    wingdings = ''
    for char in text.upper():
        wingding = text_to_wingdings_dict.get(char)
        if not wingding:
            print(f'I don\'t know how to translate this character: {char}')
            wingding = '❓'
        wingdings += wingding
    return wingdings

def from_wingdings(wingdings):
    '''Translates a string of wingding-like emojis (output by the to_wingdings function) back into readable text.'''
    text = ''
    index = 0
    while index < len(wingdings):
        wingding = wingdings[index]
        char = wingdings_to_text_dict.get(wingding)
        index_increment = 1
        if not char and index < len(wingdings) - 1:
            # Some of the wingdings are technically two or three characters, try parsing two or three at once.
            wingding += wingdings[index + 1]
            char = wingdings_to_text_dict.get(wingding)
            if char:
                index_increment = 2
            elif index < len(wingdings) - 2:
                wingding += wingdings[index + 2]
                char = wingdings_to_text_dict.get(wingding)
                if char:
                    index_increment = 3
        if not char:
            print(f'I don\'t know how to translate this character: {wingding}')
            char = '?'
        text += char
        index += index_increment
    return text
