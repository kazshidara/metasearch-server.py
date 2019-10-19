
@app.route("/user-ratings.json")
def return_user_ratings():
    """Returns all the ratings that a user made to display on a chart."""
    
    user_id = session.get('user_id')

    user = User.query.options(db.joinedload('ratings')).get(user_id)
    
    job_object = db.session.query(Job, Rating).join(Rating, Job.job_id == Rating.job_id).filter(Rating.user_id==f'{user_id}').all()
    
    # Each point in the graph will represent:
    #  company name
    #  job title
    #  location

    user_ratings = []

    for job in job_object:    

        user_ratings.append({
            "title" : job[0].title,
            "company" : job[0].company,
            "location" : job[0].location,
            "rating" : job[1].rating
            })


        #create a new list that has all the job objects that user has rated already
        #user.ratings = all the ratings that specific user has rated 
    jobs_rated = user.ratings
    
    ratings_list = []
    
    for rating in jobs_rated:
        ratings_list.append(rating.rating)
    
    # # x_axis has the number of ratings the user has made, counting the number using indices
    x_axis = []
    for i,rating in enumerate(user_ratings):
        x_axis.append(i+1)


    data_dict = {
                "data_points" : user_ratings,
                "labels": x_axis,
                "datasets": [
                    {
                        "data": ratings_list,
                        "backgroundColor": [
                            "#99d8c9"],
                        "hoverBackgroundColor": [
                            "#FF6384" for color in x_axis]
                    }]
            }
 
    return jsonify(data_dict)   #data_dict is what gets passed into JS function(data)

