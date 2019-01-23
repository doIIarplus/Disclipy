# Disclipy: A Discord CLI in Python

# Requirements

- Python 3.7

# Dev

### Doc References

- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/index.html)

- [click](http://click.palletsprojects.com/en/7.x/)

- [discord.py](https://discordpy.readthedocs.io/en/rewrite/)

### Setup virtual environment

linux/macos

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

windows

```
python3 -m venv venv
venv\scripts\activate
pip install -r requirements.txt
```

### Run test

```
python3 -m unittest tests/the_module_to_test.py
```

### Push changes

Push all files with:

```
./push.sh
```

Push individual files with:

```
./push.sh file1 file2 file3
```


