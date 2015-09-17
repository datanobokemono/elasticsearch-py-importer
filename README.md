# elasticsearch-py-importer
Python file importer for elasticsearch. All imports are working with bulk

## Dependencies
You have to install elasticsearch python client with [https://pip.pypa.io/en/stable/installing/](pip).
```pip install elasticsearch```

## Supported formats
- [x] .CSV
- [ ] .XLS *(todo)*
- [ ] .SQL *(todo)*

### Importing .CSV files
Minimum setup to import CSV file enter following command to your CLI
```python csvimport.py -i *INDEX_NAME* -t *TYPE_NAME* -id *CSV_ID_FIELD* -f *FILENAME*```

There are also following parameters in CSV import
* ```-bs *BULK_SIZE*``` Set bulk size. By default this property is set to 1000
* ```-p``` Log progress every *BULK_SIZE* rows. Also you can track number of CSV rows read like this ```-p *PROGRESS_STEP*```
* ```-d *JSON_DATA*``` Default values for empty columns. The structure of JSON file is ```{"column_name" : "defalut_value"}```