from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.models import  Likes, User, Recipes,Comments,Favourites,Contacts











# register the user--------------------------------------------------------

@app.route('/api/users', methods=['POST'])
def create_user1():

    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]
    user = User(username, email, password,photo='https://res.cloudinary.com/personal-cloud/image/upload/v1622763605/Sportify%20Images/photo_ebtvt9.png')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


# entering a recipie-------------------------------------------------------

@app.route('/api/recipie', methods=['POST'])
def create_recipie():

    data = request.json
    name = data["name"]
    preparation = data["preparation"]
    user_id = data["user_id"]
    username = data["user_name"]
    photo=data["recipe_photo"]
    recipie = Recipes(name, preparation, user_id, username, photo,likes=False,likes_status=0,favourite_status=0)
    db.session.add(recipie)
    db.session.commit()
    return jsonify(recipie.to_dict())


#login a user in##############################################
@app.route('/api/login', methods=['POST', 'GET'])
def loginUser():

    data = request.json
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        user = User.query.filter_by(username=username).first()
        return jsonify(user.to_dict())


# get the recipies for each User####

@app.route('/api/recipie/<int:id>', methods=['GET'])
def getRecipie(id):

    recipie = Recipes.query.filter_by(user_id=id)

    return jsonify([reci.to_dict() for reci in recipie])


# get  the recipies for all the users

@app.route('/api/allrecipes', methods=['GET'])
def getallRecipes():

    recipes = Recipes.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])


# get only one recipie from the user, 

@app.route('/api/recipe/<int:id>', methods=['GET'])
def editrecipe(id):

    recipe = Recipes.query.filter_by(id=id).first()

    return jsonify(recipe.to_dict())


# update the recipie
@app.route('/api/recipe1/<int:id>', methods=['PUT'])
def editrecipe1(id):

    recipe = Recipes.query.get(id)
    data = request.json
    recipe.name = data["name"]  
    recipe.preparation = data["preparation"]
    recipe.user_id = data["user_id"]
    recipe.username = data["user_name"]
    recipe.photo = data["recipe_photo"]
    
    db.session.commit()

    return jsonify(recipe.to_dict())





# delete a recipe

@app.route('/api/recipe/delete/<int:id>', methods=['DELETE'])
def deleteRecipe(id):
   
    recipe = Recipes.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    commen = Comments.query.filter_by(recipe_id=id)
    if commen:
        for com in commen:
            db.session.delete(com)
            db.session.commit()
    likes = Likes.query.filter_by(recipe_id=id)     
    if likes:
        for like in likes:
            db.session.delete(like)
            db.session.commit()   

             
    favourite = Favourites.query.filter_by(recipe_id=id)     
    if favourite:
        for fav in favourite:
            db.session.delete(fav)
            db.session.commit()   

        

    

    return jsonify([recipe.to_dict() for recipe in Recipes.query.all()])



  

#likes2.0
@app.route('/api/like/<int:id>', methods=['PUT'])
def liketRecipe(id):
    data = request.json
    user=data["username"]
    userlikes = Likes.query.filter_by(recipe_id=id)

    if user in [like.username for like in userlikes]:

        user1=Likes.query.filter_by(username=user,recipe_id=id).first()
        db.session.delete(user1)
        db.session.commit()
        likes = Recipes.query.filter_by(id=id).first()
        likes.likes -= 1
        likes.likes_status=0
        db.session.commit()
        return jsonify(likes.to_dict())
    else:
        user=Likes(user,id)
        db.session.add(user)
        db.session.commit()
        likes = Recipes.query.filter_by(id=id).first()
        data = request.json
        likes.likes += 1
        likes.likes_status=1
        db.session.commit()

        return jsonify(likes.to_dict())
    



#comments

@app.route('/api/comments/<int:id>', methods=['POST'])
def comments(id):


    data = request.json
    message=data["message"]
    user_name=data["user_name"]
    photo=data["photo"]
   
    comment=Comments(message,id,user_name,photo)
    db.session.add(comment)
    db.session.commit()

    commen = Comments.query.filter_by(recipe_id=id)

    return jsonify([comm.to_dict() for comm in commen])



    # get the comments

   

@app.route('/api/commentsget/<int:id>', methods=['GET'])
def getcomments(id):


    

    commen = Comments.query.filter_by(recipe_id=id)

    return jsonify([comm.to_dict() for comm in commen])


#delete a comment

@app.route('/api/comment/delete/<int:id>', methods=['DELETE'])
def deletecomment(id):
   
    
    commen = Comments.query.filter_by(id=id).first()
    db.session.delete(commen)
    db.session.commit()

    return jsonify(commen.to_dict())

            

        

    
