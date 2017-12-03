DROP DATABASE if EXISTS management_ipaddress ;
CREATE DATABASE management_ipaddress character set utf8mb4;

USE management_ipaddress;

CREATE TABLE ipaddress_list(
    id INT NOT NULL AUTO_INCREMENT,
    ipaddress INT UNSIGNED NOT NULL,
    subnet INT UNSIGNED NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    fqdn VARCHAR(255),
    description VARCHAR(255) NOT NULL,
    updated_at timestamp not null default current_timestamp on update current_timestamp,
    created_by VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

insert into ipaddress_list (ipaddress, subnet, hostname, fqdn, description, created_by) VALUE (INET_ATON('192.168.1.100'),24 , "hostname_test", "test.example.com" ,"server for test1", "test_user");
insert into ipaddress_list (ipaddress, subnet, hostname, fqdn, description, created_by) VALUE (INET_ATON('192.168.1.200'),24 , "hostname_test2", "test2.example.com" ,"server for test2", "test_user");
insert into ipaddress_list (ipaddress, subnet, hostname, fqdn, description, created_by) VALUE (INET_ATON('10.0.0.1'),     16 , "hostname_test3", "test3.example.com" ,"server for test3", "test_user");

-- insert into users (username, password) VALUE (hogehoge)
