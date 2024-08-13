# FITOPIA Gym Management System

Welcome to FITOPIA, a gym management system built using Streamlit. This application allows gym staff to manage gym members, including adding new members, editing member information, adding balance to a member's account, and viewing member details.

## Features

- **Add New Members**: Gym staff can add new members by entering their name, contact number, email, membership type, and uploading a photo.
- **Edit Member Info**: Allows staff to edit a member's basic information, including name, contact number, email, and photo.
- **Add Member Balance**: Staff can add balance to a member's account. This is especially useful for "Pay-as-you-go" membership types.
- **View Member Details**: Staff can view detailed information about a member, including their current balance if they have a "Pay-as-you-go" membership.
- **List Members**: Display a list of all current members in the system.

## Installation

To run this application, you need to have Python installed on your system. You can install the necessary dependencies using the following command:

```bash
pip install streamlit pandas pillow
```

## Running the Application

Once the dependencies are installed, you can run the application using the following command:

```bash
streamlit run app.py
```

**Don't run main.py**

This will start the application, and you can interact with it through your web browser.

## Usage

1. Add New Member: Use the sidebar to add a new member to the system.
2. Edit Member Info: In the main section, you can edit the details of an existing member.
3. Add Member Balance: You can add balance to a member's account by entering their contact number and the amount to add.
4. View Member Details: View the complete details of a member, including their current balance and photo.
5. List Members: Display a list of all members with their details.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
