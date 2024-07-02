# Library Sites Scraping and Database Creation using Scrapy and Rotating Proxy Servers

## Project Summary

This project aims to develop a robust web scraping solution using Scrapy and rotating proxy servers in Python to collect data on 15,000 books on sale in Serbia. The ultimate goal is to create a comprehensive database that will serve as a foundation for future machine learning (ML) algorithms.

## Project Components

### 1. Web Scraping with Scrapy

- **Scrapy Framework:** Utilize Scrapy, a powerful and flexible web scraping framework in Python, to navigate and extract data from various library websites.
- **Rotating Proxy Servers:** Implement a rotating proxy mechanism to avoid IP bans and ensure uninterrupted data scraping. This involves using a pool of proxy servers to distribute requests, mimicking different users.
- **Data Extraction:** Focus on gathering detailed information about books, including titles, authors, genres, publication dates, prices, and availability.

### 2. Data Storage and Management

- **MySQL Database:** Store the extracted data in a MySQL database. The database schema will include tables for books, authors, genres, and associations between books and genres/authors.
- **Data Cleaning:** Perform data cleaning and normalization to ensure consistency and accuracy in the stored information.

### 3. Database Preparation for ML Algorithms

- **Data Structuring:** Structure the database to facilitate easy access and manipulation for future machine learning tasks.
- **Feature Engineering:** Identify and prepare relevant features from the scraped data that will be useful for machine learning models.

## Project Goals

- **Comprehensive Database:** Create a complete and accurate database of 15,000 books available for sale in Serbia.
- **Scalable Scraping Solution:** Develop a scalable web scraping solution that can handle large volumes of data and adapt to different library websites.
- **ML Readiness:** Ensure the database is well-prepared and structured for subsequent application of machine learning algorithms, enabling various analyses and predictive modeling tasks.

## Technologies and Tools

- **Programming Language:** Python
- **Web Scraping Framework:** Scrapy
- **Database:** MySQL
- **Proxies:** Rotating proxy servers for distributed request handling
- **Data Processing:** Pandas for data manipulation and cleaning

## Future Work

Once the database is established, it will be utilized for various machine learning applications such as recommendation systems, price prediction models, and sales trend analysis. This project serves as the foundational step in creating an intelligent system for analyzing and leveraging book sales data in Serbia.

## Setup and Usage

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Dependencies:**
    ```bash
    pip install scrapy mysql-connector-python pandas scrapy-rotating-proxies
    ```

3. **Configure Proxy Servers:**
   - Add your list of proxy servers to the configuration file (proxies.txt).

4. **Run the Scrapy Spider:**
    ```bash
    # Command for scraping books from https://www.laguna.rs/ site
    scrapy crawl pszLagunaSpider

    # Command for scraping books from https://bigzknjizara.rs/ site
    scrapy crawl pszBigzSpider

    # Command for scraping books from https://makart.rs/ site
    scrapy crawl pszMakartSpider
    ```

5. **Access the Database:**
   - Connect to your MySQL database to view and manipulate the scraped data.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License