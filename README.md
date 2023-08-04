# Spider Join Dataset

[Spider](https://yale-lily.github.io/spider) is a large-scale semantic parsing and text-to-SQL dataset. We parse schema SQL files from the development set and retrieve join paths between primary keys and foreign keys as ground truth.

## Resources
`data.zip` contains raw tables in the CSV format.

`dev_metadata.csv` annotates the ground truth of join paths.

`data_loader.py` provides functionalities to load tables and metadata.

## Citation
If you find this dataset useful, please consider citing the following paper.

```
@inproceedings{DBLP:conf/cidr/CongGFJD23,
  author       = {Tianji Cong and
                  James Gale and
                  Jason Frantz and
                  H. V. Jagadish and
                  {\c{C}}agatay Demiralp},
  title        = {WarpGate: {A} Semantic Join Discovery System for Cloud Data Warehouses},
  booktitle    = {13th Conference on Innovative Data Systems Research, {CIDR} 2023, Amsterdam, The Netherlands, January 8-11, 2023},
  publisher    = {www.cidrdb.org},
  year         = {2023}
}
```