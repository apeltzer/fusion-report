# ![fusion-report](https://raw.githubusercontent.com/matq007/fusion-report/master/fusion_report/templates/assets/img/fusion-report.png)

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/fusion-report/README.html)
![build](https://github.com/Clinical-Genomics/fusion-report/actions/workflows/integration_tests.yml/badge.svg)
[![Codacy Badge](https://img.shields.io/codacy/grade/932dff8661394cc28448af7b22748bb5)](https://app.codacy.com/gh/Clinical-Genomics/fusion-report/dashboard)
[![DOI](https://zenodo.org/badge/173453958.svg)](https://zenodo.org/badge/latestdoi/173453958)
[![Slack Status](https://img.shields.io/badge/slack-join-brightgreen)](https://nfcore.slack.com/join/shared_invite/zt-418ij0q1d-16KUA7QDk0XYGV~fQ5LFog#/shared-invite/email)

This python script generates an interactive summary report from fusion detection tools. Fusion-report is part of a bigger project [nf-core/rnafusion](https://github.com/nf-core/rnafusion) which is designed to detect and report fusion genes from RNA-seq data.

> **TL;DR**: Live demo [here](https://clinical-genomics.github.io/fusion-report/example/).

## Supported tools

* [STAR-Fusion](https://github.com/STAR-Fusion/STAR-Fusion)
* [EricScript](https://sites.google.com/site/bioericscript/)
* [Pizzly](https://github.com/pmelsted/pizzly)
* [Squid](https://github.com/Kingsford-Group/squid)
* [Dragen](https://emea.illumina.com/products/by-type/informatics-products/dragen-bio-it-platform.html)
* [Arriba](https://github.com/suhrig/arriba)
* [Illumina Dragen](https://emea.illumina.com/products/by-type/informatics-products/dragen-bio-it-platform.html)
* [Jaffa](https://github.com/Oshlack/JAFFA)
* [CTAT-LR-Fusion](https://github.com/TrinityCTAT/CTAT-LR-fusion)

## Installation

### Using Conda

```bash
conda install -c bioconda fusion-report
```

### From source

```bash
# sqlite3 can be installed via conda/mamba as well
sudo apt-get install sqlite3
pip3 install -r requirements.txt && pip3 install .
```

## Usage

```bash
# Download required databases
# Currently supported databases: FusionGDB2, Mitelman and COSMIC
# COSMIC requires login credentials to download Fusion gene Database
fusion_report download --cosmic_usr '<username>' --cosmic_passwd '<password>' /path/to/db/

# Run the fusion-report
fusion_report run "<SAMPLE NAME>" /path/to/output /path/to/db/ \
  --arriba tests/test_data/arriba.tsv \
  --dragen tests/test_data/dragen.tsv \
  --ericscript tests/test_data/ericscript.tsv \
  --fusioncatcher tests/test_data/fusioncatcher.txt \
  --pizzly tests/test_data/pizzly.tsv \
  --squid tests/test_data/squid.txt \
  --starfusion tests/test_data/starfusion.tsv \
  --jaffa tests/test_data/jaffa.csv \
  --allow-multiple-gene-symbols # in case gene symbol in fusion can't be determined, treat each provided fusion as a separate one.
```

Or get help and list all possible parameters.

```bash
fusion_report --help
fusion_report run --help
fusion_report download --help
```

## Docker

You can run the CLI via Docker without installing Python locally.

```bash
# Build image locally
docker build -t fusion-report:latest .

# Show help
docker run --rm -u "$(id -u):$(id -g)" -w /db -v /path/to/db:/db fusion-report:latest --help

# Example: run report (mount output, db, and input data)
docker run --rm \
  -u "$(id -u):$(id -g)" \
  -w /db \
  -v /path/to/output:/output \
  -v /path/to/db:/db \
  -v /path/to/input:/input \
  fusion-report:latest run "sample" /output /db \
  --arriba /input/arriba.tsv \
  --starfusion /input/starfusion.tsv
```

For more info on how to run the script, please see the [documentation](https://clinical-genomics.github.io/fusion-report/).

## Documentation

- [Download resources](docs/download.md)
- [Create databases from local files](docs/createdb.md)
- [Running the tool](docs/usage.md)
- [Fusion Indication Index](docs/score.md)
- [Customize report](docs/customize_report.md)
- [Available templating variables](docs/templating.md)
- [Add new fusion tool](docs/add_tool.md)
- [Add new fusion database](docs/add_database.md)

## Credits

* Testing dataset copied from [ndaniel/fusioncatcher](https://github.com/ndaniel/fusioncatcher).
* DNA icon made by [Freepik](https://www.magnific.com/) from [Flaticon](https://www.flaticon.com) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
