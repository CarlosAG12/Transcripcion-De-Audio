from groq import Groq

client = Groq(api_key= "PENE")

def resumirTexto(texto):
    chatCompletion = client.chat.completions.create(
        messages=[
            {"role" : "user", "content" : f"Resume este texto para pedidos trata de extraer lo mas importante y escribirlo de una mejor manera: {texto}"}
        ],
        model="llama-3.1-8b-instant"
    )

    return chatCompletion.choices[0].message.content
