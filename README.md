# SEMPL-IT Backend
This is the backend of the SEMPL-IT, a web app designed to simplify Italian administrative document using SLM. 

The backend is built with FastAPI and interacts with three different fine-tuned language models to perform text simplification tasks. By sending data through a single POST endpoint, the backend processes the input text and simplifies it to make it more understandable for a wider audience.

Check out the [frontend](https://https://github.com/VerbACxSS/semp-it-frontend) of the SEMPL-IT web app.

## Getting started
### Pre-requisites
This web application is developed using FastAPI framework and Hugging Face Transformers library. The following software are required to run the application:
* Python (tested with version 3.9.18)
* Pip (tested with version 23.2.1)

Alternatively, you can use a containerized version by installing:
* Docker (tested on version 27.3.1)

### Configuration
The application can be configured using the following environment variable:
```
USE_ONNX_RUNTIME=True|False
```
If `USE_ONNX_RUNTIME` is set to `True`, the application will use ONNX runtime to run the models (faster inference, but slower startup time). Otherwise, if `USE_ONNX_RUNTIME` is set to `False` (default), the application will use PyTorch to run the models (slower inference, but faster startup time).

### Using `python` and `pip`
Create python virtual environment
```shell
python3 -m venv venv
```
Activate the virtual environment
```shell
source venv/bin/activate   # Linux/macOS
./venv/Scripts/activate    # Windows
```
Install all dependencies in requirements.txt
```shell
pip install -r requirements.txt
```
Start the server
```shell
python -m uvicorn app.app:app 
```

### Using `docker-compose`
Run the application using `docker compose`
```sh
docker compose up --build -d
```

## Usage
The web application will be running at `http://localhost:8080` by default. Make a POST request to the following endpoint:
```sh
curl -X POST "http://localhost:8000/api/v1/predict/" \
-H "Content-Type: application/json" \
-d '{
    "model": "gpt2-small-italian",
    "paragraphs": [
        "Nella fattispecie, questo documento è di natura prescrittiva.",
        "Il presente documento ha lo scopo di fornire indicazioni operative per la gestione del personale."
    ]
}'
```

## SEMPL-IT fine-tuned models
The backend interacts with three different fine-tuned models available on Hugging Face perform text simplification tasks. The models are:
* `sempl-it-mt5-small`: https://huggingface.co/VerbACxSS/sempl-it-mt5-small
* `sempl-it-umt5-small`: https://huggingface.co/VerbACxSS/sempl-it-umt5-small
* `sempl-it-gpt2-small-italian`: https://huggingface.co/VerbACxSS/sempl-it-gpt2-small-italian

## Built with
* [FastAPI](https://fastapi.tiangolo)
* [Hugging Face Transformers](https://huggingface.co/transformers/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
This contribution is a result of the research conducted within the framework of the PRIN 2020 (Progetti di Rilevante Interesse Nazionale) "VerbACxSS: on analytic verbs, complexity, synthetic verbs, and simplification. For accessibility" (Prot. 2020BJKB9M), funded by the Italian Ministero dell'Università e della Ricerca.