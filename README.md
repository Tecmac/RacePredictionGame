# Race Prediction Game



## Introduction

The aim of the project is to create a Formula 1 racing prediction game where players can register to make race result predictions. Based on the race results, players will receive points, and the goal for each player is to accumulate the most points to win the game.

## Project Scope

The requirements for the project include having a complete program logic to host a freely accessible web application. Players should be able to submit their predictions, log in, and register through a terminal. Including fully implemented admin functions, and the algorithm for player prediction submissions.

## Technologies used
* Object-oriented programming
* Implementation of Data Access Objects (DAO)
* Persistent data storage
* PostgreSQL
* Psycopg2
* Python
* Ergast API
* Fast API (not fully implemented)

## Prequesits to start the programm
* internet connection
* "DatabaseConnection.py" must be correctly configured with your database port
* PostgreSQL Database. configured with the "racingDatabase.sql"
* Python and an IDE

## UI

The programm is used via the terminal in the future i will deploy an Website with a GUI

## Diagramms and Models

       
### Relational-Model
__Player__ (<ins>Player_ID</ins>,Gamertag, Name, Vorname, Password, Points)<br>
__Tip__ ( <ins>Tip_ID</ins>,#Driver_ID,#race_ID, result, points) <br>
__Race__ (<ins>Race_ID</ins>, Season,#circuit_ID time, date) <br>
__Circuit__ (<ins>Circuit_ID</ins>, Country, Name, Locality) <br>
__bet__ (<ins>#player_Id,#tip_id</ins>) <br>
__Driver__ (<ins>Driver_ID</ins>, Name, Forename, Nationality, RaceNumber, Birthday)<br>
__Raceresult__ (<ins>#Driver,#Race_ID</ins>, result)

