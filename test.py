import boto3

bedrock_agent_runtime = boto3.client(
    service_name = "bedrock-agent-runtime",
    aws_access_key_id = 'AKIAQT2YWNM4BE2J54FQ',
    aws_secret_access_key = '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'
)

def retrieve(query, kbId, numberOfResults=5):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery= {
            'text': query
        },
        knowledgeBaseId=kbId,
        retrievalConfiguration= {
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults
            }
        }
    )

response = retrieve("What is the architecture of Llama3?", "RRC1QTO6NS")["retrievalResults"]
print(response)