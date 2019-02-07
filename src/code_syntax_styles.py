from html.parser import HTMLParser
from prompt_toolkit.styles import Style
from xml.sax.saxutils import escape

"""codehilite css
.codehilite .hll { background-color: #ffffcc }
// not converted
/.codehilite  { background: #f8f8f8; }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
// uses background instead of border
/.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #888888 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
"""

codehilite_style = Style.from_dict({
    "hll": 'bg: #ffffcc',
    "c": '#408080 italic',  # Comment
    "err": 'bg: #FF0000',  # Error
    "k": '#008000 bold',  # Keyword
    "o": '#666666',  # Operator
    "ch": '#408080 italic',  # Comment.Hashbang
    "cm": '#408080 italic',  # Comment.Multiline
    "cp": '#BC7A00',  # Comment.Preproc
    "cpf": '#408080 italic',  # Comment.PreprocFile
    "c1": '#408080 italic',  # Comment.Single
    "cs": '#408080 italic',  # Comment.Special
    "gd": '#A00000',  # Generic.Deleted
    "ge": 'italic',  # Generic.Emph
    "gr": '#FF0000',  # Generic.Error
    "gh": '#000080 bold',  # Generic.Heading
    "gi": '#00A000',  # Generic.Inserted
    "go": '#888888',  # Generic.Output
    "gp": '#000080 bold',  # Generic.Prompt
    "gs": 'bold',  # Generic.Strong
    "gu": '#800080 bold',  # Generic.Subheading
    "gt": '#0044DD',  # Generic.Traceback
    "kc": '#008000 bold',  # Keyword.Constant
    "kd": '#008000 bold',  # Keyword.Declaration
    "kn": '#008000 bold',  # Keyword.Namespace
    "kp": '#008000',  # Keyword.Pseudo
    "kr": '#008000 bold',  # Keyword.Reserved
    "kt": '#B00040',  # Keyword.Type
    "m": '#666666',  # Literal.Number
    "s": '#BA2121',  # Literal.String
    "na": '#7D9029',  # Name.Attribute
    "nb": '#008000',  # Name.Builtin
    "nc": '#0000FF bold',  # Name.Class
    "no": '#880000',  # Name.Constant
    "nd": '#AA22FF',  # Name.Decorator
    "ni": '#999999 bold',  # Name.Entity
    "ne": '#D2413A bold',  # Name.Exception
    "nf": '#0000FF',  # Name.Function
    "nl": '#A0A000',  # Name.Label
    "nn": '#0000FF bold',  # Name.Namespace
    "nt": '#008000 bold',  # Name.Tag
    "nv": '#19177C',  # Name.Variable
    "ow": '#AA22FF bold',  # Operator.Word
    "w": '#bbbbbb',  # Text.Whitespace
    "mb": '#666666',  # Literal.Number.Bin
    "mf": '#666666',  # Literal.Number.Float
    "mh": '#666666',  # Literal.Number.Hex
    "mi": '#666666',  # Literal.Number.Integer
    "mo": '#666666',  # Literal.Number.Oct
    "sa": '#BA2121',  # Literal.String.Affix
    "sb": '#BA2121',  # Literal.String.Backtick
    "sc": '#BA2121',  # Literal.String.Char
    "dl": '#BA2121',  # Literal.String.Delimiter
    "sd": '#BA2121 italic',  # Literal.String.Doc
    "s2": '#BA2121',  # Literal.String.Double
    "se": '#BB6622 bold',  # Literal.String.Escape
    "sh": '#BA2121',  # Literal.String.Heredoc
    "si": '#BB6688 bold',  # Literal.String.Interpol
    "sx": '#008000',  # Literal.String.Other
    "sr": '#BB6688',  # Literal.String.Regex
    "s1": '#BA2121',  # Literal.String.Single
    "ss": '#19177C',  # Literal.String.Symbol
    "bp": '#008000',  # Name.Builtin.Pseudo
    "fm": '#0000FF',  # Name.Function.Magic
    "vc": '#19177C',  # Name.Variable.Class
    "vg": '#19177C',  # Name.Variable.Global
    "vi": '#19177C',  # Name.Variable.Instance
    "vm": '#19177C',  # Name.Variable.Magic
    "il": '#666666'  # Literal.Number.Integer.Long
})


class HTML2PromptToolkitHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.prompt_toolkit_html = ''
        self.tags = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if 'class' in attributes:
            tag = attributes['class']

        self.tags.append(tag)
        self.prompt_toolkit_html += '<' + tag + '>'

    def handle_endtag(self, tag):
        self.prompt_toolkit_html += '</' + self.tags.pop() + '>'

    def handle_data(self, data):
        self.prompt_toolkit_html += escape(data)

    def __str__(self):
        return self.prompt_toolkit_html

    def __repr__(self):
        return self.prompt_toolkit_html


def HTML_2_prompt_toolkit_HTML(html):
    parser = HTML2PromptToolkitHTMLParser()
    parser.feed(html)
    return str(parser)
