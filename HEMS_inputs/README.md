# HEMS study source data

The study uses the [2024 SMARD hourly exports](../SMARD_2024/) and [2025 SMARD hourly exports](../SMARD_2025/) for Germany–Luxembourg day-ahead prices and German PV generation. Source and attribution: Bundesnetzagentur | SMARD.de, [CC BY 4.0](https://www.smard.de/en/datennutzung).

The `raw/` folder preserves the following publisher files. The [manifest](raw_manifest.json) records the byte count, download URL and checksum of each source file.

| Input | Original source | Coverage |
| --- | --- | --- |
| BDEW standard load profiles | [BDEW 2025 release](https://www.bdew.de/energie/standardlastprofile-strom/) as distributed in the [CC0 standardlastprofile 2.0.1 CRAN mirror](https://github.com/cran/standardlastprofile/tree/2.0.1/inst/extdata) | Original workbook distributed with the package. Its H25 table was checked cell for cell against the workbook currently on the BDEW site. BDEW derived H25 from balancing data for 2018–2019. |
| FfE residential EV field trial | [Ostermann et al., FfE BDL Project (2023), dataset 86](https://opendata.ffe.de/dataset/electric-load-profiles-and-vehicle-data-of-private-households-with-a-bidirectional-ev/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Original 15-minute JSON series and metadata. Twenty pilot households with bidirectional EVs, measured in 2021–2022. |
| WPuQ household and heat-pump loads | [Schlemminger et al., WPuQ](https://doi.org/10.5281/zenodo.5642902), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Original 2019 and 2020 15-minute HDF5 files and publisher metadata. Heat pumps in this district are water-to-water units connected to a low-temperature network. |

WPuQ HDF5 files are stored in sequential 64 MiB parts to fit GitHub's individual file limit. The parts form the original HDF5 files byte for byte. Run this from the repository's `HEMS_inputs` directory to reassemble and verify the files:

```sh
for year in 2019 2020; do
  cat raw/"${year}_data_15min.hdf5".part-* > "${year}_data_15min.hdf5"
done
printf '%s\n' \
  'f8971419fa5138c9e69be58a79e2e5a8  2019_data_15min.hdf5' \
  '404468c09dd4cb467828144fce6378c2  2020_data_15min.hdf5' | md5sum -c -
```

The [SimBench](https://simbench.de/en/download/) low-voltage networks provide the benchmark topologies and ratings.
