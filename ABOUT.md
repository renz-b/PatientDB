
<img src="../static/svg/icon.svg">**&nbsp;PatientDB**
---

***
<p align="center">
<img src="https://img.shields.io/github/pipenv/locked/python-version/renz-b/PatientDB">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/flask">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/flask-sqlalchemy">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/elasticsearch">
<img src="https://img.shields.io/github/license/renz-b/PatientDB">
<img src="https://img.shields.io/website/http/med-quicktest.herokuapp.com/.svg">
 </p>
 <p align="center" style="font-style:italic"><i>
"PatientDB is a simple web app that stores patient information, able to edit the information, <br>and able to query the database to display the patient details."</i>
</p>

## Demo
***
<p align="center"><i><b>Adding a Patient</b></i></p>
<p align="center">

<img src="https://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation.gif?raw=truehttps://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation.gif..\..\.github\readme\Animation.gif" width="75%">
</p>
<p align="center"><i><b>Querying Patient, Adding and Deleting Diagnosis</b></i></p>
<p align="center">
<img src="https://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation2.gif?raw=truehttps://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation2.gif..\..\.github\readme\Animation2.gif" width="75%">
</p>

## Database Model
***
- Patient and Diagnosis have a Many to Many relationship.
- Patient and History have a One to One relationship.
<p>&nbsp;</p>
<div align="center">
 <img src="https://github.com/renz-b/PatientDB/blob/master/.github/readme/db_diagram.svg?raw=truehttps://github.com/renz-b/PatientDB/blob/master/.github/readme/db_diagram.svg..\..\.github\readme\db_diagram.svg">
</div>


## Technologies Used:
***
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Elasticsearch
- WTForms
- JQuery
- SASS

## Resources
***
[Flask Miguel Grinberg Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search)
> Integration of elasticsearch to PostgreSQL. Since elasticsearch returns string results, the tutorial helped me return the results as objects of the Patient model with pagination. It also includes how to update the index on every commit by adding event listeners after and before commits to trigger functions that update the index.

[Pretty Printed - JQuery](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)
> Youtube channel that helped me understand how to use JQuery to create my own functions that apply to my use case.

[Code Coder - SCSS](https://www.youtube.com/channel/UCzNf0liwUzMN6_pixbQlMhQ)
> Learned how to implement flexbox and SASS for better code organization and easy implementation of CSS.
## License
***
[MIT Licence](https://github.com/renz-b/PatientDB/blob/master/LICENSE)





