
# Simple but powerful chat bot with Streamlit and xAI API

## The app is currently deployed on Streamlit Community Cloud, you need to enter your xAI API key in the sidebar in order to use the bot.
Link to the app: [BOB the assistant](https://bob-the-assistant.streamlit.app/)

1. Add you own API key into the sidebar
   - It doesn't neet to be  from xAI, you can use other API's, just change the url path and endpoint in const.py
   - I plan to add more API providers later, like OpenAI and Groq
   - Option to choose from available models for the specific API
   - If its paid API, you can send in the request only the last prompt(prompt + system message) for less token usage
   - otherwise u can send the whole conversation
2. To run the web app on localhost:
   - In terminal -> ***streamlit run server.py***

3. To run the chatbot in terminal:
   - In terminal → ***python ai_agent.py*** or ***python3 ai_agent.py***

4. I use different ***SYSTEM_MESSAGES*** to test what the bot is capable of, 
later on I will add a function to let the user choose what personality the bot should use.
   - possible ***SYSTEM_MESSAGES*** that I may add:
      - quiz maker
      - python expert
      - savage mode (it doesn't provide valuable answers, AI trying to be funny)
      - ... 


