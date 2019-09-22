# Fetching Selenium drivers using Python

To facilitate downloading the Selenium drivers from the internet, I have written this utility **GET_DRIVERS**. If you want to contribute to the repo, please make the changes and raise a pull request, I will review and merge the changes.

## Config.ini

I have created a config file with the entries for the drivers. My utility read this file and fetches the drivers from the internet and downloads it.

## How to use the utility

- Install the depedencies using requirements.txt file

  > pip install requirements.txt

- Once the dependencies are installed, run the below commands:
  > python get_drivers.py --distribution='all' --browser='all'
  ### Defaults for Distribution:
  - all
  - lin
  - mac
  - win

### Defaults for browser

- all
- firefox
- google
