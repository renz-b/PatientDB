![logo](https://github.com/renz-b/PatientDB/blob/master/app/static/svg/icon.svg)**&nbsp;PatientDB**
---
<p align="center">
<img src="https://img.shields.io/github/pipenv/locked/python-version/renz-b/PatientDB">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/flask">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/flask-sqlalchemy">
<img src="https://img.shields.io/github/pipenv/locked/dependency-version/renz-b/PatientDB/elasticsearch">
<img src="https://img.shields.io/github/license/renz-b/PatientDB">
<img src="https://img.shields.io/badge/coverage-68%25-orange">
<img src="https://img.shields.io/website/http/patientdb-heroku.herokuapp.com.svg">
 </p>
 <p align="center" style="font-style:italic"><i>
"PatientDB is a simple web app that stores patient information, able to edit the information, <br>and able to query the database to display the patient details."</i>
</p>

## :zap: Demo
***Adding a Patient***
![Demo GIF](https://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation.gif)

***Querying Patient, Adding and Deleting Diagnosis***
![Demo2 GIF](https://github.com/renz-b/PatientDB/blob/master/.github/readme/Animation2.gif)

## :abacus: Database Model
- Patient and Diagnosis have a Many to Many relationship.
- Patient and History have a One to One relationship.

<div align="center">
 <img src="https://github.com/renz-b/PatientDB/blob/master/.github/readme/db_diagram.svg">
</div>

## :3rd_place_medal: Coverage
<table class="index" data-sortable="">
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left" aria-sort="none" data-shortcut="n">Module</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="b">branches</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="p">partial</th>
                <th class="right" aria-sort="none" data-shortcut="c">coverage</th>
            </tr>
        </thead>
        <tbody>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698___init___py.html">app\__init__.py</a></td>
                <td>28</td>
                <td>14</td>
                <td>0</td>
                <td>2</td>
                <td>1</td>
                <td class="right" data-ratio="15 30">50%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_fake_py.html">app\fake.py</a></td>
                <td>18</td>
                <td>2</td>
                <td>0</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="18 20">90%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_ffc6e1978ca246d0___init___py.html">app\main\__init__.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_ffc6e1978ca246d0_errors_py.html">app\main\errors.py</a></td>
                <td>11</td>
                <td>2</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 11">82%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_ffc6e1978ca246d0_forms_py.html">app\main\forms.py</a></td>
                <td>23</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="23 23">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_ffc6e1978ca246d0_views_py.html">app\main\views.py</a></td>
                <td>182</td>
                <td>13</td>
                <td>0</td>
                <td>32</td>
                <td>9</td>
                <td class="right" data-ratio="190 214">89%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_models_py.html">app\models.py</a></td>
                <td>92</td>
                <td>72</td>
                <td>0</td>
                <td>20</td>
                <td>2</td>
                <td class="right" data-ratio="34 112">30%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_search_py.html">app\search.py</a></td>
                <td>18</td>
                <td>12</td>
                <td>0</td>
                <td>10</td>
                <td>3</td>
                <td class="right" data-ratio="9 28">32%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>375</td>
                <td>115</td>
                <td>0</td>
                <td>66</td>
                <td>15</td>
                <td class="right" data-ratio="301 441">68%</td>
            </tr>
        </tfoot>
    </table>

## 	:mechanical_arm: Technologies Used:
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Elasticsearch
- WTForms
- JQuery
- SASS

## :open_file_folder: Resources
[Flask Miguel Grinberg Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search)
> Integration of elasticsearch to PostgreSQL. Since elasticsearch returns string results, the tutorial helped me return the results as objects of the Patient model with pagination. It also includes how to update the index on every commit by adding event listeners after and before commits to trigger functions that update the index.

[Pretty Printed - JQuery](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)
> Youtube channel that helped me understand how to use JQuery to create my own functions that apply to my use case.

[Code Coder - SCSS](https://www.youtube.com/channel/UCzNf0liwUzMN6_pixbQlMhQ)
> Learned how to implement flexbox and SASS for better code organization and easy implementation of CSS.
## :page_facing_up: License
[GNU Affero General Public License v3.0](https://github.com/renz-b/PatientDB/blob/master/LICENSE)





