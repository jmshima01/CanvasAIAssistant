#!/bin/env python3
import openai

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = api_key
