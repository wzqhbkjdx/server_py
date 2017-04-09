use awesome;

create table tasks (
	id bigint not null auto_increment primary key,
	idenf varchar(100) not null,
	task_name varchar(100) not null,
	ip_repeat_days integer not null,
	level_2_days integer,
	level_2_percents real,
	level_3_days integer,
	level_3_percents real,
	level_4_days integer,
	level_4_percents real,
	level_5_days integer,
	level_5_percents real,
	level_6_days integer,
	level_6_percents real,
	level_7_days integer,
	level_7_percents real,
	level_8_days integer,
	level_8_percents real,
	new_limit integer
) engine=innodb default charset=utf8;