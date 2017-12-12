/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : facedb

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2017-12-12 00:51:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `event`
-- ----------------------------
DROP TABLE IF EXISTS `event`;
CREATE TABLE `event` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `date` char(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image_path` char(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_id` char(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for `people`
-- ----------------------------
DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` char(20) DEFAULT NULL,
  `last_name` char(20) DEFAULT NULL,
  `first_date` char(20) DEFAULT NULL,
  `last_sight` char(20) DEFAULT NULL,
  `url1` varchar(1000) DEFAULT NULL,
  `url2` varchar(1000) DEFAULT NULL,
  `url3` varchar(1000) DEFAULT NULL,
  `url4` varchar(1000) DEFAULT NULL,
  `url5` varchar(1000) DEFAULT NULL,
  `url6` varchar(1000) DEFAULT NULL,
  `url7` varchar(1000) DEFAULT NULL,
  `url8` varchar(1000) DEFAULT NULL,
  `url9` varchar(1000) DEFAULT NULL,
  `url10` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;