"""
Documentation
-------------
nothing

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="JsonToC",
        description="Convert Json to C",
        keywords="json C",
        long_description=long_description,
        version="1.0.3",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=find_packages(),
        #packages=["JsonToMarkdown"],
        package_data={},
        entry_points={
            'console_scripts':[
                'json-to-c=json_to_c.json_to_c:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
