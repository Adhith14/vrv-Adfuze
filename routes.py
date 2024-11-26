from flask import flash, redirect, render_template, request, url_for, session
from app import app
from models import AdRequest, Campaign, Negotiation, db,User,Sponsor, Influencer
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from datetime import datetime
from sqlalchemy import func
import json


#decorator for auth_required for session check

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('login'))
    return wrapper

#-------------------------------------------index

@app.route('/')

def index():
    # return render_template('index.html')
    user_id = session.get('user_id')
    user = None
    user2 = None
    if user_id:
        user = User.query.get(user_id)
    return render_template('index.html', user=user, user2=user2)

#-------------------------------------------login

@app.route('/login')
def login():
    
    return render_template('login.html')

    # user=session.get('user_id')
    # if user:
    #     return redirect(url_for('profile'))
    # return render_template('login.html')


# -------------------------------------------login post
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.passhash, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    
    session['user_id'] = user.user_id
    flash('Login successful')
    return redirect(url_for('profile'))

# -------------------------------------------sponsor registration

@app.route('/sponsor-register')
def register():
    return render_template('sponsor-register.html')

# -------------------------------------------influencer registration

@app.route('/influencer-register')
def register2():
    return render_template('influencer-register.html')

# -------------------------------------------sponsor registration post
@app.route('/sponsor-register', methods=['POST'])
def register_sponsor():
    username=request.form.get('username')
    password=request.form.get('password')
    company=request.form.get('company')
    industry=request.form.get('industry')
    budget=request.form.get('budget')

    if not username or not password or not company or not industry or not budget:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('register_sponsor'))
    
    user=User.query.filter_by(username=username).first()

    if user:
        flash('Username already exists', 'error')
        return redirect(url_for('register_sponsor'))


    password_hash = generate_password_hash(password)
    
    new_user = User(username=username, passhash=password_hash, role='sponsor')
    db.session.add(new_user)
    db.session.commit()

    new_sponsor= Sponsor(sponsor_id=new_user.user_id,company_name=company, industry=industry, budget=budget)
    db.session.add(new_sponsor)
    db.session.commit()

    return redirect(url_for('login'))

#-------------------------------------------influencer registration post
@app.route('/influencer-register', methods=['POST'])
def register_influencer():
    username=request.form.get('username')
    password=request.form.get('password')
    name=request.form.get('name')
    category=request.form.get('category')
    niche=request.form.get('niche')
    reach=request.form.get('reach')

    if not username or not password or not name or not category or not niche or not reach:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('register_influencer'))
    
    user=User.query.filter_by(username=username).first()

    if user:
        flash('Username already exists', 'error')
        return redirect(url_for('register_influencer'))
    
    password_hash = generate_password_hash(password)

    new_user = User(username=username, passhash=password_hash, role='influencer')
    db.session.add(new_user)
    db.session.commit()

    new_influencer = Influencer(influencer_id=new_user.user_id, name=name, category=category, niche=niche, reach=reach)
    db.session.add(new_influencer)
    db.session.commit()

    return redirect(url_for('login'))

#-------------------------------------------profile user , user2 takes data from to diff table to show in profile

@app.route('/profile')
@auth_required
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.role == 'admin':
        return render_template('adminProfile.html', user=user)
    elif user.role == 'sponsor':
        sponsor=Sponsor.query.get(user_id)
        return render_template('sponsorProfile.html', user=user, user2=sponsor)
    else:
        influencer=Influencer.query.get(user_id)
        return render_template('influProfile.html', user=user, user2=influencer)
    
#-------------------------------------------edit profile
@app.route('/profile' , methods=['POST'])
@auth_required

def profile_post():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        return adminProfile_post()
    elif user.role == 'sponsor':
        return sponsorProfile_post()
    else:
        return influencerProfile_post()


def adminProfile_post():
    username=request.form.get('username')
    curr_password=request.form.get('curr_password')
    new_password=request.form.get('new_password')

    if not username or not curr_password or not new_password:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('profile'))
    user=User.query.get(session['user_id'])
    if not check_password_hash(user.passhash, curr_password):
        flash('Please enter correct current password', 'error')
        return redirect(url_for('profile'))
    if username!=user.username:
        new_username=User.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists', 'error')
            return redirect(url_for('profile'))
    
    new_password_hash = generate_password_hash(new_password)
    user.username=username
    user.passhash=new_password_hash
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('profile'))

