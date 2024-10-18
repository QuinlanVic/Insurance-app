CREATE DATABASE CoolWaterDB;
GO

USE CoolWaterDB;

-- Create articles table
CREATE TABLE articles (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    title NVARCHAR(255),
    author NVARCHAR(255),
    poster NVARCHAR(255),
    [desc] NVARCHAR(MAX)
);

-- Create employees table
CREATE TABLE employees (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(255),
    job_title NVARCHAR(255),
    pic NVARCHAR(255),
    [desc] NVARCHAR(MAX)
);

-- Create policies table
CREATE TABLE policies (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(255),
    price DECIMAL(18, 2),
    poster NVARCHAR(255),
    [desc] NVARCHAR(MAX)
);

-- Create requests table
CREATE TABLE requests (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(255),
    phone_num NVARCHAR(20),
    email NVARCHAR(255),
    msg NVARCHAR(MAX)
);

-- Create users table
CREATE TABLE users (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(255),
    phone_num NVARCHAR(20),
    email NVARCHAR(255),
    msg NVARCHAR(MAX)
);
GO

INSERT INTO employees (name, job_title, pic, [desc])
VALUES
('Paul Flex', 'CEO', 'https://t4.ftcdn.net/jpg/06/35/15/47/360_F_635154757_zU5ZxxZe3Vs0hrrOQ9WBgNgX8s4Cw19s.jpg', 'Paul Flex is CoolWater''s Chief Executive Officer'),
('Sarah Blue', 'CFO', 'https://t4.ftcdn.net/jpg/06/12/73/89/360_F_612738927_LIcFCiKHQhHq9R1QhkVRKvT6RelYUmgv.jpg', 'Sarah Bleu is CoolWater''s Chief Financial Officer'),
('Mandla Ngcobo', 'CHRO', 'https://www.goodthingsguy.com/wp-content/uploads/2020/07/vusi-thembekwayo-biography-age-net-worth-wife-2.jpg', 'Mandla Ngcobo is Coolwater''s Chief Human Resources Officer');

INSERT INTO policies (name, price, poster, [desc])
VALUES
('Blue Car Insurance', 500, 'https://c4.wallpaperflare.com/wallpaper/14/17/129/2011-hyundai-i10-wallpaper-preview.jpg', 'Blue Car Insurance is affordable and is targeted at students and young professionals'),
('Cool Car Insurance', 1000, 'https://c4.wallpaperflare.com/wallpaper/373/463/605/volkswagen-rain-gti-hd-silver-coupe-wallpaper-preview.jpg', 'Cool Car Insurance is targeted at established professionals and middle aged individuals'),
('Water Car Insurance', 1500, 'https://moewalls.com/wp-content/uploads/2024/01/bmw-m4-rainy-night-thumb.jpg', 'Water Car Insurance is targeted at small families'),
('CoolWater Car Insurance', 2000, 'https://c4.wallpaperflare.com/wallpaper/634/597/281/luxury-suv-range-rover-velar-2017-4k-wallpaper-preview.jpg', 'CoolWater is targeted at medium to large families'),
('CoolCool Car Insurance', 2500, 'https://c4.wallpaperflare.com/wallpaper/131/207/698/forest-rain-forest-ford-wallpaper-preview.jpg', 'CoolCool Car Insurance is targeted at those with antique vehicles'),
('WaterCool Car Insurance', 3000, 'https://i.pinimg.com/originals/56/c3/74/56c3744dc273cab7d050b9943d2accfa.jpg', 'WaterCool Car Insurance is targeted at those with sports cars');

INSERT INTO articles (title, author, poster, [desc])
VALUES
('Only need insurance for parts?', 'Sketch Higgle', 'https://cdn.motor1.com/images/mgl/EEWQe/s3/2016-bugatti-chiron.jpg', 'CoolWater provides policies that only cover certain components of your car providing you complete freedom over your insurance portfolio'),
('Getting Ready For A Big Night?', 'Pete Loud', 'https://www.nydailynews.com/wp-content/uploads/migration/2016/06/03/DD2BKJSSALFDG3RORJ2QGRYR7E.jpg', 'CoolWater provides you with free rides home after 11pm every weekend!'),
('Our Amazing Service', 'Jermaine Fer', 'https://d39l2hkdp2esp1.cloudfront.net/img/photo/145768/145768_00_2x.jpg', 'At CoolWater we are focused on providing you with the best customer experience'),
('24-hour Emergency Service', 'Neo Deep', 'https://www.aa.co.nz/assets/motoring/blog/Driver-looking-under-bonnet-lemon.jpg', 'With CoolWater you have access to our 24-hour emergency service, 7 days a week, free of charge!');

-- View data in employees table
SELECT * FROM employees;

-- View data in policies table
SELECT * FROM policies;

-- View data in articles table
SELECT * FROM articles;

-- View data in users table
SELECT * FROM users;