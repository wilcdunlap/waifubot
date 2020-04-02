# import requests for html parsing
import requests
# import randint for random number generation
from random import randint
# import Image for image processing
from PIL import Image
# import BytesIO for image pull
from io import BytesIO
# import codecs for decoding/encoding to handle japanese text
import codecs
# import facebook to actually post the post
import facebook
# import logging for future use
import logging

# download waifu page
# no longer necessary
#waifupage = "https://www.thiswaifudoesnotexist.net/"
#waifuresult = requests.get(waifupage)

# Here we assign a random integer as the waifu number
# There are only 100,000 images in the TWDNE database
waifu_number = randint(1, 100000)

# There are 125,000 text samples
text_number = randint(1, 125000)
# For testing
#text_number = 100
# Creating a unique random integer for both means more combinations
# With one random integer, we'll get a repost as a 1 in 100,000 generation
# With two, we'll get a report 1 in every 12,500,000,000 posts

# For testing, print number:
#print(waifu_number)

# Just for testing, we can set the number manually
#waifu_number = 96192
#text_number = 96192

# TWDNE website is very intuitive. Every image is stored as integer.jpg
# where integer is between 1 and 100,000
Waifu_Url = "https://www.thiswaifudoesnotexist.net/example-"+str(waifu_number)+".jpg"
print(Waifu_Url)

# Use the text_number for pulling text snippet
Text_Url = "https://www.thiswaifudoesnotexist.net/snippet-"+str(text_number)+".txt"
print(Text_Url)

# Here we use requests to get the text snippet
data = requests.get(Text_Url)
# Very important! Format the content of data as a string, with utf-8 encoding
# This ensures that the Japanese text looks good!
data2 = str(data.content, 'utf-8', errors='replace')

# Addendum for ellipses
# Next, we split the text into sentences, and store in a list
data3 = str(data2).replace('...', 'ELLIPSES').split('.')
# Print for spacing

#print(data3)

# New idea
# Take total length of the list
# Generate a random number of sentences, like 3-5
# create upper bound and lower bound so there's no overflow
# Max length - numsen for upper bound
# No lower bound?
# Then we just start off from there

Number_of_Sentences = randint(4,6)
#print("Number_of_Sentences")
#print(Number_of_Sentences)

# upper text bound is the total length of the list data3 (number of total sentences)
upper_text_bound = (len(data3) - Number_of_Sentences - 1)

# These were for testing only
#upper_text_bound = 3
print("upper_text_bound")
print(upper_text_bound)

# Lower bound is a random number between 1 and the upper text bound
# So if we want three sentences, it will start between the first the third to last
Lower_Bound = randint( 1, upper_text_bound)
print("Lower_Bound")
print(Lower_Bound)

# True upper bound is the actual upper bound of the text we're pulling
# So Lower bound is our start and true upper bound is the end
True_Upper_Bound = Lower_Bound + Number_of_Sentences
print("True_Upper_Bound")
print(True_Upper_Bound)


# Here, we create a blank string object known as data4
data4 = ""

# We have to create a function to easily append the sentences to the string

print('data 3 as a string')


# Now, each sentence is pulled from the data3 variable, given punctuation,
# and appended to the data4 string
for i in range(Lower_Bound,True_Upper_Bound):
	#data4 = "".join(str(data3[i]).replace( 'ELLIPSES' , '...'))
	data4 = data4+str(data3[i]+'.')
	#print(str((data3[i]))+'.')
	#data4.append(str((data3[i]))+'.')
	#print(str((data3[i],'.')).replace(' .','.'))


#print(data2)
# To fix the ellipses
#print('data4')
#print(data4)
#print(data4)
data4 = str(data4).replace( 'ELLIPSES' , '...' )
data5 = data4.encode('utf-8')
#print(data4)
#print(data3.split('.'))

# For future use: this person does not exist
PersonPage = "https://www.thispersondoesnotexist.com/image"
Personresult = requests.get(PersonPage, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})



file = requests.get(Waifu_Url)
#Commenting for april fools
img = Image.open(BytesIO(file.content))
#April fools: real life waifus
#img = (Image.open(BytesIO(Personresult.content)))
#img.show()
img.save('temp.jpg')
#token=""

def postToFacebook(token, message=data5):
	graph = facebook.GraphAPI(token)
	post_id = graph.put_photo(image = open('temp.jpg', 'rb'), message = message)["post_id"]
	print(f"Successfully posted {post_id} to facebook")

postToFacebook(token)
#print(data5)
print("testing", file=open("log.log", "a"))

