# Password Generator

[![Testing](https://github.com/arthurferrai/password-generator/actions/workflows/python-tests.yml/badge.svg)](https://github.com/arthurferrai/password-generator/actions/workflows/python-tests.yml)

The aim of this project is to generate a password that:
* is random (or at least looks like)
* is hard to guess (consequently hard to remember)
* has a good entropy (default config has 77.9 bits of entropy)
* has not been leaked (using [Have I Been Pwned](https://haveibeenpwned.com/Passwords) API)

It does not save generated passwords anywhere (it's just a generator).
It does not send generated password anywhere (API check is made using part of password SHA-1 hash)

## Using
### Prepare
* Clone the repo;
* Create a venv and activate it (instructions [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment));
* Install dependencies using  `pip install -r requirements.txt`;

### Run
* Run using `python src/main.py`. The generated password will be shown on console.

### Test
* Run tests using `python tests/main_test.py`
