from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='robot-retrier',
    version='0.2.3',
    author='Suriya',
    author_email='suriya@example.com',  # Optional: replace with real email
    description='GUI Retry Debugger for Robot Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/suri-53/robotretirer',  # Optional: replace with real GitHub repo
    packages=find_packages(),  # Automatically finds RobotRetrier/
    install_requires=[
        'robotframework>=7.0'
    ],
    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'robotframework_listener': [
            'RobotRetrier = RobotRetrier:RobotRetrier',
        ]
    },
    python_requires='>=3.8',
)