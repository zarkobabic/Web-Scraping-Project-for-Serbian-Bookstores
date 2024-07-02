# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class PszwebscrapperandcrawlerPipeline:
    def process_item(self, item, spider):
        return item
    

class SaveToDatabasePipeline:

    def __init__(self):
        #povezivanje na bazu        
        self.connect_to_database()

        # Ukoliko baza ne postoji kreirati je
        self.create_database_if_not_exists()
        
        #ukoliko ne postoje tabele kreirati ih
        self.create_tables_if_not_exists()
    
    def close_spider(self, spider):
        self.cursor.close()
        self.mydb.close()

    def connect_to_database(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234"
        )

        self.cursor = self.mydb.cursor()

    def disconnect_from_database(self):
        self.cursor.close()
        self.mydb.close()

    def create_database_if_not_exists(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS pszbooks1;")
        self.cursor.execute("USE pszbooks1;")

    def create_tables_if_not_exists(self):
        
        sql_tables_creation_script = """
        CREATE TABLE IF NOT EXISTS `pszbooks1`.`books` ( 
        `idBook` INT NOT NULL AUTO_INCREMENT, 
        `title` TEXT NULL, 
        `publisher` TEXT NULL, 
        `year` INT NULL, 
        `number_of_pages` INT NULL, 
        `cover_binding` VARCHAR(45) NULL, 
        `format_height` DOUBLE NULL, 
        `format_width` DOUBLE NULL, 
        `description` LONGTEXT NULL, 
        `price` DOUBLE NULL, 
        PRIMARY KEY (`idBook`), 
        UNIQUE INDEX `idpszbookstable_UNIQUE` (`idBook` ASC) VISIBLE);"""

        self.cursor.execute(sql_tables_creation_script)

        sql_tables_creation_script = """
        CREATE TABLE IF NOT EXISTS `pszbooks1`.`authors` (
        `idAuthor` INT NOT NULL AUTO_INCREMENT,
        `name` TEXT NULL,
        UNIQUE INDEX `idAuthor_UNIQUE` (`idAuthor` ASC) VISIBLE,
        PRIMARY KEY (`idAuthor`));"""

        self.cursor.execute(sql_tables_creation_script)

        sql_tables_creation_script = """
        CREATE TABLE IF NOT EXISTS `pszbooks1`.`genres` (
        `idGenre` INT NOT NULL AUTO_INCREMENT,
        `name` TEXT NULL,
        UNIQUE INDEX `idGenre_UNIQUE` (`idGenre` ASC) VISIBLE,
        PRIMARY KEY (`idGenre`));"""

        self.cursor.execute(sql_tables_creation_script)

        sql_tables_creation_script = """
        CREATE TABLE IF NOT EXISTS `pszbooks1`.`wrote` (
        `idWrote` INT NOT NULL AUTO_INCREMENT,
        `idBook` INT NULL,
        `idAuthor` INT NULL,
        UNIQUE INDEX `idWrote_UNIQUE` (`idWrote` ASC) VISIBLE,
        PRIMARY KEY (`idWrote`),
        INDEX `idBook_idx` (`idBook` ASC) VISIBLE,
        INDEX `idAuthor_idx` (`idAuthor` ASC) VISIBLE,
        CONSTRAINT `idBook`
            FOREIGN KEY (`idBook`)
            REFERENCES `pszbooks1`.`books` (`idBook`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `idAuthor`
            FOREIGN KEY (`idAuthor`)
            REFERENCES `pszbooks1`.`authors` (`idAuthor`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);"""
        
        self.cursor.execute(sql_tables_creation_script)
        
        sql_tables_creation_script = """
        CREATE TABLE IF NOT EXISTS `pszbooks1`.`isgenre` (
        `idIsGenre` INT NOT NULL AUTO_INCREMENT,
        `idBookForGenre` INT NULL,
        `idGenre` INT NULL,
        UNIQUE INDEX `idIsGenre_UNIQUE` (`idIsGenre` ASC) VISIBLE,
        PRIMARY KEY (`idIsGenre`),
        INDEX `idGenre_idx` (`idGenre` ASC) VISIBLE,
        INDEX `idBook_idx` (`idBookForGenre` ASC) VISIBLE,
        CONSTRAINT `idBookForGenre`
            FOREIGN KEY (`idBookForGenre`)
            REFERENCES `pszbooks1`.`books` (`idBook`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `idGenre`
            FOREIGN KEY (`idGenre`)
            REFERENCES `pszbooks1`.`genres` (`idGenre`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);"""
        
        self.cursor.execute(sql_tables_creation_script)

    def insert_data_to_books_table(self, data_to_insert):
        sql_insert_query = f"""INSERT INTO BOOKS (title, publisher, year, number_of_pages, cover_binding, format_height, format_width, description, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        print("Data to insert", data_to_insert)
        self.cursor.execute(sql_insert_query, data_to_insert)


    def check_if_author_already_exists(self, author_name):
        query_to_check_if_exists = "SELECT COUNT(1) FROM authors WHERE name = %s"
        self.cursor.execute(query_to_check_if_exists, (author_name,))
        return self.cursor.fetchone()[0] > 0

    def select_author_id_with_name(self, author_name):
        query_to_select = "SELECT idAuthor FROM authors WHERE name = %s"
        self.cursor.execute(query_to_select, (author_name,))
        idAuthorsTuple = self.cursor.fetchone()
        return idAuthorsTuple[0]

    def insert_data_to_authors_table(self, authors):
        idForAuthors = []
        for author in authors:
            if not self.check_if_author_already_exists(author):
                query_to_add_author = "INSERT INTO authors (name) VALUES (%s)"
                self.cursor.execute(query_to_add_author, (author,))
                idForAuthors.append(self.cursor.lastrowid)
            else:
                oldAuthorId = self.select_author_id_with_name(author) #dohvata njegov vec postojeci id
                idForAuthors.append(oldAuthorId)
        
        return idForAuthors 

    def check_if_genre_already_exists(self, genre_name):
        query_to_check_if_exists = "SELECT COUNT(1) FROM genres WHERE name = %s"
        self.cursor.execute(query_to_check_if_exists, (genre_name,))
        return self.cursor.fetchone()[0] > 0

    def select_genre_id_with_name(self, genre_name):
        query_to_select = "SELECT idGenre FROM genres WHERE name = %s"
        self.cursor.execute(query_to_select, (genre_name,))
        idGenresTuple = self.cursor.fetchone()
        return idGenresTuple[0]

    def insert_data_to_genres_table(self, genres):
        idForGenres = []
        for genre in genres:
            if not self.check_if_genre_already_exists(genre):
                query_to_add_genre = "INSERT INTO genres (name) VALUES (%s)"
                self.cursor.execute(query_to_add_genre, (genre,))
                idForGenres.append(self.cursor.lastrowid)
            else:
                oldGenreId = self.select_genre_id_with_name(genre) #dohvata njegov stari od ako vec postoji
                idForGenres.append(oldGenreId)
        return idForGenres

    def insert_data_to_wrote_table(self, data_to_insert):
        sql_insert_query = f"""INSERT INTO wrote (idBook, idAuthor)
        VALUES (%s, %s)"""
        self.cursor.execute(sql_insert_query, data_to_insert)

    def insert_data_to_isgenre_table(self, data_to_insert):
        sql_insert_query = f"""INSERT INTO isgenre (idBookForGenre, idGenre)
        VALUES (%s, %s)"""
        self.cursor.execute(sql_insert_query, data_to_insert)

    def process_item(self, item, spider):
        data_to_insert = (item["title"], item["publisher"], item["year"], item["number_of_pages"], item["cover_binding"], item["format_height"], item["format_width"], item["description"], item["price"])
        self.insert_data_to_books_table(data_to_insert)
        addedIdBook = self.cursor.lastrowid #daje autoincrementovani key

        #vraca sve id-jeve autora koji su pisali ovu knjigu (ili dodaje autora kao novog ako ne postoji vec, ili ako vec postoji samo vrati njegov idAuthor, i tako za sve autore koji su napisali knjigu)
        authorsIdArray = self.insert_data_to_authors_table(item["authors"])

        #vraca sve id-jeve zanrova kojoj ova knjiga pripada (ili dodaje zanr kao novi ako ne postoji vec ili ako vec postoji samo vrati njegov idGenre, i tako za sve zanrove kojima knjiga pripada)
        genresIdArray = self.insert_data_to_genres_table(item["genres"])

        #dodavanje u wrote tabelu
        for idAuthor in authorsIdArray:
            data_to_insert = (addedIdBook, idAuthor)
            self.insert_data_to_wrote_table(data_to_insert)

        #dodavanje u isgenre tabelu
        for idGenre in genresIdArray:
            data_to_insert = (addedIdBook, idGenre)
            self.insert_data_to_isgenre_table(data_to_insert)

        self.mydb.commit()
        return item