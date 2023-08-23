from os import path, mkdir

from pandas import DataFrame


def save_on_csv(data, csv_filename):
    df = DataFrame(data)

    directory = './data'

    if not path.exists(directory):
        mkdir(directory)

    df.to_csv(f'{directory}/{csv_filename}.csv', index=False)

    print(f'Data saved to {csv_filename}')
