# various utility functions and constants can be used throughout this application to improve it. Here are some suggestion.

# 1. Constants for URL and File Paths: Constants for base URLs, file paths, and other frequently used strings can be defined to ensure consistency and ease of maintenance.


BASE_URL = 'https://www.iplt20.com/stats/'
BASE_FILENAME = 'Result'
DATA_FOLDER = './data/'


# 2. Text Cleaning Function: A function to clean and normalize text can be useful since dealing with web scraping is involved.

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


# 3. Logging Utility: For better debugging and tracking, a simple logging utility can be implemented.

def log_message(message, level='INFO'):
    print(f'[{level}] {message}')


# 4. Exception Handling for Network Requests: A function to handle network requests with retries and timeouts can be helpful.

def safe_request(url, max_retries=3, timeout=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            return response
        except requests.exceptions.RequestException as e:
            log_message(f'Attempt {attempt + 1}: {e}', level='WARNING')
    return None

# 5. File Handling Utilities: Functions can be added to check if a file or directory exists, create directories, or read/write files.

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def file_exists(filepath):
    return os.path.isfile(filepath)

# 6. Signal Handling Functions: If multiple scripts need to handle signals (like SIGINT for Ctrl+C), the signal handling functions can be put in the utilities file.

def setup_signal_handler(handler_function):
    signal.signal(signal.SIGINT, handler_function)
