import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}-{sha}",
        "dirty_template": "{tag}-{sha}.dirty"
    },
    setup_requires=["setuptools-git-ver"],
    name="devopstestor",
    author="Alexis PORZIER",
    author_email="alexis.porzier.pro@gmail.com",
    description="Framwork to auto test machine provisioning",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/alexis.porzier.pro/devopstestor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
        "pathlib",
        "pyyaml",
        "pytest-testinfra",
        "docker",
        "jinja2",
        "coloredlogs",
        "dateutils"
    ],
    scripts=['bin/devopstestor-presets', 'bin/devopstestor-saltstack', 'bin/devopstestor-logstash']
)
