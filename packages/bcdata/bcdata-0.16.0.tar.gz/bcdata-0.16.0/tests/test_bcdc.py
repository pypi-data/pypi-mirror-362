import json

import pytest

import bcdata
from bcdata import bcdc

AIRPORTS_PACKAGE = "bc-airports"
AIRPORTS_TABLE = "WHSE_IMAGERY_AND_BASE_MAPS.GSR_AIRPORTS_SVW"
AIRPORTS_DESCRIPTION = "BC Airports identifies locations where aircraft may take-off and land. No guarantee is given that an identified point will be maintained to sufficient standards for landing and take-off of any/all aircraft.  It includes airports, aerodromes, water aerodromes, heliports, and airstrips."
AIRPORTS_COMMENTS = """GSR_AIRPORTS_SVW is a spatially enabled layer comprising AIRPORTS is a point dataset identifying locations where aircraft can take-off and land. No guarantee is given that an identified point will be maintained to sufficient standards for landing and take-off of any/all aircraft.  It includes airports, aerodromes, water aerodromes, heliports, and airstrips."""
AIRPORTS_SCHEMA = """[{"data_precision": 200, "column_comments": "CUSTODIAN_ORG_DESCRIPTION contains the name or description of the custodial organization (usually Ministry and Branch)", "short_name": "CUST_ORG", "data_type": "VARCHAR2", "column_name": "CUSTODIAN_ORG_DESCRIPTION"}, {"data_precision": 1000, "column_comments": "BUSINESS_CATEGORY_CLASS designates the category of business, i.e., airTransportation", "short_name": "BUS_CAT_CL", "data_type": "VARCHAR2", "column_name": "BUSINESS_CATEGORY_CLASS"}, {"data_precision": 1000, "column_comments": "BUSINESS_CATEGORY_DESCRIPTION describes the category of business, i.e., Air Transportation", "short_name": "BUS_CAT_DS", "data_type": "VARCHAR2", "column_name": "BUSINESS_CATEGORY_DESCRIPTION"}, {"data_precision": 500, "column_comments": "OCCUPANT_TYPE_DESCRIPTION contains the description of the occupant type, e.g. Hospital", "short_name": "OCCPNT_TYP", "data_type": "VARCHAR2", "column_name": "OCCUPANT_TYPE_DESCRIPTION"}, {"data_precision": 20, "column_comments": "SOURCE_DATA_ID is a unique occupant id either supplied by the source data system or produced by GSR, depending on the value of SUPPLIED_SOURCE_ID_IND", "short_name": "SRCDATA_ID", "data_type": "VARCHAR2", "column_name": "SOURCE_DATA_ID"}, {"data_precision": 1, "column_comments": "SUPPLIED_SOURCE_ID_IND is an indicator of whether the source data id was supplied by the supplier (Y) or DataBC (N)", "short_name": "SRC_ID_IND", "data_type": "VARCHAR2", "column_name": "SUPPLIED_SOURCE_ID_IND"}, {"data_precision": 500, "column_comments": "AIRPORT_NAME is a business name that can identify the occupant who provides the BC Government or BC Government related services to public, e.g., Burnaby General Hospital, Golden Food Bank", "short_name": "NAME", "data_type": "VARCHAR2", "column_name": "AIRPORT_NAME"}, {"data_precision": 4000, "column_comments": "DESCRIPTION describes the Occupant in more detail, e.g., aerodrome.", "short_name": "DESCRIPTN", "data_type": "VARCHAR2", "column_name": "DESCRIPTION"}, {"data_precision": 1000, "column_comments": "PHYSICAL_ADDRESS contains the civic or non-civic address as a single string, structured according to the specification of the Physical Address and Geocoding Standard, e.g., 420 GORGE RD E, VICTORIA, BC.", "short_name": "ADDRESS", "data_type": "VARCHAR2", "column_name": "PHYSICAL_ADDRESS"}, {"data_precision": 1000, "column_comments": "ALIAS_ADDRESS contains an address string, not a parsed address.  It is the address that will be displayed for presentation purposes, e.g., 32900 Marshall Road, Abbotsford, BC", "short_name": "ALIAS_ADDR", "data_type": "VARCHAR2", "column_name": "ALIAS_ADDRESS"}, {"data_precision": 200, "column_comments": "STREET_ADDRESS is a free form expression of the site descriptor (e.g., unit) and the civic building number / street / street indicator portion of an address, e.g., Unit 1, 123 Main Street East.", "short_name": "ST_ADDRESS", "data_type": "VARCHAR2", "column_name": "STREET_ADDRESS"}, {"data_precision": 15, "column_comments": "POSTAL_CODE is the Canadian Postal code value associated with the physical address, e.g., V9Z 2K1", "short_name": "POSTAL_CD", "data_type": "VARCHAR2", "column_name": "POSTAL_CODE"}, {"data_precision": 100, "column_comments": "LOCALITY is the name of the municipality, community, Federal Indian Reserve (IR), subdivision, regional district, indigenous land or natural feature the occupant site is located in, e.g., Victoria, Saanich IR 1, Capital Regional District.", "short_name": "LOCALITY", "data_type": "VARCHAR2", "column_name": "LOCALITY"}, {"data_precision": 50, "column_comments": "CONTACT PHONE contains the general office phone number of the Occupant, e.g., (250) 555-1234 or 250-555-1234", "short_name": "CONT_PHONE", "data_type": "VARCHAR2", "column_name": "CONTACT_PHONE"}, {"data_precision": 100, "column_comments": "CONTACT_EMAIL contains the \\"general office\\" email address of the Occupant.", "short_name": "CONT_EMAIL", "data_type": "VARCHAR2", "column_name": "CONTACT_EMAIL"}, {"data_precision": 50, "column_comments": "CONTACT FAX contains the general office fax number of the Occupant, e.g., (250) 555-1234 or 250-555-1234", "short_name": "CONT_FAX", "data_type": "VARCHAR2", "column_name": "CONTACT_FAX"}, {"data_precision": 500, "column_comments": "WEBSITE_URL contains the link to the Home page of the Occupant\'s Website", "short_name": "WEBSITE", "data_type": "VARCHAR2", "column_name": "WEBSITE_URL"}, {"data_precision": 500, "column_comments": "IMAGE_URL contains a full URL link to a picture of the Occupant\'s Location.", "short_name": "IMAGE_URL", "data_type": "VARCHAR2", "column_name": "IMAGE_URL"}, {"data_precision": 9, "column_comments": "LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the location of the feature as measured from the equator, e.g., 55.323653", "short_name": "LATITUDE", "data_type": "NUMBER", "column_name": "LATITUDE"}, {"data_precision": 10, "column_comments": "LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of the location of the feature as measured from the prime meridian, e.g., -123.093544", "short_name": "LONGITUDE", "data_type": "NUMBER", "column_name": "LONGITUDE"}, {"data_precision": 1000, "column_comments": "KEYWORDS contains text strings supplied by the Custodian, to be used for search/query purposes. Keywords are separated by the ; delimiter.", "short_name": "KEYWORDS", "data_type": "VARCHAR2", "column_name": "KEYWORDS"}, {"data_precision": 7, "column_comments": "DATE_UPDATED contains the date that the Occupant data was updated in the Occupant structure (system-generated)", "short_name": "DT_UPDATE", "data_type": "DATE", "column_name": "DATE_UPDATED"}, {"data_precision": 1, "column_comments": "SITE_GEOCODED_IND contains a Flag/indicator (Y/N) that the Occupant Physical Address has been geo-coded by the DataBC Address Geocoder and the results provide a valid site address, e.g., Y, N", "short_name": "GEOCD_IND", "data_type": "VARCHAR2", "column_name": "SITE_GEOCODED_IND"}, {"data_precision": 100, "column_comments": "AERODROME STATUS identifies if the facility is certified or registered according to Transport Canada standards, or a derived status from other sources, i.e., Certified, Registered, Decommissioned, Null (unknown).", "short_name": "AER_STATUS", "data_type": "VARCHAR2", "column_name": "AERODROME_STATUS"}, {"data_precision": 1, "column_comments": "AIRCRAFT ACCESS IND indicates whether fixed wing aircraft, not including seaplanes, can land at this aerodrome, i.e., Y, N, Null (unknown).", "short_name": "AIRCR_ACS", "data_type": "VARCHAR2", "column_name": "AIRCRAFT_ACCESS_IND"}, {"data_precision": 50, "column_comments": "DATA_SOURCE is the project or resource from which the aerodrome data was derived, e.g., Canadian Flight Supplement.", "short_name": "DATA_SRCE", "data_type": "VARCHAR2", "column_name": "DATA_SOURCE"}, {"data_precision": 50, "column_comments": "DATA SOURCE YEAR is the year of the project or resource containing the listed aerodrome data, e.g., 2014.", "short_name": "DATASRC_YR", "data_type": "VARCHAR2", "column_name": "DATA_SOURCE_YEAR"}, {"data_precision": 10, "column_comments": "ELEVATION is  the published elevation (in metres) of an aerodrome, or if not published, elevation taken from Google Earth (in metres), e.g., 10", "short_name": "ELEVATION", "data_type": "NUMBER", "column_name": "ELEVATION"}, {"data_precision": 1, "column_comments": "FUEL_AVAILABILITY_IND indicates whether fuel is available at this aerodrome, i.e.,  Y, N, Null (unknown)", "short_name": "FUEL_AVAIL", "data_type": "VARCHAR2", "column_name": "FUEL_AVAILABILITY_IND"}, {"data_precision": 1, "column_comments": "HELICOPTER_ACCESS_IND indicates whether helicopters can land at this aerodrome, i.e., Y, N, Null (unknown).", "short_name": "HELI_ACS", "data_type": "VARCHAR2", "column_name": "HELICOPTER_ACCESS_IND"}, {"data_precision": 4, "column_comments": "IATA_CODE is the International Air Transport Associations\'s unique identifier code, e.g., YYJ.", "short_name": "IATA", "data_type": "VARCHAR2", "column_name": "IATA_CODE"}, {"data_precision": 4, "column_comments": "ICAO_CODE is the International Civil Aviation Organizations\'s unique identifier code, e.g., CYYJ.", "short_name": "ICAO", "data_type": "VARCHAR2", "column_name": "ICAO_CODE"}, {"data_precision": 10, "column_comments": "MAX_RUNWAY_LENGTH is  the length of the longest runway at an aerodrome in metres, e.g., 700", "short_name": "MX_RWAY_LN", "data_type": "NUMBER", "column_name": "MAX_RUNWAY_LENGTH"}, {"data_precision": 10, "column_comments": "NUMBER_OF_RUNWAYS is the total number of runways at an aerodrome, e.g., 5", "short_name": "NUM_RWAY", "data_type": "NUMBER", "column_name": "NUMBER_OF_RUNWAYS"}, {"data_precision": 1, "column_comments": "OIL_AVAILABILITY_IND indicates whether fuel oil is available at this aerodrome, i.e., Y, N, Null (unknown)", "short_name": "OIL_AVAIL", "data_type": "VARCHAR2", "column_name": "OIL_AVAILABILITY_IND"}, {"data_precision": 50, "column_comments": "RUNWAY_SURFACE identifies the material used in a runway or helipad\'s construction, e.g., gravel, asphalt, Null (unknown).", "short_name": "RWAY_SURF", "data_type": "VARCHAR2", "column_name": "RUNWAY_SURFACE"}, {"data_precision": 1, "column_comments": "SEAPLANE_ACCESS_IND indicates whether seaplanes can land at this aerodrome, i.e., Y, N, Null (unknown).", "short_name": "SEAPLN_ACC", "data_type": "VARCHAR2", "column_name": "SEAPLANE_ACCESS_IND"}, {"data_precision": 4, "column_comments": "TC_LID_CODE is the Transport Canada Location Identifier unique code, e.g., CAP5.", "short_name": "TC_LID", "data_type": "VARCHAR2", "column_name": "TC_LID_CODE"}, {"data_precision": 64, "column_comments": "SHAPE is the column used to reference the spatial coordinates defining the feature.", "short_name": "SHAPE", "data_type": "SDO_GEOMETRY", "column_name": "SHAPE"}, {"data_precision": 10, "column_comments": "SEQUENCE_ID contains a value to distinguish occupant instances. Where a single occupant can have multiple instances (representing different services, for example), this field distinguishes this occupant instance from other instances of the same or different occupants.", "short_name": "SEQ_ID", "data_type": "NUMBER", "column_name": "SEQUENCE_ID"}, {"data_precision": 4000, "column_comments": "SE_ANNO_CAD_DATA is a binary column used by spatial tools to store annotation, curve features and CAD data when using the SDO_GEOMETRY storage data type.", "data_type": "BLOB", "column_name": "SE_ANNO_CAD_DATA"}]"""


