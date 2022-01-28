import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='lines_of_code',
    version='1.4.3',
    author='Jothin kumar',
    author_email='contact@jothin.tech',
    description='Lines of code is an app to calculate the number of commits, addition and deletion by an user in git.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://jothin.tech/lines-of-code',
    packages=setuptools.find_packages(),
)
