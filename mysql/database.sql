use telegram;
CREATE TABLE `login` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `pw` varchar(255)
);

CREATE TABLE `token` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `token` varchar(255),
  `user` int
);

ALTER TABLE `token` ADD FOREIGN KEY (`user`) REFERENCES `login` (`id`);
