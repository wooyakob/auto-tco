from google.api_core.client_options import ClientOptions
from google.cloud import documentai 
import pandas as pd
from flask import Flask, render_template_string, send_file
import io

project_id = "tco-automation-430318"
location = "us"  
file_path = "/Users/wooyakob/Desktop/auto-tco/April_DEV_2024.pdf"
processor_name = "projects/tco-automation-430318/locations/us/processors/1646373740d5d523"

def quickstart(
    project_id: str,
    location: str,
    file_path: str,
    processor_name: str,
):

    print("Starting quickstart function...") 

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf", 
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document

    print("The document contains the following text:")
    #print(document.text)
    
    #for entity in document.entities:
        #print(f"Type: {entity.type_}, Mention Text: {entity.mention_text}, Confidence: {entity.confidence}")

    entities_data = []
    for entity in document.entities:
        entities_data.append({
            "Type": entity.type_,
            "Mention Text": entity.mention_text,
            "Confidence": entity.confidence
        })

    # Create DataFrame
    df = pd.DataFrame(entities_data)
    print(df)

if __name__ == "__main__":
    print("Script is starting...") 
    quickstart(project_id, location, file_path, processor_name)
    print("Script has finished.")