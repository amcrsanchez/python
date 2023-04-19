import json
import random

def getDictionary(jsonFile):
    with open(jsonFile) as file:
        return json.load(file)

def getCategories(dictionary):
    return dictionary.keys()

def categoryMenu(categories):
    print("Select a category:")
    for index, category in enumerate(categories):
        print("({}) - {}".format(index, category))

def getWordListByCategory(dictionary, category):
    return list(dictionary[category])

def replaceOccurrenceInGuessedWord(word, guessedWord, letter):
    index = 0
    while True:
        index = word.find(letter, index)
        if index == -1:
            break
        guessedWord[index] = letter
        index+=1

    return guessedWord

def main():
    dictionary = getDictionary('dictionary.json')
    categories = getCategories(dictionary)
    numberOfAttempts = 6

    while True:
        categoryMenu(categories)
        categoryInput = input()
        try:
            categoryInputInt = int(categoryInput)
            category = list(categories)[categoryInputInt]
            break
        except Exception:
            print("invalid option try again")


    print("You selected '{}' category let's guess the word! you have {} attempts...".format(category, numberOfAttempts))
    words = getWordListByCategory(dictionary, category)
    randomWord = words[random.randint(0, len(words) - 1)]
    guessedWord = []
    for i in range(len(randomWord)):
        guessedWord.append("_")
    attempt = numberOfAttempts
    
    print(" ".join(guessedWord))

    while(attempt > 0 and "_" in guessedWord):
        letter = input()
        if(len(letter) == 0):
            print("empty spaces are not allowed, try again.")
            continue

        firstLetter = letter[0].lower()

        if firstLetter not in randomWord:
            attempt-=1
            if(attempt == 0):
                print("Sorry, you did not guess it! the {} was {}".format(category, randomWord))
            else:
                print("This letter is not inside de word, try again, you have {} attempts remaining".format(attempt))
                print(" ".join(guessedWord))
            continue

        print("nice job! keep doing good")
        replaceOccurrenceInGuessedWord(randomWord, guessedWord, firstLetter)
        
        print(" ".join(guessedWord))
        if("_" not in guessedWord):
            print("you won! the word is: {}".format("".join(guessedWord)))
            break




if __name__ == "__main__":
    playAgain = True
    while playAgain:
        main()
        playAgain = input("\ndo you want to play again? y (yes) another key (no) ") == "y"
    print("Good bye!")
