"""
Demo script for running a chat interface for resume Q&A
"""
import os
import glob
import datetime
from typing import List, Dict, AsyncIterator

import gradio as gr
from dotenv import load_dotenv
from gradio import ChatInterface
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
DB_NAME = os.getenv('DB_NAME', 'vector_db')
NAME = os.getenv('NAME', 'Yu-An Lin')
FIRST_NAME, LAST_NAME = NAME.split() if ' ' in NAME else (NAME, '')
SEARCH_K = int(os.getenv('SEARCH_K', '20'))
WORK_START_DATE = os.getenv('WORK_START_DATE', '2018-04-01')

# Set environment variables
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# LLM is really bad at math, so we set the year of experience to a fixed value
work_start_date = datetime.datetime.strptime(WORK_START_DATE, "%Y-%m-%d")  # Parse from string format
today = datetime.datetime.now()
# Calculate years of experience based on the work start date and today's date, give year and month in string
total_days = (today - work_start_date).days
year_experience = total_days / 365.25  # Approximate year calculation
month_experience = (total_days % 365) / 30  # Remaining days converted to months
print(f"Year of experience for {NAME}: {int(year_experience)} years and {int(month_experience)} months")

# System template for the AI assistant
SYSTEM_TEMPLATE = f"""
Today is {datetime.datetime.now().strftime("%Y-%m-%d")}. 
You are a helpful assistant that helps {NAME} answer questions from recruiters about his experience.
Your goal is to help {NAME} secure a job offer while being honest and concise.
{NAME} has {int(year_experience)} years and {int(month_experience)} months of experience in the field excluding the internship.

Use the following retrieved job experience to answer the recruiter's question:
------
{{context}}

If you don't know the answer or if {NAME} has the experience, say so, but suggest that {NAME} can clarify if needed.
Provide link whenever possible.
Use emoji to make the conversation more engaging.
Return the result in markdown format.
"""


def add_metadata(doc, doc_type):
    doc.metadata["doc_type"] = doc_type
    return doc


def load_documents(path: str = "knowledge-base"):
    """Load documents from the knowledge base and initialize the vectorstore"""
    folders = glob.glob(f"{path}/*")
    text_loader_kwargs = {'encoding': 'utf-8'}

    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
        folder_docs = loader.load()
        documents.extend([add_metadata(doc, doc_type) for doc in folder_docs])

    return documents

def init_vectorstore(documents, db_name, verbose: bool = False):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    if verbose:
        print(f"Total number of chunks: {len(chunks)}")
        print(f"Document types found: {set(doc.metadata['doc_type'] for doc in documents)}")

    embeddings = OpenAIEmbeddings()
    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    if verbose:
        print(f"Vectorstore created with {vectorstore._collection.count()} documents")
        collection = vectorstore._collection
        count = collection.count()
        sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
        dimensions = len(sample_embedding)
        print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")
    return vectorstore


class PortfolioChatAssistant:
    def __init__(self, model_name: str, db_name: str, search_k: int, knowledge_path: str, temperature: float = 0.3):
        # Initialize components with streaming enabled
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, streaming=True)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = init_vectorstore(load_documents(knowledge_path), db_name)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": search_k})
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)
        self.chat_histories: Dict[str, List[BaseMessage]] = {}

    def get_chat_history(self, session_id: str) -> List[BaseMessage]:
        """Get or create chat history for a session"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = []
        return self.chat_histories[session_id]
    
    async def chat(self, question: str, history: List) -> AsyncIterator[str]:
        """Process a chat message and stream the response"""
        # Use default session for simplicity
        session_id = "default_session"
        chat_history = self.get_chat_history(session_id)
        
        # Retrieve relevant context
        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create messages for the LLM
        system_message = SystemMessage(content=SYSTEM_TEMPLATE.format(context=context))
        messages = [system_message] + chat_history + [HumanMessage(content=question)]
        
        # Add the human message to history (assistant message will be added after completion)
        chat_history.append(HumanMessage(content=question))
        
        # Get streaming response from the model
        full_response = ""
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content'):
                content = chunk.content
                full_response += content
                yield full_response
        
        # After streaming is complete, add the complete message to history
        chat_history.append(SystemMessage(content=full_response))

def create_chat_interface(assistant: PortfolioChatAssistant) -> ChatInterface:
    """Create the Gradio interface for the chat assistant"""
    # Interface settings
    title = f"AI Chat Assistant for {FIRST_NAME}'s Experience"
    description = f"Ask questions about {FIRST_NAME}'s resume and experience"
    
    # Example questions
    examples = [
        f"What is {FIRST_NAME}'s background and year of experience in the field?",
        f"Where are {FIRST_NAME}'s previous work experiences and or interview experiences?",
        f"What was {FIRST_NAME}'s role and key achievements at Adobe, Proofpoint, and SproutLabs?",
        f"What experience does {FIRST_NAME} have with Kubernetes and container technologies?",
        f"Tell me about {FIRST_NAME}'s skills in cloud platforms like AWS, Azure and GCP",
        f"What programming languages is {FIRST_NAME} proficient in, and some applications?",
        f"What leadership and soft skills does {FIRST_NAME} have?",
        f"What experience does {FIRST_NAME} have building CI/CD pipelines?",
        f"What is {FIRST_NAME}'s experience with LLM and Agentic AI?",
    ]
    
    # Avatar images
    user_avatar = "https://i.pinimg.com/736x/fa/89/2b/fa892ba0b545610d16e996e5ca34b54a.jpg"
    assistant_avatar = "https://cdn.dribbble.com/userupload/22515003/file/original-bed70c3fcd37fc0a0a324ad3ab075cd3.jpg?resize=752x564&vertical=center"
    
    # Create interface with streaming enabled
    return gr.ChatInterface(
        assistant.chat,
        chatbot=gr.Chatbot(
            avatar_images=(user_avatar, assistant_avatar),
            height=550,
            resizable=True,
            type="messages"
        ),
        fill_height=True,
        type="messages",
        title=title,
        description=description,
        examples=examples,
        theme=gr.themes.Default(primary_hue=gr.themes.colors.red, secondary_hue=gr.themes.colors.pink)
    )

def main():
    """Main function to initialize the assistant and launch the interface"""
    assistant = PortfolioChatAssistant(model_name=MODEL_NAME, db_name=DB_NAME, search_k=SEARCH_K, knowledge_path="knowledge-base")
    chat_interface = create_chat_interface(assistant)
    chat_interface.launch(inbrowser=True)

if __name__ == "__main__":
    main() 