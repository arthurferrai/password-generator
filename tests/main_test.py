import string
import unittest

from assertpy import assert_that, add_extension

from src.main import create_random_password


def does_not_repeat_characters(self):
    val: str = self.val

    assert_that(val).is_instance_of(str)
    assert_that(len(set(val))).is_equal_to(len(val))

    return self


add_extension(does_not_repeat_characters)


def has_any(self, set_to_search):
    val: str = self.val
    assert_that(val).is_instance_of(str)

    if not any(c in set_to_search for c in val):
        self.error(f"{val} does not have any of {set_to_search}")
    return self


add_extension(has_any)


class TestPassword(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.PASS_SIZE = 20
        cls.password = create_random_password(size=cls.PASS_SIZE, leak_checker=lambda x: False)

    def test_password_size_is_zero_then_zero_len_pass_generated(self):
        assert_that(create_random_password(size=0)).is_length(0)

    def test_password_size_is_set_then_password_has_set_size(self):
        assert_that(self.password).is_length(self.PASS_SIZE)

    def test_password_does_not_repeat_characters(self):
        assert_that(self.password).does_not_repeat_characters()

    def test_password_has_letters_numbers_and_symbols(self):
        assert_that(self.password)\
            .has_any(string.ascii_letters)\
            .has_any(string.digits)\
            .has_any(string.punctuation)

    def test_password_not_leaked(self):
        def not_leaked(_):
            not_leaked.called = True
            return False

        not_leaked.called = False

        create_random_password(size=self.PASS_SIZE, leak_checker=not_leaked)

        assert_that(not_leaked.called).is_true()

    def test_password_not_leaked_after_retries(self):
        num_retries = 3

        def not_leaked(_):
            if not_leaked.retries >= num_retries:
                return False
            not_leaked.retries += 1
            return True

        not_leaked.retries = 0

        create_random_password(size=self.PASS_SIZE, leak_checker=not_leaked)

        assert_that(not_leaked.retries).is_equal_to(num_retries)

    def test_password_does_not_contain_ignored_characters(self):
        forbidden_chars = '\\!`´'

        password = create_random_password(size=self.PASS_SIZE, leak_checker=lambda x: False, forbidden_chars=forbidden_chars)
        assert_that(password).does_not_contain(forbidden_chars)


if __name__ == '__main__':
    # run tests
    unittest.main()
