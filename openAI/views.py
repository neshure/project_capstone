from django.shortcuts import render
import os
import openai
openai.organization = "org-w1NXtfBUi8VFaFw1Zi8fIXli"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()




# curl https://api.openai.com/v1/completions \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer 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" \
# -d '{"model": "text-davinci-003", "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'