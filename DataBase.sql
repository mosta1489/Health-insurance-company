-- -----------------------------------------------------
-- Schema Insurance Company
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Insurance Company` DEFAULT CHARACTER SET utf8;
USE `Insurance Company`;
-- -----------------------------------------------------
-- Table `Insurance Company`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`customer` (
  `user_name` varchar(10),
  `name` VARCHAR(45) NOT NULL,
  `phone` varchar(11),
  `password` varchar(10),
  PRIMARY KEY (`user_name`)
);
-- -----------------------------------------------------
-- Table `Insurance Company`.`Plans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`plans` (
  `plan_ID` INT auto_increment,
  `type` VARCHAR(10),
  `owner` varchar(10),
  PRIMARY KEY (`plan_ID`),
  FOREIGN KEY (`owner`) REFERENCES `Insurance Company`.`customer` (`user_name`),
  check(`type` in ('basic', 'premium', 'golden'))
);
-- -----------------------------------------------------
-- Table `Insurance Company`.`Hospital`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`hospital` (
  `name` VARCHAR(15),
  `phone` VARCHAR(11),
  `location` varchar(10),
  PRIMARY KEY (`name`)
);
-- -----------------------------------------------------
-- Table `Insurance Company`.`dependenses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`dependents` (
  `name` VARCHAR(10) NOT NULL,
  `relationship` VARCHAR(10),
  `plan` INT,
  PRIMARY KEY (`name`, `plan`),
  FOREIGN KEY (`plan`) REFERENCES `Insurance Company`.`plans` (`plan_ID`)
);
-- -----------------------------------------------------
-- Table `Insurance Company`.`Cover`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`covers` (
  `hospital` varchar(15),
  `plan_type` varchar(10),
  PRIMARY KEY (`hospital`, `plan_type`),
  FOREIGN KEY (`hospital`) REFERENCES `Insurance Company`.`Hospital` (`name`)
);
-- -----------------------------------------------------
-- Table `Insurance Company`.`Claims`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Insurance Company`.`claims` (
  `claim_ID` INT auto_increment,
  `plan` INT,
  `state` varchar(10) not null default 'unresolved',
  `description` text,
  `cost` decimal(6, 2),
  `date_of_claim` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `beneficiary` varchar(10) unique,
  PRIMARY KEY (`claim_ID`),
  FOREIGN KEY (`plan`) REFERENCES `Insurance Company`.`plans`(`plan_ID`),
  FOREIGN KEY (`beneficiary`) REFERENCES `Insurance Company`.`dependents`(`name`),
  check (`state` in ('resolved', 'unresolved'))
);
-- we assumed that there are only 9000 plans we will sell so they will take numbers between 1000 : 10000.
ALTER TABLE
  `Insurance Company`.`plans` AUTO_INCREMENT = 1000;
-- and we begin the claims from claim number 10001 to infinty as each customer make claims as he need :)
ALTER TABLE
  `Insurance Company`.`claims` AUTO_INCREMENT = 10001;