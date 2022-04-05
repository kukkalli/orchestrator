-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: kn-mariadb:3306
-- Generation Time: Mar 10, 2022 at 04:25 PM
-- Server version: 10.7.3-MariaDB-1:10.7.3+maria~focal
-- PHP Version: 8.0.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `orchestrator`
-- CREATE DATABASE IF NOT EXISTS orchestrator;
--

-- --------------------------------------------------------

--
-- Table structure for table `service-chain`
--

CREATE TABLE `service_chain` (
  `service_uuid` UUID NOT NULL COMMENT 'Primary UUID for the table',
  `service_name` varchar(256) NOT NULL COMMENT 'Name of the service chain',
  `start_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Start date of creation of service chain',
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'End date of creation of service chain',
  `created_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Created on Date',
  `created_by` varchar(36) DEFAULT NULL COMMENT 'Created by user',
  `updated_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Updated on Date',
  `updated_by` varchar(36) NOT NULL COMMENT 'Updated by user',
  PRIMARY KEY (`service_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sc_parameters` (
    `parameter_id` UUID NOT NULL,
    `service_uuid` UUID NOT NULL,
    `key` varchar(256) NOT NULL,
    `value` varchar(256) NOT NULL,
    PRIMARY KEY (`parameter_id`, `service_uuid`),
    FOREIGN KEY (`service_uuid`) REFERENCES `service_chain`(`service_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cable_links` (
    `link_id` INT NOT NULL,
    `link_name` varchar(256) NOT NULL,
    `src_node` varchar(256) NOT NULL,
    `src_port` varchar(256) ,
    `dst_node` varchar(256) NOT NULL,
    `dst_port` varchar(256) ,
    PRIMARY KEY (`link_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Dumping data for table `service-chain`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `service-chain`
--
-- ALTER TABLE `service-chain`
--   ADD PRIMARY KEY (`id`);
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
