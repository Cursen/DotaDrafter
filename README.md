# DotaDrafter

This is my Bachelors project, It's goal is to give predictions based on a monte carlo tree search(MCTS)
with a reward function being made by a Neural Network. It also gather data from real world matches 
for use in training.

with the exception of API/JSON all other technologies shown are my first interaction with them, this includes python.
It is designed to be used with live data, of which is gathered by scraping Dotabuff.com, and calling the Stratz Api.
This info is then stored in Firebase.

The Scraper, and StratzApi folders where originally hosted in a google cloud instance, which used cron tabs to call them
automatically. This is also why there are duplicates of the firebase object.

in terms of its success, the system itself was functional with the way it was setup, however improvements can
be made within the Neural Network, and MCTS solutions performance.

Note the key shown in this Git has its access revoked, and is there merely to show how the system is setup. Do not show
a active FirebaseKey to the public.

