import setuptools

setuptools.setup(
    name="custombox",
    version="0.1.3",
    author="Kiavash Nourafshan",
    author_email="kianour9@gmail.com",
    description="Custom tkinter dialog box with flexible buttons and commands",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",  # You can leave this empty or remove it if you don't have a URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
