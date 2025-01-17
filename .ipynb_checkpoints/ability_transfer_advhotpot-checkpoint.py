import numpy as np
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
#import openai
from tqdm import tqdm
#from tenacity import retry, stop_after_attempt, wait_random_exponential

from transformers import BertTokenizer, BertModel, logging
from langchain import PromptTemplate,  LLMChain

random.seed(7)
np.random.seed(7)
torch.manual_seed(7)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
    
# flan_model=flan_model.to(device)



#Llama2

from huggingface_hub import login
access_token_read = "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"
login(token = access_token_read)
# from transformers import BitsAndBytesConfig

# bnb_config = BitsAndBytesConfig(
# load_in_4bit=True,
# bnb_4bit_use_double_quant=True,
# bnb_4bit_quant_type="nf4",
# bnb_4bit_compute_dtype=torch.bfloat16
# )
# from huggingface_hub.hf_api import HfFolder
# from langchain import HuggingFacePipeline
# from transformers import AutoTokenizer
# from transformers import AutoModelForCausalLM
import transformers

# HfFolder.save_token("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")


# model_id = "meta-llama/Llama-2-7b-chat-hf"


# model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")

# tokenizer = AutoTokenizer.from_pretrained(model_id)



# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     torch_dtype=torch.bfloat16,
#     device_map="auto",
#     do_sample=True,
#     top_k=10,
#     num_return_sequences=1,
#     max_new_tokens=150,
#     eos_token_id=tokenizer.eos_token_id
# )

# llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0.5 })

# from langchain import PromptTemplate,  LLMChain








system_message = """The following is a conversation between a Human and an AI Assistant.
The assistant is helpful, respectful and honest, and it always answers as helpfully as possible, while being safe.
The Assistant's answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
Please ensure that the Assistant's responses are socially unbiased and positive in nature.
If a question by the human does not make any sense, or is not factually coherent, the Assistant should explain why instead of answering something not correct.
If the Assistant does not know the answer to a question, please don't share false information.
####

"""




#mistral
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "meta-llama/Llama-2-7b-chat-hf"

model = AutoModelForCausalLM.from_pretrained(model_name)
pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Replace with your API keys and endpoint URLs
#api_keys = ["<API_KEY_1>", "<API_KEY_2>", "<API_KEY_3>"]
#endpoint_urls = ["<ENDPOINT_URL_1>", "<ENDPOINT_URL_2>", "<ENDPOINT_URL_3>"]
#llm_names = ["LLM 1", "LLM 2", "LLM 3"]

# api_keys = ["EMPTY", "EMPTY", "EMPTY"]#, "EMPTY"]
# endpoint_urls = ["https://d06d-130-75-87-254.ngrok-free.app"]#"https://6069-130-75-87-254.ngrok-free.app"], "https://akdeniz27-llama-2-70b-chat-hf-with-easyllm.hf.space/"]
# llm_names = []

# for api_key, endpoint_url in zip(api_keys, endpoint_urls):
#     if 'hf.space' in endpoint_url:
#         model_name = endpoint_url.replace(sss'https://', '').replace('.hf.space', '').replace('/', '')
#     else:
#         openai.api_key = api_key
#         openai.api_base = f"{endpoint_url}/v1"
#         model_names = openai.Model.list()
#         model_name = model_names["data"][0]["id"]
#     llm_names.append(model_name)

# # Function to retrieve LLM outputs using the given API key and endpoint
# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
# def get_completion(prompt, api_key, endpoint_url, hard_code_exception=False):
#     # if new_sheet_name=='poem_properties':
#     #     if hard_code_exception==True:
#     #         max_tokens=128
#     #     else:
#     #         max_tokens=150
#     # else:

#     max_tokens=256
#     if 'hf.space' in endpoint_url:
#         client = Client(endpoint_url)
#         result = client.predict(
#                         prompt, # str in 'Message' Textbox component
#                         api_name="/chat"
#         )
#         return result.strip()
#     openai.api_key = api_key
#     openai.api_base = f"{endpoint_url}/v1"
#     model_names = openai.Model.list()
#     model_name = model_names["data"][0]["id"]

#     res = openai.Completion.create(
#         model=model_name,  # Replace with your model name
#         prompt=system_message + prompt,
#         # messages=[
#         #     {"role": "system", "content": system_message},
#         #     {"role": "user", "content": prompt},
#         # ],
#         temperature=0.9,
#         top_p=0.6,
#         max_tokens=max_tokens#200#256,
#     )
#     out_text = res['choices'][0]['text'].strip()
#     return out_text
#     # return res['choices'][0]['message']['content'].strip()



# def compare_llm_outputs(user_query, hard_code_exception=False):
#     results = [get_completion(user_query, api_keys[i], endpoint_urls[i], hard_code_exception=hard_code_exception) for i in range(len(endpoint_urls))]
#     return results


def prompt_for_manual_prediction(ex, shots):

    stop_signal = "\n\n"
    showcase_examples = [
            "Q: {}\nO: {} \nA: {}. The option is {}\n".format(
                 s["question"],s["options"],
                s["rationale"], s["correct"]) for index, s in shots.iterrows()
        ]




    # prompt = "\n".join(showcase_examples)
    # prompt=prompt+"\n\n{text}\n"


    input_example = "\nQ: {}\n O: {}\nA:".format(ex['question'], ex['options'])
    prompt = "\n".join(showcase_examples + [input_example])

    return prompt
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





