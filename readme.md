# Mailgun Example Scripts

## About This Repo

This repo contains example scripts that show how to interact with the Mailgun API. These scripts are not supported and probably not production ready. They are offered as a starting point; a learning aid. We hope you find these scripts useful and welcome any suggestions for additional scripts at https://feedback.mailgun.com

These scripts have been designed to be as user friendly as possible and will prompt you for any needed information, such as your API key or file names, when ran.

---

## __create_webhooks_simple.py__

Assigns a single endpoint to every webhook for all domains on the account.

### How to use:

```
python create_webhooks_simple.py
```

---

## __delete_webhooks_simple.py__

Deletes all webhooks for all domains on the account.

### How to use:

```
python delete_webhooks_simple.py
```

---

## __export_events.py__

Exports events to csv. Will prompt for optional parameters.

### How to use:

```
python export_events.py
```

---

## __get_domains.py__

Retrieves a list of domains from an account and outputs it to a csv file. You will be prompted for your Mailgun API key.

Especially useful when dealing with larger numbers of domains. Output is stored in ./files

### How to use:

```
python get_domains.py
```

---

## __get_suppressions.py__

Exports suppressions. You provide a file containing the list of domains you wish to export from. When you run the script you will be prompted for API key, a file containing the domains you wish to export from, and which suppressions you wish to export (bounces or complaints or unsubs or everything)

Output is stored in ./files/suppressions

### How to use:

```
python export_suppressions.py
```

---


## __import_suppressions.py__

Imports supppressions. You provide the file with the list of addresses to be imported.

### How to use:

```
python import_suppresssions.py
```

---


## __verify_domains.py__

Pulls a list of all unverified domains on your account and then attempts to verify them.

### How to use:

```
python verify_domains.py
```

---
