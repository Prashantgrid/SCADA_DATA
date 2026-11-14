# SMARD hourly electricity data for 2025

Original German-language CSV exports from the SMARD Downloadcenter, covering 1 January through 31 December 2025.

| File | Series |
| --- | --- |
| [SMARD_Grosshandelspreise_DE-LU_2025_Stunde.csv](SMARD_Grosshandelspreise_DE-LU_2025_Stunde.csv) | Germany–Luxembourg day-ahead wholesale prices in €/MWh |
| [SMARD_Realisierte_Erzeugung_DE_2025_Stunde.csv](SMARD_Realisierte_Erzeugung_DE_2025_Stunde.csv) | Actual electricity generation in Germany, including `Photovoltaik [MWh]` |

Both files contain 8,760 matching hourly intervals. They use UTF-8 with a byte-order mark, a semicolon delimiter and decimal commas. The local start time `26.10.2025 02:00` occurs twice at the daylight saving transition. Preserve row order or join on UTC timestamps.

Day-ahead trading switched to 15-minute products starting 1 October 2025. This price file uses SMARD's hourly export, so prices from October through December are hourly aggregates. [SMARD announcement](https://www.smard.de/en/15-minute-wholesale-prices-available-218078)

The generation file reports nationwide PV output. For comparison, the [2024 exports](../SMARD_2024/) use the same markets and hourly resolution.

Source attribution is **Bundesnetzagentur | SMARD.de**. [SMARD Downloadcenter](https://www.smard.de/home/downloadcenter/download-marktdaten) · [SMARD data use and attribution](https://www.smard.de/home/datennutzung)
