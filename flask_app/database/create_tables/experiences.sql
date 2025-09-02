CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The experience id',
`position_id`          int(11)       NOT NULL  	              COMMENT 'The position id to be referenced',
`name`                 varchar(100)  NOT NULL                	COMMENT 'The name of the experience', 
`description`          varchar(255)  NOT NULL                	COMMENT 'Description of this experience',
`hyperlink`            varchar(100)  DEFAULT NULL            	COMMENT 'Link where people can learn more about this expereince',
`start_date`           date          DEFAULT NULL            	COMMENT 'The start date in which I started this experience',
`end_date`             date          DEFAULT NULL            	COMMENT 'The start date in which I ended this experience',  
PRIMARY KEY  (`experience_id`),
FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="My work Experiences";