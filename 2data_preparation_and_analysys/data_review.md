a. The number of books for sale by book category (genre):

```sql
SELECT g.name AS 'Category/Genre', COUNT(*) AS 'Number of books for sale' FROM books b JOIN isgenre ig ON b.idBook=ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
GROUP BY g.name
ORDER BY count(*) DESC
```

b. Number of books that are sold by each publisher:

```sql
SELECT publisher AS 'Publisher', COUNT(*) AS 'Number of books issued by the publisher' FROM books
GROUP BY publisher
ORDER BY COUNT(*) DESC
```

c. Number of books containing the word "love" in the description:

```sql
SELECT COUNT(*) AS 'The number of books that contain the word love in the description' FROM books WHERE description LIKE '%ljubav%'
```

d. Number of published books by year, in the last 7 years:

```sql
SELECT year AS 'Year', COUNT(*) AS 'Number of published books in the year' FROM books
WHERE year >= 2018 AND year <= 2024
GROUP BY year
ORDER BY year DESC
```

e. Ranking list of the top 30 most expensive books sold:

```sql
SELECT b.title AS 'Title', GROUP_CONCAT(a.name SEPARATOR ', ') AS 'Authors', GROUP_CONCAT(g.name SEPARATOR ', ') AS 'Genres/Categories', b.publisher AS 'Publisher', b.year AS 'Year of publication', b.number_of_pages AS 'Number of pages', b.cover_binding AS 'Binding type', CONCAT(b.format_width, ' x ', b.format_height) AS 'Format', b.description AS 'Description', b.price AS 'Price'
FROM books b JOIN wrote w ON b.idBook = w.idBook JOIN authors a ON w.idAuthor = a.idAuthor JOIN isgenre ig ON b.idBook = ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
GROUP BY b.idBook
ORDER BY b.price DESC
LIMIT 30;
```

f. Ranking list of all books published in 2023 or 2024, ordered ascending by selling price:

```sql
SELECT b.title AS 'Title', GROUP_CONCAT(a.name SEPARATOR ', ') AS 'Authors', GROUP_CONCAT(g.name SEPARATOR ', ') AS 'Genres/Categories', b.publisher AS 'Publisher', b.year AS 'Year of publication', b.number_of_pages AS 'Number of pages', b.cover_binding AS 'Binding type', CONCAT(b.format_width, ' x ', b.format_height) AS 'Format', b.description AS 'Description', b.price AS 'Price'
FROM books b JOIN wrote w ON b.idBook = w.idBook JOIN authors a ON w.idAuthor = a.idAuthor JOIN isgenre ig ON b.idBook = ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
WHERE b.year = 2023 or b.year = 2024
GROUP BY b.idBook
ORDER BY b.price
```

g.

TOP 30 books with the largest number of pages:

```sql
SELECT b.title AS 'Title', GROUP_CONCAT(a.name SEPARATOR ', ') AS 'Authors', GROUP_CONCAT(g.name SEPARATOR ', ') AS 'Genres/Categories', b.publisher AS 'Publisher', b.year AS 'Year of publication', b.number_of_pages AS 'Number of pages', b.cover_binding AS 'Binding type', CONCAT(b.format_width, ' x ', b.format_height) AS 'Format', b.description AS 'Description', b.price AS 'Price'
FROM books b JOIN wrote w ON b.idBook = w.idBook JOIN authors a ON w.idAuthor = a.idAuthor JOIN isgenre ig ON b.idBook = ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
GROUP BY b.idBook
ORDER BY b.number_of_pages DESC
LIMIT 30;
```

TOP 30 books with the highest price:

```sql
SELECT b.title AS 'Title', GROUP_CONCAT(a.name SEPARATOR ', ') AS 'Authors', GROUP_CONCAT(g.name SEPARATOR ', ') AS 'Genres/Categories', b.publisher AS 'Publisher', b.year AS 'Year of publication', b.number_of_pages AS 'Number of pages', b.cover_binding AS 'Binding type', CONCAT(b.format_width, ' x ', b.format_height) AS 'Format', b.description AS 'Description', b.price AS 'Price'
FROM books b JOIN wrote w ON b.idBook = w.idBook JOIN authors a ON w.idAuthor = a.idAuthor JOIN isgenre ig ON b.idBook = ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
GROUP BY b.idBook
ORDER BY b.price DESC
LIMIT 30;
```


TOP 30 books with the largest format:

```sql
SELECT b.title AS 'Title', GROUP_CONCAT(a.name SEPARATOR ', ') AS 'Authors', GROUP_CONCAT(g.name SEPARATOR ', ') AS 'Genres/Categories', b.publisher AS 'Publisher', b.year AS 'Year of publication', b.number_of_pages AS 'Number of pages', b.cover_binding AS 'Binding type', CONCAT(b.format_width, ' x ', b.format_height) AS 'Format', b.description AS 'Description', b.price AS 'Price'
FROM books b JOIN wrote w ON b.idBook = w.idBook JOIN authors a ON w.idAuthor = a.idAuthor JOIN isgenre ig ON b.idBook = ig.idBookForGenre JOIN genres g ON ig.idGenre = g.idGenre
GROUP BY b.idBook
ORDER BY (b.format_height * b.format_width) DESC
LIMIT 30;
```