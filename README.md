Funny Chat bot with Streamlit

1. Add you own API key into .env file
  1.1 It doesn't neet to be  from xAI, you can use other API's, just change the url path and endpoint in const.py
  1.2 If its paid API, you can send in the request only the last prompt(prompt + system message) for less token usage
  1.3 Otherwise u can send the whole conversation

2. To run the web app on localhost:
In terminal :
  streamlit run server.py

3. To run the chatbot in terminal:
  Just run the ai_agent.py


I use different SYSTEM_MESSAGES to test what the bot is capable of, 
later on I will add a option to let the user choose what personality the bot should use.

