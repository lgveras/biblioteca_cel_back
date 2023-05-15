from catalogo.models import Exemplar
import csv, os
from django.core.management.base import BaseCommand, CommandError
from catalogo.models import Exemplar

# Execução
# result_list python manage.py loadextodb --csv_file_name "biblioteca-cel.csv"

class Command(BaseCommand):
    help = "Reads CSV file fo Books to save in Exemplar table";

    def saveRowInDb(self, row):
        newExemplar = Exemplar(titulo = row[0], autor = row[1], exemplar = row[2], area = row[3])
        newExemplar.save();
        self.stdout.write(
            self.style.SUCCESS('Successfully Exemplares loaded on db')
        )

    def processCSVFile(self, file):
        print(os.listdir())
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'[Book: {row[0]}\nAutor:{row[1]}\nExemplar:{row[2]}\nArea:{row[3]}.')
                    line_count += 1
                    self.saveRowInDb(row)
            print(f'Processed {line_count} lines.')

    def add_arguments(self, parser):
        parser.add_argument("--csv_file_name", 
                            help="Reads te CSVs file with examplares ")

    def handle(self, *args, **options):
        fileName = options["csv_file_name"];
        try:
            self.processCSVFile(fileName)
        except FileNotFoundError as error:
            raise CommandError('Error: See if the filename {} is valid. \nCause:{}.'.format(fileName, error))
        except Exception as error:
            raise CommandError('Error: See what happened. \nCause:{}.'.format(error))