import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="getNews.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "getnews-dxuugf"

from gnewsclient import gnewsclient

def getNewsType(parameters):
    print("Entered getNews")
    top=parameters.get('newsType')
    lang=parameters.get('langType')
    retStr=str(top) + "," + str(lang)
    return retStr


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)

    if response.intent.display_name == 'getNewsType':
        retStr=getNewsType(dict(response.parameters))
        top, lang=retStr.split(",")

        if lang=="":
            lang="english"

        if top=="":
            top="Top Stories"

        if top=="Top Stories":
            print("Entered Top story")
            client=gnewsclient.NewsClient(language=lang, location="India", topic=top)
            res=client.get_news()

            newsStr=""
            
            if len(res)==0:
                newsStr+="Sorry!! No news to fetch!"
                
            else:

                for i in range(2):
                    finalStr = "\n *" + res[i]['title'] + "*" + "\n\n" + "*Link to be followed* \n" + res[i]['link'] + "\n\n"
                    newsStr+=finalStr
            return newsStr
        else:
            print("Entered else")
            client = gnewsclient.NewsClient(language=lang, location="India", topic=top, max_results=5)
            res = client.get_news()
            
            newsStr=""
            for i in range(len(res)):
                finalStr = "\n *" + res[i]['title'] + "*" + "\n\n" + "*Link to be followed* \n" + res[i]['link'] + "\n\n"
                newsStr+=finalStr
            return newsStr
        
    elif response.intent.display_name == 'workDone':
        print("Entered WorkDone!")
        retStr = "Hi!\n"+"I am your personal NewsBot!\n"+"I can get you news on various topics as listed below:\n\n"+"1.)World\n2.)Nation\n3.)Business\n4.)Entertainment\n5.)Health\n6.)Science and more.."
        return retStr
        
    else:
        return response.fulfillment_text
        

    
    