def sponsorProfile_post():
    username=request.form.get('username')
    curr_password=request.form.get('curr_password')
    new_password=request.form.get('new_password')
    company=request.form.get('company')
    industry=request.form.get('industry')
    budget=request.form.get('budget')
    if not username or not curr_password or not new_password or not company or not industry or not budget:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('profile'))
    user=User.query.get(session['user_id'])
    sponsor=Sponsor.query.get(session['user_id'])
    if not check_password_hash(user.passhash, curr_password):
        flash('Please enter correct current password', 'error')
        return redirect(url_for('profile'))
    if username!=user.username:
        new_username=User.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists', 'error')
            return redirect(url_for('profile'))
    new_password_hash = generate_password_hash(new_password)
    user.username=username
    user.passhash=new_password_hash
    sponsor.company_name=company
    sponsor.industry=industry
    sponsor.budget=budget
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('profile'))


def influencerProfile_post():
    username=request.form.get('username')
    curr_password=request.form.get('curr_password')
    new_password=request.form.get('new_password')
    name=request.form.get('name')
    category=request.form.get('category')
    niche=request.form.get('niche')
    reach=request.form.get('reach')
    if not username or not curr_password or not new_password or not name or not category or not niche or not reach:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('profile'))
    user=User.query.get(session['user_id'])
    influencer=Influencer.query.get(session['user_id'])
    if not check_password_hash(user.passhash, curr_password):
        flash('Please enter correct current password', 'error')
        return redirect(url_for('profile'))
    if username!=user.username:
        new_username=User.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists', 'error')
            return redirect(url_for('profile'))
    new_password_hash = generate_password_hash(new_password)
    user.username=username
    user.passhash=new_password_hash
    influencer.name=name
    influencer.category=category
    influencer.niche=niche
    influencer.reach=reach
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('profile'))

#-------------------------------------------logout
@app.route('/logout')
@auth_required
def logout():
    session.pop('user_id')
    flash('You have been logged out')
    return redirect(url_for('login'))


#-------------------------------------------sponsor campaign
@app.route('/sponsor-campaign')
@auth_required
def sponsor_campaign():
    user_id = session.get('user_id')
    campaigns=Campaign.query.filter_by(sponsor_id=user_id, flag=False ).all()
    user = None
    user2 ="sponsor"
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/campaign.html', user=user, user2=user2, campaigns=campaigns)

@app.route('/campaign/add')
@auth_required
def add_campaign():
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/addcampaign.html', user=user, user2=user2)

@app.route('/campaign/add', methods=['POST'])
@auth_required
def add_campaign_post():
    campaignname = request.form.get('name')
    description = request.form.get('description')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    budget = request.form.get('budget')
    visibility = request.form.get('visibility')
    goals = request.form.get('goals')

    if not campaignname or not description or not start_date_str or not end_date_str or not budget or not visibility or not goals:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('add_campaign'))

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('add_campaign'))
    
    user_id = session['user_id']
    new_campaign = Campaign(sponsor_id=user_id, name=campaignname, description=description, start_date=start_date, end_date=end_date, budget=budget, visibility=visibility, goals=goals)    
    db.session.add(new_campaign)
    db.session.commit()
    flash('Campaign added successfully')
    return redirect(url_for('sponsor_campaign'))

                 #-------------------------------------------edit campaign

@app.route('/campaign/<int:id>/update')
@auth_required
def update_campaign(id):
    campaign=Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('sponsor_campaign'))
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/updatecampaign.html', campaign=campaign,user=user, user2=user2)

