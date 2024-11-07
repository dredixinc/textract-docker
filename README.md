# Textract Webservice Docker-Image

A simple docker image to serve [textract](https://textract.readthedocs.io/) as a REST-API. Based on Python and [starlette](https://www.starlette.io).

## Supported file types

.csv via python builtins  
.doc via antiword  
.docx via python-docx2txt  
.eml via python builtins  
.epub via ebooklib  
.gif via tesseract-ocr  
.jpg and .jpeg via tesseract-ocr  
.json via python builtins  
.html and .htm via beautifulsoup4  
.mp3 via sox, SpeechRecognition, and pocketsphinx  
.msg via msg-extractor  
.odt via python builtins  
.ogg via sox, SpeechRecognition, and pocketsphinx  
.pdf via pdftotext (default) or pdfminer.six  
.png via tesseract-ocr  
.pptx via python-pptx  
.ps via ps2text  
.rtf via unrtf  
.tiff and .tif via tesseract-ocr  
.txt via python builtins  
.wav via SpeechRecognition and pocketsphinx  
.xlsx via xlrd  
.xls via xlrd  

## Build + Run 

### Docker Compose
```
docker compose up
```

### Docker
```
docker build -t textract .
docker run -t -p 8080:8080 -e PORT=8080 textract .
```




## Usage

### Example Usage With Curl

Command:
```bash
curl --request POST \
  --url 'http://localhost:8080/textract' \
  --header 'Content-Type: multipart/form-data' \
  --form 'file=@C:\Users\user.name\Document\SampleFile.txt'
```

Repsonse Body:
```json
{
	"filename": "SampleFile.txt",
	"file_content_type": "text/plain",
	"file_size": 1380,
	"file_extension": "txt",
	"text_hash": "5e684616a6b793c6689408f8fd1dc894862f0f972929144d433da409a4587764",
	"text_length": 1372,
	"duration": 0.0,
	"text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa..."
}
```

### Example Usage With Python Client
See `client/client.py` for an example uploading a file converted to base64 format.

Request json:
```
{
    "data": <base64 encoded file data>,
    "file_type": <file type / extension e. g. png, txt, etc ... (without '.')>
}
```

Response json:
```
{
    "text": <extracted text utf-8 encoded>
}
```




