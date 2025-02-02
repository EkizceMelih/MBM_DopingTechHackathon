import boto3
import json

def invoke_bedrock_model(prompt):
    """
    AWS Bedrock Claude 3 Sonnet modelini çağıran fonksiyon.

    Parametre:
        prompt (str): Claude modeline gönderilecek metin girdisi.

    Dönüş:
        str: Modelin verdiği yanıt.
    """

    # AWS Bedrock Runtime istemcisi oluştur
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',  # Bölgeyi 'us-east-1' veya 'eu-west-2' olarak güncelleyin.
    )

    # Claude 3 Sonnet model ID (AWS'den doğrulanmış)
    model_id = "anthropic.claude-3-sonnet-20240213-v1:0"

    # Model için uygun JSON formatı
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Modeli çağır
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        # Yanıtı parse et
        response_body = json.loads(response.get('body').read())

        # Model yanıtını döndür
        return response_body['content'][0]['text']

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return None

# Kullanım örneği
if __name__ == "__main__":
    prompt = "Merhaba, nasılsın?"
    response = invoke_bedrock_model(prompt)
    
    if response:
        print("Model yanıtı:", response)
    else:
        print("Model çağrısı başarısız oldu.")
