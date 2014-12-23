"""
SCRABBLE Game Program
Daniel Mockaitis
Dec 12, 2014

make it so i can tell you my letters and you tell me possible words
"""
def run_scrabble():
    make_space(5)
    print('Type the letter of what you want to do')
    print('quit ---> to end the program')
    print('a ---> See all the possible words in scrabble')
    print('b ---> Show the words with this many letters')
    print('c ---> Check if a word is legal')
    print('d ---> See all words starting with this letter or combo')
    print('e ---> See which words you can make using your letters')
    print('cheat ---> Show the words you can make from starting letter, ending letter, and length of word, or just one of these')
    command = input("Type the letter: ")
    assert type(command) == str 
    if command == 'a':
        print_words_in_scrabble()
    elif command == 'quit':
        make_space(4)
        exit()
    elif command == 'b':
        make_space(2)
        only_20_letters()
    elif command == 'c':
        make_space(2)
        is_legal()
    elif command == 'd':
        make_space(2)
        start_by_letter()
    elif command == 'e':
        make_space(2)
        use_my_letters()
    elif command == 'cheat':
        make_space(3)
        cheater()
    else:
        print("You didn't type a valid letter")
        run_scrabble()


def print_words_in_scrabble():
    for word in all_words_list():
        print(word)
    restart(print_words_in_scrabble)

def only_20_letters():
    command = input("Type a number to see the words with this many letters --> ")
    command = int(command)
    counter = 0
    make_space(2)
    for word in all_words_list():
        if len(word) == command:
            counter += 1
            print(word)
    print("There are",counter,"words with",command,"letters")
    restart(only_20_letters)
    

def all_words_list():
    fin = open('words.txt')
    words = []
    for line in fin:
        word = line.strip()
        words.append(word)
    return words

def all_words_dictionary():
    words = {}
    for word in all_words_list():
        words[word] = ''
    return words

def is_legal():
    word = str(input('Type the word you want to check '))
    assert type(word) == str
    word = word.lower()
    if word in all_words_dictionary():
        make_space(3)
        print(word, 'is valid')
    else:
        make_space(3)
        print(word, 'is not acceptable')
    restart(is_legal)

def start_by_letter():
    letter = input("Type the letter or letters you want: ")
    assert type(letter) == str
    letter = letter.lower()
    counter = 0
    length = len(letter)
    for word in all_words_list():
        if check_first_letters(word,letter):
            counter += 1
            print(word)
    if counter == 1:
        print("There is 1 word starting with'",letter,"'")
    else:
        print("There are", counter, "words starting with'",letter,"'")
    restart(start_by_letter)

def check_first_letters(word,letters):
    counter1,counter2 = 0, 0
    while counter1 < len(word) and counter2 < len(letters):
        if word[counter1] != letters[counter2]:
            return False
        counter1 += 1
        counter2 += 1
    return True

def use_my_letters():
    letters = []
    command = input('Type your letters with no spaces: ')
    counter = 0
    for x in command:
        letters.append(x)
    for word in all_words_list():
        if check_letters(word,letters):
            print(word)
            counter += 1
    print('You can make',counter,'different words using',command)
    restart(use_my_letters)

def cheater():
    print("Type the letters or letter your word must start with, or 'none' if it doesn't matter: ")
    first_letter = str(input('-->  '))
    print("Type the letters or letter your word must end with, or 'none' if it doesn't matter: ")
    last_letter = str(input('-->  '))
    print("Type the length of the word, or '0' if it doesn't matter:  ")
    length = str(input('-->  '))
    try: 
        int(length)
        length = int(length)
    except:
        print('You have to enter a number')
        restart(cheater)
    optional_letters = str(input("Type all the letters you have, or 'none' if it doesn't matter: "))
    counter = 0 
    if first_letter == 'none':
        first_letter = False
    else:
        first_letter = first_letter.lower()
    if last_letter == 'none':
        last_letter = False
    else:
        last_letter = last_letter.lower()
    if length == 0:
        length = False
    if optional_letters == 'none':
        optional_letters = False
    else:
        optional_letters = optional_letters.lower()
    make_space(1)
    print('Here is what we found')
    make_space(3)

    for word in all_words_list():
        if check_everything(word,first_letter,last_letter,length,optional_letters):
            print(word)
            counter += 1
    print('You have', counter,'options','of words with --',first_letter,'-- as the first letter')
    print('--',last_letter,'-- as the last letter --',length,'-- as the last letter --',optional_letters,'-- as other letters')
    restart(cheater)

def check_everything(word,first_letter,last_letter,length,optional_letters):
    if first_letter and not check_first_letters(word,first_letter):
        return False
    if last_letter and not check_last_letter(word,last_letter):
        return False
    if length and not check_length(word,length):
        return False
    if optional_letters and not check_letters(word,optional_letters):
        return False
    return True

def check_letters(word, letters):
    goal = len(word)
    counter = 0
    for letter in letters:
        if letter in word:
            counter += 1
    if counter >= goal or counter > 0:
        return True
    else:
        return False

def check_first_letter(word, letter):
    return word[0] == letter

def check_first_letters(word,letters):
    counter1,counter2 = 0, 0
    while counter1 < len(word) and counter2 < len(letters):
        if word[counter1] != letters[counter2]:
            return False
        counter1 += 1
        counter2 += 1
    return True

def check_last_letter(word, letters):
    counter1,counter2 = (len(word) - 1), (len(letters) - 1)
    while counter1 > 0 and counter2 > 0:
        if word[counter1] != letters[counter2]:
            return False
        counter1 -= 1
        counter2 -= 1
    return True

def check_length(word,num):
    return len(word) == num


def restart(func):
    make_space(8)
    print("To do this again press r")
    print("To use another program press any other key")
    print("To quit type --'quit' -- ")
    command = input('here ->')
    if command == 'quit':
        exit()
    elif command == 'r':
        make_space(4)
        func()
    elif command:
        make_space(4)
        run_scrabble()
    else:
        print('try again')
        restart(func)

def beginning():
    make_space(5)
    print("Scrabble Cheater created by Daniel Mockaitis")
    print("----------------------------------------------")
    print("Welcome to Scrabble Cheater press any key to begin")
    command = input('--->')
    if command:
        run_scrabble()
    else:
        print("Come on, just not 'enter'")
        make_space(4)
        beginning()

def make_space(num):
    for x in range(num):
        print()



beginning()










