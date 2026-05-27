# Create databases from local files

The `createdb` command lets you build fusion databases from local files without downloading them. This is useful when:

- You have pre-downloaded database files from institutional sources
- You want to use a specific COSMIC version without providing credentials each time
- You need to build databases in an air-gapped or offline environment
- You want to rebuild databases from custom or filtered data files

## Usage

Provide at least one database file. Only the databases for which files are supplied will be created.

### Build all three databases

```bash
fusion_report createdb /path/to/db \
    --cosmic Cosmic_Fusion_v101_GRCh38.tsv.gz \
    --mitelman mitelman_db.zip \
    --fusiongdb2 FusionGDB2_id.xlsx
```

### Build only COSMIC

```bash
fusion_report createdb /path/to/db \
    --cosmic Cosmic_Fusion_v101_GRCh38.tsv.gz
```

### Build Mitelman + FusionGDB2 (no COSMIC credentials needed)

```bash
fusion_report createdb /path/to/db \
    --mitelman mitelman_db.zip \
    --fusiongdb2 FusionGDB2_id.xlsx
```

## Supported file formats

| Database | Accepted formats | Notes |
|----------|-----------------|-------|
| **COSMIC** | `.tsv.gz` or `.tsv` | COSMIC Fusion Export file (gzipped or plain). Download from [COSMIC](https://cancer.sanger.ac.uk/cosmic/download) or the respective Qiagen (commercial case) sources |
| **Mitelman** | `.zip` or extracted `MBCA.TXT.DATA` | Mitelman database archive. Download from [Mitelman](https://mitfrednlm.nih.gov). |
| **FusionGDB2** | `.xlsx` or `.csv` | FusionGDB2 Excel export or pre-processed CSV with one fusion per line (`GENE1--GENE2`). Download from [FusionGDB2](https://compbio.uth.edu/FusionGDB2/tables). |

## Comparison: `download` vs `createdb`

| Feature | `download` | `createdb` |
|---------|-----------|-----------|
| Downloads files automatically | Yes | No |
| Requires COSMIC credentials | Yes (unless `--no-cosmic`) | No |
| Works offline | No | Yes |
| Custom file versions | No (uses version in settings) | Yes |
| Selective DB creation | Via `--no-*` flags | Only builds what you provide |

## Output

The command creates `.db` files and a `DB-timestamp.txt` in the output directory:

```
/path/to/db/
├── cosmic.db           # if --cosmic provided
├── mitelman.db         # if --mitelman provided
├── fusiongdb2.db       # if --fusiongdb2 provided
└── DB-timestamp.txt
```

These databases can then be used with `fusion_report run`:

```bash
fusion_report run "sample" /path/to/output /path/to/db/ \
    --starfusion starfusion.tsv \
    --arriba arriba.tsv
```

## All parameters

```bash
fusion_report createdb --help
```
