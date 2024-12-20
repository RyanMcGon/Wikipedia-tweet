from fastapi import FastAPI, HTTPException
import wikipediaapi
from pydantic import BaseModel

app = FastAPI()

# Create a user agent string that identifies your application
user_agent = "WikipediaContentAPI/1.0 (https://your-website.com; your@email.com)"
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

class WikiRequest(BaseModel):
    url: str

@app.post("/get-wiki-content")
async def get_wiki_content(request: WikiRequest):
    try:
        # Extract the page title from the URL
        page_title = request.url.split("/wiki/")[-1].replace("_", " ")
        
        # Get the Wikipedia page
        page = wiki.page(page_title)
        
        if not page.exists():
            raise HTTPException(status_code=404, detail="Page not found")
            
        return {
            "title": page.title,
            "summary": page.summary,
            "full_content": page.text,
            "url": page.fullurl
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Wikipedia Content API"} 