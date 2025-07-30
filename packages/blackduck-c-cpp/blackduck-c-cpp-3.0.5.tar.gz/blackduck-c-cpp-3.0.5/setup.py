"""
Copyright (c) 2021 Synopsys, Inc.
Use subject to the terms and conditions of the Synopsys End User Software License and Maintenance Agreement.
All rights reserved worldwide.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackduck-c-cpp",
    version="3.0.5",
    description="Scanning for c/c++ projects using blackduck and coverity tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["requests>=2.28.2",
                      "numpy>=1.24.2",
                      "python-dateutil>=2.8.1",
                      "pytz>=2021.1",
                      "six>=1.15.0",
                      "tqdm>=4.58.0",
                      "blackduck>=1.1.0",
                      "configargparse>=1.4",
                      "structlog>=20.1.0",
                      "pyyaml>=5.4.1",
                      "pandas>=1.1.5",
                      "urllib3>=1.26.15, <1.27",
                      "chardet>=4.0.0, <5",
                      "requests-toolbelt>=0.9.0",
                      "google-cloud-storage>=2.6.0",
                      "certifi>=2023.07.22"
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['blackduck-c-cpp=blackduck_c_cpp.run_build_capture:run']},
)
