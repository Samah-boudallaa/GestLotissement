CREATE DATABASE gest_lotissements;
USE gest_lotissements;

CREATE TABLE lotissements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    nb_etages VARCHAR(10),
    vocation VARCHAR(50)
);
