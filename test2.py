import json
import os
import sys
import boto3
import botocore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.bedrock import BedrockChat
from botocore.client import Config
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import RetrievalQA



bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_client = boto3.client('bedrock-runtime',
                              aws_access_key_id = 'AKIAQT2YWNM4BE2J54FQ',
                              aws_secret_access_key = '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')

modelId = 'anthropic.claude-3-sonnet-20240229-v1:0' # change this to use a different LLM

llm = BedrockChat(model_id=modelId, client=bedrock_client)


retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="XXC7RQRO2T",# enter knowledge base id here
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)


query = "What role did Amazon play during pandemic?"

qa = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True
)

response = qa.invoke(query)
response["result"]