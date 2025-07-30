<!--
SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen

SPDX-License-Identifier: CC0-1.0
-->

# tgadmin

A command line tool for managing your projects in the [TextGrid repository](https://textgridrep.org) without TextGridLab.

## Install

You may use this with venv or with pipx. With pipx you have the benefit of having the command available  in your shell without further manual venv creation and activation.

Install [pipx](https://pypa.github.io/pipx/), e.g. on Debian/Ubuntu `apt install pipx`

And the this tool from [pypi.org](https://pypi.org/project/tgadmin/)

        pipx install tgadmin

Upgrade to a new version with

        pipx upgrade tgadmin

If you do not want to use pipx have a look at the section "Development".

## Usage

### Export sessionID (SID)

get from https://textgridlab.org/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance=textgrid-esx2.gwdg.de

and set as env var:

        export TEXTGRID_SID=your_secret_sid_here

or set with `--sid` for every command

### Get help

        tgadmin

### List projects

list your projects:

        tgadmin list

### Create project

if there is no suitable project, create one:

        tgadmin create lab-import-test-20230605

### Upload an aggregation object like editons, aggregations and collections

You can upload aggregations as new textgrid objects like

        tgadmin --server http://test.textgridlab.org put-aggregation TGPR-...fe eng003.edition

this would assume that you have an file containing the aggragtion with local paths in
eng003.edition and metadata description files like eng003.edition.meta. After initial uploads
you find an `filename.imex` which has a mapping of lokal file names to textgrid URIs.
This can be used to update the objects from the edition like:

        tgadmin --server http://test.textgridlab.org update-imex eng003.edition.imex .

## BYOLR (Bring Your Own Link Rewriter ;-)

We use command line tools to rewrite links in TEI and aggregations. Our default choice is
[linkrewriter-cli](https://gitlab.gwdg.de/dariah-de/textgridrep/linkrewriter-cli) but you are free to
choose anything which implements the command line interface.

To use the link rewriter cli as native build (linux amd64 only for now):

```bash
wget https://gitlab.gwdg.de/api/v4/projects/45698/packages/generic/linkrewriter/0.1.23/linkrewriter-cli
chmod +x ./linkrewriter-cli
```

or on non linux-amd64 systems:
```bash
wget https://gitlab.gwdg.de/api/v4/projects/45698/packages/generic/linkrewriter/0.1.23/linkrewriter-cli.jar
echo -e '#!/bin/bash\njava -jar linkrewriter-cli.jar $@' > ./linkrewriter-cli
chmod +x ./linkrewriter-cli
```

If you are not on linux amd64, you may use linkrewriter with java. You may create a shell script calling `java -jar linkrewriter-cli.jar $#` then, or build something great with [jbang](https://www.jbang.dev/).

Or if you are not happy with linkrewriter results, create a shell script, utilizing e.g. [sed](https://sed.sourceforge.io/). Just call it linkrewriter-cli and make sure it implements the cli interface

* `-i imex_file_location`
* `-c config` you may ignore this
* `-b base` path of xml relative to the imex file location (you may ignore this too)
* `FILENAME`

## Advanced Usage

You may use the development or the test instance of the TextGrid Server.

To use tgadmin with the test instance do

        tgadmin --server https://test.textgridlab.org list

for the dev system there is a shortcut, you may call

        tgadmin --dev list

[shell completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/)

        _TGADMIN_COMPLETE=bash_source tgadmin > tgadmin-complete.bash
        . tgadmin-complete.bash

## Development

clone repo

        git clone https://gitlab.gwdg.de/dariah-de/textgridrep/tgadmin.git
        cd tgadmin

and create venv

        python3 -m venv venv
        . venv/bin/activate
        pip install --editable .[dev]

afterwards tgadmin is in your venv as command and can be executed

        tgadmin

run integration tests and check coverage

        export PROJECT_ID=[my-project-id]
        export TEXTGRID_SID=[my-session-id]
        coverage run -m pytest --junitxml=report.xml && coverage html

## Contributing

Commit convention:

- Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

Style constraints:

- Code: [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Documentation: [Google style docstrings (Chapter 3.8 from Google styleguide)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)

Coding constraints:

For your convenience, pre-commit hooks are configured to check against these constraints. Provided, you have installed the development requirements (see above), activate `pre-commit` to run on ever
y `git commit`:

        pre-commit install

## Badges

[![REUSE status](https://api.reuse.software/badge/gitlab.gwdg.de/dariah-de/textgridrep/tgadmin)](https://api.reuse.software/info/gitlab.gwdg.de/dariah-de/textgridrep/tgadmin)
[![PyPI](https://img.shields.io/pypi/v/tgadmin)](https://pypi.org/project/tgadmin/)
