import datetime
import os
import re
import smtplib
from email.message import EmailMessage
from facebook_scraper import get_posts
from secrets import fb_login, fb_pass, group_id

# Get enviroment variables necessary to proper operation of smtplib
EMAIL_ADRESS = os.environ.get('GMAIL')
EMAIL_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

# Process every post 
for post in get_posts(group= group_id, pages=20,credentials=(fb_login, fb_pass)):
    post_date = post['time']
    text = post['text']

    # Check if post date obtained correctly 
    if post_date != None:
        actual_date = datetime.datetime.now()
        timedelta = actual_date - post_date
        if timedelta.total_seconds() > 3600: continue
    else: post_date = ''
    
    # Check if post cointains any text
    if text == None or text == '': continue
    else:   
        # Check if text contains word 'inwentaryzacja'
        if re.search(r'inwentaryzacj\w+', text):
            # Create email message
            msg = EmailMessage()
            msg['Subject'] = 'OFERTA PRACY - INWENTARYZACJA'
            msg['To'] = (', ').join([EMAIL_ADRESS, 'pietrzakd53@gmail.com'])
            msg['From'] = EMAIL_ADRESS
            if post['post_url']: post_url = post['post_url'] 
            else: post_url = ''
            content = f'''{post_date}

                        {text}
            
                        {post_url}'''

            msg.set_content(content)

            # msg.add_alternative("""
            
            # """, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

