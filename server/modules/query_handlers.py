from logger import logger

# def query_chain(chain,user_input:str):
#     try:
#         logger.debug(f"Running chain for input:{user_input}")
#         result=chain({"query":user_input})
#         response={
#             "response":result["result"],
#             "sources":[doc.metadata.get("source","Unknown") for doc in result["source_documents"]]
#         }
#         logger.debug(f"Chain result: {response}")
#         return response
    
    
#     except Exception as e:
#         logger.error(f"Error in query_chain: {str(e)}")
#         raise

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")

        # New LangChain Runnable API
        result = chain.invoke(user_input)

        # result is an AIMessage (from ChatGroq), so get text like this:
        answer = result.content

        response = {
            "response": answer,
        }

        logger.debug(f"Chain result: {response}")
        return response

    except Exception as e:
        logger.error(f"Error in query_chain: {str(e)}")
        raise