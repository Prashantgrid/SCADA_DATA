# NIST PV arrays and weather station: one-minute records, 2015–2018

Source: NIST Campus Photovoltaic (PV) Arrays and Weather Station Data Sets.
Dataset DOI: https://doi.org/10.18434/M3S67G
Official download portal: https://pvdata.nist.gov/
Metadata: https://catalog.data.gov/dataset/nist-campus-photovoltaic-pv-arrays-and-weather-station-data-sets
Downloaded: 2026-10-01.

## Scope

The download contains the original annual **one-minute** ZIP archives for Canopy, Ground, Roof, WS_1 and WS_2, for calendar years 2015, 2016, 2017 and 2018. WS_1 and WS_2 are the two weather-station logger datasets. The original archives have not been edited. One-second records, photographs and I–V-curve archives are outside this download.

The `raw/` directory contains 20 original annual data archives: one per year and location. Extract the archive for the year and location you need; it contains daily CSV files arranged by year and month. The `documentation/` directory contains the NIST data dictionary, dataset description paper, and sampled column headers for each year and location. The manifest records the original filename, file size, Box file identifier, publisher SHA-1 checksum and locally computed SHA-256 checksum. Every data archive was checked against the publisher size and SHA-1 before packaging.

## Interpretation for the inverter study

These are measurements from three PV arrays in **Gaithersburg, Maryland, USA**, with one inverter per array and different configurations. They are not measurements from the 18-inverter plant in Java. They can support an external test of how a 36-day window represents a longer mission profile, across seasons and years. They cannot directly validate persistence of the relative stress ranking of the Java inverters, their failure rates, or their insurance losses.

The NIST dictionary documents AC/DC power, currents, voltages, inverter states/faults, ambient temperature, irradiance and module temperatures. Inverter temperature fields differ by array: the Roof array includes inverter heatsink and internal-air temperature; Canopy and Ground include RTD_C(10), identified as inverter internal ambient temperature. These are not measured semiconductor junction temperatures. Consult the supplied dictionary and the actual headers before assigning variables.

Timestamps use **Eastern Standard Time, UTC−05:00, without daylight saving time**, as specified in the dataset paper. One-minute variables are aggregates (average, minimum, maximum or sum), not all instantaneous samples. Missing or faulty readings must be screened; do not interpret data availability or an archive covering a calendar year as proof of a complete, valid record. The dataset paper describes outages and maintenance events, including an inverter arcing event and module removal/reinstallation at the Ground array in 2015.

## Citation

Boyd, M. (2017). Performance Data from the NIST Photovoltaic Arrays and Weather Station. Journal of Research of the National Institute of Standards and Technology, 122, Article 40. https://doi.org/10.6028/jres.122.040

Dataset DOI: https://doi.org/10.18434/M3S67G
License indicated by the official catalog: https://www.nist.gov/open/license

## Archive coverage check

The accompanying archive_inventory.csv counts daily CSV files and lists missing dates. This is a file-level check, not an audit of within-day timestamps, missing values or sensor validity.

- Roof 2015: 364 daily CSV files; 1 calendar dates have no daily file. File-date range: 2015-01-01 to 2015-12-31.
- Roof 2016: 364 daily CSV files; 2 calendar dates have no daily file. File-date range: 2016-01-01 to 2016-12-31.
- Roof 2018: 77 daily CSV files; 288 calendar dates have no daily file. File-date range: 2018-01-01 to 2018-03-18.

## Inverter temperature channels

| Array | CSV column | Measurement |
|---|---|---|
| Canopy, Ground | `RTD_C_Avg_10` | Air temperature inside the inverter |
| Roof | `InvTempHeatsink_C_Avg` | Inverter heatsink temperature |
| Roof | `InvTempInternalAir_C_Avg` | Air temperature inside the inverter general enclosure |
| Roof | `InvTempInverterAir_C_Avg` | Air temperature inside the inverter enclosure |

All temperature values are in degrees Celsius and these channels are one-minute averages. Column presence and sample readings were checked for each archive. A full channel-validity audit has not been performed. Invalid values such as `-999` occur in Roof temperature channels and must be treated as missing before thermal-cycle analysis. Semiconductor junction temperature is not directly measured.
