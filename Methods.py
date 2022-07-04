from google.cloud import vision_v1
import os
import io
import mysql.connector
import re
from mysql.connector.constants import ClientFlag
import mysql.connector
from mysql.connector.constants import ClientFlag
import pandas as pd



def Connect_database():
    #Scope: Connect to the MySQL SQL database in GCloud
    #Input: None
    #Output: PQR Table rows
    #libraries: mysql
    
    #Database parameters:    
    config = {
    'user': 'root',
    'password': 'Team209',
    'host': '34.135.47.175',
    'database': 'testdb'}

    #Establish the DB connection with Python
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)
    
    #Pull the data from the PQR table 
    cursor.execute("Select * From PQR")
    return cursor.fetchall()


def Create_dataframe():
    #Scope: Bring the data from the DB and convert it in a pandas dataframe.
    #Input: None
    #Output: dataframe with the information in PQR table.
    #libraries: pandas
 
    #Pull the data from the SQL PQR table 
    input_fetchall= Connect_database()
    
    #Convert the data from SQL to Pandas dataframe
    data = pd.DataFrame(input_fetchall, columns=['pqr', 'tipo'])
    return data




def OCR_Image():
    #Scope: Pull the PQR scan images and perform 
    #       Optical Recognition Character Recognition (OCR) over them.
    #Input: None
    #Output: Text after perform OCR on the PQR images.
    #libraries: google.cloud,
    
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fast-kiln-353017-c44d6cb4bcdd.json'
  #Cliente desde google
  Cliente = vision_v1.ImageAnnotatorClient()

  Nombre_Archivo = 'Archivo.jpg'
  #Pull file next to this Python Notebook
  Ruta = './'

  #Brings the path
  with io.open(os.path.join(Ruta,Nombre_Archivo),'rb') as f:
    contenido = f.read()

  image = vision_v1.types.Image(content = contenido)
  response = Cliente.document_text_detection(image= image, image_context ={'language_hints': ['es']} )
  text = response.full_text_annotation
  return text.text

def Upload_to_PQRtable():
    #Scope: Upload to PQR table 
    #Input: None
    #Output: Text after perform OCR on the PQR images.
    #libraries: google.cloud,

  text = OCR_Image()
  #Connection to SQL
  config = {
      'user': 'root',
      'password': 'Team209',
      'host': '34.135.47.175',
      'database': 'testdb'
            }
  
  # now we establish our connection
  cnxn = mysql.connector.connect(**config)
  cursor = cnxn.cursor() 
  
  Manual_PQR = []
  
  #Assign the category 'Unknown' to the incoming PQR
  Manual_PQR.append((text,'Unknown'))
  data = pd.DataFrame(Manual_PQR, columns=['pqr', 'tipo'])
  
  #Clean Data
  data["pqr_clean"] = data["pqr"].str.replace('\n',' ')
  for i in range(len(data["pqr_clean"])):
    data["pqr_clean"][i] = re.sub(r"[^a-zA-Z0-9 ]","",data["pqr_clean"][i])
    PQR = data['pqr_clean'].iloc[i]
  
    
  #Insert into SQL
  query = ("INSERT INTO PQR (PQR, Type) VALUES ('%s', 'unknown')" %(PQR))
  cursor.execute(query)
  cnxn.commit()
  pass


def Translate_Text(text):  
    #Scope: Translate the incoming text from spanish to english
    #Input: text: text in spanish to translate
    #Output: Translated text.
    #libraries: TextBlob

    #Translate the text
  Translation = ""
  try:
     Translation =str(TextBlob(text).translate(from_lang='es', to='en')).lower()
  except:
    ""
  return Translation


def predicciones(text):
    #Scope: Use the trained model over the PQR contained in the text. 
    #Input: text:PQR translated text
    #Output: None.
    #libraries: pandas, joblib, sklearn

    #Translate text
      Text = Translate_Text(text)
      #Charge model - the model should stay in the  
      loaded_model = joblib.load("/content/finalized_model.sav")
      
      #pass it into a dataframe
      complaints = pd.read_excel("/content/complaints.xlsx",header=0)
      complaints = complaints[["tipo","pqr_translate","tipo_token"]]

    #Prepare the data to use the model. 
    #The first step is vectorize the info.
    #The features min_df,  and ngram_range were found using try and error
      tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
      tfidf.fit_transform(complaints.pqr_translate).toarray()
    
      text_features = tfidf.transform([Text])
      predictions = int(loaded_model.predict(text_features)[0])
      
      #Traduce the signal received into a text
      response = ''
      if predictions == int(0):
        response = 'queja'
      elif predictions == int(1):
        response = 'peticion'
      else:
        response = 'reclamo'
      
    
      #Insert into Database
      config = {
          'user': 'root',
          'password': 'Team209',
          'host': '34.135.47.175',
          'database': 'testdb'
                }
    
      # now we establish our connection
      cnxn = mysql.connector.connect(**config)
      cursor = cnxn.cursor() 
      query = ("Update PQR SET Type = '%s' where Type = 'Unknown'") %(str(response))
      cursor.execute(query)
      cnxn.commit()
      pass

def textblob():
    #Scope: analize and determine the polarity and subjetivity of the text. 
    #Input: None
    #Output: polarity and subjetivity.
    #libraries: textblob
    
    #Pull the data from the PQR
    text=Create_dataframe().tail(1)
    
    #Pull the polarity and subjetivity for the text
    classifier = TextBlob(Translate_Text(text))
    polarity = classifier.sentiment.polarity
    subjectivity = classifier.sentiment.subjectivity
    return polarity,subjectivity


