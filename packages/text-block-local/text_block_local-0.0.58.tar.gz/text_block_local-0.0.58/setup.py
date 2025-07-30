import setuptools

PACKAGE_NAME = "text-block-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/text-block-local
    version='0.0.58',
    author="Circles",
    author_email="info@circlez.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Text Block",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local>=0.0.135',
        'database-mysql-local>=0.0.291',
        'user-context-remote>=0.0.75',
        'profile-local>=0.0.65',
        'person-local>=0.0.76'
    ]

)
