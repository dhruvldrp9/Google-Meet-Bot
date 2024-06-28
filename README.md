# Google-Meet-Bot
This project is a Python bot that automates the process of logging into Gmail, joining a Google Meet, recording the audio of the meeting, and then generating a summary, key points, action items, and sentiment analysis of the meeting. 

![Alt Text](/home/dhruv/Downloads/Google-Meet-Bot.jpeg)


## Prerequisites

- Python 3.8 or higher
- Chrome browser
- OpenAI Api Key
- A Gmail account
- A Google Meet link

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dhruvldrp9/Google-Meet-Bot.git
   cd google-meet-bot

2. Make python environment:

   ```bash
   python3 -m venv env

3. Activate environment(Ubuntu):

   ```bash
   source env/bin/activate

3. Activate environment(Windows):

   ```bash
   env/scripts/activate

4. Install requirements:

   ```bash
   pip install -r requirements.txt

5.  Export credentials to environments:

   ```bash
   export OPENAI_API_KEY="Your_OpenAI_Api_Key"
   
   export email_id="Your_email_id"
   
   export email_password="your_email_password"
   ```


6. Run Script:

   ```bash
   python3 join_google_meet.py

   
