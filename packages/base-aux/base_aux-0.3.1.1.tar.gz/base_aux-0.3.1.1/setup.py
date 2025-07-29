from setuptools import setup, find_packages
from PROJECT import PROJECT
from base_aux.aux_text.m1_text_aux import TextAux


# =====================================================================================================================
# VERSION = (0, 0, 1)   # use find_packages to keep all internal pkgs for pypi
VERSION = (0, 0, 2)   # fix ability to read russian text in readme


# =====================================================================================================================
with open("README.md", mode="r", encoding="utf8") as f:
    readme = f.read()


packages = [PROJECT.NAME_IMPORT, ]
pkgs_internal = find_packages(where=PROJECT.NAME_IMPORT)
for name in pkgs_internal:
    packages.append(f"{PROJECT.NAME_IMPORT}.{name}")

with open("requirements.txt", mode="r", encoding="utf8") as f:
    requirements_text = f.read()
    requirements_list = TextAux(requirements_text).parse__requirements_lines()
    print(f"{requirements_list=}")


# =====================================================================================================================
setup(
  version=str(PROJECT.VERSION),
  description=PROJECT.DESCRIPTION_SHORT,
  keywords=PROJECT.KEYWORDS,
  classifiers=[
    # "Topic :: ________________",
    *PROJECT.CLASSIFIERS_TOPICS_ADD,

    # "Framework :: ",
    "Topic :: Software Development :: Libraries :: Python Modules",
    # "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent",
    # "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Typing :: Typed",
  ],

  name=PROJECT.NAME_IMPORT,
  author=PROJECT.AUTHOR_NAME,
  author_email=PROJECT.AUTHOR_EMAIL,
  long_description=readme,
  long_description_content_type="text/markdown",

  url=PROJECT.AUTHOR_HOMEPAGE,  # HOMEPAGE
  project_urls={
    # "Documentation": f"https://github.com/centroid457/{NAME}/blob/main/GUIDE.md",
    "NestInit_Source": f"https://github.com/centroid457/{PROJECT.NAME_IMPORT}",
  },

  packages=packages,
  install_requires=requirements_list,   # setup with "pip install"
  python_requires=">=3.12"
)


# =====================================================================================================================
