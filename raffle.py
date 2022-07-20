#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import smtplib
import getpass

# Import the email modules we'll need
from email.message import EmailMessage


def send_email(name, email, server):
    msg = EmailMessage()
    msg.set_content("You are the secret santa for %s\n\n Kindest regards\nSanterin koodi\n\n\n\n"%name +\
                    "---------------------" +\
                    "This is an automated message, please do not reply or mörökölli will viedä you")
    msg['Subject'] = 'Secret santa raffle'
    msg['From'] = "erkki.esimerkki@domain.com"
    msg['To'] = email

    server.send_message(msg)


def get_contacts(fname):
    names= []
    emails = []
    with open(fname) as f:
        for line in f:
            if(not line.strip() or line.strip().startswith("#")):
                continue
            parts = line.split()
            names.append(parts[0])
            emails.append(parts[1])

    return names, emails


def raffle(names, emails):
    # shuffle data together
    data = list(zip(names, emails))
    random.shuffle(data)
    names_shuffl, email_shuffl = list(zip(*data))

    # Shift emails by one
    new_emails = list(email_shuffl[1:])
    new_emails.append(email_shuffl[0])

    return names_shuffl, new_emails


def send(names, emails):
    # This example works for helsinki.fi emails. Change to match your server.
    s = smtplib.SMTP("smtp.helsinki.fi", port=587)
    s.starttls()
    print("Authenticating helsinki.fi office365 service")
    s.login(input("AD-tunnus: ")+"@ad.helsinki.fi", getpass.getpass("Salakala: "))

    for name, email in zip(names, emails):
        send_email(name, email, s)

    s.quit()


def print_debug(names, emails):
    for name, email in zip(names, emails):
        print(name, email)


if __name__ == '__main__':
    # Get random seed from e.g. random.org and put here. Allows for reproducing in case of problems.
    # Comment to have unreproducible results
    random.seed(1337)
    names, emails = get_contacts("names_and_emails.txt")
    buyee_names, buyer_emails = raffle(names,emails)
    # Send the results
    #send(buyee_names, buyer_emails)
    # Only print
    print_debug(buyee_names, buyer_emails)
