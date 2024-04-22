import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Define the search function
def search(update, context):
    # Get the search query from the user's message
    query = update.message.text

    # If the user typed the "/search" command, remove it from the query

    results = []

    # Search the JSON file for the query in the full_name, post, phones, and comment fields
    for item in data:
        if query in item['email']\
            or query in item['no_hp']:
            results.append(item)

    
    # Send the search results to the user
    if results:
        for result in results:
            message = f"Nama: {result['nama']}\n" \
                      f"DOB :  {result['dob']}\n" \
                      f"Email :  {result['email']}\n" \
                      f"No HP :  {result['no_hp']}\n" \
                      f"Alamat :  {result['alamat']}\n" \
                      
            update.message.reply_text(message)
    else:
        update.message.reply_text("No results found.")

# Define the add contact function
def add_contact(update, context):
    # Get the contact information from the user's message
    contact_info = update.message.text.split(';')

    # Create a new contact dictionary
    new_contact = {
        'nama': contact_info[0][5:],  # Remove the first 5 characters ("/add ")
        'nohp': contact_info[1],
        'email': contact_info[2].split(','),
        'dob': contact_info[3] if len(contact_info) >= 4 else ''
    }

    # Add the new contact to the JSON file
    data.append(new_contact)
    with open('bos.json', 'w') as f:
        json.dump(data, f, indent=4)

    update.message.reply_text("Contact added.")

# Define the edit contact function
def edit_contact(update, context):
    # Get the contact information from the user's message
    contact_info = update.message.text.split(';')

    # Find the contact to edit by full_name
    contact_to_edit = None
    for contact in data:
        if contact['nama'] == contact_info[0]:
            contact_to_edit = contact
            break

    # Update the contact if it exists
    if contact_to_edit:
        contact_to_edit['nama'] = contact_info[1]
        contact_to_edit['email'] = contact_info[2]
        contact_to_edit['nohp'] = contact_info[3] if len(contact_info) >= 4 else ''
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        update.message.reply_text("Info changed.")
    else:
        update.message.reply_text("No results found.")

# Set up the Telegram bot
updater = Updater('7129357711:AAGq1DgpRDiisbo704-t4ZiAv1t_ZA6kg18', use_context=True)
dispatcher = updater.dispatcher

# Add the search command handler
search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

# Add the add contact command handler
add_contact_handler = CommandHandler('add', add_contact)
dispatcher.add_handler(add_contact_handler)

# Add the message handler to handle all incoming messages
message_handler = MessageHandler(Filters.text, search)
dispatcher.add_handler(message_handler)

# Add the edit contact command handler
edit_contact_handler = CommandHandler('edit', edit_contact)
dispatcher.add_handler(edit_contact_handler)


# Start the bot
updater.start_polling()
