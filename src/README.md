# Blindtest generator

## Purpose

this little application can select a bunch of music from a playlist on spotify. You decide yourself what kind of playlist you do want by putting keywords in the lookup argument.

> Ex : If you want to find something related to rock, you can write "rock" or "rock 90's" to get best rock song from the 90's.

As the final purpose is to create a blindtest, we need to create a playlist with easy, medium and hard songs to find, to make it more cool to play and more challenging !

Popularity is divided in 3 categories :
- Low
- Medium
- High

## How to create a blindtest playlist

To get the playlist, you need to run `python .\spotify.py [categorySize] [MinPopularity]`

As you can see, the command line takes 2 arguments :
- CategorySize : Size of each category (medium will be times 2 this size)
- MinPopularity : between 0 and 100. It's the base of the least popularity you want in the playlist.
> The low popularity will be at least of the minPopularity