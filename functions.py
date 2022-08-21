from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
import re, unicodedata
import streamlit as st


@st.cache(show_spinner=False, 
                ttl=24*3600,
                allow_output_mutation=True,
                hash_funcs={"tokenizers.Tokenizer": lambda _: None,
                            "tokenizers.AddedToken": lambda _: None})
def load_pipeline():
    
    # load the tokenizer and the model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    #model     = GPT2LMHeadModel.from_pretrained("models/jobgenerator")
    model     = GPT2LMHeadModel.from_pretrained("wilame/jobdescription")
    
    # start the pipeline
    return pipeline('text-generation', model=model, tokenizer=tokenizer)

@st.cache(show_spinner=False)
def strip_punctuation(text):
    last_char = text[-1]
    text      = text[:-1]
    last_char = re.sub(r"[^a-zA-Z0-9]", "", last_char)
    text += last_char
    return text

def generate_text_streamlit(text, generator):

    ready = False
    count = 1
    
    # get the sequences generated
    while ready == False:

        sentences = generator(text, max_length=300, num_return_sequences=1)
        sentences = [unicodedata.normalize("NFKD", s['generated_text']) for s in sentences]
        
        # return the longest sentene
        sentence = max(sentences, key=len)
        sentence = sentence.replace("|job_description|>","")

        # don't let the loop become infinite...
        count += 1

        if sentence != text or count > 20:
            break

    return sentence