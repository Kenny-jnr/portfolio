CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`             int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The skill id',
`experience_id`        int(11)       NOT NULL  	              COMMENT 'The experience id to be refrenced',
`name`                 varchar(100)  NOT NULL                	COMMENT 'The name of the skill', 
`skill_level`          varchar(100)  NOT NULL                	COMMENT 'The extent to which I have mastered this skill',
PRIMARY KEY  (`skill_id`),
FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="My Skills";