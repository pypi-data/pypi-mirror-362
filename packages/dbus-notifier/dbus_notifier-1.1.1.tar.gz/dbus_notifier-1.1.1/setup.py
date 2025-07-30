import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'dbus-next==0.2.3',
    'dbus-python==1.3.2',
    'dbusnotify==0.0.2',
    'python-dotenv==1.0.3'
]

setuptools.setup(
    name="dbus_notifier",
    author="Adam Bukolt",
    author_email="abukolt@gmx.com",
    description="Package to post dbus notifications on Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=[('dbus_notifier/icons', ['dbus_notifier/icons/feather_on_grey.png']),
                ('./', ['.env_dbus_notifier'])],
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
