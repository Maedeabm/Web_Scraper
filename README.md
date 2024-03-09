# Web_Scraper

# IPL Data Scraper

## Description

IPL Data Scraper is a Python tool designed to scrape and analyze Indian Premier League (IPL) statistics from the official IPL website. It allows users to fetch data for team rankings, player statistics, and other relevant metrics across different years.

## Features

- Fetch and store IPL team rankings and player statistics.
- Interactive user interface for selecting years and statistics to scrape.
- Data stored in CSV format for easy analysis and manipulation.
- Modular design for easy customization and extension.

## Installation

To run this project, you will need Python 3 and the following Python libraries:

- BeautifulSoup
- requests
- pandas
- numpy
- PyInquirer

You can install these dependencies using pip:

```bash
pip install beautifulsoup4 requests pandas numpy PyInquirer

## Usage

To start the application, navigate to the project directory and run:

```bash
python main.py

```

Follow the prompts to select the years and statistics you want to scrape. The scraped data will be saved in CSV files in the current directory.


## Project Structure

- `main.py`: Entry point of the application.
- `scraper.py`: Contains functions related to web scraping.
- `data_processing.py`: Includes functions for processing and storing data.
- `user_interface.py`: Handles user interactions and input.
- `utils.py`: Contains utility functions and constants.


## Contributing

Contributions to the IPL Data Scraper are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
