use awesome;

create table ip_dev_info (
	id integer not null AUTO_INCREMENT primary key,
    idenf varchar(50),
	BLUEADDRESS varchar(50),
	BUILDVERSION varchar(50),
	DEVICETOKEN varchar(100),
	ECID varchar(50),
	IAD varchar(100),
	IDFV varchar(100),
	IP varchar(50),
	IPS varchar(50),
	MLBSERIAL varchar(50),
	MODEL varchar(50),
	MODELTYPE varchar(50),
	NAME varchar(50),
	ODIN varchar(100),
	OPENUDID varchar(100),
	ORG varchar(50),
	ORGMODEL varchar(50),
	PRODUCT varchar(50),
	RSSID varchar(50),
	SERIAL varchar(50),
	UDID varchar(100),
	VERSION varchar(50),
	WIFIADDRESS varchar(50),
	iGrimaceKey varchar(50),
	rj varchar(50),
	rj2 varchar(50),
	rw varchar(50),
	rw2 varchar(50)
) engine=innodb default charset=utf8;
