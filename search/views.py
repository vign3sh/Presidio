import requests
import json
import inflect
from django.shortcuts import render
from bs4 import BeautifulSoup
import os
import google.generativeai as palm
import textwrap
import numpy as np
import pandas as pd
from collections import defaultdict
from django.contrib import messages



def get_top_links(topic):
    # set up the request parameters
    params = {
    'api_key': '7651BC95CA874A77AD24AD12BC9F293E',
        'q': topic,
        'engine': 'google',
        'gl': 'us'
    }

    # make the http GET request to SerpWow
    api_result = requests.get('https://api.serpwow.com/search', params)

    # print the JSON response from SerpWow
    results=api_result.json()
    #results={'organic_results':[{'link': 'https://en.wikipedia.org/wiki/Superconductivity'}, {'link': 'https://en.wikipedia.org/wiki/Superconductor'}, {'link': 'https://en.wikipedia.org/wiki/High-temperature_superconductivity'}, {'link': 'https://en.wikipedia.org/wiki/Room-temperature_superconductor'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_magnet'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_wire'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_electric_machine'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_radio_frequency'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_levitation'}, {'link': 'https://en.wikipedia.org/wiki/Superconducting_electronics'}]}
    return results



def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body_content = soup.find("div", id="bodyContent")
    text_content=[]
    if not(body_content):
        body_content = soup.find("div", id="content")

    if not(body_content):
        body_content = soup.find("div", id="mainContent")

    if not(body_content):
        body_content = soup.find("div", id="main")

    if not(body_content):
        body_content = soup

    # Extract the text from the <p> elements
    texts = body_content.find_all('p')
    for text in texts:
        text_content.append(text.get_text(separator=""))
    return text_content






def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)
  return prompt

#Views start here
def index(request):
    context = {}
    return render(request, 'search/index.html', context)

def topic(request):
    if (request.method == 'POST'):
        topic = request.POST['topic']
        p = inflect.engine()
        if p.singular_noun(topic):
            topic=p.singular_noun(topic)
        
        results=get_top_links(topic)
        texts=[]

        for result in results['organic_results']:
            url = result['link']
            print(url)
            text = scrape_website(url)
            texts+=text
        
        
        context = {'texts': json.dumps(texts),
                   'topic': topic}
        
        messages.success(request, 'Please add atleast one question. It will take around 30 seconds to scrape and process the information.')
        return render(request, 'search/questions.html', context)
        


def questions(request):

    if (request.method == 'POST'):
        
        key=os.environ.get('PALM_API_KEY')
        texts = json.loads(request.POST['texts'])
        topic = request.POST['topic']
        questions = json.loads(request.POST['questions'])
        palm.configure(api_key=key)
        models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]

        model = models[0]

        # Get the embeddings of each text and add to an embeddings column in the dataframe
        def embed_fn(text):
            if len(text)>0:
                return palm.generate_embeddings(model=model, text=text)['embedding']
            return palm.generate_embeddings(model=model, text='None')['embedding']

        df = pd.DataFrame(texts)
        df.columns = ['Text']
        df['Embeddings'] = df['Text'].apply(embed_fn)

        text_models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        text_model = text_models[0]

        def find_best_passage(query, dataframe):
            """
            Compute the distances between the query and each document in the dataframe
            using the dot product.
            """
            query_embedding = palm.generate_embeddings(model=model, text=query)
            dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding['embedding'])
            
            idx = np.argmax(dot_products)
            return dataframe.iloc[idx]['Text']
        
   
        answers=defaultdict(list)
        for question in questions:

            query = question.replace("topic", topic)
            passage = find_best_passage(query, df)
            prompt = make_prompt(query, passage)

            temperature = 0.5
            answer = palm.generate_text(prompt=prompt,
                                        model=text_model,
                                        candidate_count=3,
                                        temperature=temperature,
                                        max_output_tokens=1000)

            for i, candidate in enumerate(answer.candidates):
                #print(f"Candidate {i}: {candidate['output']}\n")
                answers[question].append(candidate['output'])
        answers = dict(answers)
        
        #answers={'What is this?':['This is a superconductor.', 'It is a material that can conduct electricity without resistance', 'It is also diamagnetic, which means that it repels magnet'], 'What is the difference between a superconductor and a conductor?':['A superconductor has zero resistance to the flow of electricity, while a conductor has some resistance to the flow of electricity.', 'A superconductor has zero resistance to the flow of electricity, while a conductor has some resistance to the flow of electricity.', 'A superconductor has zero resistance to the flow of electricity, while a conductor has some resistance to the flow of electricity.'], 'What are the applications of superconductors?':['Superconductors are used in MRI machines, particle accelerators, and maglev trains.', 'Superconductors are used in MRI machines, particle accelerators, and maglev trains.', 'Superconductors are used in MRI machines, particle accelerators, and maglev trains.']}
        context = {'answers': answers}
        messages.success(request,'Each question has 3 different candidate answers. All are based on the best matched passage.')
        return render(request, 'search/answers.html', context)




    

            
           
        
        
        

        


    
    

