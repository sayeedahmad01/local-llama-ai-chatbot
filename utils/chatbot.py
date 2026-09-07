from langchain_ollama import ChatOllama


def create_model(
    model_name="llama3.2",
    temperature=0.7
):
    """
    Create and return the Ollama chat model.
    """

    model = ChatOllama(
        model=model_name,
        temperature=temperature
    )

    return model


def get_response(model, messages):
    """
    Send conversation history to the model
    and return the AI response.
    """

    response = model.invoke(messages)

    return response.content