def get_embeddings1(list1):
    doc_embeddings=[]
    

    for i in list1:
        inputs_sentence1 = tokenizer_bert(i, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs_sentence1 = model_bert(**inputs_sentence1)
        embedding_sentence1 = outputs_sentence1.last_hidden_state.mean(dim=1).numpy()
        embedding_sentence1=embedding_sentence1.tolist()
        doc_embeddings.append(embedding_sentence1[0])
    return doc_embeddings




def in_context_manual_prediction(ex, training_data):
    template = prompt_for_manual_prediction(ex, training_data)
#     sys="You are a helpful, respectful and honest assistant helping to solve math word problems or tasks requiring reasoning or math, use the Chain-of-Thought methodology by following given examples to explain your step-by-step calculations or logic.Do not generate examples in your answer"+"Follow given examples and solve the Test Question at end in similar manner by decomposing the original questions"
#     template=sys+"\n\n"+template
    
    
#     prompt = PromptTemplate(template=template, input_variables=["text"])
#     input_example = "\nQ: {}\n O: {}\nA:".format(ex['question'], ex['options'])
    
#     # prompt = pipeline.tokenizer.apply_chat_template(, tokenize=False, add_generation_prompt=True)
#     # outputs = pipeline(prompt, max_new_tokens=256, do_sample=True,num_return_sequences=2,temperature=0.3, top_k=10, top_p=0.95)

#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#     raw_llm_answer = llm_chain.run(input_example)
#     pred=raw_llm_answer
#     print(pred)
#     #print("template:",template)

    # outputs=compare_llm_outputs(template)
    # print("outputs:",outputs)
    # ans=outputs[0].split("The option is ")
    #print("ans:",ans)

#     prompt = PromptTemplate(template=template, input_variables=["text"])
#     input_example = "\nQ: {}\n O: {}\nA:".format(ex['question'], ex['options'])
#     #print("prompt:",template)

    messages=[{
                "role": "user",
                "content": "You are a helpful, respectful and honest assistant helping to solve math word problems or tasks requiring reasoning or math, use the Chain-of-Thought methodology by following given examples to explain your step-by-step calculations or logic.Do not generate examples in your answer",
            }]
    text={"role": "assistant", "content":""" Follow given examples and solve the Test Question at end in similar manner by decomposing the original questions
         Examples:{}""".format(template)}
    messages.append(text)
    #print(messages)
    # outputs=compare_llm_outputs(messages)
    # print("outputs:",outputs)
    # ans=outputs[0].split("The option is ")



    prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipeline(prompt, max_new_tokens=150, do_sample=True,num_return_sequences=1,temperature=0.3, top_k=10, top_p=0.95)

    # llm_chain = LLMChain(prompt=prompt, llm=llm)
    # raw_llm_answer = llm_chain.run(input_example)
    # pred=raw_llm_answer
    #print("outputs:",outputs)
    outputs=outputs[0]['generated_text']
    temp=outputs.split("The option is ")
    #print("temp:",temp)
    print("temp:",len(temp))

    if(len(temp)>6):
      #print("the option:",ans[1][0])
      return temp[6][0].strip()
    else:
      return ""
    #print("prediction:\n",outputs)


#     #return outputs[0]
















# def flan_generate(x):
#     inputs = flan_tokenizer(x, return_tensors="pt")
#     inputs = inputs.to(device)
#     #outputs = flan_model.generate(**inputs, max_new_tokens=144, do_sample=True, temperature=0.5)
#     outputs = flan_model.generate(**inputs, max_new_tokens=144)
#     return(flan_tokenizer.batch_decode(outputs, skip_special_tokens=True))

def safe_completion(prompt, max_tokens, stop, temp=0.0, logprobs=5): 
    print("\nprompt:", prompt)
    resp = flan_generate(prompt)
    print("resp: ", resp)   
    return resp

# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model_bert = BertModel.from_pretrained("bert-base-uncased", output_hidden_states = True,)
# model_bert.eval()


tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertModel.from_pretrained('bert-base-uncased')

logging.set_verbosity_error()

_MAX_TOKENS = 144
EP_STYLE_SEP = " The answer is"
EP_POSSIBLE_SEP_LIST = [
    " The answer is",
    " First, the answer is",
    " Second, the answer is",
    " Third, the answer is"
]
######################################################################################################

def read_AHOTPOT_test_data():
    data = pd.read_csv("dev.csv")
    return data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def read_AHOTPOT_train_data():
    data = pd.read_csv("train.csv")
    return data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FsbdSearch:
    def __init__(self,data=None, num_trees=None,emb_dim=None):
        self.num_trees=num_trees
        self.emb_dim=emb_dim
    def get_tokenized_input(self, data_ls):
        test_input_ids = []
        test_attention_masks = []
        for text in data_ls:
            encoded_dict = tokenizer.encode_plus(
                                text,                      # Sentence to encode.
                                add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                                max_length = 64,           # Pad & truncate all sentences.
                                pad_to_max_length = True,
                                truncation=True,
                                return_attention_mask = True,   # Construct attn. masks.
                                return_tensors = 'pt',     # Return pytorch tensors.
                        )
            
        # Add the encoded sentence to the list.    
            test_input_ids.append(encoded_dict['input_ids'])
        
        # And its attention mask (simply differentiates padding from non-padding).
            test_attention_masks.append(encoded_dict['attention_mask'])

        # Convert the lists into tensors.
        test_input_ids = torch.cat(test_input_ids, dim=0)
        test_attention_masks = torch.cat(test_attention_masks, dim=0)
        #print(test_input_ids.shape)

        return test_input_ids, test_attention_masks
    def get_embeddings_for_data(self, data_ls):
        input_ids, attention_masks = self.get_tokenized_input(data_ls)
        with torch.no_grad():
            embeddings = model_bert(input_ids, attention_masks)
        embeddings = embeddings.hidden_states[-1]
        # Mean across dim=1
        embeddings = torch.mean(embeddings, dim=1)
        #print(embeddings.shape)
        return embeddings
    
    def calculate_feature_statistics(self, feats):
        """Calculation of the statistics used by the FID.
        Params:
        -- feats       : tensor of features with the shape [N, D]
        Returns:
        -- mu    : The mean over samples of the activations of the pool_3 layer of
                the inception model.
        -- sigma : The covariance matrix of the activations of the pool_3 layer of
                the inception model.
        """
        mu = np.mean(feats, axis=0)
        sigma = np.cov(feats, rowvar=False)
        return mu, sigma

    def calculate_frechet_distance(self, mu1, sigma1, mu2, sigma2, eps=1e-6):
        """Numpy implementation of the Frechet Distance.
        The Frechet distance between two multivariate Gaussians X_1 ~ N(mu_1, C_1)
        and X_2 ~ N(mu_2, C_2) is
                d^2 = ||mu_1 - mu_2||^2 + Tr(C_1 + C_2 - 2*sqrt(C_1*C_2)).
        Stable version by Dougal J. Sutherland.
        Params:
        -- mu1   : Numpy array containing the activations of a layer of the
                inception net (like returned by the function 'get_predictions')
                for generated samples.
        -- mu2   : The sample mean over activations, precalculated on an
                representative data set.
        -- sigma1: The covariance matrix over activations for generated samples.
        -- sigma2: The covariance matrix over activations, precalculated on an
                representative data set.
        Returns:
        --   : The Frechet Distance.
        """

        mu1 = np.atleast_1d(mu1)
        mu2 = np.atleast_1d(mu2)

        sigma1 = np.atleast_2d(sigma1)
        sigma2 = np.atleast_2d(sigma2)

        assert mu1.shape == mu2.shape, \
            'Training and test mean vectors have different lengths'
        assert sigma1.shape == sigma2.shape, \
            'Training and test covariances have different dimensions'

        diff = mu1 - mu2

        # Product might be almost singular
        covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
        if not np.isfinite(covmean).all():
            msg = ('fid calculation produces singular product; '
                'adding %s to diagonal of cov estimates') % eps
            print(msg)
            offset = np.eye(sigma1.shape[0]) * eps
            covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

        # Numerical error might give slight imaginary component
        if np.iscomplexobj(covmean):
            if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
                m = np.max(np.abs(covmean.imag))
                raise ValueError('Imaginary component {}'.format(m))
            covmean = covmean.real

        tr_covmean = np.trace(covmean)

        return (diff.dot(diff) + np.trace(sigma1)
                + np.trace(sigma2) - 2 * tr_covmean)
    def get_top_n_neighbours(self,sentence,data_emb,transfer_data,k):
        sent_emb = self.get_embeddings_for_data([sentence]).squeeze()
        #data_emb = self.get_embeddings_for_data(transfer_questions)
        print("new_emb", sent_emb.squeeze().shape, data_emb.shape)
        distances = []
        for index, emb in enumerate(data_emb):
            source_stats_mu, source_stats_sigma = self.calculate_feature_statistics(emb.numpy())
            target_stats_mu, target_stats_sigma = self.calculate_feature_statistics(sent_emb.numpy())
            distance = self.calculate_frechet_distance(source_stats_mu,source_stats_sigma,target_stats_mu,target_stats_sigma)
            distances.append(distance)
        #text_sims = cosine_similarity(data_emb,[sent_emb]).tolist()
        results_sims = zip(range(len(distances)), distances)
        sorted_similarities = sorted(results_sims, key=lambda x: x[1], reverse=False)
        #print("text_sims",sorted_similarities[:2])
        top_questions = []
        for idx, item in sorted_similarities[:k]:
            top_questions.append(transfer_data[idx])
        return top_questions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_sep_text(chain_answer):
    for sep in EP_POSSIBLE_SEP_LIST:
        if sep in chain_answer:
            return sep
    return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convert_paragraphs_to_context(s, connction="\n"):
    return " ".join(eval(s['pars']))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



def MAPE(Y_actual,Y_Predicted):
    mape = np.mean(np.abs((Y_actual - Y_Predicted)/Y_actual))*100
    return mape
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def LLM_avg_error(exemplars_set, val_data):
    stop_signal = "\n\n"
    error=[]
    # increment error if model predicted answer is not equal to the ground truth answer for the test question by passing the exemplars
    for exemplars in tqdm(exemplars_set,total=len(exemplars_set),desc="predicting"):
        matches = 0
        mismatches =0
        acc_records = []
        for index, row in val_data.iterrows():
            #prompt = prompt_for_manual_prediction(row, exemplars)
            #chain_answer = safe_completion(prompt=prompt, max_tokens=_MAX_TOKENS, stop=stop_signal, temp=0.0, logprobs=5)

            # outputs=compare_llm_outputs(prompt)
            # ans=outputs[0].split("The option is ")
            answer=in_context_manual_prediction(row,exemplars)


    #         if(len(ans)>1):
    #   #print("the option:",ans[1][0])
    #             answer= ans[1][0].strip()
    #         else:
    #             answer=""
            # chain_answer = chain_answer[0]

            # text = chain_answer
            # text = text.strip()

            # # place holder
            # answer = "null"
            # rationale = "null"

            # sep = get_sep_text(chain_answer)
            # if sep is not None:
            #     segments = text.split(sep)
            #     answer = segments[1].strip().strip('.')
            #     rationale = segments[0].strip()
            # else:
            #     answer = text

            ground_truth = row["correct"]

            print("\nanswer:",answer)
            print("ground_truth:",ground_truth)

            if answer==ground_truth:
                matches+=1
            else:
                mismatches+=1

        error.append(mismatches/(matches+mismatches))

        #     acc, (f1, pre, rec), gt_ans = hotpot_evaluation_with_multi_answers(answer, row["answer_choices"])
        #     acc_records.append(acc)

        # mean_of_array = lambda x: sum(x) / len(x)
        # acc = mean_of_array(acc_records)
        # loss = (1 - acc)

        # print("acc ",acc)
        # print("loss ",loss)

        # error.append(loss)

    return error
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def LLM_error_indicator(exemplars_set, val_data):
    stop_signal = "\n\n"
    error=[]
    # increment error if model predicted answer is not equal to the ground truth answer for the test question by passing the exemplars
    for exemplars in tqdm(exemplars_set,total=len(exemplars_set),desc="predicting"):
        for index, row in val_data.iterrows():
            #print("exemplars:",exemplars)
            #print("row:",row)
    #         prompt = prompt_for_manual_prediction(row, exemplars)
    #         #chain_answer = safe_completion(prompt=prompt, max_tokens=_MAX_TOKENS, stop=stop_signal, temp=0.0, logprobs=5)
    #         outputs=compare_llm_outputs(prompt)
    #         ans=outputs[0].split("The option is ")


    #         if(len(ans)>1):
    #   #print("the option:",ans[1][0])
    #             answer= ans[1][0].strip()
    #         else:
    #             answer=""

            answer=in_context_manual_prediction(row,exemplars)


            # chain_answer = chain_answer[0]

            # text = chain_answer
            # text = text.strip()

            # # place holder
            # answer = "null"
            # rationale = "null"

            # sep = get_sep_text(chain_answer)
            # if sep is not None:
            #     segments = text.split(sep)
            #     answer = segments[1].strip().strip('.')
            #     rationale = segments[0].strip()
            # else:
            #     answer = text

            ground_truth = row["correct"]

            print("\nanswer:",answer)
            print("ground_truth:",ground_truth)

            if answer==ground_truth:
                loss=0
            else:
                loss=1

            error.append(loss)

            # acc, (f1, pre, rec), gt_ans = hotpot_evaluation_with_multi_answers(answer, row["answer_choices"])
            # loss = (1-acc)

            # print("acc ",acc)
            # print("loss ",loss)

            # error.append(loss)

    return error
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def static_subset_selection(val_data, train_data, k, test_data):

    #test_data = test_data[:15]
    val_data = val_data[:20]
    # val_data=20, k=5, L=100, U=10, V=5, L-U=90
    
    knn_instance = FsbdSearch()
    print("checkpoint-1:")


    dbfile1 = open('val_emb.pkl', 'rb')    
    val_emb = pickle.load(dbfile1)



    #dbfile2 = open('test_emb.pkl', 'rb')    
    #test_emb = pickle.load(dbfile2)


    dbfile3 = open('transfer_emb.pkl', 'rb')    
    transfer_emb = pickle.load(dbfile3)

    #Calculate embeddings for all validation questions
    # val_emb = get_embeddings1(val_data["question"].tolist())
    # with open("val_emb.pkl", 'wb') as f:
    #         pickle.dump(val_emb, f)
    
    # print("1-done")
    # test_emb = get_embeddings1(test_data["question"].tolist())
    # with open("test_emb.pkl", 'wb') as f:
    #         pickle.dump(test_emb, f)

    # print("2-done")
    # transfer_emb = get_embeddings1(train_data["question"].tolist())
    # with open("transfer_emb.pkl", 'wb') as f:
    #         pickle.dump(transfer_emb, f)
    # print("3-done")


    # k-means clustering on train_data with k=5
    kmeans = KMeans(n_clusters=5, random_state=0).fit(transfer_emb)
    #print(kmeans.labels_)
    # Make clusters of train_data with same cluster label
    train_data['cluster'] = kmeans.labels_

    # # Do stratified sampling from train_data based on the first word of the question
    # train_data['w1'] = train_data['question'].str.split().str[0]

    # Create index column in train_data using arange
    train_data['index'] = np.arange(len(train_data))

    # Create L=_ subsets of size k total, with each group having k/num_gr examples
    num_gr = len(train_data['cluster'].unique())
    L = []
    L_indices = []

    # Initialize L, 40 random set of subsets from train_data 
    for i in range(100):
        subset = []
        for name, group in train_data.groupby('cluster'):
            # subset.append(group.sample(k//num_gr))   
            subset.append(group.sample(1))   
        subsets = pd.concat(subset)
        L.append(subsets)
        L_indices.append(subsets['index'].tolist())


    # Initialize U, 10 random set of subsets from L 
    ind_L = np.arange(0,len(L)).tolist()
    
    ind_total = random.sample(ind_L, 15)
    ind_U = ind_total[:10]
    ind_V = ind_total[10:]

    ind_L_minus_U = [x for x in ind_L if x not in ind_U]    

    U = []
    for i in ind_U:
        U.append(L[i])
    V = []
    for i in ind_V:
        V.append(L[i])
        
    L_minus_U = []
    for i in ind_L_minus_U:
        L_minus_U.append(L[i])

    print("check-point-2:")
    
    # Calculate the similarity matrix, Eij = cosine similarity between exemplar x_i=train_data and test example u_j=val_data
    E_val = cosine_similarity(transfer_emb, val_emb)
    #E_test = cosine_similarity(transfer_emb, test_emb)

    # Calculate Loss(Y,S) for all S in U
    LLM_loss = LLM_error_indicator(U, val_data)
    #LLM_loss_on_test_data = LLM_error_indicator(U, test_data)
    LLM_loss_on_L_minus_U = LLM_error_indicator(L_minus_U, val_data)
    LLM_loss_on_V = LLM_error_indicator(V, val_data)
    print("check-point-3:")
    


    approx_error_on_U = []
    approx_error_on_U_after_update = []
    approx_error_on_L_minus_U = []
    approx_error_on_L_minus_U_after_update = []
    approx_error_on_V = []
    approx_error_on_V_after_update = []
    
    # approx_error_on_U_on_test_data = []
    # approx_error_on_U_after_update_on_test_data = []
    # approx_error_on_L_minus_U_on_test_data = []
    # approx_error_on_L_minus_U_after_update_on_test_data = []
    # approx_error_on_V_on_test_data = []
    # approx_error_on_V_after_update_on_test_data = []

    approx_value_on_U = []
    approx_value_on_U_after_update = []
    approx_value_on_L_minus_U = []
    approx_value_on_L_minus_U_after_update = []
    approx_value_on_V = []
    approx_value_on_V_after_update = []
    
    # approx_value_on_U_on_test_data = []
    # approx_value_on_U_after_update_on_test_data = []
    # approx_value_on_L_minus_U_on_test_data = []
    # approx_value_on_L_minus_U_after_update_on_test_data = []
    # approx_value_on_V_on_test_data = []
    # approx_value_on_V_after_update_on_test_data = []

    LLM_loss_on_val = []
    avg_LLM_loss_on_val = []
    min_LLM_loss_on_val = []
    max_LLM_loss_on_val = []
    LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss, (len(U),-1))
    LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
    LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
    avg_LLM_loss_on_val.append(LLM_loss_on_val_avg.tolist()) 
    min_LLM_loss_on_val.append(LLM_loss_on_val_min.tolist())
    max_LLM_loss_on_val.append(LLM_loss_on_val_max.tolist())
    print("\n********* LLM LOSS ON U FOR VALIDATION DATA *********")
    print("\nLLM_loss_on_val ",LLM_loss_on_val)
    print("AVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_val)
    print("MIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_val)
    print("MAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_val)
    #===============================================================================



    #LLM_loss_on_test = []
    avg_LLM_loss = []
    min_LLM_loss = []
    max_LLM_loss = []
    # LLM_loss_for_each_subset = np.reshape(LLM_loss_on_test_data, (len(U),-1))
    # LLM_loss_for_each_subset = np.average(LLM_loss_for_each_subset, axis=1)
    # LLM_loss_avg = np.average(LLM_loss_for_each_subset)
    # LLM_loss_min = np.min(LLM_loss_for_each_subset)
    # LLM_loss_max = np.max(LLM_loss_for_each_subset)
    # #LLM_loss_on_test.append(LLM_loss_for_each_subset.tolist())
    # avg_LLM_loss.append(LLM_loss_avg.tolist()) 
    # min_LLM_loss.append(LLM_loss_min.tolist())
    # max_LLM_loss.append(LLM_loss_max.tolist())
    # print("\n********* LLM LOSS ON U FOR TEST DATA *********")
    # print("\nLLM_loss_on_test ",LLM_loss_on_test)
    # print("AVG_LLM_loss_on_TEST_data ",avg_LLM_loss)
    # print("MIN_LLM_loss_on_TEST_data ",min_LLM_loss)
    # print("MAX_LLM_loss_on_TEST_data ",max_LLM_loss)
    #===============================================================================

   

    LLM_loss_on_L_minus_U_on_val = []
    avg_LLM_loss_on_L_minus_U_on_val = []
    min_LLM_loss_on_L_minus_U_on_val = []
    max_LLM_loss_on_L_minus_U_on_val = []
    LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss_on_L_minus_U, (len(L_minus_U),-1))
    LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
    LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
    avg_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_avg.tolist()) 
    min_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_min.tolist())
    max_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_max.tolist())
    print("\n********* LLM LOSS ON L_minus_U FOR VALIDATION DATA *********")
    print("\nLLM_loss_on_val ",LLM_loss_on_L_minus_U_on_val)
    print("AVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_L_minus_U_on_val)
    print("MIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_L_minus_U_on_val)
    print("MAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_L_minus_U_on_val)
    #===============================================================================

    # LLM_loss_on_L_minus_U_on_test_data = LLM_error_indicator(L_minus_U, test_data)
    # LLM_loss_on_L_minus_U_on_test = []
    # avg_LLM_loss_on_L_minus_U = []
    # min_LLM_loss_on_L_minus_U = []
    # max_LLM_loss_on_L_minus_U = []
    # LLM_loss_for_each_subset = np.reshape(LLM_loss_on_L_minus_U_on_test_data, (len(L_minus_U),-1))
    # LLM_loss_for_each_subset = np.average(LLM_loss_for_each_subset, axis=1)
    # LLM_loss_avg = np.average(LLM_loss_for_each_subset)
    # LLM_loss_min = np.min(LLM_loss_for_each_subset)
    # LLM_loss_max = np.max(LLM_loss_for_each_subset)
    # LLM_loss_on_L_minus_U_on_test.append(LLM_loss_for_each_subset.tolist())
    # avg_LLM_loss_on_L_minus_U.append(LLM_loss_avg.tolist()) 
    # min_LLM_loss_on_L_minus_U.append(LLM_loss_min.tolist())
    # max_LLM_loss_on_L_minus_U.append(LLM_loss_max.tolist())
    # print("\n********* LLM LOSS ON L_minus_U FOR TEST DATA *********")
    # print("\nLLM_loss_on_test ",LLM_loss_on_L_minus_U_on_test)
    # print("AVG_LLM_loss_on_TEST_data ",avg_LLM_loss_on_L_minus_U)
    # print("MIN_LLM_loss_on_TEST_data ",min_LLM_loss_on_L_minus_U)
    # print("MAX_LLM_loss_on_TEST_data ",max_LLM_loss_on_L_minus_U)
    #===============================================================================


    LLM_loss_on_V_on_val = []
    avg_LLM_loss_on_V_on_val = []
    min_LLM_loss_on_V_on_val = []
    max_LLM_loss_on_V_on_val = []
    LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss_on_V, (len(V),-1))
    LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
    LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
    LLM_loss_on_V_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
    avg_LLM_loss_on_V_on_val.append(LLM_loss_on_val_avg.tolist()) 
    min_LLM_loss_on_V_on_val.append(LLM_loss_on_val_min.tolist())
    max_LLM_loss_on_V_on_val.append(LLM_loss_on_val_max.tolist())
    print("\n********* LLM LOSS ON V FOR VALIDATION DATA *********")
    print("\nLLM_loss_on_val ",LLM_loss_on_V_on_val)
    print("AVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_V_on_val)
    print("MIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_V_on_val)
    print("MAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_V_on_val)


    #===============================================================================
    # Calculate the pairwise overlap between the subsets in U
    overlaps=[]
    for i in range(len(U)):
        inner_overlaps=[]
        for j in range(len(U)):
            if i!=j:
                overlap=0
                for index_j, s_i in U[i].iterrows():
                    for index_j, s_j in U[j].iterrows():
                        if s_i["question"].lower() in s_j["question"].lower() or s_j["question"].lower() in s_i["question"].lower():
                            overlap+=1
                inner_overlaps.append(overlap)
        overlaps.append(inner_overlaps)
            
    print("\noverlaps ",overlaps)
    print("len overlaps ",len(overlaps))

    overlap_for_subset = []
    avg_overlap = []
    min_overlap = []
    max_overlap = []
    overlap_for_each_subset = np.average(overlaps, axis=1)
    overlap_avg = np.average(overlap_for_each_subset)
    overlap_min = np.min(overlap_for_each_subset)
    overlap_max = np.max(overlap_for_each_subset)
    overlap_for_subset.append(overlap_for_each_subset.tolist())
    avg_overlap.append(overlap_avg.tolist()) 
    min_overlap.append(overlap_min.tolist())
    max_overlap.append(overlap_max.tolist())
    print("\n********* PAIRWISE OVERLAP *********")
    print("\noverlap_for_subset ",overlap_for_subset)
    print("\nAVG_overlap ",avg_overlap)
    print("MIN_overlap ",min_overlap)
    print("MAX_overlap ",max_overlap)
    #===============================================================================








    ################################################################################
    # Storing the indices of the subsets in U_t
    U_indices = []
    for i in range(len(U)):
        U_indices.append(U[i]['index'].tolist())

    V_indices = []
    for i in range(len(V)):
        V_indices.append(V[i]['index'].tolist())

    L_minus_U_indices = []
    for i in range(len(L_minus_U)):
        L_minus_U_indices.append(L_minus_U[i]['index'].tolist())


    ################################################################################
    # fill W = E_{ij} for all i in U_t
    l = len(U)
    W_val = np.zeros((l*len(val_emb), len(transfer_emb)))
    #W_test = np.zeros((l*len(test_emb), len(transfer_emb)))
    for u in range(l):
        for i in range(len(transfer_emb)):
            if i in U_indices[u]:
                W_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                #W_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]


    ################################################################################
    # fill V = E_{ij} for all i in V_t
    v = len(V)
    V_val = np.zeros((v*len(val_emb), len(transfer_emb)))
    #V_test = np.zeros((v*len(test_emb), len(transfer_emb)))
    for u in range(v):
        for i in range(len(transfer_emb)):
            if i in V_indices[u]:
                V_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                #V_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]



    ##############################################################################
    # make X = E_{ij} for all i in L-U_t 
    L_minus_U_len = len(L)-len(U)
    X_val = np.zeros((L_minus_U_len*len(val_emb), len(transfer_emb)))
    # X_test = np.zeros((L_minus_U_len*len(test_emb), len(transfer_emb)))
    for u in range(L_minus_U_len):
        for i in range(len(transfer_emb)):
            if i in L_minus_U_indices[u]:
                X_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                # X_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]








    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! WHILE LOOP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    t=0
    while t<10:

        ################################################################################
        # min_alpha_i (LLM_loss-W*alpha)^2
        #alpha = np.linalg.lstsq(W_val, LLM_loss, rcond=None)[0]
        # increase rows of llm loss by appending llm loss of V
        # increase rows of W by appending V
 
        LLM_loss_on_U_V = LLM_loss + LLM_loss_on_V
        W_V_val = np.concatenate((W_val, V_val), axis=0)

        print("\n LLM_loss_on_U_V_len",len(LLM_loss_on_U_V))
        print("\n LLM_loss_on_U_V ",LLM_loss_on_U_V)
        print("\n W_V_val_shape ",W_V_val.shape)
        print("\n W_V_val ",W_V_val)

        alpha = np.linalg.lstsq(W_V_val, LLM_loss_on_U_V, rcond=None)[0]
        # Print alpha

        print("\nalpha shape ",alpha.shape)
        print("\nalpha ",alpha)



        ################################################################################
        # Calculate the worst subset S_worst ∈ U_t that maximizes the approximate loss
        mul1 = np.matmul(W_val, alpha)
        mul_new1 = np.reshape(mul1, (len(U),-1))
        S_worst_ind = np.argmax(np.sum(mul_new1, axis=1))
        S_worst = U[S_worst_ind]

        ##############################################################################
        #mul1_test = np.matmul(W_test, alpha)

        ###############################################################################
        # Calculate the top set S_star ∈ L \ U_t that minimizes the approximate loss
        mul2 = np.matmul(X_val, alpha)
        mul_new2 = np.reshape(mul2, (L_minus_U_len,-1))
        S_star_ind = np.argmin(np.sum(mul_new2, axis=1))
        S_star = L_minus_U[S_star_ind]

        ###############################################################################
        mul3 = np.matmul(V_val, alpha)

        ###############################################################################

        
        #********* APPROX VALUE ON U ON VALIDATION DATA *********
        approx_value_on_U_for_each_subset = np.reshape(mul1, (len(U),-1))
        approx_value_on_U_for_each_subset = np.average(approx_value_on_U_for_each_subset, axis=1)
        approx_value_on_U.append(approx_value_on_U_for_each_subset.tolist())


        #********* APPROX VALUE ON U ON TEST DATA *********
        # approx_value_on_U_on_test_for_each_subset = np.reshape(mul1_test, (-1,len(test_data)))
        # approx_value_on_U_on_test_for_each_subset = np.average(approx_value_on_U_on_test_for_each_subset, axis=1)
        # approx_value_on_U_on_test_data.append(approx_value_on_U_on_test_for_each_subset.tolist())


        #********* APPROX VALUE ON L-U ON VALIDATION DATA *********
        approx_value_on_L_minus_U_for_each_subset = np.reshape(mul2, (-1,len(val_data)))
        approx_value_on_L_minus_U_for_each_subset = np.average(approx_value_on_L_minus_U_for_each_subset, axis=1)
        approx_value_on_L_minus_U.append(approx_value_on_L_minus_U_for_each_subset.tolist())

        #********* APPROX VALUE ON V ON VALIDATION DATA *********
        approx_value_on_V_for_each_subset = np.reshape(mul3, (-1,len(val_data)))
        approx_value_on_V_for_each_subset = np.average(approx_value_on_V_for_each_subset, axis=1)
        approx_value_on_V.append(approx_value_on_V_for_each_subset.tolist())


        #calculate the approximate error = (LLM_loss-W*alpha) on U
        print("\n*************Approximation error of Validation Data on U ************")
        print("\nLLM Loss ",LLM_loss) 
        print("\napproximation \n",mul1)
        # mape = MAPE(np.array(LLM_loss), mul1)
        # approx_error_on_U.append(mape.tolist())
        # print("\napprox error on U ",approx_error_on_U)
        error1 = np.abs(np.array(LLM_loss) - mul1)
        error1 = np.reshape(error1, (-1,len(val_data)))
        error1 = np.mean(error1, axis=1)
        approx_error_on_U.append(error1.tolist())
        print("\napprox error on U on val data ",approx_error_on_U) 


        # print("\n*************Approximation error of Test Data on U ************")
        # print("\nLLM Loss ",LLM_loss_on_test_data) 
        # print("\napproximation \n",mul1_test)
        # error1 = np.abs(np.array(LLM_loss_on_test_data) - mul1_test)
        # error1 = np.reshape(error1, (-1,len(test_data)))
        # error1 = np.mean(error1, axis=1)
        # approx_error_on_U_on_test_data.append(error1.tolist())
        # print("\napprox error on U on test data ",approx_error_on_U_on_test_data) 


        #calculate the approximate error = (LLM_loss_on_L_minus_U - X*alpha) on L_minus_U
        print("\n*************Approximation error of Validation Data on L_minus_U ************")
        print("\nLLM Loss on L_minus_U ",LLM_loss_on_L_minus_U)
        print("\napproximation \n",mul2)
        error2 = np.abs(np.array(LLM_loss_on_L_minus_U) - mul2)
        error2 = np.reshape(error2, (-1,len(val_data)))
        error2 = np.mean(error2, axis=1)
        approx_error_on_L_minus_U.append(error2.tolist())
        print("\napprox error on L_minus_U on Val data ",approx_error_on_L_minus_U) 


        # print("\n*************Approximation error of Test Data on L_minus_U ************")
        # print("LLM Loss on L_minus_U ",LLM_loss_on_L_minus_U_on_test_data)
        # mul2_test = np.matmul(X_test, alpha)     
        # print("\napproximation \n",mul2_test)
        # error2 = np.abs(np.array(LLM_loss_on_L_minus_U_on_test_data) - mul2_test)
        # error2 = np.reshape(error2, (-1,len(test_data)))
        # error2 = np.mean(error2, axis=1)
        # approx_error_on_L_minus_U_on_test_data.append(error2.tolist())
        # print("\napprox error on L_minus_U on test data ",approx_error_on_L_minus_U_on_test_data) 
        
        print("\n*************Approximation error of Validation Data on V ************")
        print("\nLLM Loss on V ",LLM_loss_on_V)
        print("\napproximation \n",mul3)
        error3 = np.abs(np.array(LLM_loss_on_V) - mul3)
        error3 = np.reshape(error3, (-1,len(val_data)))
        error3 = np.mean(error3, axis=1)
        approx_error_on_V.append(error3.tolist())
        print("\napprox error on V on Val data ",approx_error_on_V) 

        #################################################################################
        # Calculate the new U_{t+1} by removing worst subset from U_t and adding the best subset from L \ U_t
        U.pop(S_worst_ind)
        U.append(S_star)


        #################################################################################
        # Make new L_minus_U by removing best subset from it and adding worst subset of U_t to it
        L_minus_U.pop(S_star_ind)
        L_minus_U.append(S_worst) 


        #################################################################################
        # Calculate Loss(Y,Star) 
        LLM_loss = LLM_loss[0:S_worst_ind*len(val_data)] + LLM_loss[(S_worst_ind*len(val_data))+len(val_data):]
        S_star_list = []
        S_star_list.append(S_star)
        new_LLM_loss = LLM_error_indicator(S_star_list, val_data)
        LLM_loss.extend(new_LLM_loss)


        # LLM_loss_on_test_data = LLM_loss_on_test_data[0:S_worst_ind*len(test_data)] + LLM_loss_on_test_data[(S_worst_ind*len(test_data))+len(test_data):]
        # new_LLM_loss = LLM_error_indicator(S_star_list, test_data)
        # LLM_loss_on_test_data.extend(new_LLM_loss)


        LLM_loss_on_L_minus_U = LLM_loss_on_L_minus_U[0:S_star_ind*len(val_data)] + LLM_loss_on_L_minus_U[(S_star_ind*len(val_data))+len(val_data):] 
        S_worst_list = []
        S_worst_list.append(S_worst)
        LLM_loss_of_worst_on_val_data = LLM_error_indicator(S_worst_list, val_data)
        LLM_loss_on_L_minus_U.extend(LLM_loss_of_worst_on_val_data)


        # LLM_loss_on_L_minus_U_on_test_data = LLM_loss_on_L_minus_U_on_test_data[0:S_star_ind*len(test_data)] + LLM_loss_on_L_minus_U_on_test_data[(S_star_ind*len(test_data))+len(test_data):] 
        # LLM_loss_of_worst_on_test_data = LLM_error_indicator(S_worst_list, test_data)
        # LLM_loss_on_L_minus_U_on_test_data.extend(LLM_loss_of_worst_on_test_data)

        
        ################################################################################
        # Storing the indices of the subsets in U_t
        U_indices = []
        for i in range(len(U)):
            U_indices.append(U[i]['index'].tolist())

        L_minus_U_indices = []
        for i in range(len(L_minus_U)):
            L_minus_U_indices.append(L_minus_U[i]['index'].tolist())

        ################################################################################
        # fill W = identity(x_i \in S) E_{ij} 
        l = len(U)
        W_val = np.zeros((l*len(val_emb), len(transfer_emb)))
       # W_test = np.zeros((l*len(test_emb), len(transfer_emb)))
        for u in range(l):
            for i in range(len(transfer_emb)):
                if i in U_indices[u]:
                    W_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                    #W_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]


        ##############################################################################
        # make X = E_{ij} for all i in L \ U_t 
        L_minus_U_len = len(L)-len(U)
        X_val = np.zeros((L_minus_U_len*len(val_emb), len(transfer_emb)))
        # X_test = np.zeros((L_minus_U_len*len(test_emb), len(transfer_emb)))
        for u in range(L_minus_U_len):
            for i in range(len(transfer_emb)):
                if i in L_minus_U_indices[u]:
                    X_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                    # X_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]


        ################################################################################
        mul1 = np.matmul(W_val, alpha)
        #mul1_test = np.matmul(W_test, alpha)
        mul2 = np.matmul(X_val, alpha)
 

        #################################################################################
        #################################################################################
        print("\nMake new V by taking top v highest loss subsets from L \ U")
        #################################################################################

        mul_new2 = np.reshape(mul2, (L_minus_U_len,-1))
        sum_mul_new2 = np.sum(mul_new2, axis=1)
        v_worst_ind = np.argpartition(sum_mul_new2,-len(V))[-len(V):]
        V_new = [L_minus_U[i] for i in v_worst_ind]

        V_new_indices = []
        for i in range(len(V_new)):
            V_new_indices.append(V_new[i]['index'].tolist())

#         print("\n All the error values =",sum_mul_new2)
#         print("\n Top v highest error indices =",v_worst_ind)

#         print("\n V_old_indices =",V_indices)
#         print(" V_new_indices =",V_new_indices)
#         print("\n LLM_loss_on_old_V = ",LLM_loss_on_V)

#         set_difference = [item for item in V_new_indices if item not in V_indices]

#         # #new_items_in_V = [train_data[i] for i in set_difference]
#         new_items_in_V = []
#         for pos, ind in enumerate(L_indices):
#             if ind in set_difference:
#                 new_items_in_V.append(L[pos])


#         LLM_loss_of_new_items_in_V = LLM_error_indicator(new_items_in_V, val_data)
#         V_indices_overlap = []
#         LLM_loss_on_V_overlap = []
#         for pos, ind in enumerate(V_indices):
#             if ind in V_new_indices:
#                 V_indices_overlap.append(ind)
#                 LLM_loss_on_V_overlap.extend(LLM_loss_on_V[pos*len(val_data):(pos*len(val_data)+len(val_data))])
    

#         LLM_loss_on_V = LLM_loss_on_V_overlap + LLM_loss_of_new_items_in_V
#         V_indices = V_indices_overlap + set_difference

#         print("\n V_indices_overlap =",V_indices_overlap)
#         print(" V_new-V_old = set_difference =",set_difference)
#         print("\n V_latest_UPDATED_indices =",V_indices)
#         print("\n LLM_loss_on_V_overlap = ",LLM_loss_on_V_overlap)
#         print(" LLM_loss_of_new_items_in_V = ",LLM_loss_of_new_items_in_V)
#         print("\n LLM_loss_on_latest_UPDATED_V = ",LLM_loss_on_V)

#         #V = [train_data[i] for i in V_indices]
#         V = []
#         for pos, ind in enumerate(L_indices):
#             if ind in V_indices:
#                 V.append(L[pos])

        ######################################################
        V = V_new
        V_indices = V_new_indices
        LLM_loss_on_V = LLM_error_indicator(V, val_data)
        ######################################################
        

        # fill V = E_{ij} for all i in V_t
        v = len(V)
        V_val = np.zeros((v*len(val_emb), len(transfer_emb)))
        #V_test = np.zeros((v*len(test_emb), len(transfer_emb)))
        for u in range(v):
            for i in range(len(transfer_emb)):
                if i in V_indices[u]:
                    V_val[u*len(val_emb):(u*len(val_emb)+len(val_emb)),i] = E_val[i]
                    #V_test[u*len(test_emb):(u*len(test_emb)+len(test_emb)),i] = E_test[i]

        #####################################################################################################
        #####################################################################################################
        
        LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss, (len(U),-1))
        LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
        LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
        avg_LLM_loss_on_val.append(LLM_loss_on_val_avg.tolist()) 
        min_LLM_loss_on_val.append(LLM_loss_on_val_min.tolist())
        max_LLM_loss_on_val.append(LLM_loss_on_val_max.tolist())
        print("\n***********************************")
        print("S_worst_ind ",S_worst_ind)
        print("\n********* LLM LOSS ON U ON VALIDATION DATA *********")
        print("\nLLM_loss_on_val ",LLM_loss)
        print("\nAVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_val)
        print("\nMIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_val)
        print("\nMAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_val)



        
        # LLM_loss_for_each_subset = np.reshape(LLM_loss_on_test_data, (len(U),-1))
        # LLM_loss_for_each_subset = np.average(LLM_loss_for_each_subset, axis=1)
        # LLM_loss_avg = np.average(LLM_loss_for_each_subset)
        # LLM_loss_min = np.min(LLM_loss_for_each_subset)
        # LLM_loss_max = np.max(LLM_loss_for_each_subset)
        # #LLM_loss_on_test.append(LLM_loss_for_each_subset.tolist())
        # avg_LLM_loss.append(LLM_loss_avg.tolist()) 
        # min_LLM_loss.append(LLM_loss_min.tolist())
        # max_LLM_loss.append(LLM_loss_max.tolist())
        # print("\n***********************************")
        # print("S_worst_ind ",S_worst_ind)
        # print("\n********* LLM LOSS ON U FOR TEST DATA *********")
        # print("\nLLM_loss_on_test ",LLM_loss_on_test)
        # print("\nAVG_LLM_loss_on_TEST_data ",avg_LLM_loss)
        # print("\nMIN_LLM_loss_on_TEST_data ",min_LLM_loss)
        # print("\nMAX_LLM_loss_on_TEST_data ",max_LLM_loss)
        



        LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss_on_L_minus_U, (len(L_minus_U),-1))
        LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
        LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
        avg_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_avg.tolist()) 
        min_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_min.tolist())
        max_LLM_loss_on_L_minus_U_on_val.append(LLM_loss_on_val_max.tolist())
        print("\n***********************************")
        print("S_best_ind ",S_star_ind)
        print("\n********* LLM LOSS ON L_minus_U FOR VALIDATION DATA *********")
        print("\nLLM_loss_on_val ",LLM_loss_on_L_minus_U_on_val)
        print("\nAVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_L_minus_U_on_val)
        print("\nMIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_L_minus_U_on_val)
        print("\nMAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_L_minus_U_on_val)

        # LLM_loss_for_each_subset = np.reshape(LLM_loss_on_L_minus_U_on_test_data, (len(L_minus_U),-1))
        # LLM_loss_for_each_subset = np.average(LLM_loss_for_each_subset, axis=1)
        # LLM_loss_avg = np.average(LLM_loss_for_each_subset)
        # LLM_loss_min = np.min(LLM_loss_for_each_subset)
        # LLM_loss_max = np.max(LLM_loss_for_each_subset)
        # LLM_loss_on_L_minus_U_on_test.append(LLM_loss_for_each_subset.tolist())
        # avg_LLM_loss_on_L_minus_U.append(LLM_loss_avg.tolist()) 
        # min_LLM_loss_on_L_minus_U.append(LLM_loss_min.tolist())
        # max_LLM_loss_on_L_minus_U.append(LLM_loss_max.tolist())
        # print("\n***********************************")
        # print("S_best_ind ",S_star_ind)
        # print("\n********* LLM LOSS ON L_minus_U FOR TEST DATA *********")
        # print("\nLLM_loss_on_test ",LLM_loss_on_L_minus_U_on_test)
        # print("\nAVG_LLM_loss_on_TEST_data ",avg_LLM_loss_on_L_minus_U)
        # print("\nMIN_LLM_loss_on_TEST_data ",min_LLM_loss_on_L_minus_U)
        # print("\nMAX_LLM_loss_on_TEST_data ",max_LLM_loss_on_L_minus_U)


        LLM_loss_on_val_for_each_subset = np.reshape(LLM_loss_on_V, (len(V),-1))
        LLM_loss_on_val_for_each_subset = np.average(LLM_loss_on_val_for_each_subset, axis=1)
        LLM_loss_on_val_avg = np.average(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_min = np.min(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_val_max = np.max(LLM_loss_on_val_for_each_subset)
        LLM_loss_on_V_on_val.append(LLM_loss_on_val_for_each_subset.tolist())
        avg_LLM_loss_on_V_on_val.append(LLM_loss_on_val_avg.tolist()) 
        min_LLM_loss_on_V_on_val.append(LLM_loss_on_val_min.tolist())
        max_LLM_loss_on_V_on_val.append(LLM_loss_on_val_max.tolist())
        print("\n********* LLM LOSS ON V FOR VALIDATION DATA *********")
        print("\nLLM_loss_on_val ",LLM_loss_on_V_on_val)
        print("\nAVG_LLM_loss_on_VAL_data ",avg_LLM_loss_on_V_on_val)
        print("\nMIN_LLM_loss_on_VAL_data ",min_LLM_loss_on_V_on_val)
        print("\nMAX_LLM_loss_on_VAL_data ",max_LLM_loss_on_V_on_val)
        #===============================================================================





        #********* APPROX VALUE ON U ON VALIDATION DATA after updating U *********
        approx_value_on_U_for_each_subset = np.reshape(mul1, (len(U),-1))
        approx_value_on_U_for_each_subset = np.average(approx_value_on_U_for_each_subset, axis=1)
        approx_value_on_U_after_update.append(approx_value_on_U_for_each_subset.tolist())


        #********* APPROX VALUE ON U ON TEST DATA after updating U *********
        # approx_value_on_U_on_test_for_each_subset = np.reshape(mul1_test, (-1,len(test_data)))
        # approx_value_on_U_on_test_for_each_subset = np.average(approx_value_on_U_on_test_for_each_subset, axis=1)
        # approx_value_on_U_after_update_on_test_data.append(approx_value_on_U_on_test_for_each_subset.tolist())


        #********* APPROX VALUE ON L-U ON VALIDATION DATA after updating L-U *********
        approx_value_on_L_minus_U_for_each_subset = np.reshape(mul2, (-1,len(val_data)))
        approx_value_on_L_minus_U_for_each_subset = np.average(approx_value_on_L_minus_U_for_each_subset, axis=1)
        approx_value_on_L_minus_U_after_update.append(approx_value_on_L_minus_U_for_each_subset.tolist())


        #********* APPROX VALUE ON V ON VALIDATION DATA after updating V *********
        mul3 = np.matmul(V_val, alpha)
        approx_value_on_V_for_each_subset = np.reshape(mul3, (-1,len(val_data)))
        approx_value_on_V_for_each_subset = np.average(approx_value_on_V_for_each_subset, axis=1)
        approx_value_on_V_after_update.append(approx_value_on_V_for_each_subset.tolist())

        ###############################################################################


        #calculate the approximate error = (LLM_loss-W*alpha) on U
        print("\n*************Approximation error of Validation Data on U after updating U************")
        print("\nUpdated LLM Loss on U for Validation Data ",LLM_loss)
        print("\napproximation \n",mul1)
        # mape = MAPE(np.array(LLM_loss), mul1)
        # approx_error_on_U.append(mape.tolist())
        # print("\napprox error on U ",approx_error_on_U)
        error1 = np.abs(np.array(LLM_loss) - mul1)
        error1 = np.reshape(error1, (-1,len(val_data)))
        error1 = np.mean(error1, axis=1)
        approx_error_on_U_after_update.append(error1.tolist())
        print("\napprox error on U for Validation Data after updating U ",approx_error_on_U_after_update) 



        # print("\n*************Approximation error of Test Data on U after updating U************")
        # print("\nUpdated LLM Loss on U for Test Data ",LLM_loss_on_test_data)
        # print("\napproximation \n",mul1_test)
        # error1 = np.abs(np.array(LLM_loss_on_test_data) - mul1_test)
        # error1 = np.reshape(error1, (-1,len(test_data)))
        # error1 = np.mean(error1, axis=1)
        # approx_error_on_U_after_update_on_test_data.append(error1.tolist())
        # print("\napprox error on U for Test Data after updating U ",approx_error_on_U_after_update_on_test_data) 
        


        #calculate the approximate error = (LLM_loss_on_L_minus_U - X*alpha) on L_minus_U
        print("\n*************Approximation error of Validation Data on L_minus_U after updating L_minus_U************")
        print("\nUpdated LLM Loss on L_minus_U for Validation Data ",LLM_loss_on_L_minus_U)
        print("\napproximation \n",mul2)
        error2 = np.abs(np.array(LLM_loss_on_L_minus_U) - mul2)
        error2 = np.reshape(error2, (-1,len(val_data)))
        error2 = np.mean(error2, axis=1)
        approx_error_on_L_minus_U_after_update.append(error2.tolist())
        print("\napprox error on L_minus_U for Validation Data after updating L_minus_U ",approx_error_on_L_minus_U_after_update) 

        # #calculate the approximate error = (LLM_loss_on_L_minus_U - X*alpha) on L_minus_U
        # print("\n*************Approximation error of Test Data on L_minus_U after updating L_minus_U************")
        # print("Updated LLM Loss on L_minus_U for Test Data ",LLM_loss_on_L_minus_U_on_test_data)
        # print("\napproximation \n",mul2_test)
        # error2 = np.abs(np.array(LLM_loss_on_L_minus_U_on_test_data) - mul2_test)
        # error2 = np.reshape(error2, (-1,len(test_data)))
        # error2 = np.mean(error2, axis=1)
        # approx_error_on_L_minus_U_after_update_on_test_data.append(error2.tolist())
        # print("\napprox error on L_minus_U for Test Data after updating L_minus_U ",approx_error_on_L_minus_U_after_update_on_test_data) 


        #calculate the approximate error = (LLM_loss_on_V - V*alpha) on V
        print("\n*************Approximation error of Validation Data on V after updating V************")
        print("\nUpdated LLM Loss on V for Validation Data ",LLM_loss_on_V)
        print("\napproximation \n",mul3)
        error3 = np.abs(np.array(LLM_loss_on_V) - mul3)
        error3 = np.reshape(error3, (-1,len(val_data)))
        error3 = np.mean(error3, axis=1)
        approx_error_on_V_after_update.append(error3.tolist())
        print("\napprox error on V for Validation Data after updating V ",approx_error_on_V_after_update) 
    



        ###########################################################################################
        #Calculate pairwise overlap between subsets in U
        # overlaps=[]
        # for i in range(len(U)):
        #     for index_j, s_i in U[i].iterrows():
        #         overlap=0
        #         for j in range(len(U)):
        #             if i!=j:
        #                 for index_j, s_j in U[j].iterrows():
        #                     if s_i["question"].lower() in s_j["question"].lower() or s_j["question"].lower() in s_i["question"].lower():
        #                         overlap+=1
        #         overlaps.append(overlap)

        overlaps=[]
        for i in range(len(U)):
            inner_overlaps=[]
            for j in range(len(U)):
                if i!=j:
                    overlap=0
                    for index_j, s_i in U[i].iterrows():
                        for index_j, s_j in U[j].iterrows():
                            if s_i["question"].lower() in s_j["question"].lower() or s_j["question"].lower() in s_i["question"].lower():
                                overlap+=1
                    inner_overlaps.append(overlap)
            overlaps.append(inner_overlaps)
                

        print("\noverlaps ",overlaps)
        print("len overlaps ",len(overlaps))


        overlap_for_each_subset = np.average(overlaps, axis=1)
        overlap_avg = np.average(overlap_for_each_subset)
        overlap_min = np.min(overlap_for_each_subset)
        overlap_max = np.max(overlap_for_each_subset)

        overlap_for_subset.append(overlap_for_each_subset.tolist())
        avg_overlap.append(overlap_avg.tolist()) 
        min_overlap.append(overlap_min.tolist())
        max_overlap.append(overlap_max.tolist())
        print("\n********* PAIRWISE OVERLAP *********")
        print("\noverlap_for_subset ",overlap_for_subset)
        print("\nAVG_overlap ",avg_overlap)
        print("MIN_overlap ",min_overlap)
        print("MAX_overlap ",max_overlap)
        

        folder1 = f"./loss_folder1"
        np.savez(f'{folder1}',  avg_LLM_loss = avg_LLM_loss, min_LLM_loss = min_LLM_loss, max_LLM_loss = max_LLM_loss, LLM_loss_on_val = LLM_loss_on_val, avg_LLM_loss_on_val = avg_LLM_loss_on_val, min_LLM_loss_on_val = min_LLM_loss_on_val, max_LLM_loss_on_val = max_LLM_loss_on_val, LLM_loss_on_L_minus_U_on_val = LLM_loss_on_L_minus_U_on_val, avg_LLM_loss_on_L_minus_U_on_val = avg_LLM_loss_on_L_minus_U_on_val, min_LLM_loss_on_L_minus_U_on_val = min_LLM_loss_on_L_minus_U_on_val, max_LLM_loss_on_L_minus_U_on_val = max_LLM_loss_on_L_minus_U_on_val, LLM_loss_on_V_on_val = LLM_loss_on_V_on_val, avg_LLM_loss_on_V_on_val = avg_LLM_loss_on_V_on_val, min_LLM_loss_on_V_on_val = min_LLM_loss_on_V_on_val, max_LLM_loss_on_V_on_val = max_LLM_loss_on_V_on_val, approx_error_on_U = approx_error_on_U, approx_error_on_L_minus_U = approx_error_on_L_minus_U, approx_error_on_V = approx_error_on_V, approx_error_on_U_after_update = approx_error_on_U_after_update, approx_error_on_L_minus_U_after_update = approx_error_on_L_minus_U_after_update, approx_error_on_V_after_update = approx_error_on_V_after_update,  approx_value_on_U = approx_value_on_U, approx_value_on_U_after_update = approx_value_on_U_after_update, approx_value_on_L_minus_U = approx_value_on_L_minus_U, approx_value_on_L_minus_U_after_update = approx_value_on_L_minus_U_after_update, approx_value_on_V = approx_value_on_V, approx_value_on_V_after_update = approx_value_on_V_after_update,  overlap_for_subset = overlap_for_subset , avg_overlap = avg_overlap, min_overlap = min_overlap, max_overlap = max_overlap)
        #==============================================================================================================

        # Increment t
        t+=1

    return U
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_open_source_completions(test_data, data):

    stop_signal = "\n\n"
    matches = 0
    mismatches =0
    print("started running:")

    question_df = {"question":[],"answers":[]}

    train_data, val_data = train_test_split(data, test_size=0.3, random_state=42)
    val_data=val_data[:20]

    exemplars = static_subset_selection(val_data, train_data, 5, test_data)
    #merged_exemplars = pd.read_csv("static_subset_selection_mistral_aquarat_latest1.csv")
    #print("exemplars:",exemplars)
    #exemplars=np.array_split(merged_exemplars, 10)

    merged_exemplars = pd.concat(exemplars)
    merged_exemplars.to_csv("static_subset_selection_Llama_aquarat_latest12.csv")
    # *****************************************************************************
    print("\n\n\n_____________Take the exemplar with minimum validation loss and use it as the exemplar")
    avg_err = LLM_avg_error(exemplars, val_data)
    print("\n\navg_err ",avg_err)
    ind = np.argmin(avg_err)
    print("\n\nmin ind ",ind)
    exemplars = exemplars[ind]
    print("exemplars:",exemplars)

    index=0
    acc_records = []
    

    for index, row in test_data.iterrows():
        # if(index==3):
        #     break

        # prompt = prompt_for_manual_prediction(row, exemplars)
        # #chain_answer = safe_completion(prompt=prompt, max_tokens=_MAX_TOKENS, stop=stop_signal, temp=0.0, logprobs=5)
        # outputs=compare_llm_outputs(prompt)
        # ans=outputs[0].split("The option is ")
        # answer=""
        #answer=in_context_manual_prediction(row,exemplars)
        x=5
        answer=""
        optionlist=[0,0,0,0,0]

        while(x):
          y=in_context_manual_prediction(row,exemplars)
          y=y.lower()
          if y=='a':
            optionlist[0]+=1
          elif y=='b':
            optionlist[1]+=1
          elif y=='c':
            optionlist[2]+=1
          elif y=='d':
            optionlist[3]+=1
          elif y=='e':
            optionlist[4]+=1
          x-=1


        opt=''
        ans=0
        ind=-1
        for i in range(len(optionlist)):
          if(optionlist[i]>ans):
            ans=optionlist[i]
            ind=i
        if ind==0:
          opt='A'
        elif ind==1:
          opt='B'
        elif ind==2:
          opt='C'
        elif ind==3:
          opt='D'
        elif ind==4:
          opt='E'





        #predictions.append(opt)
        print("opt:",opt)
        answer=opt


    #     if(len(ans)>1):
    #   #print("the option:",ans[1][0])
    #         answer= ans[1][0].strip()
    #     else:
    #         answer=""
        #chain_answer = chain_answer[0]
        # question_df['question'].append(row["question"])
        # question_df["answers"].append(outputs)
        # final_questions = pd.DataFrame(question_df)
        # final_questions.to_csv("mistral_static_Llama_question_answer_latest12.tsv",sep="\t",index=False)

        # text = chain_answer
        # text = text.strip()

        # # place holder
        # answer = "null"
        # rationale = "null"

        # sep = get_sep_text(chain_answer)
        # if sep is not None:
        #     segments = text.split(sep)
        #     answer = segments[1].strip().strip('.')
        #     rationale = segments[0].strip()
        # else:
        #     answer = text

        ground_truth = row["correct"]

        print("\nanswer:",answer)
        print("ground_truth:",ground_truth)

        if answer==ground_truth:
            matches+=1
        else:
            mismatches+=1
        print("no.of completed",matches+mismatches)
        print("Accuracy:",matches/(matches+mismatches))


    #     acc, (f1, pre, rec), gt_ans = hotpot_evaluation_with_multi_answers(answer, row["answer_choices"])
    #     acc_records.append(acc)

    # mean_of_array = lambda x: sum(x) / len(x)
    # print("\naccuracy:", mean_of_array(acc_records))

    # with open("output/advhotpot/acc_advhotpot_static.pkl", 'wb') as f:
    #     pickle.dump(acc_records, f)
    # print(final_questions)

    print("EM", matches/(matches+mismatches))

    return final_questions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_few_shot_prediction():

    # ADVHOTPOT train dataset
    train_data = read_AHOTPOT_train_data()

    # ADVHOTPOT test dataset
    test_data = read_AHOTPOT_test_data()

    final_df = get_open_source_completions(test_data, train_data)
    print(final_df)


if __name__=='__main__':
    test_few_shot_prediction()