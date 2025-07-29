from setuptools import setup, find_packages
setup(
    name="py-telecast",
    version="1.0.0",
    author="Manji Devs",
    description="A simple Telegram broadcast module with support for JSON, SQLite, and MongoDB backends.",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.6",
        "pymongo>=4.6.3"
    ],
    keywords=["telegram", "broadcast", "bot", "ptb", "manji", "manjidevs"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
