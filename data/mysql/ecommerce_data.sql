-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-04-2025 a las 16:06:38
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ecommerce`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`) VALUES
(1, 2, 1, 1),
(2, 2, 3, 2),
(3, 3, 5, 1),
(4, 3, 7, 1),
(5, 4, 2, 1),
(6, 5, 4, 1),
(7, 5, 6, 2),
(8, 6, 8, 3),
(9, 7, 10, 1),
(10, 8, 12, 1),
(11, 9, 14, 2),
(12, 10, 1, 1),
(13, 10, 15, 1),
(14, 12, 1, 6),
(15, 12, 3, 1),
(16, 12, 2, 5),
(17, 12, 7, 1),
(18, 12, 4, 3),
(19, 13, 8, 2),
(20, 12, 12, 1),
(21, 12, 6, 2),
(22, 14, 1, 1),
(23, 15, 4, 2),
(24, 15, 14, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `status` enum('pending','completed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total`, `status`, `created_at`) VALUES
(1, 2, 2899.98, 'completed', '2025-04-09 20:39:06'),
(2, 3, 439.98, 'completed', '2025-04-09 20:39:06'),
(3, 4, 999.99, 'completed', '2025-04-09 20:39:06'),
(4, 5, 469.98, 'pending', '2025-04-09 20:39:06'),
(5, 6, 209.97, 'completed', '2025-04-09 20:39:06'),
(6, 7, 199.99, 'cancelled', '2025-04-09 20:39:06'),
(7, 8, 129.99, 'completed', '2025-04-09 20:39:06'),
(8, 9, 239.98, 'pending', '2025-04-09 20:39:06'),
(9, 10, 1249.99, 'completed', '2025-04-09 20:39:06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `image_url`) VALUES
(1, 'Laptop', 'Laptop empresarial con procesador i7, 16GB RAM, 512GB SSD', 1200.00, 153, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(2, 'iPhone 13 Pro', 'Smartphone Apple con pantalla Super Retina XDR, 128GB', 999.99, 8, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(3, 'Samsung Galaxy S22', 'Smartphone Android con cámara de 108MP, 256GB', 849.50, 12, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(4, 'Monitor Dell 27\"', 'Monitor QHD de 27 pulgadas con tasa de refresco de 144Hz', 349.99, 20, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(5, 'Teclado Mecánico RGB', 'Teclado gaming mecánico con retroiluminación RGB', 89.99, 30, 'https://example.com/images/teclado-rgb.jpg'),
(6, 'Mouse Inalámbrico Logitech', 'Mouse ergonómico con conexión Bluetooth y 2 años de batería', 59.99, 25, 'https://example.com/images/mouse-logitech.jpg'),
(7, 'Auriculares Sony WH-1000XM4', 'Auriculares inalámbricos con cancelación de ruido, calidad de sonido excepcional', 349.99, 12, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(8, 'Disco Duro Externo 1TB', 'Disco duro portátil USB 3.0, compatible con PC y Mac', 69.99, 18, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(9, 'Tablet Samsung Galaxy Tab S7', 'Tablet con S Pen incluido, pantalla de 11\", 128GB', 499.99, 7, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(10, 'Impresora Multifunción HP', 'Impresora láser con escáner y copiadora, WiFi', 199.99, 5, 'https://example.com/images/impresora-hp.jpg'),
(11, 'Smartwatch Apple Watch Series 7', 'Reloj inteligente con monitor de actividad y ECG', 399.99, 9, 'https://example.com/images/apple-watch.jpg'),
(12, 'Router WiFi 6', 'Router de última generación con soporte para WiFi 6', 129.99, 14, 'https://images-cdn.ubuy.co.in/64cd7303d0cad1527f2ede56-lenovo-ideapad-5-14-1080p-touchscreen.jpg'),
(13, 'Altavoz Bluetooth JBL', 'Altavoz portátil resistente al agua con 20h de autonomía', 119.99, 22, 'https://example.com/images/altavoz-jbl.jpg'),
(14, 'Cargador Inalámbrico Rápido 15W', 'Base de carga inalámbrica rápida 15W compatible con dispositivos Qi', 34.99, 40, 'https://example.com/images/cargador-inalambrico.jpg'),
(15, 'Webcam HD 1080p', 'Cámara web con micrófono integrado y enfoque automático', 49.99, 17, 'https://example.com/images/webcam-hd.jpg'),
(101, 'Cargador Inalámbrico 15W', 'Cargador inalámbrico rápido 15W, compatible con dispositivos Qi', 34.99, 50, 'https://example.com/images/cargador-inalambrico.jpg'),
(102, 'Auriculares Sony WH-1000XM4', 'Auriculares inalámbricos con cancelación de ruido, sonido premium', 349.99, 20, 'https://example.com/images/auriculares-sony.jpg'),
(103, 'Funda Silicona iPhone 13', 'Funda de silicona protectora para iPhone 13, color negro', 19.99, 150, 'https://example.com/images/funda-iphone-13.jpg'),
(104, 'Protector de Pantalla Samsung Galaxy S22', 'Protector de pantalla de cristal templado para Samsung Galaxy S22', 12.99, 100, 'https://example.com/images/protector-s22.jpg'),
(105, 'Auriculares Bluetooth Samsung Galaxy Buds Pro', 'Auriculares inalámbricos con cancelación de ruido', 199.99, 50, 'https://example.com/images/galaxy-buds-pro.jpg'),
(106, 'Cargador Rápido iPhone 20W', 'Cargador rápido de 20W compatible con iPhone 12 y superiores', 24.99, 80, 'https://example.com/images/cargador-iphone-20w.jpg'),
(107, 'Funda TPU Samsung Galaxy S21', 'Funda protectora de TPU para Samsung Galaxy S21, resistente a caídas', 15.99, 200, 'https://example.com/images/funda-galaxy-s21.jpg'),
(108, 'Power Bank 10000mAh', 'Batería externa portátil de 10000mAh, carga rápida', 29.99, 100, 'https://example.com/images/power-bank-10000.jpg'),
(109, 'Soporte Ajustable para Celular', 'Soporte ajustable para celular, ideal para videollamadas y ver películas', 14.99, 150, 'https://example.com/images/soporte-celular.jpg'),
(110, 'Cable de Carga USB-C a Lightning', 'Cable de carga USB-C a Lightning, 1 metro, compatible con iPhone', 9.99, 300, 'https://example.com/images/cable-iphone-usbc.jpg'),
(1100, 'Cargador Inalámbrico 20W', 'Cargador inalámbrico rápido 20W para dispositivos móviles', 39.99, 150, 'https://example.com/images/cargador-inalambrico-20w.jpg'),
(1101, 'dqw', 'qwq', 23.00, 2, 'http://localhost:5000/admin/products/add'),
(1102, 'dqw', 'qwq', 23.00, 2, 'http://localhost:5000/admin/products/add');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','client') DEFAULT 'client'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`) VALUES
(1, 'admin1', 'admin1@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'admin'),
(2, 'juanperez', 'juan.perez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(3, 'mariagarcia', 'maria.garcia@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(4, 'carloslopez', 'carlos.lopez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(5, 'anatorres', 'ana.torres@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(6, 'luishernandez', 'luis.hernandez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(7, 'sofiaramirez', 'sofia.ramirez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(8, 'pedrogomez', 'pedro.gomez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(9, 'lauramartinez', 'laura.martinez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(10, 'davidrodriguez', 'david.rodriguez@example.com', '$2y$10$HfzIhGCCaxqyaIdGgjARSuOKAcm1Uy82YfLuNaajn6JrjLWy9Sj/W', 'client'),
(11, 'new_user', 'test@gmail.com', '$2b$12$wV5AlMIV2pRz2WXYL4ub1ueRs6k9z8x3ZsHhtIUgrRI8KICjZ2tWq', 'client'),
(12, 'desarrollamelo', 'pericena12@gmail.com', '$2b$12$sCTdTh3Unv/N7tNLRnzLOOqXIpciVCbAsehFXqfbWRjnyZ0Wwr9.i', 'client'),
(13, 'pericena1aa2@gmail.com', 'pericena1aa2@gmail.com', '$2b$12$F7iFWyJEYQGp1Zvz9NQLb.Z.YAdBzCvcBOnr202/.yOTSkpjJDAmq', 'client'),
(14, 'Yeshd', 'pericenssa12@gmail.com', '$2b$12$jCBX.7AaqYKJ9w7P6ClMv.1z3H/1ATZj1k5c7aLRlcRcoC1iFSdpy', 'client'),
(15, 'pedrito', 'pedro@gmail.com', '$2b$12$DeW/d8OD2nz20027A.R5jemN3gofJ3ma/Gh9JBtkcU7fpUiY//KKe', 'client');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1103;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Filtros para la tabla `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
