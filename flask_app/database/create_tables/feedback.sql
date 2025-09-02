CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The comment id',
`name`              varchar(100)  NOT NULL                	COMMENT 'The name of the commentator', 
`email`             varchar(100)  NOT NULL                	COMMENT 'The email of the commentator', 
`comment`           varchar(255)  NOT NULL                	COMMENT 'The message sent by the commentator',

PRIMARY KEY  (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="My feedback page that has comments from people.";
