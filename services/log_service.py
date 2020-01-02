from datetime import datetime

def log_new_user(my_account):
    now = datetime.utcnow().replace(microsecond=0)
    log_note = f'LOG>{now}>NEW_ACCOUNT_REGISTERED>{my_account.fname}>{my_account.lname}>{my_account.phone}'
    with open("logs/full.txt", "a") as f:
        f.write('\n')
        f.write(log_note)
    print(log_note)

def log_error_new_user(e):
    now = datetime.utcnow().replace(microsecond=0)
    log_note = f'LOG>{now}>ERROR>NEW_ACCOUNT_REGISTERED>{e}'
    with open("logs/full.txt", "a") as f:
        f.write('\n')
        f.write(log_note)
    print(log_note)

def log_new_route(my_route):
    now = datetime.utcnow().replace(microsecond=0)
    log_note = f'LOG>{now}>NEW_ROUTE>{my_route.id}>{my_route.phone}>{my_route.start_location}>{my_route.end_location}'
    with open("logs/full.txt", "a") as f:
        f.write('\n')
        f.write(log_note)
    print(log_note)

def log_run_route(my_route, response):
    now = datetime.utcnow().replace(microsecond=0)
    log_note = f'LOG>{now}>RUN_ROUTE>{my_route.id}>{my_route.phone}>\
        {my_route.start_location}>{my_route.end_location}\n\
            {response}'
    with open("logs/full.txt", "a") as f:
        f.write('\n')
        f.write(log_note)
    print(log_note)


