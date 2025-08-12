# Email Scheduler

A simple web application that exposes a POST endpoint to store email messages in a database. Each email is targeted to a specific group of recipients and is automatically sent at a scheduled time.

## Tech Stack

- Flask
- Celery
- Redis
- PostgreSQL
- Docker

## How it Works

First, open your browser and enter the address where the application is running (by default, application runs in http://localhost:5000). Go to `/save_emails` endpoint and there will be a form that takes 5 parameters:

- Event ID (Integer)
- Email Subject (String)
- Email Content (String)
- Timestamp (Datetime)
- Recipients (String)

Follow the fields' guide to fill in the form and click on "Submit" button to save the email. After submitting the form, you will see a short message telling you that your email has been saved and will be sent at the timestamp you specified.

Diving into the system itself, the saved email will remain in the database and wait until it is sent. This application uses Celery Beat to run a periodic task, which checks the scheduled emails' timestamp **every minute**. If now is greater than or equal to the email's timestamp, then the email will be added to the queue for sending.

## How to Run

1. Open terminal in the root directory
2. Create a new .env file
3. Copy all content in .env.example file and paste it to .env, then fill all the parameters there
5. Run the following command

```
>>> docker-compose run migrate
>>> docker-compose up --build
```

The above commands will run database migration and build the whole application.

## Specification

- System stores timestamp data in UTC, but takes users' input as their local timezone.  
- Recipients are not stored statically, they are stored dynamically by the user's input to represent a real case situation.
- Email supports unicode characters, such as Japanese (こんにちは) and Arabic (مرحبا)
- Recipient is stored as a string delimited by semicolon (;), it represents the list of recipients that should receive the email.
- To send email, you need to set your email and use your **app password** in .env file.
- The email server provider is **Google**, make sure to use your Gmail account and get your app password in https://myaccount.google.com/apppasswords.

## Testing

Testing is done by **pytest** with several patching techniques, like Monkeypatch.