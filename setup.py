from setuptools import setup, find_packages

setup(
    name='url-shortener',
    version='1.0',
    url="https://github.com/jms/url-shortener",
    author="Jeronimo Martinez Sanchez",
    author_email="jms@rz0r.net",
    description="URL shortener ",
    py_modules=['main'],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ]
)
