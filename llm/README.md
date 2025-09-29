// How to Run LangChain + Neo4j Connector


1️⃣
 Set Up Neo4j

Ensure your Neo4j instance is running.

APOC plugin should be installed.

Note down your URI, username, and password. (of the instance)


2️⃣ Configure the Project

Navigate to the folder containing langchain_connector.py.

Create a .env file and add your credentials:

OPENAI_API_KEY= your-openai-api-key 
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS= your own


3️⃣ Set Up a Virtual Environment (if set up is not there)

 ##  python -m venv agriner_env 


4️⃣ Install Dependencies

Install the required packages: (in terminal)

##  pip install langchain langchain-openai langchain-neo4j neo4j python-dotenv 

5️⃣ Run the Connector Script (in terminal)

##   python langchain_connector.py

6️⃣ Chat with KrishiAI
