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
-- Database: `kn`
--

-- --------------------------------------------------------

--
-- Table structure for table `service-chain`
--

CREATE TABLE `service-chain` (
  `id` binary(16) NOT NULL COMMENT 'Primary UUID for the table',
  `name` varchar(256) NOT NULL COMMENT 'Name of the service chain',
  `start_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Start date of creation of service chain',
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'End date of creation of service chain',
  `created_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Created on Date',
  `created_by` varchar(36) DEFAULT NULL COMMENT 'Created by user',
  `updated_on` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Updated on Date',
  `updated_by` varchar(36) NOT NULL COMMENT 'Updated by user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `service-chain`
--

INSERT INTO `service-chain` (`id`, `name`, `start_date`, `end_date`, `created_on`, `created_by`, `updated_on`, `updated_by`) VALUES
(0x30303030303030303030303030303031, 'test', '2022-03-11 00:00:00', '2022-03-10 00:00:00', '2022-03-10 16:24:28', 'kn', '2022-03-10 16:24:28', 'kn');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `service-chain`
--
ALTER TABLE `service-chain`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