@app.route('/campaign/<int:id>/update', methods=['POST'])
@auth_required
def update_campaign_post(id):
    campaign=Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('sponsor_campaign'))
    campaignname = request.form.get('name')
    description = request.form.get('description')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    budget = request.form.get('budget')
    visibility = request.form.get('visibility')
    goals = request.form.get('goals')

    if not campaignname or not description or not start_date_str or not end_date_str or not budget or not visibility or not goals:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('update_campaign', id=id))
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('update_campaign', id=id))
    
    campaign.name=campaignname
    campaign.description=description
    campaign.start_date=start_date
    campaign.end_date=end_date
    campaign.budget=budget
    campaign.visibility=visibility
    campaign.goals=goals
    db.session.commit()
    flash('Campaign updated successfully')
    return redirect(url_for('sponsor_campaign'))

                    #-------------------------------------------delete campaign

@app.route('/campaign/<int:id>/delete')
@auth_required
def delete_campaign(id):
    campaign=Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('sponsor_campaign'))
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/deletecampaign.html', campaign=campaign, user=user, user2=user2)

@app.route('/campaign/<int:id>/delete', methods=['POST'])
@auth_required
def delete_campaign_post(id):
    campaign=Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found', 'error') 
        return redirect(url_for('sponsor_campaign'))
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully')
    return redirect(url_for('sponsor_campaign'))


#-------------------------------------------sponcer ad request
@app.route('/sponsor-adrequest')
@auth_required
def sponsor_adrequest():
    user_id = session.get('user_id')
    adrequests=AdRequest.query.join(Campaign).filter(Campaign.sponsor_id==user_id, AdRequest.flag==False).all()
    negotiations=Negotiation.query.filter_by(sponsor_id=user_id).all()
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/adrequest.html', user=user, user2=user2, adrequests=adrequests,negotiations=negotiations)

@app.route('/adrequest/add')
@auth_required
def add_adrequest():
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    campaigns=Campaign.query.filter_by(sponsor_id=user_id,flag=False).all()
    influencers=Influencer.query.filter_by(flag=False).all()
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/add_adrequest.html', user=user, user2=user2, campaigns=campaigns, influencers=influencers)

@app.route('/adrequest/add', methods=['POST'])
@auth_required

def add_adrequest_post():
    campaign_id = request.form.get('campaign_id')
    influencer_id = request.form.get('influencer_id')
    messages = request.form.get('messages')
    requirements = request.form.get('requirements')
    payment_amount = request.form.get('payment_amount')

    if not campaign_id or not influencer_id or not messages or not requirements or not payment_amount:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('add_adrequest'))

    user_id = session['user_id']
    new_adrequest = AdRequest(campaign_id=campaign_id, influencer_id=influencer_id, messages=messages, requirements=requirements, payment_amount=payment_amount)    
    db.session.add(new_adrequest)
    db.session.commit()
    flash('Ad Request added successfully')
    return redirect(url_for('sponsor_adrequest'))

                    #-------------------------------------------edit ad request
@app.route('/adrequest/<int:id>/update')
@auth_required
def update_adrequest(id):
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('sponsor_adrequest'))
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    campaigns=Campaign.query.filter_by(sponsor_id=user_id).all()
    influencers=Influencer.query.all()
    if user_id:
        user = User.query.get(user_id)
    return render_template('sponsorfunction/update_adrequest.html', adrequest=adrequest, user=user, user2=user2, campaigns=campaigns, influencers=influencers)

@app.route('/adrequest/<int:id>/update', methods=['POST'])
@auth_required
def update_adrequest_post(id):
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('sponsor_adrequest'))
    campaign_id = request.form.get('campaign_id')
    influencer_id = request.form.get('influencer_id')
    messages = request.form.get('messages')
    requirements = request.form.get('requirements')
    payment_amount = request.form.get('payment_amount')

    if not campaign_id or not influencer_id or not messages or not requirements or not payment_amount:
        flash('Please enter all the fields', 'error')
        return redirect(url_for('update_adrequest', id=id))
    
    adrequest.campaign_id=campaign_id
    adrequest.influencer_id=influencer_id
    adrequest.messages=messages
    adrequest.requirements=requirements
    adrequest.payment_amount=payment_amount
    db.session.commit()
    flash('Ad Request updated successfully')
    return redirect(url_for('sponsor_adrequest'))

                #-------------------------------------------delete ad request
