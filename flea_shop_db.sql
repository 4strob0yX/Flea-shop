-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-08-2025 a las 08:18:37
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
  `comprador_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `owner_user_id`, `nombre`, `descripcion`, `precio`, `imagen_path`, `vendido`, `comprador_user_id`) VALUES
(4, 2, 'tung tung tung sahur', 'tung', 100.00, '', 0, NULL),
(5, 1, 'tralalero', 'tralalero', 1000.00, '', 1, 2),
(6, 2, 'La vaca saturno saturnita', 'La vaca', 1000.00, '', 1, 2),
(7, 1, 'Los tralaleritos', 'Los tralaleritos', 1000.00, '', 1, 2),
(8, 2, 'Los tralaleritoss', 'Los tralaleritoss', 1000.00, '', 0, NULL),
(9, 2, 'Ta ta ta ta sahur', 'ta ta ta ta ta sahur', 1000.00, '', 0, NULL),
(10, 2, 'Prr prr patapim', 'Prr prr patapim', 1000.00, '', 0, NULL),
(11, 2, 'tung tung', 'Ta ta ta', 1000.00, '', 0, NULL);

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

--
-- Volcado de datos para la tabla `trades`
--

INSERT INTO `trades` (`id`, `proposer_user_id`, `proposer_product_id`, `receiver_user_id`, `receiver_product_id`, `status`, `created_at`) VALUES
(1, 1, 4, 2, 5, 'completado', '2025-08-06 04:12:52'),
(2, 2, 8, 1, 7, 'pendiente', '2025-08-06 04:54:37'),
(3, 2, 4, 1, 7, 'pendiente', '2025-08-06 04:56:17'),
(4, 2, 8, 1, 7, 'pendiente', '2025-08-06 05:00:00');

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
  `nivel` varchar(50) DEFAULT 'Nuevo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `nombre`, `apellidos`, `email`, `password_hash`, `telefono`, `fecha_registro`, `username`, `foto_perfil`, `direccion`, `fecha_nacimiento`, `is_admin`, `estado`, `ultimo_login`, `verificado`, `reputacion`, `nivel`) VALUES
(1, 'Sam', 'Gutierrez', 's@gmail.com', '$2b$12$K44ZQgPVKSnHs/kKqzgoEuZCExSUG4SKLfJbqxDrmrZDA2f43AnEi', '7224108974', '2025-08-06 03:58:21', NULL, NULL, NULL, NULL, 0, 'activo', NULL, 0, 0, 'Nuevo'),
(2, 'Sam', 'Gutierrez', 'sam2@gmail.com', '$2b$12$DPX6K9z1PkhaMqhpJtSuiuwC4WS5ApgSLMMx5GWPbLn0.A2POXK/W', '7224108993', '2025-08-06 04:11:14', '', NULL, '', '0000-00-00', 0, 'activo', NULL, 0, 0, 'Nuevo');

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
-- Volcado de datos para la tabla `wishlists`
--

INSERT INTO `wishlists` (`id`, `user_id`, `product_id`, `created_at`) VALUES
(1, 2, 5, '2025-08-06 04:53:19'),
(2, 2, 7, '2025-08-06 04:54:21'),
(3, 2, 4, '2025-08-06 05:17:45');

--
-- Índices para tablas volcadas
--

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
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `trades`
--
ALTER TABLE `trades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `wishlists`
--
ALTER TABLE `wishlists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

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
