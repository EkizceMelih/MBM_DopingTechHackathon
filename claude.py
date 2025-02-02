import boto3
import base64
import json

# AWS Bedrock istemcisini oluştur (Kimlik bilgileri ~/.aws/credentials üzerinden alınır)
aws_region = "us-east-1"  # Kendi AWS bölgeni kontrol et
bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)

def encode_image_to_base64(image_path):
    """Görseli Base64 formatına çevirir."""
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

def analyze_image_with_claude(image_path):
    """Claude 3 Haiku'ya görseli göndererek analiz eder."""
    image_base64 = encode_image_to_base64(image_path)

    # Claude 3 Haiku'ya gönderilecek payload
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    }
                ]
            }
        ]
    }

    # API isteğini gönder
    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )

    # Yanıtı işle
    response_body = json.loads(response["body"].read().decode("utf-8"))
    return response_body

# 📌 Test için görseli analiz et
image_path = "image.jpg"  # Kendi görsel yolunu buraya yaz
result = analyze_image_with_claude(image_path)

# Yanıtı ekrana yazdır
print(json.dumps(result, indent=2))
