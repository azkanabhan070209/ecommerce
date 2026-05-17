-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 16, 2026 at 01:51 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce_flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `detail_pesanan`
--

CREATE TABLE `detail_pesanan` (
  `id_detail` int(11) NOT NULL,
  `id_pesanan` int(11) DEFAULT NULL,
  `id_produk` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `subtotal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detail_pesanan`
--

INSERT INTO `detail_pesanan` (`id_detail`, `id_pesanan`, `id_produk`, `qty`, `harga`, `subtotal`) VALUES
(3, 5, 57, 1, 85000, 85000);

-- --------------------------------------------------------

--
-- Table structure for table `kategori`
--

CREATE TABLE `kategori` (
  `id_kategori` int(11) NOT NULL,
  `nama_kategori` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kategori`
--

INSERT INTO `kategori` (`id_kategori`, `nama_kategori`) VALUES
(1, 'Elektronik'),
(2, 'Fashion'),
(3, 'Makanan'),
(4, 'Gaming'),
(6, 'Fashion'),
(7, 'Gaming'),
(8, 'Olahraga');

-- --------------------------------------------------------

--
-- Table structure for table `keranjang`
--

CREATE TABLE `keranjang` (
  `id_keranjang` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_produk` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT 1,
  `subtotal` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pesanan`
--

CREATE TABLE `pesanan` (
  `id_pesanan` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `tanggal` datetime DEFAULT current_timestamp(),
  `total_harga` int(11) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `status` enum('pending','diproses','dikirim','selesai') DEFAULT 'pending',
  `bukti_bayar` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pesanan`
--

INSERT INTO `pesanan` (`id_pesanan`, `id_user`, `tanggal`, `total_harga`, `alamat`, `status`, `bukti_bayar`, `created_at`) VALUES
(1, 2, '2026-05-16 17:19:25', 270000, 'JL', 'selesai', NULL, '2026-05-16 10:19:25'),
(5, 3, '2026-05-16 18:49:36', 85000, 'Kebon kopi', 'dikirim', NULL, '2026-05-16 11:49:36');

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

CREATE TABLE `produk` (
  `id_produk` int(11) NOT NULL,
  `id_kategori` int(11) DEFAULT NULL,
  `nama_produk` varchar(150) NOT NULL,
  `harga` int(11) NOT NULL,
  `stok` int(11) DEFAULT 0,
  `foto` varchar(255) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id_produk`, `id_kategori`, `nama_produk`, `harga`, `stok`, `foto`, `deskripsi`, `created_at`) VALUES
(23, 1, 'Samsung Galaxy S24', 13500000, 10, 's24.jpg', 'Smartphone flagship Samsung', '2026-05-16 11:21:57'),
(24, 1, 'MacBook Air M2', 16500000, 5, 'macbook.jpg', 'Laptop Apple chipset M2', '2026-05-16 11:21:57'),
(25, 1, 'Smart TV LG 43 Inch', 4200000, 7, 'tvlg.jpg', 'Smart TV LG Full HD', '2026-05-16 11:21:57'),
(26, 1, 'Kamera Sony Alpha', 9800000, 4, 'sonyalpha.jpg', 'Kamera mirrorless Sony', '2026-05-16 11:21:57'),
(27, 1, 'Apple Watch Series 9', 6200000, 8, 'applewatch.jpg', 'Smartwatch Apple terbaru', '2026-05-16 11:21:57'),
(28, 2, 'Hoodie Vintage', 275000, 20, 'hoodievintage.jpg', 'Hoodie vintage premium', '2026-05-16 11:21:57'),
(29, 2, 'Kaos Oversize', 120000, 35, 'oversize.jpg', 'Kaos oversize cotton combed', '2026-05-16 11:21:57'),
(30, 2, 'Sepatu Vans Oldskool', 899000, 12, 'vans.jpg', 'Sepatu Vans original', '2026-05-16 11:21:57'),
(31, 2, 'Celana Jeans Baggy', 230000, 18, 'baggy.jpg', 'Celana jeans baggy style', '2026-05-16 11:21:57'),
(32, 2, 'Topi Streetwear', 85000, 25, 'topi.jpg', 'Topi streetwear kekinian', '2026-05-16 11:21:57'),
(33, 3, 'Mie Pedas Korea', 25000, 40, 'mie.jpg', 'Mie instan pedas Korea', '2026-05-16 11:21:57'),
(34, 3, 'Kopi Arabica', 95000, 20, 'kopi.jpg', 'Kopi Arabica premium', '2026-05-16 11:21:57'),
(35, 3, 'Coklat Swiss', 65000, 30, 'swiss.jpg', 'Coklat import Swiss', '2026-05-16 11:21:57'),
(36, 3, 'Keripik Kentang', 18000, 50, 'keripik.jpg', 'Snack keripik kentang', '2026-05-16 11:21:57'),
(37, 3, 'Susu Protein', 120000, 15, 'protein.jpg', 'Susu protein gym', '2026-05-16 11:21:57'),
(38, 4, 'PlayStation 5', 9500000, 4, 'ps5.jpg', 'Console Sony PS5', '2026-05-16 11:21:57'),
(39, 4, 'Nintendo Switch', 4200000, 6, 'switch.jpg', 'Nintendo Switch OLED', '2026-05-16 11:21:57'),
(40, 4, 'Gaming Mouse Razer', 650000, 14, 'razer.jpg', 'Mouse gaming RGB', '2026-05-16 11:21:57'),
(41, 4, 'Mechanical Keyboard', 780000, 11, 'keyboard.jpg', 'Keyboard gaming mechanical', '2026-05-16 11:21:57'),
(42, 4, 'Gaming Headset', 550000, 16, 'headset.jpg', 'Headset gaming surround', '2026-05-16 11:21:57'),
(43, 6, 'Sweater Knit', 240000, 14, 'sweater.jpg', 'Sweater knit aesthetic', '2026-05-16 11:21:57'),
(44, 6, 'Cardigan Korea', 210000, 13, 'cardigan.jpg', 'Cardigan Korean style', '2026-05-16 11:21:57'),
(45, 6, 'Cargo Pants', 280000, 17, 'cargo.jpg', 'Celana cargo pria', '2026-05-16 11:21:57'),
(46, 6, 'Tas Tote Bag', 95000, 22, 'totebag.jpg', 'Tote bag canvas', '2026-05-16 11:21:57'),
(47, 6, 'Sepatu Running', 650000, 9, 'running.jpg', 'Sepatu running nyaman', '2026-05-16 11:21:57'),
(48, 7, 'Gaming Chair', 1750000, 5, 'chair.jpg', 'Kursi gaming RGB', '2026-05-16 11:21:57'),
(49, 7, 'Monitor Gaming 144Hz', 3200000, 7, 'monitor.jpg', 'Monitor gaming smooth', '2026-05-16 11:21:57'),
(50, 7, 'Joystick PS5', 950000, 10, 'joystick.jpg', 'Controller PS5 original', '2026-05-16 11:21:57'),
(51, 7, 'Webcam Streaming', 780000, 8, 'webcam.jpg', 'Webcam streaming HD', '2026-05-16 11:21:57'),
(52, 7, 'Mousepad XL', 120000, 25, 'mousepad.jpg', 'Mousepad gaming XL', '2026-05-16 11:21:57'),
(53, 8, 'Sepatu Futsal', 450000, 14, 'futsal.jpg', 'Sepatu futsal ringan', '2026-05-16 11:21:57'),
(54, 8, 'Bola Basket', 320000, 10, 'basket.jpg', 'Bola basket official', '2026-05-16 11:21:57'),
(55, 8, 'Raket Badminton', 550000, 7, 'raket.jpg', 'Raket badminton carbon', '2026-05-16 11:21:57'),
(56, 8, 'Matras Yoga', 150000, 20, 'yoga.jpg', 'Matras yoga anti slip', '2026-05-16 11:21:57'),
(57, 8, 'Botol Gym', 85000, 29, 'botol.jpg', 'Botol minum gym', '2026-05-16 11:21:57');

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `id_review` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_produk` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `komentar` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`id_review`, `id_user`, `id_produk`, `rating`, `komentar`, `created_at`) VALUES
(4, 2, 27, 5, 'Sangat bagus sekali', '2026-05-16 11:29:23'),
(5, 3, 27, 5, 'P p apa', '2026-05-16 11:45:13');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `nama`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'Administrator', 'admin@gmail.com', 'admin123', 'admin', '2026-05-16 09:32:59'),
(2, 'alif', 'ferimardani69@gmail.com', '123', 'user', '2026-05-16 09:41:53'),
(3, 'Iyan', 'alif@gmail.com', '123', 'user', '2026-05-16 11:44:40');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  ADD PRIMARY KEY (`id_detail`),
  ADD KEY `id_pesanan` (`id_pesanan`),
  ADD KEY `id_produk` (`id_produk`);

--
-- Indexes for table `kategori`
--
ALTER TABLE `kategori`
  ADD PRIMARY KEY (`id_kategori`);

--
-- Indexes for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD PRIMARY KEY (`id_keranjang`),
  ADD KEY `fk_keranjang_user` (`id_user`),
  ADD KEY `fk_keranjang_produk` (`id_produk`);

--
-- Indexes for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD PRIMARY KEY (`id_pesanan`),
  ADD KEY `fk_pesanan_user` (`id_user`);

--
-- Indexes for table `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`id_produk`),
  ADD KEY `id_kategori` (`id_kategori`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id_review`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_produk` (`id_produk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  MODIFY `id_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `kategori`
--
ALTER TABLE `kategori`
  MODIFY `id_kategori` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `keranjang`
--
ALTER TABLE `keranjang`
  MODIFY `id_keranjang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `pesanan`
--
ALTER TABLE `pesanan`
  MODIFY `id_pesanan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `produk`
--
ALTER TABLE `produk`
  MODIFY `id_produk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id_review` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  ADD CONSTRAINT `detail_pesanan_ibfk_1` FOREIGN KEY (`id_pesanan`) REFERENCES `pesanan` (`id_pesanan`) ON DELETE CASCADE,
  ADD CONSTRAINT `detail_pesanan_ibfk_2` FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id_produk`) ON DELETE CASCADE;

--
-- Constraints for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD CONSTRAINT `fk_keranjang_produk` FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id_produk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_keranjang_user` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `keranjang_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `keranjang_ibfk_2` FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id_produk`) ON DELETE CASCADE;

--
-- Constraints for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD CONSTRAINT `fk_pesanan_user` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `pesanan_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE;

--
-- Constraints for table `produk`
--
ALTER TABLE `produk`
  ADD CONSTRAINT `produk_ibfk_1` FOREIGN KEY (`id_kategori`) REFERENCES `kategori` (`id_kategori`) ON DELETE SET NULL;

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id_produk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
