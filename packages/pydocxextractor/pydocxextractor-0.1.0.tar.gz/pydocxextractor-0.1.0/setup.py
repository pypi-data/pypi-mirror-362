from setuptools import setup, find_packages

setup(
    name="pydocxextractor",
    version="0.1.0",
    description="A library to extract text and images from DOCX files, returning a flattened string or structured data.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    py_modules=["extract_question_image"],
    install_requires=[
        "lxml",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="",
    long_description="""
A simple library to extract text and images from DOCX files, returning a flattened string (with image placeholders) or a structured list. Useful for MCQ and exam document parsing.
""",
    long_description_content_type="text/markdown",
) 