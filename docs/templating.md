# Available templating variables

The report is generated using [Jinja2](https://jinja.palletsprojects.com/). Shown below are all
available variables that can be used in the report.

## Variables

* `title`: Title of the page
* `filename`: Name of the file
* `view`: View used to generate the page
* `modules: Dict[str, Any]`: Dictionary of modules and their variables
* `menu`: List of menu items

Each `Page` can include custom extra variables. Therefore, you may also observe variables such as `sample`, `db_path`, `fusion`, or `tool_cutoff`.

## Functions

* `get_id()`: converts title page into a HTML id tag (used in menu to scroll exactly on the section)
* `include_raw()`: loads custom CSS or JS. This is necessary because each file has these resources injected into the page source.
This removes the need for an external `assets` folder, at the cost of larger output files.
