from main import get_post_content

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SocialMediaPost(BaseModel):
    post_content: str
    platform: str
    

@app.post("/generate-content/")
async def generate_content(request: SocialMediaPost):
    result = get_post_content(request.post_content, request.platform)
    return {"response": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)