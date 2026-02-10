import os
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_classic.memory.buffer import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# 1. Load Environment Variables from .env file
load_dotenv() 
# Ensure your .env file has: GOOGLE_API_KEY=your_actual_key

# 2. Setup Vector Database (Run once)
def initialize_retriever():
    # Load all recipe .txt files
    loader = DirectoryLoader('./recipes', glob="./*.txt", loader_cls=TextLoader)
    docs = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    db_name = "recipe_vector_db"
    # Create Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

# Create vectorstore
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=db_name)
    return vectorstore.as_retriever()

retriever = initialize_retriever()

# 3. Setup Gemini & Memory
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# This object stores the "Chat History"
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True,
    output_key="answer" # Required for this specific chain type
)

# 4. Create the Conversational Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    verbose=False # Set to True to see the "thought process" in terminal
)

# 5. Gradio Logic
def chat_function(message, history):
    # The chain automatically pulls context from DB and history from memory
    response = qa_chain.invoke({"question": message})
    return response["answer"]

# 6. Launch Interface
demo = gr.ChatInterface(
    fn=chat_function,
    title="🥦 Smart Recipe & Nutrition Bot",
    description="I remember our conversation! Ask me about ingredients, then follow up with nutrition questions.",
    examples=["Tell me about the Quinoa Salad.", "How much protein is in that?"]
)

if __name__ == "__main__":
    demo.launch()