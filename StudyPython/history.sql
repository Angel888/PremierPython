create database grab;
use grab;
drop table history;
create table history(
id int unsigned primary key auto_increment,
username varchar(100) not null default '' comment '用户名',
ip varchar(40) not null default '' comment 'ip',
keyword varchar(100) not null default '' comment '关键字',
create_time int (10) not null default 0 comment '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='history table';
