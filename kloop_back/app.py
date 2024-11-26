import hashlib
import os
import openai
from pinecone import Pinecone, ServerlessSpec
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2 
import tiktoken
import whisper
import tempfile
from dotenv import load_dotenv
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
import time



## Adding ad configuring Promotheus

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
REQUEST_LATENCY = Summary('http_request_latency_seconds', 'Request latency in seconds')






load_dotenv()

app = Flask(__name__)



@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.after_request
def after_request(response):
    """Calculate the request latency and observe it."""
    if hasattr(request, 'start_time'):  # Ensure start_time was set
        latency = time.time() - request.start_time
        REQUEST_LATENCY.observe(latency)
    return response



CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize Pinecone
api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=api_key)
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'
spec = ServerlessSpec(cloud=cloud, region=region)

index_name = 'kloopindex'
if index_name not in pc.list_indexes().names():
    pc.create_index(index_name, dimension=1536, metric='cosine', spec=spec)
index_main = pc.Index(index_name)

openai.api_key = os.getenv('OPENAI_API_KEY')
embed_model = "text-embedding-ada-002"

# Retrieve relevant contexts from Pinecone
def retrieve(query):
    MIN_CONFIDENCE_THRESHOLD = 0.8
    res = openai.embeddings.create(input=[query], model=embed_model)
    xq = res.data[0].embedding
    contexts = []
    time_waited = 0
    while len(contexts) < 3 and time_waited < 30:
        res = index_main.query(vector=xq, top_k=3 ,include_metadata=True)
        relevant_matches = [x for x in res['matches'] if x['score'] >= MIN_CONFIDENCE_THRESHOLD]
        contexts += [x['metadata']['text'] for x in relevant_matches]
        print(f"Retrieved {len(contexts)} contexts, Thinking!....")
        time_waited+=1


    if time_waited >= 30:
        print("Timed out waiting for contexts to be retrieved.")
        contexts = ["No contexts retrieved. Try not to answer the question yourself!"]


    max_context_length = 4000  # Allow room for prompt + response
    combined_contexts = " ".join(contexts)
    if len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(combined_contexts)) > max_context_length:
        combined_contexts = combined_contexts[:max_context_length]  # Truncate context if too long

    prompt = f"""
    You are an intelligent assistant designed to answer questions strictly based on the extracted context provided. Below is the user query and the retrieved context from the database:

    **Query:**
    {query}

    **Context:**
    {contexts}

    Answer the query concisely and factually based on the provided context. Do not include explanations about the context itself. If the context does not contain enough information to fully answer the query, respond only with: "The provided context does not contain sufficient information to answer the question."
    """


    
    return prompt

# Generate a response based on query and contexts
def complete(query_with_contexts):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=query_with_contexts, 
       max_tokens=150,  # Set this value based on your expected response length
        temperature=0 
    )
    return response.choices[0].text


def generate_embeddings(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

@app.route('/', methods=['GET'])
def index():
    return {"message": "Welcome to the backend API!"}, 200

# Route to handle user queries
@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query', '')
    print(user_query)
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    # Retrieve relevant contexts and generate response
    query_with_contexts = retrieve(user_query)
    print(query_with_contexts)
    response = complete(query_with_contexts)
    return jsonify({"response": response})

whisper_model = whisper.load_model("base")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    chunk_size = 500
    metadata = None

    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Secure the filename and save the file temporarily
    filename = secure_filename(file.filename)
    file_extension = os.path.splitext(filename)[1].lower()
    temp_file_path = tempfile.mktemp(suffix=file_extension)

    # Save file to temporary location
    file.save(temp_file_path)

    if filename.endswith('.pdf'):
        # Process PDFs as before
        text_chunks = process_pdf(temp_file_path, chunk_size)

    elif filename.endswith(('.mp3', '.wav')):
        # Process audio files
        text_chunks = process_audio(temp_file_path, chunk_size)

    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Batch process and index each chunk
    batch_size = 50
    data_to_index = []
    for idx, chunk_text in text_chunks:
        embedding = generate_embeddings(chunk_text)
        chunk_metadata = {
            "segment_number": idx + 1,
            "text": chunk_text
        }

        vector_data = {
            "id": f"segment{idx + 1}_{hashlib.md5(chunk_text.encode()).hexdigest()}",
            "values": embedding,
            "metadata": chunk_metadata
        }
        data_to_index.append(vector_data)

        if len(data_to_index) >= batch_size:
            index_main.upsert(vectors=data_to_index)
            data_to_index = []

    if data_to_index:
        index_main.upsert(vectors=data_to_index)

    print("Indexed file successfully.")
    return jsonify({"message": "File indexed successfully"})


def process_pdf(file_path, chunk_size):
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(file_path)
    text_chunks = []
    for page_num, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()
        if page_text:
            words = page_text.split()
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i + chunk_size])
                text_chunks.append((page_num, chunk))
    return text_chunks


def process_audio(file_path, chunk_size):
    # Transcribe audio file using Whisper
    print('Entered Audio')
    print(file_path)
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcript = result["text"]
    words = transcript.split()
    text_chunks = [
        (i, " ".join(words[i:i + chunk_size]))
        for i in range(0, len(words), chunk_size)
    ]
    return text_chunks



@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)