This project uses Twitter API to fetch live tweets about various cryptocurrencies, performs the sentimental analysis on those tweets ( using LSTM ) and then plots a graph showing how the sentiments vary every hour ( we can choose this time).

We have trained our LSTM model in the Model.ipynb notebook and saved it in the model_new.h5 file.

We are fetching live tweets in the Main.ipynb notebook using the Twitter API and then predicting their sentiment using the previously trained model. Then we are plotting the sentiment plots.

The Main.py is exactly same as the Main.ipynb notebook.

We are preprocessing the tweets using the twitter_preprocessor.py file, where we are converting the tweets into vectors which will serve as an input to our model.

We are cleaning the tweets using the sentence_cleaner.py file, where we are cleaning the input tweets.

We are saving the words to integer mappings ( or the word tokenizer ) in the tokenizer.pickle file.

We can check the tweets status in the debug.txt file, which prints a line after every 10 tweets.

-------------------------------------

The projects still contain a number of issues : 

1. The plot is not dynamic i.e. Whenever we get a new point for the plot, a new plot is drawn containing all the previous points.

2. We also have to set the axis of the plot.

3. The model still requires a lot of improvements. 

-------------------------------------

Future Plans :

I am thinking of making a dash app which contains a dropdown list showing the various cryptocurrenices. Also, the app will show the dynamic sentiment plot of the selected cryptocurrency from the dropdown list. I will be implementing this functionality whenever I get some free time.