@app.route('/adrequest/<int:id>/delete', methods=['POST'])
@auth_required
def delete_adrequest(id):
    adrequest = AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found')
        return redirect(url_for('sponsor_adrequest'))
    
    db.session.delete(adrequest)
    db.session.commit()
    flash('Ad Request deleted successfully')
    return redirect(url_for('sponsor_adrequest'))

#-------------------------------------------show influencer
@app.route('/influencer')
@auth_required
def allinfluencer():
    user_id = session.get('user_id')
    influencers=Influencer.query.filter_by(flag=False).all()
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)

    paramameter = request.args.get('parameter')
    query = request.args.get('query')
    if paramameter and query:
        if paramameter == 'category':
            influencers = Influencer.query.filter(Influencer.category.ilike(f'%{query}%'), Influencer.flag==False).all()
        elif paramameter == 'niche':
            influencers = Influencer.query.filter(Influencer.niche.ilike(f'%{query}%'), Influencer.flag==False).all()
        elif paramameter == 'reach':
            influencers = Influencer.query.filter(Influencer.reach >= query, Influencer.flag==False).all()
    
    return render_template('sponsorfunction/allinfluencers.html', user=user, user2=user2, influencers=influencers)


#-------------------------------------------influencer function

@app.route('/publiccampaign')
@auth_required
def publiccampaign():
    user_id = session.get('user_id')
    campaigns=Campaign.query.filter_by(flag=False, visibility='public').all()
    user = None
    user2 = "influencer"
    if user_id:
        user = User.query.get(user_id)

    parameter = request.args.get('parameter')
    query = request.args.get('query')
    if parameter and query:
        if parameter == 'campaign':
            campaigns = Campaign.query.filter(Campaign.name.ilike(f'%{query}%'), Campaign.flag==False, Campaign.visibility=='public').all()
        elif parameter == 'budget':
            campaigns = Campaign.query.filter(Campaign.budget >= query, Campaign.flag==False, Campaign.visibility=='public').all()
    return render_template('influencerfunction/publiccampaign.html', user=user, user2=user2, campaigns=campaigns)

#-------------------------------------------influencer show ad request

@app.route('/alladrequest')
@auth_required
def alladrequest():
    user_id = session.get('user_id')
    adrequests = AdRequest.query.filter_by(flag=False, influencer_id=user_id).filter(AdRequest.status.in_(['pending', 'accepted','negotiating'])).all()
    
    user = None
    user2 = "influencer"
    if user_id:
        user = User.query.get(user_id)
    return render_template('influencerfunction/alladrequest.html', user=user, user2=user2, adrequests=adrequests)

#-------------------------------------------influencer accept ad request
@app.route('/adrequest/<int:id>/accept')
@auth_required
def accept_adrequest(id):
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('alladrequest'))
    adrequest.status='accepted'
    db.session.commit()
    flash('Ad Request accepted successfully')
    return redirect(url_for('alladrequest'))

#-------------------------------------------influencer reject ad request
@app.route('/adrequest/<int:id>/reject', methods=['POST'])
@auth_required
def reject_adrequest(id):
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('alladrequest'))
    adrequest.status='rejected'
    db.session.commit()
    flash('Ad Request rejected successfully')
    return redirect(url_for('alladrequest'))

#-------------------------------------------influencer negotiate ad request
@app.route('/adrequest/<int:id>/negotiate')
@auth_required
def nego_adrequest(id):
    user_id = session.get('user_id')
    user = None
    user2 = "influencer"
    if user_id:
        user = User.query.get(user_id)
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('alladrequest'))
    return render_template('influencerfunction/negotiate.html', user=user, user2=user2, adrequest=adrequest)

