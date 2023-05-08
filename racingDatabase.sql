
CREATE TABLE Player
(
    Player_ID serial primary key not null ,
    Gamertag varchar(12) unique not null ,
    Name     varchar(100) not null ,
    forename  varchar(100) not null ,
    Password varchar(160) not null
);

CREATE TABLE Driver(
    Driver_ID serial primary key,
    Name varchar not null ,
    forename varchar not null ,
    nationality varchar not null,
    raceNumber smallint not null ,
    birthday date not null,

    unique (Name,forename,nationality,birthday)
);

CREATE TABLE Circuit(
    Circuit_ID serial primary key not null ,
    name varchar not null,
    country varchar not null,
    locality varchar not null,
     unique (Name,country,locality)
);

CREATE TABLE Race(
    Race_ID serial primary key not null,
    GP_ID integer references Circuit(Circuit_ID),
    Season integer not null ,
    Time time not null,
    Date date not null,
     unique (GP_ID,Season)
);

CREATE TABLE Tip
(
    Tip_ID serial primary key not null ,
    Driver_ID integer references Driver(Driver_ID),
    Race_ID integer references Race(Race_ID),
    result smallint not null
);

CREATE TABLE bet(
    Player_ID int references Player(Player_ID),
    Tip_ID int references Tip(Tip_ID)
);

CREATE TABLE Raceresults(
    Driver_ID int references Driver(Driver_ID),
    Race_ID int references Race(Race_ID),
    result smallint not null,
    unique (Driver_ID,Race_ID)
)