#changing profile photo

@app.route('/api/profile_photo_change', methods=['PUT'])
def changeImage():


    data = request.json
    user_name=data["user_name"]
    user = User.query.filter_by(username=user_name).first()
    user.photo =data["photo"]
    db.session.commit()
    return jsonify(user.to_dict())


# Changing the user name and password.

@app.route('/api/profile_info', methods=['PUT'])
def updateuser():


    data = request.json
    old_user=data["old_user"]
    user_name=data["username"]
    email=data["email"]
    password=data["password"]
    
    user = User.query.filter_by(username=old_user).first()
    user.username =user_name
    user.password=password
    user.email=email
    db.session.commit()
    return jsonify(user.to_dict())


# show all users

@app.route('/api/allusers', methods=['GET'])
def getallusers():
    chefs = User.query.all()
    return jsonify([chef.to_dict() for chef in chefs])




# adding Contacts

@app.route('/api/addcontacts/<int:id>', methods=['POST'])
def AddContacts(id):

    data = request.json
    username=data["username"]

    exist_contact = Contacts.query.filter_by(username=username)
    if id not in [exist.contact_id for exist in exist_contact]:
        contact = Contacts(username,id)
        db.session.add(contact)
        db.session.commit()

    return jsonify('Success from the backend')

#getting contacts

@app.route('/api/getcontacts', methods=['POST'])
def GetContacts():

    data = request.json
    username=data["username"]
    exist_contact = Contacts.query.filter_by(username=username)
    contactid=[exist.contact_id for exist in exist_contact]

    chefs = User.query.all()
    return jsonify([chef.to_dict() for chef in chefs if chef.id in contactid])




# Deleting a contact from contacts
@app.route('/api/contact/delete/<int:id>/<string:user>', methods=['DELETE'])
def deletecontact(id,user):
   
    
    contact = Contacts.query.filter_by(username=user,contact_id=id).first()
    db.session.delete(contact)
    db.session.commit()  

    exist_contact = Contacts.query.filter_by(username=user)
    contactid=[exist.contact_id for exist in exist_contact]

    chefs = User.query.all()
    return jsonify([chef.to_dict() for chef in chefs if chef.id in contactid])







# addFavourites

@app.route('/api/addfavourites/<int:id>', methods=['POST'])
def AddFavourites(id):

    data = request.json
    username=data["username"]
    exist_recipe = Favourites.query.filter_by(username=username)
    if id not in [exist.recipe_id for exist in exist_recipe]:
        favourite = Favourites(username,id)
        db.session.add(favourite)
        db.session.commit()
        fav = Recipes.query.filter_by(id=id).first()
        fav.favourite_status=1
        db.session.commit()
        return jsonify(fav.to_dict())
    else:
        fav=Favourites.query.filter_by(username=username,recipe_id=id).first()
        db.session.delete(fav)
        db.session.commit()
        fav = Recipes.query.filter_by(id=id).first()
        fav.favourite_status=0
        db.session.commit()
        return jsonify(fav.to_dict())


   
# getFavourites

    
@app.route('/api/getfavourites', methods=['POST'])
def GetFavourites():

    data = request.json
    username=data["username"]
    exist_favourites = Favourites.query.filter_by(username=username)
    recipeid=[exist.recipe_id for exist in exist_favourites]

    favs = Recipes.query.all()
    return jsonify([fav.to_dict() for fav in favs if fav.id in recipeid])


# Get profile
@app.route('/api/getprofile/<string:user>', methods=['GET'])
def GetProfile(user):

    current_user = User.query.filter_by(username=user).first()
    return jsonify(current_user.to_dict())

# Delete Account

@app.route('/api/account/delete/<string:user>', methods=['DELETE'])
def DeleteAccount(user):

    current_user = User.query.filter_by(username=user).first()
    db.session.delete(current_user)
    db.session.commit()
    

    recipe = Recipes.query.filter_by(username=user)
    if recipe:
        for reci in recipe:
            db.session.delete(reci)
            db.session.commit()
    
    commen = Comments.query.filter_by(user_name=user)
    if commen:
        for com in commen:
            db.session.delete(com)
            db.session.commit()

    likes = Likes.query.filter_by(username=user)     
    if likes:
        for like in likes:
            db.session.delete(like)
            db.session.commit()   

             
    favourite = Favourites.query.filter_by(username=user)     
    if favourite:
        for fav in favourite:
            db.session.delete(fav)
            db.session.commit() 

    contacts = Contacts.query.filter_by(username=user)     
    if contacts:
        for con in contacts:
            db.session.delete(con)
            db.session.commit()           
    
    return jsonify("Successful")