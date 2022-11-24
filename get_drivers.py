import os
import click
import tarfile
import requests

# part imports
from zipfile import ZipFile
from configparser import ConfigParser


def download_drivers(distribution='all', browser='all'):
    '''
        Funtion for downloading drivers
        @param distribution: distribution of the os driver has to be downloaded for
                        default are all, lin, mac, win
        @param browser: browser for which driver is requested
                        default are all, firefox, google
        @returns: None
    '''

    # defining some base objects
    root_dir = os.path.abspath('.')

    # defining config reader
    cfg = ConfigParser()
    cfg.read('config.ini')

    for i in cfg.sections():

        # check if options provided by user satisfy the section
        if browser != 'all' and browser != i.lower():
            continue

        print(f'Downloading for browser {i}')
        os.chdir(root_dir)
        base_dir = os.path.join(root_dir, i)
        if not os.path.exists(base_dir):
            print(f'base directory does not exists, creating {base_dir}')
            os.makedirs(base_dir)
        os.chdir(base_dir)
        base_url = cfg[i].pop('BASE_URL')
        if i:
            for j in cfg[i].keys():
                if distribution == 'all':
                    pass
                elif not distribution in j.lower():
                    continue
                os.makedirs(j, exist_ok=True)
                filename = cfg[i].get(j)
                print(f'Downloading driver for {j}')

                # Downloading the file and writing it
                with open(filename, 'wb') as f:
                    url = base_url.format(filename)
                    print(url)
                    r = requests.get(url, allow_redirects=True)
                    f.write(r.content)

                # unzipping tar files
                if '.tar.gz' in filename:
                    with tarfile.open(filename, 'r:gz') as tar:
                        tar.list()
                        def is_within_directory(directory, target):
                            
                            abs_directory = os.path.abspath(directory)
                            abs_target = os.path.abspath(target)
                        
                            prefix = os.path.commonprefix([abs_directory, abs_target])
                            
                            return prefix == abs_directory
                        
                        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                        
                            for member in tar.getmembers():
                                member_path = os.path.join(path, member.name)
                                if not is_within_directory(path, member_path):
                                    raise Exception("Attempted Path Traversal in Tar File")
                        
                            tar.extractall(path, members, numeric_owner=numeric_owner) 
                            
                        
                        safe_extract(tar, j)
                        print('unzipped successfully !')

                # unzipping zip files
                elif '.zip' in filename:
                    with ZipFile(filename, 'r') as zip:
                        print(zip.printdir())
                        zip.extractall(j)
                        print('unzipped successfully !')
                # deleting files are unzipping
                os.unlink(filename)


@click.command()
@click.option('--distribution', default='all',
              type=click.Choice(['all', 'mac', 'lin', 'win']),
              help='driver for specific os distribution, \
                  default options include all, lin, mac, win')
@click.option('--browser', default='all',
              type=click.Choice(['all', 'google', 'firefox']),
              help='Browser for which driver has to be downloaded, default choices are \
                  all, google, firefox')
def main(distribution, browser):
    '''
        Main function for the execution
        @param distribution: distribution of the os driver has to be downloaded for
                        default are all, lin, mac, win
        @param browser: browser for which driver is requested
                        default are all, firefox, google
        @returns: None
    '''
    download_drivers(distribution, browser)


if __name__ == '__main__':
    main()
