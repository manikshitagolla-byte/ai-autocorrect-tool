from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from happytransformer import HappyTextToText, TTSettings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

print("Loading AI Grammar Model... Please wait.")

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

settings = TTSettings(num_beams=5, min_length=1)

print("Model Loaded Successfully!")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "original_text": "",
            "corrected_text": "",
            "char_count": 0,
            "word_count": 0,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def correct_text(request: Request, text: str = Form(...)):
    input_text = "grammar: " + text

    result = happy_tt.generate_text(input_text, args=settings)

    corrected = result.text

    char_count = len(text)
    word_count = len(text.split())

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "original_text": text,
            "corrected_text": corrected,
            "char_count": char_count,
            "word_count": word_count,
        },
    )
