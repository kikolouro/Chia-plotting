CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(255),
  `token` varchar(255),
  `password` varchar(255),
  `publickey` varchar(255),
  `poolkey` varchar(255)
);

CREATE TABLE `orders` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `externalid` varchar(255),
  `user` int,
  `state` varchar(255),
  `pool` int
);

CREATE TABLE `pool` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `downloadlink` varchar(255),
  `state` varchar(255),
  `price` varchar(255),
  `eta` varchar(255)
);

CREATE TABLE `notifications` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user` int,
  `seen` varchar(255),
  `notificationdate` timestamp,
  `body` varchar(255)
);

CREATE TABLE `notificationsorders` (
  `order` int,
  `notification` int,
  PRIMARY KEY (`order`, `notification`)
);

ALTER TABLE `notificationsorders` ADD FOREIGN KEY (`order`) REFERENCES `orders` (`id`);

ALTER TABLE `notificationsorders` ADD FOREIGN KEY (`notification`) REFERENCES `notifications` (`id`);

ALTER TABLE `notifications` ADD FOREIGN KEY (`user`) REFERENCES `users` (`id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`user`) REFERENCES `users` (`id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`pool`) REFERENCES `pool` (`id`);

