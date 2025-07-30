# bcdata 

[![Actions Status](https://github.com/smnorris/bcdata/actions/workflows/tests.yml/badge.svg)](https://github.com/smnorris/bcdata/actions?query=workflow%3Atests)
[![pypi](https://img.shields.io/pypi/v/bcdata.svg)](https://pypi.python.org/pypi/bcdata/)

Python and command line tools for quick access to DataBC geo-data available via WFS.

There is a [wealth of British Columbia geographic information available as open
data](https://catalogue.data.gov.bc.ca/dataset?download_audience=Public),
but most sources are available only via WFS - and the syntax to download WFS data via `ogr2ogr` and/or `curl/wget` can be awkward.

This tool attempts to simplify downloads of BC geographic data and smoothly integrate with PostGIS and Python GIS tools like `geopandas`, `fiona` and `rasterio`. The tool only accesses geographic data [avialable via WFS](https://bcgov.github.io/data-publication/pages/tips_tricks_webservices.html) - for other BC open data, download the files directly with `requests` / `curl` / `ogr2ogr` / etc (or the [bcdata R package](https://github.com/bcgov/bcdata)).

If downloads are failing, consult the [BCGov Data Systems and Services uptime monitor](https://uptime.com/statuspage/bcgov-dss) - this tool depends on BC Open Geospatial Web Services API at [openmaps.gov.bc.ca](https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&request=Getcapabilities) and the [BC Data Catalogue API](https://catalogue.data.gov.bc.ca/dataset/bc-data-catalogue-api). 

**Disclaimer**  
*Data are generally licensed as [OGL-BC](http://www2.gov.bc.ca/gov/content/governments/about-the-bc-government/databc/open-data/open-government-license-bc), but it is the user's responsibility to check the licensing for any downloads.*

## Installation and dependencies

Install with `pip`:

    $ pip install bcdata

Note that `bcdata` requires `gdal` to already be installed to a known location.
If this is not the case on your system, the [GeoPandas guide](https://geopandas.org/en/stable/getting_started/install.html) is useful for setting up a stand alone environment with `conda`.

## Configuration

### Default PostgreSQL database

The default target database connection (used by `bc2pg`) can be set via the `DATABASE_URL` environment variable (the password parameter should not be required if using a [.pgpass file](https://www.postgresql.org/docs/current/libpq-pgpass.html))

Linux/Mac: `export DATABASE_URL=postgresql://{username}:{password}@{hostname}:{port}/{database}`

Windows:   `SET DATABASE_URL=postgresql://{username}:{password}@{hostname}:{port}/{database}`


### Layer list / layer schema cache

To reduce the volume of requests, information about data requested is cached locally. 
Schemas of individual layers that have previously been requested are cached with the cache file name matching the object/table name.
Location of the cache defaults to `~/.bcdata` but can be modified by setting the `BCDATA_CACHE` environment variable:

`export BCDATA_CACHE=/path/to/bcdata_cache`

The cache will automatically refresh after 30 days - force a cache refresh by deleting the files in the cache or the entire cache folder.

## Usage

Typical usage will involve a manual search of the [DataBC Catalogue](https://catalogue.data.gov.bc.ca/dataset?download_audience=Public) to find a layer of interest. Once a dataset of interest is found, note the key with which to retreive it. This can be either the `id`/`package name` (the last portion of the url) or the `Object Name` (Under `Object Description`).

For example, for [BC Airports]( https://catalogue.data.gov.bc.ca/dataset/bc-airports), either of these keys will work:

- id/package name: `bc-airports`
- object name: `WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW`

Note that some packages [may have more than one layer](https://catalogue.data.gov.bc.ca/dataset/forest-development-units) - if you request a package like this, `bcdata` will prompt you with a list of valid object/table names to use instead of the package name.


### Python module

```python
import bcdata

# get a feature as geojson
geojson = bcdata.get_data(
    'bc-airports',
    query="AIRPORT_NAME='Terrace (Northwest Regional) Airport'"
)
geojson
{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': 'WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW.fid-f0cdbe4_16811fe142b_-6f34', 'geometry': {'type': 'Point', ...

# optionally, load data as a geopandas GeoDataFrame
gdf = bcdata.get_data(
    'bc-airports',
    query="AIRPORT_NAME='Terrace (Northwest Regional) Airport'",
    as_gdf=True
)
gdf.head()
AERODROME_STATUS AIRCRAFT_ACCESS_IND                          AIRPORT_NAME                ...                TC_LID_CODE WEBSITE_URL                          geometry
0        Certified                   Y  Terrace (Northwest Regional) Airport                ...                       None        None  POINT (-128.5783333 54.46861111)
```

### CLI
Commands available via the bcdata command line interface are documented with the --help option

```

$ bcdata --help

Usage: bcdata [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  bc2pg  Load a DataBC WFS layer to a postgres db
  cat    Write DataBC features to stdout as GeoJSON feature objects.
  dump   Write DataBC features to stdout as GeoJSON feature collection.
  info   Print basic metadata about a DataBC WFS layer as JSON.
  list   List DataBC layers available via WFS
```

#### bc2pg

```
$ bcdata bc2pg --help

Usage: bcdata bc2pg [OPTIONS] DATASET

  Load a DataBC WFS layer to a postgres db

   $ bcdata bc2pg whse_imagery_and_base_maps.gsr_airports_svw

Options:
  -db, --db_url TEXT              Target database url, defaults to
                                  $DATABASE_URL environment variable if set
  --table TEXT                    Destination table name
  --schema TEXT                   Destination schema name
  --geometry_type TEXT            Spatial type of geometry column
  --query TEXT                    A valid CQL or ECQL query
  --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                  bottom, right, top]". Coordinates are BC
                                  Albers (default) or --bounds_crs
  --bounds-crs, --bounds_crs TEXT
                                  CRS of provided bounds
  -c, --count INTEGER             Total number of features to load
  -k, --primary_key TEXT          Primary key of dataset
  -s, --sortby TEXT               Name of sort field
  -e, --schema_only               Create empty table from catalogue schema
  -a, --append                    Append to existing table
  -r, --refresh                   Truncate from existing table before load
  -t, --no_timestamp              Do not log download to bcdata.log
  -v, --verbose                   Increase verbosity.
  -q, --quiet                     Decrease verbosity.
  --help                          Show this message and exit.
```

#### cat

```
$ bcdata cat --help

Usage: bcdata cat [OPTIONS] DATASET

  Write DataBC features to stdout as GeoJSON feature objects.

Options:
  --query TEXT                    A valid CQL or ECQL query
  -c, --count INTEGER             Number of features to request and dump
  --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                  bottom, right, top]". Coordinates are BC
                                  Albers (default) or --bounds_crs
  --bounds-crs, --bounds_crs TEXT
                                  CRS of provided bounds
  --indent INTEGER                Indentation level for JSON output
  --compact / --not-compact       Use compact separators (',', ':').
  -s, --sortby TEXT               Name of sort field
  -l, --lowercase                 Write column/properties names as lowercase
  -m, --promote-to-multi          Promote features to multipart
  -v, --verbose                   Increase verbosity.
  -q, --quiet                     Decrease verbosity.
  --help                          Show this message and exit.
```

#### dump 

```
$ bcdata dump --help

Usage: bcdata dump [OPTIONS] DATASET

  Write DataBC features to stdout as GeoJSON feature collection.

    $ bcdata dump bc-airports
    $ bcdata dump bc-airports --query "AIRPORT_NAME='Victoria Harbour (Shoal Point) Heliport'"
    $ bcdata dump bc-airports --bounds xmin ymin xmax ymax

   It can also be combined to read bounds of a feature dataset using Fiona: 
   $ bcdata dump bc-airports --bounds $(fio info aoi.shp --bounds)

Options:
  --query TEXT                    A valid CQL or ECQL query
  -c, --count INTEGER             Number of features to request and dump
  --bounds TEXT                   Bounds: "left bottom right top" or "[left,
                                  bottom, right, top]". Coordinates are BC
                                  Albers (default) or --bounds_crs
  --bounds-crs, --bounds_crs TEXT
                                  CRS of provided bounds
  -s, --sortby TEXT               Name of sort field
  -l, --lowercase                 Write column/properties names as lowercase
  -m, --promote-to-multi          Promote features to multipart
  -v, --verbose                   Increase verbosity.
  -q, --quiet                     Decrease verbosity.
  --help                          Show this message and exit.
```

#### info

```
$ bcdata info --help

Usage: bcdata info [OPTIONS] DATASET

  Print basic metadata about a DataBC WFS layer as JSON.

  Optionally print a single metadata item as a string.

Options:
  --indent INTEGER  Indentation level for JSON output
  --count           Print the count of features.
  --name            Print the table name of the dateset.
  --description     Print the description of the dateset.
  -v, --verbose     Increase verbosity.
  -q, --quiet       Decrease verbosity.
  --help            Show this message and exit.
```

#### list

```
$ bcdata list --help

Usage: bcdata list [OPTIONS]

  List DataBC layers available via WFS

Options:
  -r, --refresh  Refresh the cached list
  --help         Show this message and exit.
```

#### CLI notes

Note that `bc2pg` creates `bcdata.log` and logs the most recent download date for each table downloaded.
Disable with the switch `--no_timestamp` if you do not wish to create this table.

Example of a record in `bcdata.log`:

```
mydb=# select * from bcdata.log;
                 table_name                  |        latest_download
---------------------------------------------+-------------------------------
 whse_imagery_and_base_maps.gsr_airports_svw | 2021-02-17 11:50:34.044481-08
```


#### CLI examples

Search the data listing for airports:

      $ bcdata list | grep AIRPORTS
      WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW

Describe a dataset. Note that if we know the id of a dataset, we can use that rather than the object name:

    $ bcdata info bc-airports --indent 2
    {
      "name": "WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW",
      "count": 455,
      "schema": {
        "properties": {
          "CUSTODIAN_ORG_DESCRIPTION": "string",
          "BUSINESS_CATEGORY_CLASS": "string",
          "BUSINESS_CATEGORY_DESCRIPTION": "string",
          "OCCUPANT_TYPE_DESCRIPTION": "string",
          ...etc...
        },
        "geometry": "GeometryCollection",
        "geometry_column": "SHAPE"
      }
    }

The JSON output can be manipulated with [jq](https://stedolan.github.io/jq/). For example, to show only the fields available in the dataset:

    $ bcdata info bc-airports | jq '.schema'
    {
      "CUSTODIAN_ORG_DESCRIPTION": "string",
      "BUSINESS_CATEGORY_CLASS": "string",
      "BUSINESS_CATEGORY_DESCRIPTION": "string",
      "OCCUPANT_TYPE_DESCRIPTION": "string",
      etc...
    }

Dump data as supplied by server (BC Albers):

    $ bcdata dump bc-airports > bc-airports.geojson

Dump data to geojson that conforms to [RFC7946](https://tools.ietf.org/html/rfc7946#section-4)):

    $ bcdata dump bc-airports | \
        ogr2ogr -f GeoJSON -lco RFC7946=YES /vsistdout/ /vsistdin/ > bc-airports-4326.geojson

Dump to Parquet on S3:

    $ bcdata dump bc-airports | \
        ogr2ogr -f Parquet /vsis3/$BUCKET/airports.parquet /vsistdin/

Load data to postgres and run a spatial query:

    $ bcdata bc2pg bc-airports \
        --db_url postgresql://postgres:postgres@localhost:5432/postgis

    $ bcdata bc2pg WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP \
        --db_url postgresql://postgres:postgres@localhost:5432/postgis

    $ psql -c \
      "SELECT airport_name
       FROM whse_imagery_and_base_maps.gsr_airports_svw a
       INNER JOIN whse_legal_admin_boundaries.abms_municipalities_sp m
       ON ST_Intersects(a.geom, m.geom)
       WHERE admin_area_name LIKE '%Victoria%'"
                               airport_name
    ------------------------------------------------------------------
     Victoria Harbour (Camel Point) Heliport
     Victoria Inner Harbour Airport (Victoria Harbour Water Airport)
     Victoria Harbour (Shoal Point) Heliport
    (3 rows)

## Projections / CRS

All data are as supplied from the server by default: BC Albers / `EPSG:3005`. 
Use some other tool to reproject the data as required.

## Development and testing

`bc2pg` tests require database `postgresql://postgres@localhost:5432/test_bcdata` exists and has PostGIS installed:

    psql -c "create database test_bcdata"
    psql test_bcdata -c "create extension postgis"

Create virtualenv and install `bcdata` in development mode:

    $ git clone git@github.com:bcgov/bcdata_py.git
    $ cd bcdata_py
    $ python -m venv .venv
    $ source .venv/bin/activate
    (.venv)$ pip install -e .[test]
    (.venv)$ py.test


## Other implementations
- [bcdata R package](https://github.com/bcgov/bcdata) - official BC Open Data R client
- [OWSLib](https://github.com/geopython/OWSLib) - used internally by `bcdata`
- [pgsql-ogr-fdw](https://github.com/pramsey/pgsql-ogr-fdw) - read WFS data directly into with postgres foreign data wrapper
- general purpose command line tools [(`ogr2ogr`/`curl`/`wget`)](ogr2ogr.md) 
