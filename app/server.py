import base64
import hashlib
import os
import sys
import time

import aiohttp
import asyncio
import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import json
import textract as txrct
import tempfile
from base64 import b64decode

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])


@app.route('/textract', methods=['POST'])
async def upload_file(request):
    try:
        start_time = time.time()
        form = await request.form()

        # Check if the file is in the request and a file was uploaded
        if "file" not in form or form["file"] is None:
            return JSONResponse({"error": "No file was found in the request"}, status_code=422)

        file = form["file"]

        # Check if the file extension is allowed
        allowed_file_extensions = [".csv", ".doc", ".docx", ".eml", ".epub", ".gif", ".jpg", ".jpeg", ".json", ".html", ".htm", ".msg", ".odt", ".ogg", ".pdf", ".png", ".pptx", ".ps", ".rtf", ".tif", ".tiff", ".txt",  ".wav", ".xls", ".xlsx"]
        file_extension = os.path.splitext(file.filename)[1].replace(".", "").lower()
        if not any(file.filename.endswith(ext) for ext in allowed_file_extensions):
            return JSONResponse({"error": f"File extension not allowed. Allowed file extensions are {', '.join(allowed_file_extensions)}"}, status_code=422)

        # create a file name with a random name and the original extension
        new_filename = f'{base64.urlsafe_b64encode(os.urandom(6)).decode("utf-8")}{os.path.splitext(file.filename)[1]}'
        with open(f'/tmp/{new_filename}', 'wb') as f:
            f.write(await file.read())

        text = txrct.process(f'/tmp/{new_filename}')
        decoded_text = text.decode('utf-8')

        # Get the sha256 hash of the decoded text
        try:
            text_hash = hashlib.sha256(decoded_text.encode()).hexdigest()
        except Exception as e:
            print(f"Error while trying to get the hash of the text: {str(e)}")
            text_hash = None

        # Try to remove the file
        try:
            os.remove(f'/tmp/{new_filename}')
        except Exception as e:
            print(f"Error while trying to remove the file: {str(e)}")

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        return JSONResponse({
            "filename": file.filename,
            "file_content_type": file.content_type,
            "file_size": file.size,
            'file_extension': file_extension,
            "text_hash": text_hash,
            "text_length": len(decoded_text),
            "duration": duration,
            "text": decoded_text
        })
    except Exception as e:
        print(f"Error while processing the file: {str(e)}")
        return JSONResponse({"error": "There was an error while processing the file", 'exception:': str(e)}, status_code=500)

@app.route('/textract-base64', methods=['POST'])
async def textract(request):      
    data = await request.body()
    data_json = json.loads(data)
    file_type = data_json['file_type']
    file_dec = b64decode(data_json['data'])

    suffix = f'.{file_type}'

    with tempfile.NamedTemporaryFile(suffix=suffix, buffering=0) as t:
        t.write(file_dec)
        text = txrct.process(t.name)

    resp = {'text': text.decode('utf-8')}
    return JSONResponse(resp)

@app.route('/status', methods=['GET'])
def status(request):
    res = {'status': 'OK'}
    return JSONResponse(res)

if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), log_level="info")