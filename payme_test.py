import inspect
from unittest import TestLoader, TextTestRunner


class CustomTestLoader(TestLoader):
    # pylint: disable=missing-class-docstring
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        return sorted(
            test_names,
            key=lambda method_name: inspect.getsourcelines(
                getattr(testCaseClass, method_name))[1],
        )


def run_test_cases():
    loader = CustomTestLoader().discover(start_dir="tests", pattern="test_*.py")
    result = TextTestRunner().run(loader)
    return result


if __name__ == '__main__':
    run_test_cases()
