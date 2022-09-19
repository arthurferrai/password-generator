import hashlib
import random
import string
import warnings
from typing import Callable, Iterable

import requests as requests


def __leaked(password):
    if isinstance(password, list):
        password = ''.join(password)

    sha1_pass = hashlib.sha1(password.encode())
    digest = sha1_pass.hexdigest().upper()

    result = requests.get('https://api.pwnedpasswords.com/range/{}'.format(digest[:5]))
    if not result.ok:
        warnings.warn("Unable to check if password {} is leaked".format(password))
        return False

    for line in result.text.splitlines():
        part_hash, count = line.split(':')
        if part_hash in digest:
            warnings.warn("Password {} has been used at least {} times".format(password, count))
            return True

    return False


def create_random_password(
    size: int,
    forbidden_chars: str = '',
    characters_groups: Iterable[str] = None,
    leak_checker: Callable[[Iterable[str]], bool] = __leaked
) -> str:

    if not characters_groups:
        characters_groups = (
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            string.punctuation
        )

    characters = ['a', 'a']
    remove_forbidden = str.maketrans("", "", forbidden_chars)

    while character_repeats(characters) or leak_checker(characters):
        characters = []
        amount_to_add = size // len(characters_groups)

        for g in characters_groups:
            characters.extend(random.choices(g.translate(remove_forbidden), k=amount_to_add))

        for _ in range(size - len(characters)):
            characters.append(random.choice(characters_groups[0]))

        random.shuffle(characters)
    return ''.join(characters)


def character_repeats(password):
    return len(set(password)) < len(password)


if __name__ == '__main__':
    print(create_random_password(size=12, forbidden_chars='`\\´¨'))
