# Cross Referencing Guides to CRISPRs

The *Index* stage of the pipeline will create a binary file containing the gRNA guides. In order to cross reference the guides to the CRISPRs found in the *Gather* stage it is recommended to use a database as *Search* and *Align* will only give a CRISPR ID.
For most applications this will be a SQLite database (as it is read-only) but other databases can be used.

To set up an SQLite database, first install SQLite3 and then create a database file:

```bash
sqlite3 crispr.db
```

we will use a table to hold the CRISPRs data as follows:

```sql
CREATE TABLE crisprs (
    id integer primary key,
    chr_name text,
    chr_start integer,
    seq text,
    pam_right integer,
);
```

We include a script to automate this for you using SQLite3:

```bash
python scripts/index_database.py -d crispr.db \
  -i chromosome.1.csv \
  -i chromosome.2.csv \
  -i chromosome.3.csv \
  ...
```

Note that the offset is set to 0 by default, if you have set a different offset in the *Index* stage then you will need to set the offset with the *-o* flag.

Also note that the sequence with which the *-i* flag is used determines the order of the importation of the CRISPRs into the database.

