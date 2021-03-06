CREATE TABLE shows (
  id INT(11) PRIMARY KEY AUTO_INCREMENT,
  show_name VARCHAR(250) UNIQUE NOT NULL,
  show_type ENUM('movie', 'episode', 'series') DEFAULT 'movie' NOT NULL,
  director_id INT(11) DEFAULT NULL,
  deleted_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (director_id) REFERENCES directors (id)
);
