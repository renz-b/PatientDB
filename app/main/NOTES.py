    #wtforms for forms
    #first form includes first name last name middle initial DONE
    #queries database if there is duplicate and show list of hits DONE
    #show choices to continue or return CURRENT TODO
    #second form include diagnosis and history
    #if diagnosis is not included in current list show add diagnosis that commits in the same webpage
    #commit

    #From views.py first line
    ## @main.before_app_request
    # def before_request():
    #     g.search_form = SearchForm()
    # SEARCH BAR PRESENT IN ALL ROUTES FUNCTION
    # currently commented out since this used search function in the global g context, i did not use this


#MAIN TODO:

# add at least 10 model instances - unable to add yet models are not finalized
# add forms for adding patient DONE
# add pagination, done css for tables and searchbar with card DONE
# z index: when in results page the dropdown menu is behind card DONE
# change min_score variable when doin patient search during quering for specific matches but should be low when searching normally DONE

# change AGE to birthday and calculate age on render based on birthday

# 1. add patient button in index DONE
# 2. add (% if %) statement in tables.html instead of re writing to show code if the requests comes from add_patient DONE instead of if statement in jinja placed it in jquery.jr 
# 3. I think i should add a new html for showing tables of add_patient where es min score is 0.9 DONE current min score is 0.8 for similar_results view function
# 4. in the new html table add markup for "Renz Baticados Bustillo already has a record please check to avoid duplicates" DONE
# 5. Add buttons to cancel to return to home or add another patient or continue URGENT!
# 6. Next form already rendered the general data (first name, last name) with empty forms below containing diagnosis and history DONE
# 7. Enable option to fill later and commit - add Edit functionality at the rightmost after searching to enable edit
# 8. use ajax jquery to display the search if there is a similar patient after query DONE

# TODO FOR TODAY:
# 1. Finish Form DONE
# 2. Hard code diagnosis entries figure out how to dynamically produce selectfields later and try to use ajax jquery to update selectfield if possible if not idk
# 3. Try and commit first model from front end... LETS GOOOOO DOOOOOOOOOONEEEEEEEEEEE

#NOTES:
# run elastisearch.exe as admin
# check if reindex function just adds the new added models for __searchable__ or adds on top of it
# add flask-msearch if ever elastic search is not available
# in tables.html only show general data, add drop down to show history - drop down or link?
# when querying pls use get_or_404 TODO TODO TODO TODO TODO but i query using elastic to return models....

# connected to a new test database, currently making forms no tables or rows in database and elasticsearch cannot reindex an empty database
# # notes: Edited search code to include score for searches remove after ADDED: score variable in search.py, models.py and in html
# also added ES_MIN_SCORE config variable






# TOO TIRED TO PLASTAR MY THINKING
# DONE I COMMITTED ITS SOMETHING!!
# but few errors tho:
# elastic does not like it if you commit on empty database after create_table DONE did a try except block so that I would not query database each time similar_patient function is called
# but i fixed it with an if statement at similar_patient
# problem with validation how to check or query database if input already exists that is a problem for tomorow
# unique constraint was only found on email I removed it since anyone can have the same email maybe in flask login in the future to query if there is similar


#TODO Nov 10
# 1. Create 2 view functions: one for viewing patient details including everythin, second the one in the youtube video where the form is already populated by the User model 
# 2. 2 new HTML and SCSS for the view functions
# 3. Create link in the tables.html to view patient details

#TODO Nov 11
# 1. CSS for patient details html
# 2. Change age to birthday and calculate on render, add gender to forms and html
# 3. if statement in forms for OB history if male or female
# 4. try ajax to update patient details without refresh? possible?

# 5. too tired to fully fix (pagination  in allpatients requires pagination object to be called in the template and not in the view function)
# 6. all patients html does not scroll properly change height to auto later

#TODO NOV 12
# 1. Do the diagnosis
# 2. Use jquery flexdata list download and implement
# 3. add a query to similar patient of diagnosis and pass it to render template
# 4. add html and jquery for diagnosis
# 5. add Show all results on focus but place button if diagnosis is not there add diagnosis
# 6. add autocomplete=off on form tags so that previously submitted values are not saved

# NOTES:
# in final_diagnosis it shows a class repr format but i changed the backref lazy to dynamic it still shows repr due to its already committed it will change back tp shpowing only the disease when i drop the db

# Nov 12 Notes:
# data list done only needs css and positioning left, also did the referring buttons and made it correctly redirect, class bg-verylightgray not working
# left to do is to drop database -> change age to birthday render age according to birthday
# clean up code when done some variables are confusing
# diagnosis del patient and upate patient seem repeptitive try to use only one function and use an if statement

# Nov 23:
# 1. Add 2 buttons in add_patient when a similar_patient is found
# 2. change the return link after commit_patient to patient/id
# 3. add option to delete patient
# 4. clean up code