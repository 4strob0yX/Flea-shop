-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-08-2025 a las 04:58:56
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flea_shop_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message_text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `receiver_id`, `message_text`, `created_at`, `is_read`) VALUES
(1, 2, 1, 'Hey q onda', '2025-08-12 02:10:17', 0),
(2, 1, 2, 'Q onda', '2025-08-12 02:39:31', 0),
(3, 3, 1, 'Hola', '2025-08-12 02:40:26', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `owner_user_id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen_path` varchar(255) DEFAULT NULL,
  `vendido` tinyint(1) DEFAULT 0,
  `comprador_user_id` int(11) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `owner_user_id`, `nombre`, `descripcion`, `precio`, `imagen_path`, `vendido`, `comprador_user_id`, `direccion`) VALUES
(14, 1, 'Tralaleritos', 'Los tralaleritos', 1000.00, 'images/Tralaleritos_14.jpg', 0, NULL, NULL),
(16, 1, 'La vaca saturno saturnita', 'La vaca saturno saturnita', 1000.00, 'images/La_vaca_saturno_saturnita_1754962749.jpeg', 0, NULL, NULL),
(17, 1, 'Tung tung tung tung tung tung tung tung sahur', 'Tung tung sahur', 1000.00, 'images/Tung_tung_tung_tung_tung_tung_tung_tung_sahur_1754963028.jpg', 0, NULL, NULL),
(18, 2, 'Kar kir kur', 'Kar kir kur', 1500.00, 'images/Kar_kir_kur_1754964559.png', 0, NULL, 'Lerma, Mexico'),
(19, 2, 'Chicleteira bicicleteira', 'Chicletera bicicletera', 1695.00, 'images/Chicleteira_bicicleteira_1754964602.jpeg', 0, NULL, 'Lerma, Estado de Mexico');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trades`
--

CREATE TABLE `trades` (
  `id` int(11) NOT NULL,
  `proposer_user_id` int(11) NOT NULL,
  `proposer_product_id` int(11) NOT NULL,
  `receiver_user_id` int(11) NOT NULL,
  `receiver_product_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT 'pendiente',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(50) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `estado` enum('activo','suspendido') DEFAULT 'activo',
  `ultimo_login` datetime DEFAULT NULL,
  `verificado` tinyint(1) DEFAULT 0,
  `reputacion` float DEFAULT 0,
  `nivel` varchar(50) DEFAULT 'Nuevo',
  `cart_items` text DEFAULT '[]'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `nombre`, `apellidos`, `email`, `password_hash`, `telefono`, `fecha_registro`, `username`, `foto_perfil`, `direccion`, `fecha_nacimiento`, `is_admin`, `estado`, `ultimo_login`, `verificado`, `reputacion`, `nivel`, `cart_items`) VALUES
(1, 'Sam', 'Gutierrez', 's@gmail.com', '$2b$12$K44ZQgPVKSnHs/kKqzgoEuZCExSUG4SKLfJbqxDrmrZDA2f43AnEi', '7224108974', '2025-08-06 03:58:21', NULL, NULL, NULL, NULL, 0, 'activo', NULL, 0, 0, 'Nuevo', '[]'),
(2, 'Sam', 'Gutierrez', 'sam2@gmail.com', '$2b$12$DPX6K9z1PkhaMqhpJtSuiuwC4WS5ApgSLMMx5GWPbLn0.A2POXK/W', '7224108993', '2025-08-06 04:11:14', '', NULL, '', '0000-00-00', 0, 'activo', NULL, 0, 0, 'Nuevo', '[]'),
(3, '', '', 'a@gmail.com', '$2b$12$CN.vSFNQs4AkAsxVlILJ6eJO6ytVzyTPs2XfJdevDpFArb6Ws/JF.', '', '2025-08-12 02:40:01', 'Aposho', '', '', '0000-00-00', 0, 'activo', NULL, 0, 0, 'Nuevo', '[]');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `wishlists`
--

CREATE TABLE `wishlists` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `idx_messages_sender_receiver` (`sender_id`,`receiver_id`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `owner_user_id` (`owner_user_id`),
  ADD KEY `fk_comprador` (`comprador_user_id`);

--
-- Indices de la tabla `trades`
--
ALTER TABLE `trades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `proposer_user_id` (`proposer_user_id`),
  ADD KEY `proposer_product_id` (`proposer_product_id`),
  ADD KEY `receiver_user_id` (`receiver_user_id`),
  ADD KEY `receiver_product_id` (`receiver_product_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `wishlists`
--
ALTER TABLE `wishlists`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_fav` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `trades`
--
ALTER TABLE `trades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `wishlists`
--
ALTER TABLE `wishlists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_comprador` FOREIGN KEY (`comprador_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `trades`
--
ALTER TABLE `trades`
  ADD CONSTRAINT `trades_ibfk_1` FOREIGN KEY (`proposer_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trades_ibfk_2` FOREIGN KEY (`proposer_product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trades_ibfk_3` FOREIGN KEY (`receiver_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trades_ibfk_4` FOREIGN KEY (`receiver_product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `wishlists`
--
ALTER TABLE `wishlists`
  ADD CONSTRAINT `wishlists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wishlists_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
