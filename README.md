# "100 Days of Code" Portfolio Projects

This repository features projects I developed during days 82 to 100 of the Udemy course "100 Days of Code".

## Day 82 - String to Morse

The exercise on day 82 involved creating a text-based converter that converts strings into Morse code. In my solution, I developed a simple console program that loads the input argument, converts it to its Morse code representation and returns the result.

### Usage  
To run the program, use the following command:  

```powershell
py D82_StringToMorse\main.py "example text."  
```

## Day 84 - Tic Tac Toe

The task of this day was to build a text based tic tac toe game.

### Features

- Two game modes: PvP (Player vs Player) and PvC (Player vs Computer)
- Includes a temporary scoreboard
- Detects if someone has won the current game or if its a tie
- Includes a algorithm to handle computer turns

### Usage  
To start the Game, use the following command:  

```powershell
py D84_TextBasedTicTacToe\main.py
```

## Day 85 - Image Watermark App

The goal of day 85 included developing a desktop app which adds a water mark to one or multiple images.

### Features

- customizable watermark text and output directory

### Usage  
To start the application, use the following command:  

```powershell
# create a virtual environment
py -m venv venv

# activate the virtual environment
.\venv\Scripts\activate

# install requirements
py -m pip install -r .\requirements.txt

# start the program
py .\main.py

```

## Day 86 - Speed Typing Test

The task for today was to create a speed typing application using a Tkinter GUI.

### Features

- Execute a short 60 second speed typing test and prints the result
  - Words per minute
  - characters per minute
  - including the number of errors, categorized into corrected typos and entered misspellings.
- Has a Scoreboard, which displays the best 5 runs

### Usage  
To start the application, use the following command:  

```powershell
# create a virtual environment
py -m venv venv

# activate the virtual environment
.\venv\Scripts\activate

# install requirements
py -m pip install -r .\requirements.txt

# start the program
py .\main.py

```
