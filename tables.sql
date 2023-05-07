
CREATE TABLE Spieler
(
    Spieler_ID serial primary key not null ,
    Gamertag varchar(12) unique not null ,
    Name     varchar(100) not null ,
    Vorname  varchar(100) not null ,
    Passwort varchar(160) not null
);

CREATE TABLE Fahrer(
    Fahrer_ID serial primary key,
    Name varchar not null ,
    Vorname varchar not null ,
    Nationalität varchar not null,
    Kürzel varchar not null,
    Rennnumer smallint,
    geburtstag date,

    unique (Name,Vorname,Nationalität,geburtstag)
);

CREATE TABLE GrandPrix(
    GP_ID serial primary key not null ,
    Name varchar not null,
    Land varchar not null,
    Ort varchar not null,
     unique (Name,Land,Ort)
);

CREATE TABLE Rennen(
    Rennen_ID serial primary key not null,
    GP_ID integer references GrandPrix(GP_ID),
    Saison integer not null ,
    Uhrzeit time not null,
    Datum date not null,
     unique (GP_ID,Saison)
);

CREATE TABLE Tipp
(
    Tipp_ID serial primary key not null ,
    Fahrer_ID integer references Fahrer(Fahrer_ID),
    Rennen_ID integer references Rennen(Rennen_ID),
    Platzierung smallint not null
);

CREATE TABLE Wette(
    Spieler_ID int references Spieler(Spieler_ID),
    Tipp_ID int references Tipp(Tipp_ID)
);

CREATE TABLE Rennergebnis(
    Fahrer_ID int references Fahrer(Fahrer_ID),
    Rennen_ID int references Rennen(Rennen_ID),
    Platzierung smallint not null,
    unique (Fahrer_ID,Rennen_ID)
)