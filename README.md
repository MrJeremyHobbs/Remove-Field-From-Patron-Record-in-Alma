# Remove Gender Field (or any Field) from Alma User Record
Currently Alma doesn't support the ability to remove a value from the "gender" field in a patron's user record using a job.

This script runs through a text file of patron primary ID's and removing the gender field from each record.

# How it works
This script first calls the GetUserDetails API to retrieve a user's patron data as XML.
Then, using the ElementTree library, the script searches for the "gender" field and removes it.
Finally, it updates the user record using the UpdateUserDetails API, using PUT.

# Installation
Use the requirements.txt file to install all necessary libraries.

```
pip install -r requirements.txt
```

If necessary, create a blank log.txt file in the same directory as the script.

# Requirements
This script accepts a single column text file (users.txt) of primary IDs, without any headers.

Example:
```
user123345
user234234
user234234
user234234
```

# Apikey
This script requires an Alma Users API key.

Place this key as an environmental variable on your local machine and insert in on the following line:

```
# get apikey
apikey = os.getenv('ALMA_SANDBOX_API_KEY')
```

# Outputs
The script outputs a simple log of user primary IDs to make testing easier.

It also does a dump of every user's original patron data in XML in case data needs to be restored.

# How to Use
Just type the following in your console to get started.

```
remove_gender_from_patron_record.py
```

A progressbar will run across the screen to show your progress and estimated time to finish.

# Error Handling
This script uses the alma_helper python library to handle the api calls.

All errors coming from Alma are filtered back to the results of the API call by taking the name of the returned object and adding .errors.message.

```
# check for errors
if new_user.errors.exist:
    print(new_user.errors.message)
```

# Testing
To test the results, it's recommended you run this process in your sandbox first before pushing to production.

Once you've done a run through, open the log.txt file and copy and paste primary IDs into Alma to see if the desired field was removed.

It's also recommended you check the "history" tab in the record to see if anything significant was changed that you didn't intend to.

# Plug and Play
If you want to remove any field from the patron record, instead of "gender", just substitute the desired field.

# Documentation
Users API: https://developers.exlibrisgroup.com/alma/apis/users/