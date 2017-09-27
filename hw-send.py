#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
    Berke Emrecan Arslan <berke@beremaran.com>

    140315025
    Faculty of Engineering, Computer Science & Engineering
    Manisa Celal Bayar University

    Taken from;
    https://github.com/beremaran/cbu-cse3113
'''

import httplib2
import base64
import sys
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'CSE3113 Homework Sender'

MY_EMAIL = "beremaran@gmail.com"
INSTRUCTOR_MAIL = "sukruozan@gmail.com"
STUDENT_ID = "140315025"
COURSE_ID = "CSE3113"


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    secret_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if flags:
        #credentials = tools.run_flow(flow, store, None)
        # else:
        credentials = tools.run(flow, store)

    return credentials


def create_message(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    fp = open(file, 'r')
    msg = MIMEText(fp.read(), _subtype='text')
    fp.close()

    msg.add_header('Content-Disposition', 'attachmnet',
                   filename=get_filename())
    message.attach(msg)

    return {
        'raw': base64.urlsafe_b64encode(bytes(message.as_string(), "ascii")).decode('ascii')
    }


def send_message(service, user_id, message):
    message = service.users().messages().send(
        userId=user_id, body=message).execute()
    print('Message Id: %s' % message['id'])
    return message


def get_week(a):
    return a[2:-3]


def get_subject():
    return "{} HW{} {}".format(COURSE_ID, get_week(sys.argv[1]), STUDENT_ID)


def get_filename():
    return "{}HW{}.py".format(STUDENT_ID, get_week(sys.argv[1]))


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    msg = create_message(
        MY_EMAIL, INSTRUCTOR_MAIL, get_subject(),
        u"Composed by CSE3113 HW Composer.", sys.argv[1]
    )
    send_message(service, 'me', msg)


if __name__ == "__main__":
    main()
