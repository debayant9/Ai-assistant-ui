import urllib.request
import json
import os
import ssl
import streamlit as st
from gtts import gTTS
from io import BytesIO
import json

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

st.set_page_config("AI Assistant")
st.header("AI Assistant")

user_incident = st.text_input("Current Incident")
data = {"question": user_incident}

body = str.encode(json.dumps(data))

url = 'https://ai-competencedevelopment-assist.eastus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'AM4fHRcXaVYzbziKTp4h8lOOn2oFaGaD'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'ai-competencedevelopment-assist' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = json.loads(response.read())
    st.write("Reply: ", result["output"])

    audio = BytesIO()
    #sound_file = BytesIO()
    #tts = gTTS(result, lang='en')
    #tts.write_to_fp(audio)
    #st.audio(audio)

    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))