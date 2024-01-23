# Presidio
This application accepts a topic as a string input from the user, searches the internet for information about it, and answers any questions.<br/>
<br/>Detailed steps of how this works:-
1. Input the word and use Serpwow API to get the links from the first page of Google search results. Scrapping Google results directly can result in the blocking of IP addresses.
2. Scrape the websites received from Serpwow API and store the data as a list of passages(paragraphs).
3. Take the questions from the user.
4. Tokenize the scraped data and questions using the embeddings from the PaLM API.
5. Find the best possible passage match to each question based on the dot product of their embeddings.
6. Send the passage and question to PaLM text generation models to find the possible answers to your query based on it.
7. Display the top 3 results for each question.
<br/>
<br/>
Requirements:-
<br/>
<br/>
1. API key for Serpwow. Gives 100 free searches.<br/>
2. PALM API access key. Request the free api key from the link mentioned in the top answer [here](https://www.googlecloudcommunity.com/gc/AI-ML/Google-Bard-API/m-p/538517)
<br/>
<br/>
The website is deployed [here](https://presidio.onrender.com/). This is a free deployement. It can timeout sometimes if there text for scraping is large.
<br/>
The sample video is [here](The Answer Machine.mp4)
