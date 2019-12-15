import csv
import unittest

def get_data(test, data):
    output = []
    for i in data:
        if i == test:
            output = i
            yield output
    yield output


class TestExtractedData(unittest.TestCase):

    def test1(self):
        line = 'Ammann,Roller Parts,ASC100,ND011710,LEFT COVER'
        with open('catalogue9.csv', 'r') as f:
            csvreader = csv.reader(f)
            # extract = (row for row in csvreader if row == line.split(','))
            extract = get_data(line.split(','), csvreader)
            print(next(extract))
            self.assertEqual(next(extract), line.split(','))

    def test2(self):
        line = 'Ammann,Roller Parts,ASC100,ND011710 - LEFT COVER'
        with open('catalogue9.csv', 'r') as f:
            csvreader = csv.reader(f)
            # extract = (row for row in csvreader if row == line.split(','))
            extract = get_data(line.split(','), csvreader)
            print(next(extract))
            self.assertEqual(next(extract), [])

if __name__ == '__main__':
    unittest.main()
