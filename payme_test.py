import inspect
from unittest import TextTestRunner, TestLoader

from tests.base import BaseTestCase


class CustomTestLoader(TestLoader):
    def getTestCaseNames(self, test_case_class):
        test_names = super().getTestCaseNames(test_case_class)
        return sorted(
            test_names,
            key=lambda method_name: inspect.getsourcelines(getattr(test_case_class, method_name))[1],
        )


def run_test_cases():
    loader = CustomTestLoader().discover(start_dir="tests", pattern="test_*.py")
    result = TextTestRunner().run(loader)
    return result


if __name__ == '__main__':
    run_test_cases()
