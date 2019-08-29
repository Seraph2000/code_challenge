#endpoints:


##/register
###methods=['POST', 'GET']

**to do: 
add methods PUT, DELETE, so that user can update their:**

###password, payment details, address


##/reserve
###methods=['POST', 'GET']

**to do:
add methods PUT, DELETE, so that user can cancel reservation**


##/purchased
###methods=['GET']



#EDGE CASES:

##register()

- valid email address
- valid postal address
- unique name, not already in database

##reserve()

- user needs to be logged in to view page
- 0 < tickets <= 5
- if user doesn't order a ticket, value of purchased_ticket=False, ticket_id=0
- 0 > # users in db

##purchased()

- purchased\_ticket=True or purchased_ticket=False
- payment needs to be successful
- user needs to be logged in to view page