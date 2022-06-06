def send_email(to_who, parsed_msg):
    return requests.post(
            'https://api.mailgun.net/v3/sandbox8a5127e16fc94bffa137de60a7f181ca.mailgun.org',
            auth=('api', '49ae72b3019b77348d609e506d3cd0eb-523596d9-a73e3e85'),
            data={'from': 'postmaster@sandbox8a5127e16fc94bffa137de60a7f181ca.mailgun.org',
                'to': to_who,
                'subject': 'Password Reset Instructions',
                'text': parsed_msg})
