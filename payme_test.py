import inspect
from unittest import TestLoader, TextTestRunner


class CustomTestLoader(TestLoader):
    # pylint: disable=missing-class-docstring
    def getTestCaseNames(self, test_case_class):
        test_names = super().getTestCaseNames(test_case_class)
        return sorted(
            test_names,
            key=lambda method_name: inspect.getsourcelines(
                getattr(test_case_class, method_name))[1],
        )


def run_test_cases() -> None:
    loader = CustomTestLoader().discover(start_dir="tests", pattern="test_*.py")
    result = TextTestRunner().run(loader)
    if not result.wasSuccessful():
        exit(1)


if __name__ == '__main__':
    run_test_cases()
