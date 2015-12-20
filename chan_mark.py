"""
Markup class allows the use of easy-to-write characters to style the text
instead of using escape codes.

==text== --> reverse video
'''text''' --> bold
~~text~~ --> strikethrough

Copyright (c) 2015 makos <matmak@protonmail.com>, chibi
"""

import re



class Marker():

    def esc(self, input_text):
        input_text = input_text.replace('\033', '\\033')
        return input_text

    def demarkify(self, input_text):
        """Prints out a marked-up piece of text."""
        output_text = self.esc(input_text)
        # strikethrough
        output_text = re.sub(
            '~~(?P<substring>.*?)~~', '\033[0;9m\g<substring>\033[0m',
            output_text)
        # bold
        output_text = re.sub(
            '\'\'\'(?P<substring>.*?)\'\'\'', '\033[0;1m\g<substring>\033[0m',
            output_text)
        # rv
        output_text = re.sub(
            '==(?P<substring>.*?)==', '\033[0;7m\g<substring>\033[0m',
            output_text)

        return output_text