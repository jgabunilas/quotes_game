# Quotes Game
A quote guessing game showcasing webscraping, HTML requests, and game logic.

This exercise is a coding challenge that is part of [The Modern Python 3 Bootcamp](https://www.udemy.com/course/the-modern-python3-bootcamp/) course taught by Colt Steel.

The exercise utilizes the **BeautifulSoup** webscraping library to obtain famous (or not-so-famous) quotes from the website [Quotes To Scrape](http://quotes.toscrape.com/). The quotes are collected and used in a guessing game in which the player attempts to guess the author of the quote. They player has a total of 4 attempts to correctly guess the author, with a hint provided after each incorrect guess. 


## Gathering URLs

The Quotes to Scrap website is updated regularly and typically contains 10 quotes per page. As mroe pages are added, the program must be flexible to ensure that it scrapes every available page of quotes. In the first part of the program, **BeautifulSoup** is used to access the main page and then systematically crawl its way through each page of quotes, collecting the URL information for each page as it goes. This is accomplished by searching the soup for an HTML element of the class `next`, which contains an anchor tag with an `href` hyperlink to the next page. This URL is saved to a list of URLs to scrape. A new HTML request is made to the next page, and the cycle continues until a `next` class element is no longer found, indicating that there are no further pages to scrape. At the end of this process, we have a list of all URLs containing quotes that need to be scraped.

## Webscraping Quote Information

Next, the program loops through the list of gathered URLs and proceeds to scrape each page for the quote text, the author's name, and the link to the author's biography. 
* Each quote is self-contained with an HTML element of the class `quote`. Using BeautifulSoup, we find all `quote` classes on the page, then dig in to that object to obtain the desired information.
* The text of the quote is within a child element of the `quote` class under a class called `text`. It can be obtained with the `get_text()` method.
* The author of the quote is within a child element of the `quote` class under a class called `author`. This can also be obtained with the `get_text()` method.
* Finally, the link to the author's bio is within a child anchor `<a>` element, which contains an `href` attribute with the URL. 
As each quote is scraped, the information is added to a growing list of all quotes. The end result is a list of sub-lists, which each sublist containing the text, author, and biography URL information. 

## Quote Guessing Game

Finally, this information is used to run a guessing game. The game logic proceeds as follows:
1. The `random` module is used to select a random quote from the list of all quotes assembled during the webscraping section. Once selected, that quote is removed from the list so that it is not re-used should the player decide to play again.
2. The text of the quote is presented to the player, who must `input` their guess of the author of the quote. The guess is not case-sensitive. 
3. If the player guesses incorrectly, they are notified as such as the game provides a hint in the form of the author's birthdate and birth place. This information is accessed from the quote that was selected in step **1**. The biography URL is used to make a new HTML request to that URL, and BeautifulSoup is then used to scrape the author birth date and birth location from that URL
* The author's birth date is contained within an element of the class `author-born-date`. The actual text can be obtained using the `get_text()` method.
* The author's birth location is contained within an element of the class `author-born-location`. The actual text can be obtained using the `get_text()` method.
The player is then asked to guess again.
4. If the player guesses incorrectly a second time, they are notified as such and the game provides a hint in the form of the author's *first* initial. This information is likewise accessed from the quote data that was selected in step **1**. The player is then asked to guess again.
5. If the player guesses incorrectly a third time, they are notified as such and the game provides a hint in the form of the author's *last* initial. This information is likewise accessed from the quote data that was selected in step **1**. The player is then asked to guess a final time.
6. If the player guesses incorrectly a fourth and final time, the game reveals the author of the quote and prompts the player if they would like to play again.
7. If the player guesses correctly at any point, they are congratulated and the game prompts the player if they would like to play again.

## Example of Losing Playthrough
![Lose](images/game_lost.png?raw=true)

## Example of Winning Playthrough
![Win](images/game_win.png?raw=true)
