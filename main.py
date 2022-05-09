import requests, threading

def getEmail():
	url = "https://api.internal.temp-mail.io/api/v3/email/new"
	headers = {'user-agent': 'vscode-restclient'}
	response = requests.request("POST", url, headers=headers).json()
	return response["email"]

def zalandoNewsLetterSignup(email):
	url = "https://www.zalando.fr/api/graphql/"
	payload = "[{\"id\":\"06fe5b50b4218612aa3fa8494df326aef7ff35a75a8563b3455bb53c15168872\",\"variables\":{\"input\":{\"email\":\"" + email + "\",\"preference\":{\"category\":\"MEN\",\"topics\":[{\"id\":\"recommendations\",\"isEnabled\":true},{\"id\":\"item_alerts\",\"isEnabled\":true},{\"id\":\"fashion_fix\",\"isEnabled\":true},{\"id\":\"follow_brand\",\"isEnabled\":true},{\"id\":\"subscription_confirmations\",\"isEnabled\":true},{\"id\":\"offers_sales\",\"isEnabled\":true},{\"id\":\"survey\",\"isEnabled\":true}]},\"referrer\":\"nl_subscription_banner_one_click\",\"clientMutationId\":\"1652116788642\"}}}]"
	headers = {'user-agent': 'vscode-restclient'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response.status_code

def getMessage(email):
	url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
	headers = {'user-agent': 'vscode-restclient'}
	response = requests.request("GET", url, headers=headers)
	if response.status_code == 200 and len(response.json()) > 0:
		for message in response.json():
			if message["from"] == "\"Zalando Team\" <info@service-mail.zalando.fr>":
				return message["body_text"]
	else: return "Wait"

def getCode(message):
	message = message.split("Entrez le code lors du paiement")
	message = message[1]
	message = message.split("[→]")
	message = message[0]
	message = message.strip()
	print(message)
	return message

def saveCode(code):
	with open("codes.txt", "a") as f:
		f.write(code + "\n")

def main():
	email = getEmail()
	print(email)
	status = zalandoNewsLetterSignup(email)
	print(status)
	if status == 200:
		while True:
			message = getMessage(email)
			if message != "Wait":
				code = getCode(message)
				saveCode(code)
				main()
				break
			else:
				continue

if __name__ == "__main__":
	threads = input("How many threads do you want to run? ")
	for i in range(int(threads)):
		t = threading.Thread(target=main)
		t.start()
