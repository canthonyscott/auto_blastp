import pandas as pd
import numpy as np

class Filtering:

    def __init__(self):
        self.species_to_keep = ['homo sapiens', 'mus musculus', 'danio rerio', 'xenopus laevis',
                       'caenorhabditis elegans', 'drosophila melanogaster', 'rattus rattus',
                       'rattus norvegicus', 'gallus gallus', 'gallus gallus domesticus',
                       'oryctolagus cuniculus', 'sus scrofa', 'sus domesticus']

    def filter_data_set(self, file, type="csv"):
        """
        Takes a CSV file with species, filters them against pre-selected species and creates a new column with the results.
        A column labeled 'species' must exist.
            :param file: string path to a csv file generated
            :param type: type of data; either 'csv' or 'tab'
            :return: pandas dataframe from the original file with a filtered species column
        """

        if type == "csv":
            df = pd.read_csv(file, index_col=0)
        elif type == "tab":
            df = pd.read_table(file, index_col=0)
        else:
            raise TypeError("Unknown filetype entered")

        species_to_keep = ['homo sapiens', 'mus musculus', 'danio rerio', 'xenopus laevis',
                           'caenorhabditis elegans', 'drosophila melanogaster', 'rattus rattus',
                           'rattus norvegicus', 'gallus gallus', 'gallus gallus domesticus',
                           'oryctolagus cuniculus', 'sus scrofa', 'sus domesticus']

        new_col = []
        for x in range(len(df)):
            new_species = []
            row = df.iloc[x]
            try:
                species = row['species'].split(';')
            except AttributeError:
                new_species = np.nan
                new_col.append(new_species)
                continue
            for item in species:
                if item.lower() in species_to_keep:
                    new_species.append(item)
            new_species = ';'.join(new_species)
            new_col.append(new_species)

        df['filtered_species'] = new_col

        return df

    def filter_list_data(self, data: list):
        """
        Takes a list. Each item on the list should be a string with semi-colons separating the species names.
        This function filters that list based on pre-defined species. Use Filtering.species_to_keep to view.
            :param data: list of strings. example: ['Homo Sapiens;Danio Rerio;...]
            :return: Input list with only designated species kept. Empty rows contain np.nan.
        """
        new_data = []
        for row in data:
            new_species = []
            try:
                species = row.split(';')
            except AttributeError:
                new_species = np.nan
                new_data.append(new_species)
                continue
            for individual in species:
                if individual.lower() in self.species_to_keep:
                    new_species.append(individual)
            new_species = ';'.join(new_species)
            new_data.append(new_species)

        return new_data
