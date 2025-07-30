from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="samhiqmailer",
    version="3.2",
    author="Md Sameer Iqbal",
    author_email="contact.samhiq@gmail.com",
    description="Professional Bulk Email Client with Modern UI and Advanced Features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samhiq/SamhiqMailer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyQt5>=5.15.0",
        "openpyxl>=3.0.0",
        "requests>=2.25.0",
    ],
    package_data={'samhiqmailer': ['resources/*']},
    entry_points={'console_scripts': ['samhiqmailer=samhiqmailer.SamhiqMailer:main']},
)
