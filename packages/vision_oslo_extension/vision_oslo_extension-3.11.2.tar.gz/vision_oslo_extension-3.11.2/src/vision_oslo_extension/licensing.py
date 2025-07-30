#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Nov 2023
# Last Modified: Feb 2024
#=================================================================
# Copyright (c) 2024 [Jieming Ye]
#
# This Python source code is licensed under the 
# Open Source Non-Commercial License (OSNCL) v1.0
# See LICENSE for details.
#=================================================================
"""
Pre-requisite: 
N/A
Used Input:
N/A
Expected Output:
True/Flase
Description:
This module is the license process

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import os
import uuid
import requests
import psutil
from datetime import datetime, timedelta

from vision_oslo_extension.shared_contents import SharedVariables
from vision_oslo_extension.shared_contents import SharedMethods

# Constants for file path
LICENSE_FILE = SharedVariables.license_file

# Function to get the MAC address of the current machine
def get_mac_address():
    mac_addresses = []
    try:
        # mac_code = uuid.UUID(int=uuid.getnode()).hex[-12:]
        # mac = ":".join([mac_code[e:e+2] for e in range(0, 11, 2)])        
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:  # AF_LINK corresponds to MAC addresses
                    # mac_addresses.append((interface, addr.address)) # Return interface name and MAC address
                    mac_addresses.append(addr.address)

    except Exception as e:
        SharedMethods.print_message(f"ERROR: Fail to read mac address: {e}","31")

    return mac_addresses

# Function to fetch the allowed MAC addresses from an online file
def fetch_allowed_macs(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check for HTTP errors
        lines = response.text.splitlines()
        
        allowed_macs = []

        # Process each line
        for line in lines:
            line = line.strip()
            # Ignore lines that start with '//'
            if line.startswith("//"):
                continue
            # If the line looks like a MAC address (e.g., xx-xx-xx-xx-xx-xx)
            if len(line) == 17 and all(c in "0123456789ABCDEFabcdef-:" for c in line):
                # # Convert MAC to lowercase and replace '-' with ':'
                # formatted_mac = line.lower().replace('-', ':')
                allowed_macs.append(line)

        return allowed_macs
    
    except requests.exceptions.Timeout:
        SharedMethods.print_message("ERROR: Request timed out after 5 seconds. POOR INTERNET...", "31")
        return []
    
    except Exception as e:
        SharedMethods.print_message(f"ERROR: Error fetching allowed MAC addresses: {e}","31")
        return []

# Function to check if the MAC address is allowed
def is_mac_allowed(mac_address, allowed_macs):
    # if any mac address in the list is allowed, return True
    for mac in mac_address:
        if mac in allowed_macs:
            return True
    # if no mac address in the list is allowed, return False
    return False

# Function to read from the license file
def read_license_file():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    status = lines[0].strip()
                    expiry_date_str = lines[1].strip()
                    unique_key = lines[2].strip()
                    return status, expiry_date_str, unique_key
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Error reading license: {e}","31")
            return None, None, None       
               
    return None, None, None

# Function to write to the license file
def write_license_file(status, expiry_date_str, unique_key):
    try: 
        with open(LICENSE_FILE, 'w') as file:
            file.write(f"{status}\n")
            file.write(f"{expiry_date_str}\n")
            file.write(f"{unique_key}\n")
    except Exception as e:
        SharedMethods.print_message(f"ERROR: Error writing license: {e}","31")
    return

# Function to check if the license is still valid
def is_license_valid(expiry_date_str,days_valid):
    try:
        if expiry_date_str:
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
            start_date = expiry_date - timedelta(days=days_valid)
            return start_date <= datetime.now() <= expiry_date
    except:
        return False
    return False

# Function to set license expiry in the license file
def set_license_expiry(days_valid, unique_key):
    expiry_date = datetime.now() + timedelta(days=days_valid)
    expiry_date_str = expiry_date.strftime("%Y-%m-%d")
    write_license_file("1", expiry_date_str, unique_key)

# Function to allow user try five times password
def admin_password_bypass():
    
    max_attempts = 5
    
    for attempt in range(1, max_attempts + 1):
        SharedMethods.print_message(f"ATTENTION: Attempt: ({attempt}/{max_attempts})","33")
        user_input = input(f"Enter Admin Password: ")
        if user_input == SharedVariables.admin_password:
            SharedMethods.print_message(f"Temporary access granted. Please connect to the open internet to renew the license when possible.", '32')
            return True
        else:
            SharedMethods.print_message(f"ERROR: Incorrect password. Try Again.","31")
    
    SharedMethods.print_message("ERROR: Access Denied. Too many failed attempts.","31")
    return False

# Main function to start the application
def main():
    # disable in debug mode (bypass the process in debug mode):
    if SharedMethods.is_debug_mode():
        return True
    
    # Read the license information from the file
    license_status, expiry_date_str, unique_key = read_license_file()

    if license_status == "1" and is_license_valid(expiry_date_str,30):
        SharedMethods.print_message(f"Valid License. Due to expiry on {expiry_date_str}.", '32')
        return True
    
    else:
        SharedMethods.print_message(f"WARNING: License not valid. Online validation process started...","33")
        SharedMethods.print_message(f"ATTENTION: Ensure you have a valid online connection...","33")
        mac_address = get_mac_address()
        allowed_macs_url = SharedVariables.license_online  # Replace with your URL
        allowed_macs = fetch_allowed_macs(allowed_macs_url)

        if not allowed_macs or not is_mac_allowed(mac_address, allowed_macs):
            SharedMethods.print_message(f"ERROR: Unauthorized machine. Validation Fail. The application cannot be started.","31")
            # Set license file status to 0 (failed check)
            write_license_file("0", "", unique_key)
            SharedMethods.print_message(f"ATTENTION: To authorize your machine. Please send all your machines MAC address to {SharedVariables.contacts}.","33")
            SharedMethods.print_message(f"ATTENTION: To fetch your mac address. Please refer to '{SharedVariables.support_online}' and follow instructions.","33")
            SharedMethods.print_message(f"ATTENTION: If you believe there is any issue, please contact support via {SharedVariables.contacts}.","33")
            
            # allow user to bypass the password
            if admin_password_bypass():
                return True
            else:
                return False

        # License check passed, generate a unique key if it doesn't exist and set expiry
        # (TODO) This is to be updated to a more secure and encrpted way in the future.
        # Due to the source code is able to be modified and licensing can be bypassed. No addtional encrption is considered.
        if unique_key == None:
            unique_key = str(uuid.uuid4())

        set_license_expiry(days_valid=30, unique_key=unique_key)
        SharedMethods.print_message(f"License created / updated successfully. Due to be reviewed in 30 days.", '32')
        return True
        

# Programme running
if __name__ == '__main__':
    main()