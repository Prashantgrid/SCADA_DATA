# SMARD hourly electricity data for 2024

Original German-language CSV exports from the SMARD Downloadcenter, covering 1 January through 31 December 2024.

| File | Series |
| --- | --- |
| [SMARD_Grosshandelspreise_DE-LU_2024_Stunde.csv](SMARD_Grosshandelspreise_DE-LU_2024_Stunde.csv) | Germany–Luxembourg day-ahead wholesale prices in €/MWh |
| [SMARD_Realisierte_Erzeugung_DE_2024_Stunde.csv](SMARD_Realisierte_Erzeugung_DE_2024_Stunde.csv) | Actual electricity generation in Germany, including `Photovoltaik [MWh]` |

Both files contain 8,784 matching hourly intervals. They use UTF-8 with a byte-order mark, a semicolon delimiter and decimal commas. The local start time `27.10.2024 02:00` occurs twice at the daylight saving transition. Preserve row order or join on UTC timestamps.

Source attribution is **Bundesnetzagentur | SMARD.de**. [SMARD Downloadcenter](https://www.smard.de/home/downloadcenter/download-marktdaten) · [SMARD data use and attribution](https://www.smard.de/home/datennutzung)
