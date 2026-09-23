CREATE TABLE Teams (
    team_pos INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    championships INTEGER,
    points INTEGER,
    engine_supplier TEXT
);

CREATE TABLE Drivers (
    driver_pos INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    nationality TEXT,
    wins INTEGER,
    podiums INTEGER,
    points INTEGER,
    race_number INTEGER,
    team_name TEXT,
    FOREIGN KEY (team_name) REFERENCES Teams (team_name)
);

CREATE TABLE Races (
    race_id INTEGER PRIMARY KEY,
    grand_prix TEXT NOT NULL UNIQUE,
    date TEXT NOT NULL,
    winner TEXT,
    laps INTEGER,
    FOREIGN KEY (winner) REFERENCES Drivers (name)
);

CREATE TABLE Race_Drivers (
    grand_prix TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    position INTEGER,
    points INTEGER,
    fast_lap TEXT,
    PRIMARY KEY (grand_prix, driver_name),
    FOREIGN KEY (grand_prix) REFERENCES Races (grand_prix),
    FOREIGN KEY (driver_name) REFERENCES Drivers (name)
);

CREATE TABLE Race_Teams (
    grand_prix TEXT NOT NULL,
    team_name TEXT NOT NULL,
    total_points INTEGER,
    PRIMARY KEY (grand_prix, team_name),
    FOREIGN KEY (grand_prix) REFERENCES Races (grand_prix),
    FOREIGN KEY (team_name) REFERENCES Teams (team_name)
);

