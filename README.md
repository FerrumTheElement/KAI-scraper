# KAI-Scraper

in this short paragraph im going to explain to you(ian) how the fuck ur code works so u dont forget it in the future

## Imports

Selenium - used to fetch HTML data and organises it in a very neat and clean manner

datetime - managing and makes time calculation less of a hassle

argparse - make CLI arguments to make it usable without an graphic interface

# Function find()

this function’s purpose is to collect all the train data and organises it into a single list called: “combined”. In which this function’s result will be the returned list: “combined”

## For loops

most for loops are identical fetching every single data required onto the list in which each “category” has their own array which we will be needing at the end

Some however are different because the destination and the departure stations are alternating for example:

Surabaya
Yogyakarta
Surabaya

*in one “class_” 

So, for some of the loops we have to use an alternating loop using a simple count and modulus so that half of the numbers that are even will be the departing station and the odd numbers will be the arriving station.

The last but certainly not least for loop ties every single array down onto a single list named: combined

# Function loop()

for each item in the combined list. it is filtered organisedly depending on the users input if they have inputted a filter for Time, Trainclass(Economy/Executive), MaximumPrice.

Item[0] = Departure Time
Item[1] = Departure City + Station Code
Item[2] = Arrival Time
Item[3] = Arrival City + Station Code
Item[4] = Train Class (Economy/Executive)
Item[5] = Ticket Price
Item[6] = Name of Train + Train Number
Item[7] = Type of train (Premium, New Generation, Panoramic)

The while True loop is responsible for the output and formatting of the categories given in the find() function. when typed: “>> or <<” in the interface it would either add or decrease the date by 1 in order to check for each day.
