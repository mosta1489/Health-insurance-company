
-- -----------------------------------------------------
-- Schema Insurance Company
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Insurance Company` DEFAULT CHARACTER SET utf8 ;
USE `Insurance Company` ;

-- -----------------------------------------------------
-- Table `Insurance Company`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`customer` (
  `user_name` varchar(15),
  `name` VARCHAR(45) NOT NULL,
  `phone` varchar(15),
  `password` varchar(6),
  
  PRIMARY KEY (`user_name`));
  
-- -----------------------------------------------------
-- Table `Insurance Company`.`Plans`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Insurance Company`.`plans` (
  `plan_ID` INT auto_increment,
  `type` VARCHAR(10),
  `owner` varchar(8),
  
  PRIMARY KEY (`plan_ID`),
  FOREIGN KEY (`owner`) REFERENCES `Insurance Company`.`customer` (`user_name`),
  check(`type` in ('basic', 'premium', 'golden')));

-- -----------------------------------------------------
-- Table `Insurance Company`.`Hospital`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`hospital` (
  `name` VARCHAR(45),
  `phone` VARCHAR(45),
  `location` varchar(45),

  PRIMARY KEY (`name`));

-- -----------------------------------------------------
-- Table `Insurance Company`.`dependenses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`dependents` (
  `name` VARCHAR(30) NOT NULL,
  `relationship` VARCHAR(20) ,
  `plan` INT,
  PRIMARY KEY (`name`, `plan`),
  
  FOREIGN KEY (`plan`)
  REFERENCES `Insurance Company`.`plans` (`plan_ID`));

-- -----------------------------------------------------
-- Table `Insurance Company`.`Cover`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`covers` (
   `hospital` varchar(45),
   `plan_type` varchar(10),
   
   PRIMARY KEY (`hospital`, `plan_type`),
	FOREIGN KEY (`hospital`)
	REFERENCES `Insurance Company`.`Hospital` (`name`));
    
-- -----------------------------------------------------
-- Table `Insurance Company`.`Claims`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`claims` (
   `claim_ID` INT auto_increment,
   `plan` INT,
   `state` varchar(10) not null,
   `description` text,
   `cost` decimal(6, 2),
   data datetime,
   
   PRIMARY KEY (`claim_ID`),
   FOREIGN KEY (`plan`)
   REFERENCES `Insurance Company`.`plans`(`plan_ID`),
   check (`state` in ('resolved', 'unresolved'))
   );
   



-- we assumed that there are only 9000 plans we will sell so they will take numbers between 10000.
-- and we begin the claims from claim number 10001 to infinty as each customer make claims as he need )
ALTER TABLE `Insurance Company`.`claims` AUTO_INCREMENT = 10001;
ALTER TABLE `Insurance Company`.`plans` AUTO_INCREMENT = 1000;
-- CREATE VIEW  customers_list as select user_name, name, phone from customer;
alter table customer modify column phone varchar(15);
