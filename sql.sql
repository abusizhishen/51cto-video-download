create database if not exists 51cto charset utf8mb4;

use 51cto;

create table if not exists train(
	id int auto_increment,
	train_id int not null,
	train_name varchar(60),
	course_num int default 0,
	primary key(id),
	unique (train_id),
	index (train_name)
)  engine innodb charset utf8mb4;

create table if not exists train_course(
	id int auto_increment,
	tra_id int not null,
	train_course_id int not null,
	course_id int not null,
	course_name varchar(60) not null,
	lesson_num int not null default 0,
	number int not null,
	primary key(id),
	unique (tra_id,train_course_id),
	CONSTRAINT `foreign_key_tra_id` FOREIGN KEY (`tra_id`) REFERENCES `train` (`id`) on delete cascade on UPDATE CASCADE
) engine innodb charset utf8mb4;

create table if not exists course_lesson(
	id int auto_increment,
	cou_id int not null,
	lesson_id int not null,
	lesson_name varchar(60) not null,
	video_id int not null,
	video_url varchar(100) not null,
	video_num int not null,
	primary key(id),
	unique (cou_id,lesson_id,video_id),
	CONSTRAINT `foreign_key_cou_id` FOREIGN KEY (`cou_id`) REFERENCES `train_course` (`id`) on delete cascade on UPDATE CASCADE
) engine innodb charset utf8mb4;

