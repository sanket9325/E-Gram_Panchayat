-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2024 at 07:17 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gram_panchayat`
--

-- --------------------------------------------------------

--
-- Table structure for table `complaints`
--

CREATE TABLE `complaints` (
  `cid` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `message` text NOT NULL,
  `image` text NOT NULL,
  `status` text NOT NULL DEFAULT 'Pending',
  `com_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `complaints`
--

INSERT INTO `complaints` (`cid`, `id`, `title`, `message`, `image`, `status`, `com_date`) VALUES
(1, 1, 'Road Light In My Area', 'Cras fermentum odio eu feugiat lide par naso tierra videa magna derita valies. Cras fermentum odio eu feugiat lide par naso tierra videa magna derita valies', 'back2.jpg', 'In Process', '2024-05-21'),
(2, 4, 'Water Supply', 'Water supply not regular from last week', 'IMG_20211104_191446.jpg', 'In Process', '2024-05-27');

-- --------------------------------------------------------

--
-- Table structure for table `electricity`
--

CREATE TABLE `electricity` (
  `eid` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `document_type` text NOT NULL,
  `doc_img` text NOT NULL,
  `type` text NOT NULL,
  `status` text NOT NULL DEFAULT 'Pending',
  `req_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `electricity`
--

INSERT INTO `electricity` (`eid`, `id`, `document_type`, `doc_img`, `type`, `status`, `req_date`) VALUES
(1, 1, 'Aadhar Card', 'aadhar slider.jpg', 'Home', 'In Process', '2024-05-21'),
(2, 4, 'Aadhar Card', 'IMG_20211008_073247.jpg', 'Home', 'Pending', '2024-05-27');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `mobile` text NOT NULL,
  `voter_id` text NOT NULL,
  `aadhar` text NOT NULL,
  `ward_no` text NOT NULL,
  `gender` text NOT NULL,
  `address` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `photo` text NOT NULL,
  `status` text NOT NULL DEFAULT 'Inactive'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`id`, `name`, `email`, `mobile`, `voter_id`, `aadhar`, `ward_no`, `gender`, `address`, `username`, `password`, `photo`, `status`) VALUES
(1, 'Sanket Babhulkar', 'sanket@gmail.com', '9325924978', '546556988721', '468656523658', '01', 'Male', 'Amravati', 'sanket', 's1', 'profile_img.png', 'Active'),
(2, 'Abhi patil', 'abhi@gmail.com', '7856123654', '569556465454', '84646654654', '01', 'Male', 'Gadge Nagar, Amravati', 'abhi', 'a1', 'face3.jpg', 'Inactive'),
(3, 'Amit Kumar', 'amit@gmail.com', '9503351933', 'BK90898', '457868767868', '01', 'Male', 'Rathi Nagar', 'amit', 'a123', 'profiledummy.png', 'Inactive'),
(4, 'Vijay Kumar', 'vijay@gmail.com', '7845125566', 'GH847t48', '4567899876', '01', 'Male', 'Rathi Nagar', 'vijay', 'v123', 'IMG_20211001_200315.jpg', 'Active'),
(5, 'Ravina thakare', 'ravina@gmail.com', '4646464665', 'BK908985', '457868767868', '02', 'Female', 'Amravati', 'ravina', 'r1', 'face10.jpg', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `ward`
--

CREATE TABLE `ward` (
  `wid` int(11) NOT NULL,
  `ward_no` text NOT NULL,
  `area_name` text NOT NULL,
  `land_mark` text NOT NULL,
  `no_of_family` text NOT NULL,
  `no_of_voter` text NOT NULL,
  `councillor_name` text NOT NULL,
  `councillor_mobile` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ward`
--

INSERT INTO `ward` (`wid`, `ward_no`, `area_name`, `land_mark`, `no_of_family`, `no_of_voter`, `councillor_name`, `councillor_mobile`) VALUES
(1, '01', 'Rathi Nagar', 'Jawarkar Hospital', '500', '1560', 'Amar Tiwari', '7898654523'),
(2, '02', 'Ravi Nagar', 'Near Hanuman Temple', '400', '800', 'Raja Patil', '7845125566');

-- --------------------------------------------------------

--
-- Table structure for table `water_pipe`
--

CREATE TABLE `water_pipe` (
  `wpid` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `document_type` text NOT NULL,
  `doc_img` text NOT NULL,
  `type` text NOT NULL,
  `status` text NOT NULL DEFAULT 'Pending',
  `req_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `water_pipe`
--

INSERT INTO `water_pipe` (`wpid`, `id`, `document_type`, `doc_img`, `type`, `status`, `req_date`) VALUES
(1, 1, 'Pan Card', 'pan slider.jpg', 'Shop', 'Pending', '2024-05-26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `complaints`
--
ALTER TABLE `complaints`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `electricity`
--
ALTER TABLE `electricity`
  ADD PRIMARY KEY (`eid`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `water_pipe`
--
ALTER TABLE `water_pipe`
  ADD PRIMARY KEY (`wpid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
