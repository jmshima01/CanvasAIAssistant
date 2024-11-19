# MarvinAI
AI Assistant for Canvas and Edstem Discusion

## Dependencies:
`python3.10+`

`requirements.txt`

`pip install -r requirements.txt` 

## Canvas Data Scrapper Usage (canvas.py):
- Login to Canvas
- -> Account -> Settings -> + New Access Token
- Save the token and the home canvas url in `.env`

`cat .env`

```
CANVAS_API_URL="https://elearning.mines.edu"
CANVAS_API_KEY="your_access_token_here"
```

##### Then to run...

`./canvas.py`
 
 or

 `make canvas`

## Ed Usage edstem.org (ed.py):
- Goto https://edstem.org/us/settings/api-tokens
- Create Token and again put it in `.env`

`cat .env`

```
ED_API_TOKEN="your_edstem_token_here"
```

`./ed.py`

or 

`make ed`


## Ask a question (Work in progress with FastAPI):
`./llm.py` 
will ask a question and give a response or post to ed if asked
