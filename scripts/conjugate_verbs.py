import csv
import json
import shutil
from tempfile import NamedTemporaryFile

from pykatsuyou import getInflections

fields = [
    'expression', 'stem', 'dictionary form', 'present affirmative', 'present negative', 'past affirmative', 'past negative', 'volitional form', 'te form'
]

tempfile = NamedTemporaryFile(mode='w', delete=False)
with open("./src/data/Verb Conjugations.csv", 'r') as f, tempfile:
    reader = csv.DictReader(
        f,
        delimiter=',',
        quoting=csv.QUOTE_NONE,
        lineterminator='\n',
        fieldnames=fields)
    writer = csv.DictWriter(
        tempfile,
        delimiter=',',
        quoting=csv.QUOTE_NONE,
        lineterminator='\n',
        fieldnames=fields)

    for row in reader:
        if row['dictionary form'] != '':
            writer.writerow(row)
            continue

        expression = str(row['expression'])
        inflections = getInflections(
            expression)
        json_string = inflections['json']
        if json_string == 'Not a verb/adjective':
            writer.writerow(row)
            continue

        json_data = json.loads(json_string)
        new_row = {
            'expression': expression,
            'stem': row['stem'],
            'dictionary form': json_data['Affirmative']['Dict-Form'],
            'present affirmative': json_data['Affirmative']['Non-Past Polite'],
            'present negative': json_data['Negative']['Non-Past Polite'],
            'past affirmative': json_data['Affirmative']['Past Polite'],
            'past negative': json_data['Negative']['Past Polite'],
            'volitional form': json_data['Affirmative']['Volitional'],
            'te form': json_data['Affirmative']['Te-Form']
        }
        writer.writerow(new_row)

shutil.move(tempfile.name, "./src/data/Verb Conjugations.csv")
