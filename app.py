import os
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def load_model():
    persist_dir = "./acap-db"
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.7}
    )

    TEMPLATE = """
        Answer the following question:
        {question}

        To answer the question, use only the following context:
        {context}

        At the end of the response, specify the name of the source page it came from.
    """
    prompt_template = PromptTemplate.from_template(TEMPLATE)

    chat = ChatOpenAI(model_name="gpt-4", temperature=0.7, max_tokens=500)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt_template
        | chat
        | StrOutputParser()
    )

    print("Model loaded and chain is set up.")
    return chain


chain = load_model()


def answer_query(user_input):
    print("Received question:", user_input)
    response = chain.invoke(user_input)
    return response


interface = gr.Interface(
    fn=answer_query,
    inputs=gr.components.Textbox(lines=2, placeholder="Enter your question here..."),
    outputs="text",
    title="ACAP Student QA Bot",
    description="A Retrieval-Augmented Generation bot ACAP student resources. Ask your questions about college student resources and get answers!",
)

if __name__ == "__main__":
    interface.launch(share=True)
