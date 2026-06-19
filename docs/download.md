# Download resources

> If you already have the database files locally, you can use [`fusion_report createdb`](createdb.md) to build databases without downloading.

Currently the tool supports three different databases:

* [FusionGDB2](https://compbio.uth.edu/FusionGDB/combined_tables/combinedFGDB2genes_genes_ID_04302024.txt)
* [Mitelman](https://mitelmandatabase.isb-cgc.org/)
* [COSMIC](https://cancer.sanger.ac.uk/cosmic/download/cosmic/v104/fusion)

You can download the databases running:

```bash
fusion_report download
    --cosmic_usr '<username>'
    --cosmic_passwd '<password>'
    /path/to/db
```

With a non-academic/research login -> using QIAGEN with a commercial license:

```bash
fusion_report download
    --cosmic_usr '<QIAGEN username>'
    --cosmic_passwd 'QIAGEN <password>'
    --qiagen
    /path/to/db
```

You can exclude a specific database with --no-cosmic/--no-mitelman/--no-fusiongdb2. Example for no COSMIC:

```bash
fusion_report download
    --no-cosmic
    /path/to/db
```

## Download with Docker

```bash
# Build image locally
docker build -t fusion-report:latest .

# Download databases into host directory
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -w /db \
    -v /path/to/db:/db \
    fusion-report:latest download \
    --cosmic_usr "<username>" \
    --cosmic_passwd "<password>" \
    /db
```


## Manual download

### Mitelman

Website: [https://mitelmandatabase.isb-cgc.org/](https://mitelmandatabase.isb-cgc.org/)

```bash
wget -O mitelman_db.zip "https://storage.googleapis.com/mitelman-data-files/prod/mitelman_db.zip"
fusion_report createdb /path/to/db --mitelman mitelman_db.zip
```

### COSMIC

Website: [https://cancer.sanger.ac.uk/cosmic/download/cosmic/v104/fusion](https://cancer.sanger.ac.uk/cosmic/download/cosmic/v104/fusion)

```bash
PASSWD=$(echo -n "<username>:<password>" | base64)
URL=$(curl -s -H "Authorization: Basic ${PASSWD}" \
  "https://cancer.sanger.ac.uk/api/mono/products/v1/downloads/scripted?bucket=downloads&path=grch38/cosmic/v104/Cosmic_Fusion_Tsv_v104_GRCh38.tar" \
  | jq -r .url)
curl -L "$URL" -o Cosmic_Fusion_Tsv_v104_GRCh38.tar
tar -xf Cosmic_Fusion_Tsv_v104_GRCh38.tar Cosmic_Fusion_v104_GRCh38.tsv.gz
gunzip Cosmic_Fusion_v104_GRCh38.tsv.gz
fusion_report createdb /path/to/db --cosmic Cosmic_Fusion_v104_GRCh38.tsv
```
