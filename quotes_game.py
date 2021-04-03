import requests
import random
from bs4 import BeautifulSoup

# This quote scraping game scrapes information from quotes.toscrape.com and then challenges the player to guess the person who said or wrote that quote.
# Written by Jason Gabunilas

# Get the response object from quotes.toscrape.com
response = requests.get("http://quotes.toscrape.com/")

# We will need to scrape quotes from every single page on this website, which may be updated in the future with more quotes. So let's first build a list of URLs that we will need to scrape from. Start by initializing a list with the base URL
URLs_to_scrape = ['http://quotes.toscrape.com/']

# Create a boolean that tracks whether there is another page of quotes to be scraped
next_page_exists = True
while next_page_exists:
        soup = BeautifulSoup(response.text, "html.parser")

        # Get the next page URL by searching for the "next" <li> class, if it exists.
        # If it does exist, drill down to get the href from the anchor tag
        if soup.find(class_ = "next"):
                next_page = soup.find(class_ = "next").find('a')['href']
                # Update the next_page variable to include the entire URL that will need to be visited next
                next_page_full = f"http://quotes.toscrape.com{next_page}"
                # Append the full URL to the list of URLs to scrape
                URLs_to_scrape.append(next_page_full)
                # Now update the response response so that the next cycle of the loop goes into the 
                response = requests.get(next_page_full)
        # If the "next" class does not exist on the current page, set next_page_exists to false to break the loop
        else:
                next_page_exists = False


# Create an empty list of quotes, authors, and bios to be populated with this information.
quotes_list = []

# Now that we have the URLs, let's work our way through them one by one
for page in URLs_to_scrape:
        response = requests.get(page)
        soup = BeautifulSoup(response.text, "html.parser")

        # Each self-contained quote is within a class called "text"
        all_quotes_on_page = soup.find_all(class_='quote')

        # For each quote, dig down into the text div to get the text of the quote
        for quote in all_quotes_on_page:
                quote_text = quote.find(class_='text').get_text()

                # The author is found within a class called "author", which is also within the quote class
                author = quote.select(".author")[0].get_text()

                # Finally, get the URL for the bio page. This is also within the quote lcass under an anchor tag
                bio_link = f"http://quotes.toscrape.com{quote.find('a')['href']}"

                # Store the information in a the quotes list, with each quote being a list of the quote, author, and bio link. This will be a list of lists.
                quotes_list.append([quote_text, author, bio_link])

# print(f"This list contains {len(quotes_list)} quotes.")

### The code below dictates the game logic

playing = True
while playing:

        # Select a random quote from the list of quotes, and then remove it from the list so that the player does not receive that same quote should he/she choose to play again
        quote = quotes_list.pop(random.randint(0, len(quotes_list)))
        # print(quote)

        # Initialize the number of guesses
        guesses_remaining = 4

        print("Welcome to Guess the Quote! Your goal is the guess the author of the following quote:")
        print(quote[0])
        guess = input(f"Who is the author of this quote?: ")

        if guess.lower() == quote[1].lower():
                print("Congratulations, you guessed correctly!")
        else:
                # Decrement the number of guesses
                guesses_remaining -= 1

                print(f"Sorry, you guessed incorrectly. You have {guesses_remaining} guess(es) remaining.")


                # If the player guesses incorrectly, go to the bio page and scrape the date and place of birth.
                response = requests.get(quote[2])
                soup = BeautifulSoup(response.text, "html.parser")
                birth_date = soup.find(class_ ="author-born-date").get_text()
                birth_loc = soup.find(class_="author-born-location").get_text()
                # print(birth_date, birth_loc)
                print(f"Here is a hint: this author was born on {birth_date} {birth_loc}")

                # Ask the user to guess again
                guess = input("Please guess again: ")
                if guess.lower() == quote[1].lower():
                        print("Congratulations, you guessed correctly!")
                        
                
                else:
                        # Decrement the number of guesses
                        guesses_remaining -= 1
                        print(f"Sorry, you guessed incorrectly. You have {guesses_remaining} guess(es) remaining.")


                        # Provide the author's first initial
                        print(f"Here is a hint: this author's first name starts with \"{quote[1].split(' ')[0][0]}\"")

                        # Ask the user to guess again
                        guess = input("Please guess again: ")
                        if guess.lower() == quote[1].lower():
                                print("Congratulations, you guessed correctly!")
                        
                        else: 
                                print(f"Sorry, you guessed incorrectly. You have {guesses_remaining} guess(es) remaining.")
                        
                                # Provide the author's last initial
                                print(f"Here is a hint: this author's last name starts with \"{quote[1].split(' ')[1][0]}\"")

                                # Ask the user to guess again
                                guess = input("Please make your final guess: ")
                                if guess.lower() == quote[1].lower():
                                        print("Congratulations, you guessed correctly!")
                                
                                else:
                                        print("Sorry, you have guessed incorrectly.")
                                        print(f"You have run out of guesses. The author of this quote is {quote[1]}.")

        # Create a loop for asking the player if they would like to play again.
        ask_to_play = True
        while ask_to_play:
                play_again = input("Would you like to play again? (y/n) ")
                if play_again == "y":
                        playing = True
                        ask_to_play = False
                elif play_again == "n":
                        print("Thanks for playing!")
                        playing = False
                        ask_to_play = False
                else: 
                        print("Invalid entry. Please enter \"y\" or \"n\". ")
        
