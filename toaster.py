import os
import requests
import json
from colorama import Fore, Style, init
import base64
import hashlib

# Initialize colorama
init()

def send_message(webhook_url, content):
    headers = {'Content-Type': 'application/json'}
    data = {'content': content}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 204:
        print(Fore.GREEN + "[+] Message sent successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Error sending message. Status code: {response.status_code}" + Style.RESET_ALL)

def change_webhook_name(webhook_url, new_name):
    headers = {'Content-Type': 'application/json'}
    data = {'name': new_name}
    response = requests.patch(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(Fore.GREEN + f"[+] Webhook name changed to: {new_name}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Error changing webhook name. Status code: {response.status_code}" + Style.RESET_ALL)

def upload_avatar(avatar_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(avatar_url, headers=headers)

    if response.status_code == 200:
        with open('avatar.png', 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Error downloading avatar. Status code: {response.status_code}")
        return False

def get_avatar_hash():
    with open('avatar.png', 'rb') as f:
        avatar_bytes = f.read()
        avatar_base64 = base64.b64encode(avatar_bytes).decode('utf-8')

        hash_object = hashlib.sha1(avatar_bytes)
        hex_dig = hash_object.hexdigest()

        return f'data:image/png;base64,{avatar_base64}', hex_dig

def change_webhook_avatar(webhook_url, avatar_url):
    avatar_downloaded = upload_avatar(avatar_url)

    if avatar_downloaded:
        avatar_data, avatar_hash = get_avatar_hash()

        headers = {'Content-Type': 'application/json'}
        data = {'avatar': avatar_data}
        response = requests.patch(webhook_url, headers=headers, json=data)

        if response.status_code == 200:
            print(Fore.GREEN + f"[+] Webhook avatar changed." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error changing webhook avatar. Status code: {response.status_code}" + Style.RESET_ALL)

        os.remove('avatar.png')  # Clean up the downloaded avatar file

def display_ascii_ui():
    print(
        Fore.MAGENTA +
"""
 ________                               __                               
/        |                             /  |                              
$$$$$$$$/______    ______    _______  _$$ |_     ______    ______        
   $$ | /      \  /      \  /       |/ $$   |   /      \  /      \       
   $$ |/$$$$$$  | $$$$$$  |/$$$$$$$/ $$$$$$/   /$$$$$$  |/$$$$$$  |      
   $$ |$$ |  $$ | /    $$ |$$      \   $$ | __ $$    $$ |$$ |  $$/       
   $$ |$$ \__$$ |/$$$$$$$ | $$$$$$  |  $$ |/  |$$$$$$$$/ $$ |            
   $$ |$$    $$/ $$    $$ |/     $$/   $$  $$/ $$       |$$ |            
   $$/  $$$$$$/   $$$$$$$/ $$$$$$$/     $$$$/   $$$$$$$/ $$/             
                                                       by Toasty8i                  
                                                                         
""" + Style.RESET_ALL
    )

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_webhook_info(webhook_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(webhook_url, headers=headers)

    if response.status_code == 200:
        webhook_data = response.json()
        print(Fore.CYAN + f"Name: {webhook_data['name']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"Guild ID: {webhook_data['guild_id']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"Channel ID: {webhook_data['channel_id']}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Error retrieving webhook information. Status code: {response.status_code}" + Style.RESET_ALL)

def delete_webhook(webhook_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(webhook_url, headers=headers)

    if response.status_code == 204:
        print(Fore.GREEN + "[+] Webhook deleted successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Error deleting webhook. Status code: {response.status_code}" + Style.RESET_ALL)

if __name__ == "__main__":
    webhook_url = ""
    webhook_name = ""
    webhook_avatar = ""  # Added variable for webhook avatar
    
    while True:
        clear_console()
        display_ascii_ui()
        print(Fore.MAGENTA + "\nSelect an option:" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Set Webhook URL")
        print(Fore.BLUE + "2. Webhook Sender")
        print(Fore.GREEN + "3. Get Webhook Info")
        print(Fore.RED + "4. Delete Webhook")
        print(Fore.LIGHTGREEN_EX + "5. Change Webhook Avatar" + Style.RESET_ALL)  # Adjusted formatting
        print(Fore.LIGHTMAGENTA_EX + "6. Change Webhook Name" + Style.RESET_ALL)  # Added Option 6
        print(Fore.CYAN + "7. Exit" + Style.RESET_ALL)

        choice = input("> ")

        if choice == "1":
            webhook_url = input("Enter the webhook URL: ")
        elif choice == "2":
            if webhook_url:
                message_content = input("Enter the message content: ")
                num_messages = int(input("Enter the number of messages to send: "))

                for i in range(num_messages):
                    send_message(webhook_url, message_content)
            else:
                print(Fore.RED + "Webhook URL not set. Please use Option 1 to set it." + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "3":
            if webhook_url:
                get_webhook_info(webhook_url)
                input("Press Enter to return to the selection UI...")
            else:
                print(Fore.RED + "Webhook URL not set. Please use Option 1 to set it." + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "4":
            if webhook_url:
                delete_webhook(webhook_url)
                webhook_url = ""  
                input("Press Enter to return to the selection UI...")
            else:
                print(Fore.RED + "Webhook URL not set. Please use Option 1 to set it." + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "5":
            if webhook_url:
                webhook_avatar = input("Enter the new avatar URL: ")
                change_webhook_avatar(webhook_url, webhook_avatar)
            else:
                print(Fore.RED + "Webhook URL not set. Please use Option 1 to set it." + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "6":
            if webhook_url:
                new_name = input("Enter the new webhook name: ")
                change_webhook_name(webhook_url, new_name)
            else:
                print(Fore.RED + "Webhook URL not set. Please use Option 1 to set it." + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "7":
            print(Fore.MAGENTA + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