def test_get_table_name():
    table = bcdc.get_table_name(AIRPORTS_PACKAGE)
    assert table == AIRPORTS_TABLE


def test_get_table_name_invalid():
    with pytest.raises(ValueError):
        bcdc.get_table_name("bc-airports-doesnotexist")


def test_table_name_uppercase():
    table = bcdc.get_table_name(AIRPORTS_PACKAGE.upper())
    assert table == AIRPORTS_TABLE


def test_get_table_definition():
    table_definition = bcdc.get_table_definition(AIRPORTS_TABLE)
    assert table_definition["description"] == AIRPORTS_DESCRIPTION
    assert table_definition["comments"] == AIRPORTS_COMMENTS
    assert table_definition["schema"] == json.loads(AIRPORTS_SCHEMA)


def test_get_table_definition_format_multi():
    table_definition = bcdc.get_table_definition(
        "WHSE_FOREST_VEGETATION.OGSR_PRIORITY_DEF_AREA_CUR_SP"
    )
    assert table_definition["description"]
    assert table_definition["comments"]
    assert table_definition["schema"]
    columns = [c["column_name"] for c in table_definition["schema"]]
    assert (
        bcdata.primary_keys["whse_forest_vegetation.ogsr_priority_def_area_cur_sp"].upper()
        in columns
    )


def test_get_table_definition_format_multi_nopreview():
    table_definition = bcdc.get_table_definition("WHSE_BASEMAPPING.FWA_NAMED_POINT_FEATURES_SP")
    assert table_definition["description"]
    assert table_definition["comments"]
    assert table_definition["schema"]


def test_get_table_definition_format_multi_nolayer():
    table_definition = bcdc.get_table_definition(
        "WHSE_HUMAN_CULTURAL_ECONOMIC.HIST_HISTORIC_ENVIRONMNT_PA_SV"
    )
    assert table_definition["description"]
    # assert table_definition["comments"] there are no comments associated with this dataset
    assert table_definition["schema"]


def test_get_table_definition_format_oracle_sde():
    table_definition = bcdc.get_table_definition(
        "WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_RSRV_DESIGN_SP"
    )
    assert table_definition["description"]
    assert table_definition["comments"]
    assert table_definition["schema"]


def test_get_table_definition_nr_districts():
    table_definition = bcdc.get_table_definition("WHSE_ADMIN_BOUNDARIES.ADM_NR_DISTRICTS_SPG")
    assert table_definition["description"]
    assert table_definition["comments"]
    assert table_definition["schema"]
