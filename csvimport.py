# datanobokemono
# v 0.1
import datetime
import csv
import json
import sys
import bokuno_console
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Get arguments as dictionary of parameters as keys and their values 
# If the parameter was given without value it will return 0 by default
args = bokuno_console.get_args()

# ------------------------------------------------------------------------------------------------------

# Get the index name
index_name = "" if not "-i" in args else args["-i"]

# Get the type name
type_name = "" if not "-t" in args else args["-t"]

# Setting ID column
id_name = "" if not "-id" in args else args["-id"]

# Getting CSV file name from arguments
filename = ""
if "-f" in args:
	filename = args["-f"]

# ------------------------------------------------------------------------------------------------------

# Checking vital parameters
if filename and index_name and type_name and id_name:

	# Initialize ElasticSearch
	es = Elasticsearch()

	# Setting bulk size that defines how many rows will be sent in one request to Elastic
	# and how many rows of CSV data will be hold in memory
	bulk_size = 1000
	if "-bs" in args:
		bulk_size = args["-bs"]
	bulk_data = []

	# Rows processed meter
	count = 0

	# Set the progress step in order to track the import progress in command line logs.
	# Progress step is set by -p parameter
	progress_divisor = 0
	if "-p" in args:
		progress_divisor = bulk_size if args["-p"] == 0 else int(args["-p"])

	# Log execution time to optimize it
	time_started = datetime.datetime.now()

	# Initializing default values for empty row cells from json object in -d parameter
	default_values = {}
	if "-d" in args:
		default_values = json.loads(args["-d"])

	# Log beginning of parsing
	print("Parsing file %s" % filename)

	# Opening the file and processing rows
	with open(filename, 'rt', encoding='utf-8') as csv_file:
		if "-ch" in args:
			csv_data = csv.reader(csv_file)
		else:
			csv_data = csv.DictReader(csv_file)

		for row in csv_data:
			count += 1

			#TODO: AUTOINCREMENT

			# Checking if row has id value
			if row[id_name]:
				id_value = row[id_name]

				# Setting default values
				if "-d" in args:
					for k in default_values:
						if not row[k]:
							row[k] = default_values[k]

				# Collecting data as bulk action
				action = {
					"_index" : index_name,
					"_type" : type_name,
					"_id" : id_value,
					"_source" : row
				}
				bulk_data.append(action)

				# -p in arguments stands for Progress allows to track current row
				if progress_divisor and count % progress_divisor == 0:
					bokuno_console.update_print ("%d rows processed\r" % count)

				if count % bulk_size == 0:
					helpers.bulk(es, bulk_data)
					bulk_data = []

	# Index any data left from CSV file
	if len(bulk_data):
		helpers.bulk(es, bulk_data)
		bulk_data = []

	# Outputting number of rows processed
	bokuno_console.update_print ("%d rows processed\r" % count)
	print("")

	# Outputting 
	time_finished = datetime.datetime.now()
	time_took = time_finished - time_started
	print("Your operation took %d minutes and %d seconds" % divmod(time_took.days * 86400 + time_took.seconds, 60))

else:
	print("ERROR: Check your import settings")
