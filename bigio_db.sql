-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 21 Agu 2024 pada 14.52
-- Versi server: 8.0.30
-- Versi PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bigio_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `chapters`
--

CREATE TABLE `chapters` (
  `id` int NOT NULL,
  `story_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `chapters`
--

INSERT INTO `chapters` (`id`, `story_id`, `title`, `content`, `created_at`, `updated_at`) VALUES
(5, 11, 'Chapter 1', 'This is the content of the first chapter.', '2024-08-21 11:54:59', '2024-08-21 11:54:59'),
(6, 11, 'Chapter 2', 'This is the content of the second chapter.', '2024-08-21 11:54:59', '2024-08-21 11:54:59'),
(7, 14, 'Chapter 1: The Call to Adventure', 'Once upon a time, in a quiet village...', '2024-08-21 14:47:28', '2024-08-21 14:47:28'),
(8, 14, 'Chapter 2: Into the Unknown', 'The journey into the unknown begins...', '2024-08-21 14:47:28', '2024-08-21 14:47:28');

-- --------------------------------------------------------

--
-- Struktur dari tabel `stories`
--

CREATE TABLE `stories` (
  `id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `synopsis` text,
  `category` enum('Financial','Technology','Health','Fantasy','Sport','Culture') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cover_image` varchar(255) DEFAULT NULL,
  `status` enum('Publish','Draft') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `stories`
--

INSERT INTO `stories` (`id`, `title`, `author`, `synopsis`, `category`, `cover_image`, `status`, `created_at`, `updated_at`) VALUES
(11, 'My First Story', 'John Doe', 'This is a story about testing the FastAPI service.', 'Technology', 'https://example.com/cover.jpg', 'Publish', '2024-08-21 11:54:59', '2024-08-21 11:54:59'),
(12, 'string', 'string', 'string', 'Financial', 'string', 'Publish', '2024-08-21 12:19:28', '2024-08-21 12:19:28'),
(13, 'string', 'string', 'string', 'Financial', 'string', 'Publish', '2024-08-21 13:47:38', '2024-08-21 13:47:38'),
(14, 'The Adventure Begins', 'John Doe', 'A thrilling journey through uncharted lands.', 'Health', 'https://example.com/images/adventure.jpg', 'Draft', '2024-08-21 14:47:28', '2024-08-21 14:47:28');

-- --------------------------------------------------------

--
-- Struktur dari tabel `story_tags`
--

CREATE TABLE `story_tags` (
  `story_id` int NOT NULL,
  `tag_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `story_tags`
--

INSERT INTO `story_tags` (`story_id`, `tag_id`) VALUES
(11, 20),
(11, 21),
(14, 22),
(14, 23);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tags`
--

CREATE TABLE `tags` (
  `id` int NOT NULL,
  `tag_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `tags`
--

INSERT INTO `tags` (`id`, `tag_name`) VALUES
(22, 'Adventure'),
(23, 'Fantasy'),
(21, 'FastAPI'),
(20, 'Python');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `chapters`
--
ALTER TABLE `chapters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `story_id` (`story_id`);

--
-- Indeks untuk tabel `stories`
--
ALTER TABLE `stories`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `story_tags`
--
ALTER TABLE `story_tags`
  ADD PRIMARY KEY (`story_id`,`tag_id`),
  ADD KEY `tag_id` (`tag_id`);

--
-- Indeks untuk tabel `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tag_name` (`tag_name`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `chapters`
--
ALTER TABLE `chapters`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `stories`
--
ALTER TABLE `stories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT untuk tabel `tags`
--
ALTER TABLE `tags`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `chapters`
--
ALTER TABLE `chapters`
  ADD CONSTRAINT `chapters_ibfk_1` FOREIGN KEY (`story_id`) REFERENCES `stories` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `story_tags`
--
ALTER TABLE `story_tags`
  ADD CONSTRAINT `story_tags_ibfk_1` FOREIGN KEY (`story_id`) REFERENCES `stories` (`id`),
  ADD CONSTRAINT `story_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
