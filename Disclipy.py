from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

AutoCompleter = WordCompleter(['abcde', 'bcdef', 'cdefg', 'defgh'],
                              ignore_case=True)

while True:
    user_input = prompt('Discord>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=AutoCOmpleter,
                        )
    print(user_input)
