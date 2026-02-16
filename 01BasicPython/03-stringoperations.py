# The Thirsty Crow - A Classic Fable
## """ stands for holding string with multiple lines start and end with """
story = """Once upon a time, there was a thirsty crow flying across a barren and dry land.
The sun blazed mercilessly, and the crow's throat was parched with thirst.

After hours of flying, the crow spotted a pitcher lying on the ground.
With hope in his heart, he landed near it and peered inside.
There was water at the bottom, but the pitcher's neck was too narrow for the crow to reach it with his beak.

The crow tried again and again, but the water remained out of reach.
Just as despair was setting in, the crow noticed some pebbles scattered around.

An idea struck him! The crow began picking up pebbles one by one and dropping them into the pitcher.
With each pebble, the water level rose higher and higher.

Finally, after dropping many pebbles, the water rose high enough for the crow to reach it.
With great relief, the crow drank the fresh water and quenched his terrible thirst.

Moral: Little by little does the trick. With patience and perseverance, even the most difficult problems can be solved.
The crow learned that sometimes the best solutions come from clever thinking and persistent effort."""

# print(story)


# print("Length of the story is:", len(story)) #lengh of story
# print("Number of times 'crow' appears in the story:", story.count("crow")) #counting number of times crow appears in story
# print(f"crow found at index: {story.find('crow')}") #finding index of crow in story
# print("Is the story in uppercase?", story.isupper()) #checking if story is in uppercase
# print("Is the story in lowercase?", story.islower()) #checking if story is in lowercase
# print("Is the story title cased?", story.istitle()) #checking if story is title cased
# print("Does the story start with 'Once'?", story.startswith("Once")) #checking if
# print(f"{story.index('crow')} is the index of first occurrence of 'crow' in story") #finding index of crow in story using index method
# print(f"{story.find('crow')} is the index of first occurrence of 'crow' in story") #finding index of crow in story after index 50
# story = story.replace("crow", "raven") #replacing crow with raven in story, string is immutable so it will return new string with crow replaced by raven
# print(story)

# print(story.upper())
# print(story.lower())
# print(story.title())
# print(f"{story.split('crow')}") #splitting story into list of sentences using . as separator

words = story.split() #splitting story into list of words using space as separator
for word in words:
    print(word)