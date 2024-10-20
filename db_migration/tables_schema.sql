/* 2024-10-20 14:40:23 [140 ms] */ 
CREATE TABLE books(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(100),
    year_published DATE,
    summary VARCHAR(1000),
    created_at DATE
);
/* 2024-10-20 14:48:09 [141 ms] */ 
CREATE TABLE reviews(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    book_id int NOT NULL,
    
    user_id VARCHAR(100),
    review_text VARCHAR(100),
    rating int ,
    created_at DATE,
    CONSTRAINT fk_book_id
      FOREIGN KEY(book_id) 
	  REFERENCES books(id) ON DELETE CASCADE 
);
