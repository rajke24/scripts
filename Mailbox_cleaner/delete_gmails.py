from imapclient import IMAPClient
from datetime import datetime
import os

def delete_msg(unseen_for_days=0):
    mailbox = IMAPClient('imap.gmail.com', ssl=True, port=993)
    EMAIL_ADRESS = os.environ.get('GMAIL')
    EMAIL_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
    mailbox.login(EMAIL_ADRESS, EMAIL_PASSWORD)
    inbox_mails = mailbox.select_folder('INBOX')
    print('You have total number %d of mails in your inbox' % inbox_mails[b'EXISTS'])
    seen_msg = mailbox.search('SEEN')
    mailbox.delete_messages(seen_msg)
    print(f'{len(seen_msg)} already seen messages has been deleted')
    unseen_msg = mailbox.search('UNSEEN')
    no_unseen_deleted = 0
    unseen_del = []
    for id, data in mailbox.fetch(unseen_msg, ['INTERNALDATE']).items():
        date_of_recipt = data[b'INTERNALDATE']
        delta = (datetime.now() - date_of_recipt).days
        if delta > unseen_for_days:
            unseen_del.append(id)
            no_unseen_deleted += 1
    if no_unseen_deleted > 0:
        mailbox.delete_messages(unseen_del)

    print(f'{no_unseen_deleted} unseen_del for more than {unseen_for_days} days mails deleted.')
    mailbox.logout()