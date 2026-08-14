import markovify
import ezgmail
import os

#REBUILD GMAIL CREDENTIALS FROM GITHUB SECRETS
with open("credentials.json","w") as f:
    f.write(os.environ["GMAIL_CREDENTIALS"])
with open("token.json","w") as f:
    f.write(os.environ{"GMAIL_TOKEN"})

# READ THE QOTE FILE
with open("quotes.txt") as f:
    text = f.read()

# BUILD THE MARKOV MODEL
model = markovify.Text(text,state_size = 2)

## generate several candidates
candidates = []
for _ in range(15):
    sentence = model.make_sentence(tries=100)
    if sentence:
        word_count = len(sentence.split())
        words = sentence.split()
        no_repeats = len(words) == len(set(words))
        if 8 <= word_count <= 20 and no_repeats:
            candidates.append(sentence)

new_quote = candidates[0] if candidates else None

#Fallback in case markovify fails to generate a new quote
if new_quote is None:
    new_quote = "Keep pushing forward, that is how progress is made"

print(new_quote)

# Send the quote via email
ezgmail.send(
             "atharvverma1011@gmail.com, saumyaverma3107@gmail.com",
             "Today's Motivational Quote",
             new_quote
              )