@app.route('/adrequest/<int:id>/negotiate', methods=['POST'])
@auth_required
def nego_adrequest_post(id):
    adrequest = AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('alladrequest'))
    
    counter_price = request.form.get('counter_price')
    user_id = session['user_id']

    # Check if a negotiation already exists for this ad request
    negotiation = Negotiation.query.filter_by(ad_request_id=id).first()
    
    if negotiation:
        # Update the existing negotiation
        negotiation.counter_price = counter_price
        flash('Negotiation updated successfully')
    else:
        # Create a new negotiation
        new_negotiation = Negotiation(
            ad_request_id=id,
            sponsor_id=adrequest.campaign.sponsor_id,
            influencer_id=user_id,
            initial_price=adrequest.payment_amount,
            counter_price=counter_price
        )
        db.session.add(new_negotiation)
        adrequest.status = 'negotiating'
        flash('Negotiation started successfully')
    
    db.session.commit()
    return redirect(url_for('alladrequest'))

# @app.route('/adrequest/<int:id>/negotiate', methods=['POST'])
# @auth_required
# def nego_adrequest_post(id):
#     adrequest=AdRequest.query.get(id)
#     if not adrequest:
#         flash('Ad Request not found', 'error')
#         return redirect(url_for('alladrequest'))
#     counter_price = request.form.get('counter_price')
    
#     user_id = session['user_id']
#     new_negotiation = Negotiation(ad_request_id=id, sponsor_id=adrequest.campaign.sponsor_id, influencer_id=user_id, initial_price=adrequest.payment_amount, counter_price=counter_price)    
#     db.session.add(new_negotiation)
#     db.session.commit()

#     adrequest.status='negotiating'
#     db.session.commit()
    
#     flash('Negotiation started successfully')
#     return redirect(url_for('alladrequest'))

#-------------------------------------------admin dashboard

@app.route('/admin-dashboard/allusers')
@auth_required
def allusers():
    user_id = session.get('user_id')
    users=User.query.all()
    user = None
    user2 = "admin"
    if user_id:
        user = User.query.get(user_id)
    influencers=Influencer.query.all()
    sponsors=Sponsor.query.all()
    campaigns=Campaign.query.all()
    adrequests=AdRequest.query.all()
    return render_template('admindashboard/allusers.html', user=user, user2=user2, users=users, influencers=influencers, sponsors=sponsors, campaigns=campaigns, adrequests=adrequests)

#-------------------------------------------admin flag users

@app.route('/admin-dashboard/flaguser/<int:id>', methods=['POST'])
@auth_required
def flaguser(id):
    user=User.query.get(id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('allusers'))
    role=user.role
    if role=='influencer':
        influencer=Influencer.query.get(id)
        if influencer.flag:
            influencer.flag=False
        else:
            influencer.flag=True
    elif role=='sponsor':
        sponsor=Sponsor.query.get(id)
        if sponsor.flag:
            sponsor.flag=False
        else:
            sponsor.flag=True
    db.session.commit()
    flash('Flag Updated Successfully')
    return redirect(url_for('allusers'))

#-------------------------------------------admin flag campaign
@app.route('/admin-dashboard/flagcampaign/<int:id>', methods=['POST'])
@auth_required
def flagcampaign(id):
    campaign=Campaign.query.get(id)
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('allusers'))
    if campaign.flag:
        campaign.flag=False
    else:
        campaign.flag=True
    db.session.commit()
    flash('Flag Updated Successfully')  
    return redirect(url_for('allusers'))

#-------------------------------------------admin flag ad request
@app.route('/admin-dashboard/flagadrequest/<int:id>', methods=['POST'])
@auth_required
def flagadrequest(id):
    adrequest=AdRequest.query.get(id)
    if not adrequest:
        flash('Ad Request not found', 'error')
        return redirect(url_for('allusers'))
    if adrequest.flag:
        adrequest.flag=False
    else:
        adrequest.flag=True
    db.session.commit()
    flash('Flag Updated Successfully')
    return redirect(url_for('allusers'))



#-------------------------------------------Statistics

#-------------------------------------------admin statistics

