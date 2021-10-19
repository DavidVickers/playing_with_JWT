Very Basic code to demonstrate getting an access token and loging in to SFDC using a JWT token flow.

We will be using  OpenSSl and Keytool to check if these are already installed then type the following into your terminal 
openssl version

david.vickers@dvickerfs-ltm JWTCertsAndKeys % openssl version
LibreSSL 2.8.3

If you get a response with a version then you are good

For Keytool just type keytool into the prompt you should get a list of commands if it is installed

david.vickers@dvickerfs-ltm JWTCertsAndKeys % keytool
Key and Certificate Management Tool

Commands:

 -certreq Generates a certificate request
 -changealias Changes an entry's alias ........................... etc
 
If you have Java installed then Keytool should be installed

If you do not have openssl then the simplest way to install is via Brew

david.vickers@dvickerfs-ltm JWTCertsAndKeys % brew install openssl
If you do not have brew (homebrew) installed then WhyNot ?????  ok but seriously  if you don’t then follow the instructions here:-
https://treehouse.github.io/installation-guides/mac/homebrew

*Once you have Keytool and Open SSL then let's begin*

In terminal make sure you have changed directory to  the one where you want all your keyfiles certs ets to be created.

example 
david.vickers@dvickerfs-ltm ~ % cd /Users/david.vickers/Documents/testcertifications/JWTCertsAndKeys 

This  makes the next steps easier as all the files you create will end up in the same directory.
we are going to use the following commands in order

openssl genrsa -des3 -passout pass:MyjwtDemo -out server.pass.key 2048

openssl rsa -passin pass:MyjwtDemo -in server.pass.key -out myserver.key

openssl req -new -key myserver.key -out myserver.csr

openssl x509 -req -sha256 -days 365 -in myserver.csr -signkey myserver.key -out myserver.crt


*At the command Prompt paste in*

openssl genrsa -des3 -passout pass:MyjwtDemo -out server.pass.key 2048

Note you are specifying a password ( pass:) of MyjwtDemo
and creating an output file (-out) called server.pass.key 
you should now have  server.pass.key file 

*Now insert the next command*
openssl rsa -passin pass:MyjwtDemo -in server.pass.key -out myserver.key
note  you are passing in the password you set before -passin pass:MyjwtDemo
and the input (-in) is your server.pass.key  so if you changed that then change it here too!
(-out) you are creating a file called myserver.key   
and you should now have a myserver.key file in your directory

Why you are here  right click on server.pass.key and duplicate this file

Rename the duplicated of your key file to server.pass.pem. we will need the pem file later if you wanted to create a JKS store ( not needed for  the Python script demo but needed for  SFDC to SFDC and named credentials)

*Ok back to the terminal window and  paste in the next command*
openssl req -new -key myserver.key -out myserver.csr
so here we read in the key file and output a csr!
When you enter this you will get questions !
You can fill in as much as you like
You will also be asked to create a password I suggest for the next steps keeping the same password as it's much easier to keep track off. This password protects you certificate so you need to remember it
I will use the cunning password .....password  

*We need a 509 certificate so now we can use our csr file to create that* 
*paste in the next command*

openssl x509 -req -sha256 -days 365 -in myserver.csr -signkey myserver.key -out myserver.crt

note this reads in both your CSR and your signing ( private key) that you created earlier  and outputs a cert valid for 365 days ( max for a sha256 cert)  This cert gets added to your connected app in SFDC to Authenticate the JWT. Your python code gets the Pricate key generated above and the Consumer key from the  SFDC connected app

*Ok for creating a connected app to support a JWT token flow this is all you need, but for a Salesforce to Salesforce connection we are going to be using  Named Credentials and for that we are going to need to store our certificate in  Salesforce and for that we need this in a Java Key store format ( jks)*

So onward!!! here are the next commands we will use

Openssl pkcs12 -export -in myserver.crt -inkey server.pass.pem -out mykeystore.p12

Keytool -importkeystore -srckeystore mykeystore.p12 -srcstoretype pkcs12 -destkeystore servercert.jks -deststoretype JKS

Keytool -keystore servercert.jks -changealias -alias 1 -destalias jwtDemo


First we paste into the terminal window
Openssl pkcs12 -export -in myserver.crt -inkey server.pass.pem -out mykeystore.p12
Note this uses that PEM file we created earlier ( the copy of the key file)
This routing takes in the cert and the pem file and outputs a keystore in a p12 format you will need to input your PEM password, so if you forgot that then you are now  SOL! but this was the password you used to generate the key remember 

openssl genrsa -des3 -passout pass:MyjwtDemo -out server.pass.key 2048
Note you are specifying a password ( pass:) of MyjwtDemo  as specified in one of the first steps

and you will get a 2kb mykeystore.p12 file. if you get a zero kb file then the operation failed delete the file and try again

So now with your p12 file you need to make it a .jks file so we run the next command

Keytool -importkeystore -srckeystore mykeystore.p12 -srcstoretype pkcs12 -destkeystore servercert.jks -deststoretype JKS

we will be prompted for a password. this is the password you set for the export password in the previous step you will then be asked for a destination password you will begin to see that there are a lot of passwords in this sequence so staying with the same one all the way though makes things simpler!

don’t worry about the warning 

Okay we are nearly done there is one final issue  this PKS file will have the default alias of 1. Salesforce does not allow you to upload a JKS file with the default alias  so we need to change it. The Alias you give will be the label of  the Certificate / keystore entry when you upload it to Salesforce.
*Paste in the final command*

Keytool -keystore servercert.jks -changealias -alias 1 -destalias jwtDemo

Enter your password  and hit enter. you will get the same  warning as before but your JKS file will now have a new alias in this case “jwtdemo” ( unless you picked a different alias)

























