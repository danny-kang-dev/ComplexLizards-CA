import sys


def assert_python_version(major, minor=0):
    """ Checks whether the current version of Python is
        greater or equal to the specified version. Otherwise,
        prints an error messages and closes the program.

        inputs:
            major (int): Most significant version number (3.6 -> 3)
            minor (int): Secondary version number (3.6 -> 6)
    """

    actual_major = sys.version_info.major
    actual_minor = sys.version_info.minor

    if major > actual_major or (major == actual_major and minor >= actual_minor):
        return

    print("This program requires Python version %s.%s. You are using Python %s.%s." %
          (major, minor, actual_major, actual_minor))
    sys.exit()
