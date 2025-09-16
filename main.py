from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import base64
import io

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Base64 to xlsx converter</title>
    </head>
    <body>
        <h1>Base64 to xlsx converter</h1>
        <p>This is an API that should be called. You should not directly access this page.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/convert")
async def convert_base64_to_xlsx(request: Request):
    data = await request.json()
    base64_str = data.get("base64")

    if not base64_str:
        return {"error": "Missing base64 string in request."}

    try:
        # Decode the base64 string
        xlsx_bytes = base64.b64decode(base64_str)
        xlsx_stream = io.BytesIO(xlsx_bytes)

        # Return the XLSX file as a downloadable response
        return StreamingResponse(
            xlsx_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=converted.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}
