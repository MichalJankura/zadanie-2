CREATE TABLE kniznice (
    id_kniznice         INT PRIMARY KEY,
    nazov_kniznice      VARCHAR(255) NOT NULL,
    ulica               VARCHAR(255),
    psc                 VARCHAR(20),
    mesto               VARCHAR(100),
    kraj                VARCHAR(100),
    krajina             VARCHAR(100),
    zemepisna_sirka     DECIMAL(9,6),
    zemepisna_dlzka     DECIMAL(9,6),
    cas_otvorenia       VARCHAR
);
