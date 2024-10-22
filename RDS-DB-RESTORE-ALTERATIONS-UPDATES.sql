-- CREATE DATABASE coolwaterdb;
-- CREATE DATABASE IF NOT EXISTS coolwaterdb;

-- Switch to the database
USE coolwaterdb;

-- Create the employees table
-- CREATE TABLE IF NOT EXISTS employees (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     job_title VARCHAR(255) NOT NULL,
--     pic TEXT,
--     `desc` TEXT
-- );

ALTER TABLE employees DROP PRIMARY KEY; -- Only if needed
ALTER TABLE employees
MODIFY id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID());

ALTER TABLE articles DROP PRIMARY KEY; -- Only if needed
ALTER TABLE articles
MODIFY id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID());

-- Insert values into the employees table
INSERT INTO employees (name, job_title, pic, `desc`)
VALUES
('Paul Flex', 'CEO', 'https://t4.ftcdn.net/jpg/06/35/15/47/360_F_635154757_zU5ZxxZe3Vs0hrrOQ9WBgNgX8s4Cw19s.jpg', 'Paul Flex is CoolWater\'s Chief Executive Officer'),
('Sarah Blue', 'CFO', 'https://t4.ftcdn.net/jpg/06/12/73/89/360_F_612738927_LIcFCiKHQhHq9R1QhkVRKvT6RelYUmgv.jpg', 'Sarah Bleu is CoolWater\'s Chief Financial Officer'),
('Mandla Ngcobo', 'CHRO', 'https://www.goodthingsguy.com/wp-content/uploads/2020/07/vusi-thembekwayo-biography-age-net-worth-wife-2.jpg', 'Mandla Ngcobo is Coolwater\'s Chief Human Resources Officer');

-- Create the policies table
-- CREATE TABLE IF NOT EXISTS policies (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     price DECIMAL(10, 2) NOT NULL,
--     poster TEXT,
--     `desc` TEXT
-- );

-- Create the articles table
-- CREATE TABLE IF NOT EXISTS articles (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     author VARCHAR(255) NOT NULL,
--     poster TEXT,
--     `desc` TEXT
-- );

-- Insert values into the articles table
INSERT INTO articles (title, author, poster, `desc`)
VALUES
('Only need insurance for parts?', 'Sketch Higgle', 'https://cdn.motor1.com/images/mgl/EEWQe/s3/2016-bugatti-chiron.jpg', 'CoolWater provides policies that only cover certain components of your car providing you complete freedom over your insurance portfolio'),
('Getting Ready For A Big Night?', 'Pete Loud', 'https://www.nydailynews.com/wp-content/uploads/migration/2016/06/03/DD2BKJSSALFDG3RORJ2QGRYR7E.jpg', 'CoolWater provides you with free rides home after 11pm every weekend!'),
('Our Amazing Service', 'Jermaine Fer', 'https://d39l2hkdp2esp1.cloudfront.net/img/photo/145768/145768_00_2x.jpg', 'At CoolWater we are focused on providing you with the best customer experience'),
('24-hour Emergency Service', 'Neo Deep', 'https://www.aa.co.nz/assets/motoring/blog/Driver-looking-under-bonnet-lemon.jpg', 'With CoolWater you have access to our 24-hour emergency service, 7 days a week, free of charge!');


-- ALTER TABLE policies DROP PRIMARY KEY; -- Only if needed
-- ALTER TABLE policies
-- MODIFY id CHAR(36) NOT NULL DEFAULT (UUID());

-- ALTER TABLE users DROP PRIMARY KEY; -- Only if needed
-- ALTER TABLE users
-- MODIFY id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID());

SHOW CREATE TABLE employees;

SELECT 
    CONSTRAINT_NAME, 
    TABLE_NAME 
FROM 
    information_schema.KEY_COLUMN_USAGE 
WHERE 
    REFERENCED_TABLE_NAME = 'policies' OR 
    REFERENCED_TABLE_NAME = 'users';

ALTER TABLE usersclaims 
DROP FOREIGN KEY usersclaims_ibfk_2;

ALTER TABLE userspolicies 
DROP FOREIGN KEY userspolicies_ibfk_1;

ALTER TABLE userspolicies 
DROP FOREIGN KEY userspolicies_ibfk_2;

ALTER TABLE policies 
DROP PRIMARY KEY;

ALTER TABLE users 
DROP PRIMARY KEY;


ALTER TABLE policies 
MODIFY id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID());

ALTER TABLE users 
MODIFY id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID());

ALTER TABLE usersclaims 
ADD CONSTRAINT usersclaims_ibfk_2 
FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE userspolicies 
ADD CONSTRAINT userspolicies_ibfk_1 
FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE userspolicies 
ADD CONSTRAINT userspolicies_ibfk_2 
FOREIGN KEY (policy_id) REFERENCES policies(id);

SET SQL_SAFE_UPDATES = 0;

START TRANSACTION;
-- Insert values into the policies table
INSERT INTO policies (name, price, poster, `desc`)
VALUES
('Blue Car Insurance', 500, 'https://c4.wallpaperflare.com/wallpaper/14/17/129/2011-hyundai-i10-wallpaper-preview.jpg', 'Blue Car Insurance is affordable and is targeted at students and young professionals'),
('Cool Car Insurance', 1000, 'https://c4.wallpaperflare.com/wallpaper/373/463/605/volkswagen-rain-gti-hd-silver-coupe-wallpaper-preview.jpg', 'Cool Car Insurance is targeted at established professionals and middle aged individuals'),
('Water Car Insurance', 1500, 'https://moewalls.com/wp-content/uploads/2024/01/bmw-m4-rainy-night-thumb.jpg', 'Water Car Insurance is targeted at small families'),
('CoolWater Car Insurance', 2000, 'https://c4.wallpaperflare.com/wallpaper/634/597/281/luxury-suv-range-rover-velar-2017-4k-wallpaper-preview.jpg', 'CoolWater is targeted at medium to large families'),
('CoolCool Car Insurance', 2500, 'https://c4.wallpaperflare.com/wallpaper/131/207/698/forest-rain-forest-ford-wallpaper-preview.jpg', 'CoolCool Car Insurance is targeted at those with antique vehicles'),
('WaterCool Car Insurance', 3000, 'https://i.pinimg.com/originals/56/c3/74/56c3744dc273cab7d050b9943d2accfa.jpg', 'WaterCool Car Insurance is targeted at those with sports cars');

UPDATE policies
SET poster = 'https://images.unsplash.com/photo-1580654712603-eb43273aff33?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGJsdWUlMjBjYXJ8ZW58MHx8MHx8fDA%3D'
WHERE name = 'Blue Car Insurance';

UPDATE policies
SET poster = 'https://live.staticflickr.com/7421/15739335263_724d7f9f3e_h.jpg'
WHERE name = 'CoolCool Car Insurance';

UPDATE policies
SET poster = 'https://wallpapers.com/images/featured/cool-cars-pictures-dc207131626mci2i.jpg'
WHERE name = 'Cool Car Insurance';

UPDATE policies
SET poster = 'https://www.motortrend.com/uploads/2023/02/2024-Lamborghini-Invencible-1.jpg?w=768&width=768&q=75&format=webp'
WHERE name = 'WaterCool Car Insurance';

UPDATE policies
SET poster = 'https://static1.hotcarsimages.com/wordpress/wp-content/uploads/2020/11/McLaren-F1-LM-Front-Quarter.jpg'
WHERE name = 'CoolWater Car Insurance';

COMMIT;

Use coolwaterdb;
SELECT * FROM policies;





