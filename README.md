# Mines Game

## Introduction
**Mines** is an interactive game developed using Python's `Tkinter` library. The game combines elements of chance with strategic decision-making, allowing users to place bets and attempt to reveal safe tiles while avoiding a hidden "danger" tile. Players can cash out at any time, collecting their winnings based on the number of safe tiles they reveal.

## Features
- **Betting System:** Players can place bets, double them (2x), or halve them (1/2) before starting a round.
- **Wallet Management:** Integrated wallet functionality allows players to manage their balance, deposit, and withdraw funds using a simulated UPI ID.
- **Game Grid:** A 5x5 grid with 25 tiles where players can reveal safe tiles or hit the hidden danger tile.
- **Odds and Multipliers:** The game calculates odds dynamically, rewarding players based on the number of safe tiles revealed before cashing out.
- **Max Win:** A maximum win is achieved if all 24 safe tiles are revealed without hitting the danger tile.

## Gameplay
1. **Start a Round:** Click the "Bet" button to start a round. This will subtract the bet amount from your balance and activate the grid.
2. **Reveal Tiles:** Click on any of the 25 tiles. If the tile is safe, it will turn green. If it is the danger tile, it will turn red, and the round will end.
3. **Cash Out:** At any point during the round, you can click "Cash Out" to collect your winnings. The winnings are calculated based on the number of safe tiles revealed.
4. **Wallet Management:** Use the "Wallet" button to view your balance, deposit funds, or withdraw funds.
