use awesome;

create table if not exists task_name_remain (
	idenf varchar(50) not null,
	id integer not null primary key, 
	create_time datetime not null,
	update_time timestamp not null,
	status integer not null,
	last_date date,
	reach_date date,
	done_date varchar(2000)
) engine=innodb default charset=utf8;