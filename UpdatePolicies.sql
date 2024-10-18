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

UPDATE users 
SET pic = 'https://i.pinimg.com/originals/9d/8d/f3/9d8df3614a0554ea1086bb77d165e323.jpg'
WHERE name = 'Quinlan';


-- DROP TABLE users;

-- Create users table
CREATE TABLE users (
    id NVARCHAR(50) PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(200) UNIQUE NOT NULL,
    password NVARCHAR(200) NOT NULL,
    pic NVARCHAR(255) DEFAULT '' NOT NULL
);

-- Create userpolicy table
CREATE TABLE userspolicies (
    id NVARCHAR(50) PRIMARY KEY DEFAULT NEWID(),
    user_id NVARCHAR(50) NOT NULL,
    policy_id NVARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);

-- Create claims table
CREATE TABLE claims (
    id NVARCHAR(50) PRIMARY KEY DEFAULT NEWID(),
    amount FLOAT NOT NULL,
    descr NVARCHAR(500) DEFAULT '' NOT NULL
);

-- Create userclaim table
CREATE TABLE usersclaims (
    id NVARCHAR(50) PRIMARY KEY DEFAULT NEWID(),
    claim_id NVARCHAR(50),
    user_id NVARCHAR(50),
    FOREIGN KEY (claim_id) REFERENCES claims(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP Table articles, employees, policies, requests

sp_help 'employees';

ALTER TABLE employees
ADD CONSTRAINT DF_Employee_ID DEFAULT NEWID() FOR id;

ALTER TABLE articles
ADD CONSTRAINT DF_Article_ID DEFAULT NEWID() FOR id;

ALTER TABLE policies
ADD CONSTRAINT DF_Policy_ID DEFAULT NEWID() FOR id;
