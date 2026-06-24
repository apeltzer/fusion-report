# Add new fusion database

1. Implement a new database in `fusion_report/data/{database}.py`. You have to include a method `get_all_fusions()`
which should return list of all gene fusion in your database in format `GENEA--GENEB`.

```python
"""Test Database"""
import re
from typing import List

from fusion_report.common.db import Db
from fusion_report.common.singleton import Singleton


class Test(Db, metaclass=Singleton):
    """Implementation of Test Database. All core functionality is handled by parent class."""

    def __init__(self, path: str) -> None:
        super().__init__(path, 'Test', 'Test.sql')

    def get_all_fusions(self) -> List[str]:
        """Returns all fusions from database."""
        query: str = '''SELECT DISTINCT XYZ FROM XYZ'''
        res = self.select(query)

        return res['fusions']
```

2. Create database schema in `fusion_report/data/schema/{database.sql}`. This is a SQL script which defines a structure of your database.
3. Update `enrich()` function in `fusion_report/app.py`

   Add a positive flag derived from a new `--no-testdb` CLI argument, then conditionally load your database:

```python
def enrich(self, params: Namespace) -> None:
    local_fusions: Dict[str, List[str]] = {}
    include_cosmic     = not params.no_cosmic
    include_fusiongdb2 = not params.no_fusiongdb2
    include_mitelman   = not params.no_mitelman
    include_testdb     = not params.no_testdb  # add this line

    if include_cosmic:
        local_fusions.update(
            {CosmicDB(params.db_path).name: CosmicDB(params.db_path).get_all_fusions()}
        )
    if include_fusiongdb2:
        local_fusions.update(
            {FusionGDB2(params.db_path).name: FusionGDB2(params.db_path).get_all_fusions()}
        )
    if include_mitelman:
        local_fusions.update(
            {MitelmanDB(params.db_path).name: MitelmanDB(params.db_path).get_all_fusions()}
        )
    if include_testdb:  # add this block
        local_fusions.update(
            {TestDB(params.db_path).name: TestDB(params.db_path).get_all_fusions()}
        )
    ...
```

   Also add `--no-testdb` to the `databases` list in `fusion_report/arguments.json` so it becomes a recognised CLI flag.

4. Give yourself a high five for awesome job! :+1:
