# -*- coding: utf-8 -*-

from huggingface_hub import login
access_token_read = "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"
login(token = access_token_read)

#import numpy as np
from numpy import linalg
import random
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error
import torch

import pickle 
import json
from tqdm import tqdm

random.seed(7)
#np.random.seed(7)
torch.manual_seed(7)

import transformers
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

# CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 ./cuda_executable
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model = model.to(device)
pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_name, torch_dtype=torch.float16)

def prompt_for_manual_prediction(ex, shots):
    stop_signal = "\n\n"
    showcase_examples = [
            "Q: {}\nO: {} \nA: {}. The option is {}\n".format(
                 s["question"],s["options"],
                s["rationale"], s["correct"]) for s in shots
        ]




   


    input_example = "\nQ: {}\n O: {}\nA:".format(ex['question'], ex['options'])
    prompt = "\n".join(showcase_examples + [input_example])

    return prompt, stop_signal






def in_context_manual_prediction(ex, training_data):
    template,stop = prompt_for_manual_prediction(ex, training_data)

    messages=[{
                "role": "user",
                "content": "You are a helpful, respectful and honest assistant helping to solve math word problems or tasks requiring reasoning or math, use the Chain-of-Thought methodology by following given examples to explain your step-by-step calculations or logic.Do not generate examples in your answer",
            }]
    text={"role": "assistant", "content":""" Follow given examples and solve the Test Question at end in similar manner by decomposing the original questions
         Examples:{}""".format(template)}
    messages.append(text)


    prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipeline(prompt, max_new_tokens=200, do_sample=True, num_return_sequences=10, temperature=0.5, top_k=10, top_p=1.0)
        
    out_text = []
    for x in range(0, 10):
        out_text.append(outputs[x]["generated_text"])
    return out_text








#import faiss
from transformers import BertTokenizer, BertModel, logging
from sklearn.metrics.pairwise import cosine_similarity
import torch
import random
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import os
import json
import pickle
#import openai
#SSfrom tenacity import retry, stop_after_attempt, wait_random_exponential
import json


tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertModel.from_pretrained('bert-base-uncased')

logging.set_verbosity_error()


def mmr(doc_embeddings, query_embedding, lambda_param, top_k):
    """
    Maximal Marginal Relevance (MMR) function using Faiss.

    Parameters:
    - doc_embeddings: 2D array, each row represents the embedding of a document.
    - query_embedding: 1D array, the embedding of the query.
    - lambda_param: float, controls the trade-off between relevance and diversity.
    - top_k: int, the number of documents to return.

    Returns:
    - selected_indices: List of indices representing the selected documents.
    """

    # Normalize embeddings
    doc_embeddings = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # Number of documents
    num_docs = doc_embeddings.shape[0]
    

    # Create an index for Faiss
    index = faiss.IndexFlatIP(doc_embeddings.shape[1])

    index.add(doc_embeddings.astype(np.float32))

    # Query the index for similar documents
    _, similarity_indices = index.search(query_embedding.reshape(1, -1).astype(np.float32), top_k)

    # Compute relevance scores
    relevance_scores = np.dot(doc_embeddings, query_embedding)

    # Initialize selected set
    selected_set = set()

    # Add the most relevant document to the selected set
    max_relevance_index = np.argmax(relevance_scores)
    selected_set.add(max_relevance_index)

    # Compute MMR scores and select documents iteratively
    while len(selected_set) < top_k:
        remaining_indices = list(set(similarity_indices[0]) - selected_set)
        remaining_embeddings = doc_embeddings[remaining_indices]

        # Compute similarity with the query for remaining documents
        similarity_scores = np.dot(remaining_embeddings, query_embedding)

        # Compute MMR scores
        mmr_scores = lambda_param * relevance_scores[remaining_indices] - (1 - lambda_param) * similarity_scores

        # Select document with maximum MMR score
        max_mmr_index = remaining_indices[np.argmax(mmr_scores)]
        selected_set.add(max_mmr_index)

    # Convert selected set to a list of indices
    selected_indices = list(selected_set)

    return selected_indices




def self_con(tmp_list):
    ans_list = []
    for tmp in tmp_list:
        # tmp_list.append(compare_llm_outputs(user_query))
        # tmp = compare_llm_outputs(user_query)
        # print(tmp)
        ans = ""
        if len(tmp.split("The option is "))>6:
            ans = tmp.split("The option is ")[6][0]
            print(ans)
            # ans = ans.split("\n")[0]
        # ans = ans.replace("$", "")
        # ans = ans.strip()
        ans_list.append(ans)

    # print(ans_list)

    d = {}
    for i in ans_list:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    print(d)
    n = sorted(d.items(), key=lambda x:x[1], reverse=True)
    return n
    








def test_few_shot_manual_prediction():
    print("Running prediction")
    with open('dev.jsonl', 'r') as json_file1:
        json_list1 = list(json_file1)
    dev_set=[]


    for json_str in json_list1:
        result1 = json.loads(json_str)
        dev_set.append(result1)
    dev_set=dev_set[:2]


    with open('train.jsonl', 'r') as json_file:
        json_list = list(json_file)

    train_set=[]


    random.seed(7)


    for json_str in json_list:
        result = json.loads(json_str)
        train_set.append(result)
    train_set=train_set[:20]
    for i in train_set:
        inputs_sentence1 = tokenizer_bert(i["question"], return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs_sentence1 = model_bert(**inputs_sentence1)
        embedding_sentence1 = outputs_sentence1.last_hidden_state.mean(dim=1).numpy()[0]
        doc_embeddings.append(embedding_sentence1)

    
    print("started Running:")
    matches=0
    mismatches=0

    for ex in tqdm(dev_set,total=len(dev_set),desc="predicting"):
        #user_query,stop=prompt_for_manual_prediction(ex,new_rand_train)

        query = tokenizer_bert(ex['question'], return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs_sentence1 = model_bert(**query)
        query_embedding=outputs_sentence1.last_hidden_state.mean(dim=1).numpy()[0]

        # Set the lambda parameter (trade-off between relevance and diversity)
        lambda_param = 0.5

        # Set the number of documents to return
        top_k = 5

        # Apply MMR function
        selected_indices = mmr(doc_embeddings, query_embedding, lambda_param, top_k)
        print("selected indices:",selected_indices)
        train_set_1=[]
        for i in selected_indices:
          train_set_1.append(train_set[i])
        user_query,stop=prompt_for_manual_prediction(ex,train_set_1)

        tmp_list = in_context_manual_prediction(ex,train_set_1)
        # print(len(tmp_list))
        
        # n = self_con(tmp_list)
        # answer = n[0][0]
        # if answer=="" and len(n)>1: answer = n[1][0]
        ans=''
        if len(tmp_list[0].split("The option is "))>1:
            ans = tmp_list[0].split("The option is ")[1][0]
        answer=ans
        print("\nAnswer: ", answer)
        gt = ex["correct"]
        print("GT: ", gt)
        if(answer.strip().lower()==gt.strip().lower()):
          matches+=1
        else:
          mismatches+=1
    print("EM:",matches/(matches+mismatches))

test_few_shot_manual_prediction()