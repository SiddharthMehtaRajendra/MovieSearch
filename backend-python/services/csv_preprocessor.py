import csv

class CSVReader:

    def __init__(self, path):
        self.path = path

    def file_reader(self, domain):
        with open(self.path + '/' + domain + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader) #Skip first (header) row
            line_count = 0
            self.data = []
            for row in csv_reader:
                self.data.append(row)
                line_count += 1
            return self.data
            


