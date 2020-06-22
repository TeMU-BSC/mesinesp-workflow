# mesinesp-workflow

##### Steps to send emails: 
1. Create 2 message files, one with the plain text and another with the formatted text. See file examples in body/toy/

	Store them under body/task-name/ subdirectory.

	It is important that they have the SAME name, that will be your KEYWORD (for example, message.txt and message.html; their keyword is message).

	To transform a formatted text into HTML code, you may use this online editor: https://html-online.com/editor/

2. Create a csv list with the mail list. It MUST have the same name as the message files, the KEYWORD (for example, message.csv).

	Store it in the same directory as mails.py 

	See the examples personalizado_toy.csv & general_toy.csv

	Please, write to antonio.miranda@bsc.es to receive the mail lists used in the Cantemist and CodiEsp shared tasks.

3. Modify mails.py, line 25 and 26. Change "mesinesp" by your task-name

4. Modify mails.py, line 28 with your BSC email

5. Modify mails.py, line 29 with the people you will CC

6. If you are writing a personalized email (your message.html and message.txt should contain the variable {fullname}): 

	+ comment lines: 49, 92

	+ uncomment lines: 48, 91, 103
If not: 

	+ uncomment lines: 49, 92

	+ comment lines: 48, 91, 103

7. Execute

```
python mails.py 
Template KEYWORD: 
BSC intranet username [From]: <intranet username>
Password: <intranet password>
```
