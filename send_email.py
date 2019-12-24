import smtplib
server = smtplib.SMTP('smtp.gmail.com', 465)

#Next, log in to the server
server.login("himelbrand@gmail.com", "superkut272")

#Send the mail
msg = "Hello!" # The /n separates the message from the headers
server.sendmail("himelbrand@gmail.com", "omrihim@post.bgu.ac.il", msg)