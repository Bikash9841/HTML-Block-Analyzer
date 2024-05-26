from fastapi import FastAPI
from pydantic import BaseModel
from extract import extract_product_info, load_llm


pipeline = load_llm()
app = FastAPI()


class HTMLInput(BaseModel):
    html_content: str


@app.get("/")
async def root():
    return {"message": "This one for PLAYSTATION."}


@app.post("/process-html/")
async def process_html(html_input: HTMLInput):
    html_content = html_input.html_content
    extracted_data = extract_product_info(html_content, pipeline)
    return extracted_data
