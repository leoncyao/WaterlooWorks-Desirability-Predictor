import os.path
import base64
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

import argparse

import mimetypes

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"
				]

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
										prog='ProgramName',
										description='What the program does',
										epilog='Text at the bottom of help')

	parser.add_argument('--company', '-c', dest='company_name', help='Name of company I am applying to', \
		 nargs='*', default="Amazon")
	parser.add_argument('--role', '-r', dest='role_name', help='Name of role I am applying for', \
		 nargs='*', default="Software Developer")
	parser.add_argument('--email', '-e', dest='target_email', help='Email I sending my application to')
	parser.add_argument('--cover_letter', '-cl',  action='store_true', \
		 help='Flag to indicate whether to generate a cover letter with')
	parser.add_argument('--send', '-s', dest='send', action='store_true', \
		 help='Flag to indicate whether to directly send or to make a draft')

	args = parser.parse_args()

	# role_name = " ".join(args.role_name.split("_"))
	# company_name = " ".join(args.company_name.split("_"))

	role_name = " ".join(args.role_name)
	company_name = " ".join(args.company_name)

	print(role_name)

	
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
					"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	try:

		# Call the Gmail API
		service = build("gmail", "v1", credentials=creds)

		message = EmailMessage()

		message.set_content(
			f"Dear Hiring Manager,\n\nI am emailing to apply for the {role_name} position at {company_name}." + \
			"I have attached the required documents in this email.\n\n" + \
			"Thank you for your consideration.\nBest, Leon"
			) 

		message["To"] = args.target_email
		message["From"] = "leoncyao@gmail.com"
		message["Subject"] = f"{role_name} Application"

		attachment_filename = "pdfs/Leon_Yao___Resume___November___2023.pdf"
		type_subtype, _ = mimetypes.guess_type(attachment_filename)
		maintype, subtype = type_subtype.split("/")
		with open(attachment_filename, "rb") as fp:
			attachment_data = fp.read()
		message.add_attachment(attachment_data, maintype, subtype, filename='Leon_Yao___Resume___November___2023.pdf')

		if args.cover_letter:

			compile_command = "xelatex -interaction nonstopmode -halt-on-error -file-line-error " \
			"'\\newcommand{\positionnamevalue}{%s} \\newcommand{\companynamevalue}{%s} \input cover_letter'" % (role_name, company_name)
			
			os.system(compile_command)

			time.sleep(6)

			copy_command = "cp cover_letter.pdf pdfs/cover_letter.pdf"

			os.system(copy_command)
			
			time.sleep(6)


			attachment_filename = "pdfs/cover_letter.pdf"
			type_subtype, _ = mimetypes.guess_type(attachment_filename)
			maintype, subtype = type_subtype.split("/")
			with open(attachment_filename, "rb") as fp:
				attachment_data = fp.read()
			message.add_attachment(attachment_data, maintype, subtype, filename='cover_letter.pdf')


		# encoded message
		encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

		create_message = {"message": {"raw": encoded_message}}

		if args.send:
			send_message = (
					service.users()
					.messages()
					.send(userId="me", body=create_message.get('message'))
					.execute()
			)
		else:		
			draft = (
				service.users()
				.drafts()
				.create(userId="me", body=create_message)
				.execute()
			)

		# pylint: disable=E1101


		# print(f'Message Id: {send_message["id"]}')

	except HttpError as error:
		# TODO(developer) - Handle errors from gmail API.
		print(f"An error occurred: {error}")