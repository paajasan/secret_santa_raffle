#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import smtplib
import getpass

# Import the email modules we'll need
from email.message import EmailMessage


def laheta(nimi, sapo, server):
    msg = EmailMessage()
    msg.set_content("You are the secret santa for %s\n\n Kindest regards\nSanterin koodi\n\n\n\n"%nimi +\
                    "---------------------" +\
                    "This is an automated message, please do not reply or mörökölli will viedä you")
    msg['Subject'] = 'Secret santa raffle'
    msg['From'] = "erkki.esimerkki@domain.com"
    msg['To'] = sapo

    server.send_message(msg)


def get_contacts(fname):
    nimet = []
    sapot = []
    with open(fname) as f:
        for line in f:
            if(not line.strip() or line.strip().startswith("#")):
                continue
            parts = line.split()
            nimet.append(parts[0])
            sapot.append(parts[1])

    return nimet, sapot


def arvo(nimet, sapot):
    ostettava = []

    valinnat = nimet.copy()


    for i in range(len(nimet)):
        c = random.choice(valinnat)
        while c == nimet[i]:
            if(len(valinnat)==1):
                print("Arvotaan ostajalle %s, mutta vain hän jäljellä")
                print("Arvotaanpas uudelleen")
                return arvo(nimet, sapot)
            c = random.choice(valinnat)
        ostettava.append(c)
        valinnat.remove(c)

    return ostettava, sapot


def send(ostettava, sapot):
    # This example works for helsinki.fi emails. Change to match your server.
    s = smtplib.SMTP("smtp.helsinki.fi", port=587)
    s.starttls()
    print("Authenticating helsinki.fi office365 service")
    s.login(input("AD-tunnus: ")+"@ad.helsinki.fi", getpass.getpass("Salakala: "))

    for ostett, sapo in zip(ostettava, sapot):
        laheta(ostett, sapo, s)

    s.quit()


def print_debug(ostettava, sapot):
    for ostett, sapo in zip(ostettava, sapot):
        print(ostett, sapo)


if __name__ == '__main__':
    # Get random seed from e.g. random.org and put here. Allows for reproducing in case of problems.
    random.seed(340338373)
    nimet, sapot = get_contacts("nimet_ja_sapot.txt")
    ostettava, ostaja_sapo = arvo(nimet,sapot)
    # Send the results
    #send(ostettava, sapot)
    # Only print
    print_debug(ostettava, ostaja_sapo)
