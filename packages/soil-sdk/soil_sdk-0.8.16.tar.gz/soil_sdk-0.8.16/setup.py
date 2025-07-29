"""Setup configuration for soil-sdk"""

from setuptools import setup

if __name__ == "__main__":
    setup(
        use_scm_version={
            "write_to": "soil/_version.py",
            "write_to_template": '__version__ = "{version}"',
        },
    )
