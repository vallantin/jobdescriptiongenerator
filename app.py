from functions import *
from transformers import pipeline
from collections import Counter

# config layout
st.set_page_config(page_title='Job description generator',
                   #layout = 'wide',
                   page_icon = 'img/icon.png',
                   initial_sidebar_state = 'collapsed'
                   )

# hold missing questions
missing_questions = st.sidebar.empty()

st.header('📝 Job description generator')

st.write("""
         What if there was an easy way to write more inclusive, diversity-focused job descriptions? 
         This text generator uses a GPT-2 template trained with job descriptions that promote equality 
         and diversity within the organizational environment. 
        """)

st.markdown("<p>Here you can ⬇️<a href='https://huggingface.co/wilame/jobdescription/' target='_blank'>download and use this model</a> on your own projects.", unsafe_allow_html=True)

        
     

#load the pipeline
info = st.empty()
info.info('⏳ Loading model: it may take a few seconds. Please, wait...')
pipeline = load_pipeline()
info.empty()

# Check if there's generated text
if 'generated' not in st.session_state:
    
    # if there's no text, provide a kickstart for the suer
    placeholder_text = "The ideal candidate is"
    # initialize the session state for the generated text
    st.session_state['generated'] = placeholder_text
    generated = placeholder_text

else:
    placeholder_text = None
    generated = st.session_state['generated']

# count the number of unique suggestions
if 'suggestions' not in st.session_state:
    # initialize the session state for the suggestions
    st.session_state['suggestions'] = []
    c = Counter(st.session_state['suggestions'])
    c[''] = 0
else:
    c = Counter(st.session_state['suggestions'])
    c[''] = 0

# ------------------------------------------------------------------------------------
st.markdown("""---""")
st.subheader('Write a short sentence')
st.write('The model will continue it for you.')
text = st.text_area('Your text here', value=generated, placeholder=placeholder_text)
text = text.strip()

# if the last char is punctuation, remove it. Otherwise the model won't generate predictions
if text != None and text != '':

    # if the suggestion is always the same, remove the punctuation
    if max(dict(c).values()) >= 2 and max(dict(c).values()) < 3:
        text = strip_punctuation(text)
    elif max(dict(c).values()) >= 2:
        st.warning('🤔 Getting the same suggestion over and over? Try to change a few words in your text.')

    if len(text) > 1000:

        st.warning("⚠️ Your text is longer than 1,000 characters. Please shorten your text.")

    else:
        
        # if there's something on the text box, continue with the predictions    
        if st.button('Generate'):
                
            generated = generate_text_streamlit(text, pipeline)
            st.success(generated)
            st.session_state['generated'] = generated
            st.session_state['suggestions'].append(generated)
            st.experimental_rerun()

# ------------------------------------------------------------------------------------
st.markdown("""---""")
st.subheader('To go further')
st.write("[5 Must-Do’s for Writing Inclusive Job Descriptions](https://www.linkedin.com/business/talent/blog/talent-acquisition/must-dos-for-writing-inclusive-job-descriptions)")
st.write("[How to Write Inclusive Job Descriptions](https://www.lever.co/blog/how-to-write-an-inclusive-job-description/)")


st.subheader('Other projects')
st.write("[Document similarity](https://vallantin-textsimilarity-app-gopds6.streamlitapp.com/)")

# ------------------------------------------------------------------------------------
st.markdown("""---""")
st.image('img/icon.png', width=80)
st.markdown("<h6 style='text-align: left; color: grey;'>Made by <a href='https://wila.me/' target='_blank'>wila.me</a></h6>", unsafe_allow_html=True)