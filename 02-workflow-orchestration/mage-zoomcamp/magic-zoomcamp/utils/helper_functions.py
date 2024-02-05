def camel_to_snake(s):
    result = ''

    # Iterate through the rest of the characters
    for i, char in enumerate(s[:-1]):
        # Convert the first character to lower case
        if i == 0:
            result += char.lower()

        # If the character is upper and in between other uppercase dont add _
        elif char.isupper() and s[i - 1].isupper() and s[i + 1].isupper():
            result += char.lower()

        # If the character is uppercase followed by lowercase, insert an underscore before it and convert to lower case
        elif char.isupper() and s[i - 1].isupper() and s[i + 1].islower():
            result += '_'
            result += char.lower()

        # If the character is uppercase preceded by lowercase, insert an underscore before it and convert to lower case
        elif char.isupper() and s[i - 1].islower():
            result += '_'
            result += char.lower()
        else:
            result += char

    result += s[-1]
    result = result.lower()
    return result