# PQRs-project
Team 209 - Data Science for All DS4A

Team members: Ader Villar, Cristian Polanco, Patricia González, Camilo Serna, and Javier Zúñiga.

Stakeholders: Ibague's Town Hall.

Project name: PQRs - project


## Abstract
The health industry is characterized by the huge number of suggestions, complaints, and petitions (SCP) that are received on a daily basis. The Ibague’s town hall is proposing a project in which SCPs are classified upon arrival by their content, the profile of the person submitting the SCP (age, vulnerability), and perform a characterization of the SCPs according to their content. The main challenge besides classification is proper determination of SCP to assign the right resources and help to reduce the number of legal allegations against Ibague’s Health Secretary. This project presents an alternative combining Computer Science techniques such as Optical Character Recognition (OCR), and Term Frequency - inverse document Frecuency as a Data Science tool to address and determine if a request corresponds to a Suggestion, Complaint or a petition presented in a dynamic dashboard.

## Technical Summary
The architecture presented below is sectioned in four mayor areas: SQL Database, Natural Language Processing model, Data Pulling based on Manual construction and web scrapping, and Data Consumption on a constructed Web Page.
![Architecture](https://user-images.githubusercontent.com/108638762/177217861-ed914f1e-2dac-43f6-951a-a05c550cf377.png)

## Github Content
The proposed solution was constructed on Python and CSS and all the documentation is placed here.
In this github you could find the following archives:

1. _Creation and connection - database.py_: Contains the procedure to connect the project back with the SQL Google Cloud database.
2. _Methods.py_: Contains the used methods any time an request is submitted.
3. _fast-kiln-353017-c44d6cb4bcdd.json_: Contains the Google credentials. It satisfies a security procedure.
4. _Finalized_Model.sav_: It stores the NLP used model.
