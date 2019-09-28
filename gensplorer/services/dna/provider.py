import csv
from io import StringIO
import zipfile
import os

from enum import Enum


ftdna_mappings = {
    "name": "Name",
    "matchname": "Match Name",
    "chromosome": "Chromosome",
    "start": "Start Location",
    "end": "End Location",
    "centimorgans": "Centimorgans",
    "snps": "Matching SNPs"
}

myheritage_mappings = {
    "DNA Match ID": "myheritageid",
    "name": "Name",
    "matchname": "Match name",
    "chromosome": "Chromosome",
    "start": "Start Location",
    "end": "End Location",
    "startRSID": "Start RSID",
    "endRSID": "End RSID",
    "centimorgans": "Centimorgans",
    "snps": "SNPs"
}


def dict2dict(input, mapping):
    output = {}
    for dest, source in mapping.items():
        output[dest] = input[source].strip()

    return output


class DNAProvider(str, Enum):
    ftdna: str = "ftdna"
    myheritage: str = "myheritage"

    @staticmethod
    def parse_overlap(data, provider):
        if provider == DNAProvider.ftdna:
            return DNAProvider.parse_overlap_ftdna(data)

        if provider == DNAProvider.myheritage:
            return DNAProvider.parse_overlap_myheritage(data)

    @staticmethod
    def parse_overlap_ftdna(data):

        f = StringIO(data)
        reader = csv.DictReader(f)

        segments = []
        for row in reader:
            segments.append(dict2dict(row, ftdna_mappings))

        return {'segments': segments,
                'name': segments[0]['name'],
                'matchname': segments[0]['matchname']}

    @staticmethod
    def parse_overlap_myheritage(data):
        mappings = {k: myheritage_mappings[k] for k in (
            'chromosome', 'start', 'end', 'centimorgans', 'name', 'matchname', 'snps')}
        # Idiotic hack because MyHeritage can't decide on casing
        mappings['matchname'] = "Match Name"
        f = StringIO(data)
        reader = csv.DictReader(f)

        segments = []
        for row in reader:
            segments.append(dict2dict(row, mappings))

        return {'segments': segments,
                'name': segments[0]['name'],
                'matchname': segments[0]['matchname']}

    @staticmethod
    def parse_matchfile_ftdna(data):
        mappings = {k: ftdna_mappings[k] for k in (
            'chromosome', 'start', 'end', 'centimorgans', 'snps')}

        f = StringIO(data.decode('utf-8-sig'))
        reader = csv.DictReader(f)

        current_name = None
        segments = []
        for row in reader:
            if row['Match Name'] != current_name:
                if current_name is not None:
                    yield {'segments': segments, 'matchname': current_name}
                current_name = row['Match Name']
                segments = []

            segments.append(dict2dict(row, mappings))
        yield {'segments': segments, 'matchname': current_name}

    @staticmethod
    def parse_matchfile_myheritage(data):
        mappings = {k: myheritage_mappings[k] for k in (
            'chromosome', 'start', 'end', 'centimorgans', 'snps')}

        f = StringIO(data.decode('utf-8'))
        reader = csv.DictReader(f)

        current_name = None
        segments = []
        for row in reader:
            if row['Match name'] != current_name:
                if current_name is not None:
                    yield {'segments': segments, 'matchname': current_name}
                current_name = row['Match name']
                segments = []

            segments.append(dict2dict(row, mappings))
        yield {'segments': segments, 'matchname': current_name}

    @staticmethod
    def parse_matchfile(provider, datafile):
        data = None
        if zipfile.is_zipfile(datafile):
            filename = ".".join(os.path.basename(
                datafile).split('.')[0:-1]) + ".csv"
            print(filename)
            with zipfile.ZipFile(datafile) as zipped:
                with zipped.open(filename) as f:
                    data = f.read()
        else:
            with open(datafile, 'rb') as f:
                data = f.read()

        if provider == DNAProvider.ftdna:
            return DNAProvider.parse_matchfile_ftdna(data)

        if provider == DNAProvider.myheritage:
            return DNAProvider.parse_matchfile_myheritage(data)
