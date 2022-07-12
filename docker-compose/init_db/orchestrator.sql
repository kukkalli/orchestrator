-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: kn-mariadb:3306
-- Generation Time: Jul 11, 2022 at 02:48 PM
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
--

-- --------------------------------------------------------

--
-- Table structure for table `cable_links`
--

CREATE TABLE `cable_links` (
  `link_id` int(11) NOT NULL,
  `link_name` varchar(256) NOT NULL,
  `src_node` varchar(256) NOT NULL,
  `src_port` varchar(256) DEFAULT NULL,
  `dst_node` varchar(256) NOT NULL,
  `dst_port` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sc_parameters`
--

CREATE TABLE `sc_parameters` (
  `service_uuid` uuid NOT NULL,
  `key` varchar(256) NOT NULL,
  `value` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `service_chain`
--

CREATE TABLE `service_chain` (
  `service_uuid` uuid NOT NULL COMMENT 'Primary UUID for the table',
  `service_name` varchar(256) NOT NULL COMMENT 'Name of the service chain',
  `start_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Start date of creation of service chain',
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'End date of creation of service chain',
  `created_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Created on Date',
  `created_by` varchar(36) DEFAULT NULL COMMENT 'Created by user',
  `updated_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Updated on Date',
  `updated_by` varchar(36) NOT NULL COMMENT 'Updated by user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cable_links`
--
ALTER TABLE `cable_links`
  ADD PRIMARY KEY (`link_id`);

--
-- Indexes for table `sc_parameters`
--
ALTER TABLE `sc_parameters`
  ADD PRIMARY KEY (`service_uuid`,`key`),
  ADD UNIQUE KEY `service_uuid` (`service_uuid`,`key`);

--
-- Indexes for table `service_chain`
--
ALTER TABLE `service_chain`
  ADD PRIMARY KEY (`service_uuid`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sc_parameters`
--
ALTER TABLE `sc_parameters`
  ADD CONSTRAINT `sc_parameters_ibfk_1` FOREIGN KEY (`service_uuid`) REFERENCES `service_chain` (`service_uuid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