@app.route('/admin-dashboard/statistics')
@auth_required
def statistics():
    user_id = session.get('user_id')
    user = None
    user2 = "admin"
    if user_id:
        user = User.query.get(user_id)
    
    # Fetching counts for flagged and unflagged users and ad requests
    flagged_users_count = {
        'sponsors': Sponsor.query.filter_by(flag=True).count(),
        'influencers': Influencer.query.filter_by(flag=True).count()
    }
    unflagged_users_count = {
        'sponsors': Sponsor.query.filter_by(flag=False).count(),
        'influencers': Influencer.query.filter_by(flag=False).count()
    }
    flagged_adrequests_count = AdRequest.query.filter_by(flag=True).count()
    unflagged_adrequests_count = AdRequest.query.filter_by(flag=False).count()
    
    # Fetching campaigns data
    total_campaigns_count = Campaign.query.count()
    public_campaigns_count = Campaign.query.filter_by(visibility='public').count()
    private_campaigns_count = Campaign.query.filter_by(visibility='private').count()
    flagged_campaigns_count = Campaign.query.filter_by(flag=True).count()
    unflagged_campaigns_count = Campaign.query.filter_by(flag=False).count()
    
    # Fetching user data
    total_sponsors_count = Sponsor.query.count()
    total_influencers_count = Influencer.query.count()
    
    return render_template(
        'admindashboard/adminstat.html', 
        user=user, 
        user2=user2, 
        flagged_users_count=json.dumps(flagged_users_count),
        unflagged_users_count=json.dumps(unflagged_users_count),
        flagged_adrequests_count=flagged_adrequests_count,
        unflagged_adrequests_count=unflagged_adrequests_count,
        total_campaigns_count=total_campaigns_count,
        public_campaigns_count=public_campaigns_count,
        private_campaigns_count=private_campaigns_count,
        flagged_campaigns_count=flagged_campaigns_count,
        unflagged_campaigns_count=unflagged_campaigns_count,
        total_sponsors_count=total_sponsors_count,
        total_influencers_count=total_influencers_count
    )

#-------------------------------------------sponsor statistics


@app.route('/sponsor-dashboard/statistics')
@auth_required
def sponsorstat():
    user_id = session.get('user_id')
    user = None
    user2 = "sponsor"
    if user_id:
        user = User.query.get(user_id)
    
    campaigns = Campaign.query.filter_by(sponsor_id=user_id).all()
    adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == user_id).all()
    
    ad_request_status_counts = db.session.query(
        AdRequest.status, func.count(AdRequest.status)
    ).join(Campaign).filter(Campaign.sponsor_id == user_id).group_by(AdRequest.status).all()
    ad_request_status_counts = [{'status': status, 'count': count} for status, count in ad_request_status_counts]
    
    campaign_creation_dates = db.session.query(
        func.strftime('%Y-%m', Campaign.start_date), func.count(Campaign.campaign_id)
    ).filter(Campaign.sponsor_id == user_id).group_by(func.strftime('%Y-%m', Campaign.start_date)).all()
    campaign_creation_dates = [{'date': date, 'count': count} for date, count in campaign_creation_dates]
    
    return render_template(
        'sponsorfunction/sponsorstat.html', 
        user=user, 
        user2=user2, 
        campaigns=campaigns, 
        adrequests=adrequests, 
        ad_request_status_counts=json.dumps(ad_request_status_counts), 
        campaign_creation_dates=json.dumps(campaign_creation_dates)
    )
#-------------------------------------------influencer statistics

@app.route('/influencer-dashboard/statistics')
@auth_required
def influencerstat():
    user_id = session.get('user_id')
    user = None
    user2 = "influencer"
    if user_id:
        user = User.query.get(user_id)
    
    # Fetch ad requests and negotiations
    adrequests = AdRequest.query.filter_by(influencer_id=user_id).all()
    negotiations = Negotiation.query.filter_by(influencer_id=user_id).all()
    
    # Fetch ad request status counts
    ad_request_status_counts = db.session.query(
        AdRequest.status, func.count(AdRequest.status)
    ).filter(AdRequest.influencer_id == user_id).group_by(AdRequest.status).all()
    ad_request_status_counts = [{'status': status, 'count': count} for status, count in ad_request_status_counts]
    
    return render_template(
        'influencerfunction/influstat.html', 
        user=user, 
        user2=user2, 
        adrequests=adrequests, 
        negotiations=negotiations, 
        ad_request_status_counts=json.dumps(ad_request_status_counts)
    )
