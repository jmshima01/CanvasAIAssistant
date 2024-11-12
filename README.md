# CanvasAIAssistant
AI Assistant for Canvas/Ed

## Dependencies:
`python3.10+`

`requirements.txt`

`pip install -r requirements.txt` 

## Canvas Data Scrapper Usage:
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
