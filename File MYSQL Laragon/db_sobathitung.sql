-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versi server:                 8.0.30 - MySQL Community Server - GPL
-- OS Server:                    Win64
-- HeidiSQL Versi:               12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- membuang struktur untuk table db_sobathitung.tbl_activity_log
CREATE TABLE IF NOT EXISTS `tbl_activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int NOT NULL,
  `action` varchar(255) NOT NULL,
  `detail` varchar(500) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tbl_activity_log__user` (`user`),
  CONSTRAINT `fk_tbl_activity_log__user` FOREIGN KEY (`user`) REFERENCES `tbl_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Pengeluaran data tidak dipilih.

-- membuang struktur untuk table db_sobathitung.tbl_chat_history
CREATE TABLE IF NOT EXISTS `tbl_chat_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int NOT NULL,
  `model_name` varchar(50) NOT NULL,
  `prompt` varchar(5000) NOT NULL,
  `response` varchar(10000) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tbl_chat_history__user` (`user`),
  CONSTRAINT `fk_tbl_chat_history__user` FOREIGN KEY (`user`) REFERENCES `tbl_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Pengeluaran data tidak dipilih.

-- membuang struktur untuk table db_sobathitung.tbl_uploaded_file
CREATE TABLE IF NOT EXISTS `tbl_uploaded_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  `original_name` varchar(255) NOT NULL,
  `file_type` varchar(10) NOT NULL,
  `file_size` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tbl_uploaded_file__user` (`user`),
  CONSTRAINT `fk_tbl_uploaded_file__user` FOREIGN KEY (`user`) REFERENCES `tbl_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Pengeluaran data tidak dipilih.

-- membuang struktur untuk table db_sobathitung.tbl_user
CREATE TABLE IF NOT EXISTS `tbl_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `location` varchar(100) NOT NULL,
  `bio` varchar(500) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `verification_token` varchar(100) NOT NULL,
  `reset_token` varchar(100) NOT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `notif_email` tinyint(1) NOT NULL,
  `dark_mode` tinyint(1) NOT NULL,
  `save_history` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Pengeluaran data tidak dipilih.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
