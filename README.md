# pass-man
My very own CLI password manager


#1. Clone the repository

Click on the Green "Code" button at the top right of your screen. 
<img width="365" alt="Screen Shot 2022-08-17 at 2 44 08 PM" src="https://user-images.githubusercontent.com/65196684/185248768-f9d3949c-a334-4e88-b30a-a7cf953334b3.png">

Then Click on the "Download ZIP" button.
<img width="553" alt="Screen Shot 2022-08-17 at 2 46 22 PM" src="https://user-images.githubusercontent.com/65196684/185248989-e7ae81ab-2c46-42e0-bd62-cc3732b0a510.png">

Unzip the file, and you are ready to move on

#2. Installation

Make sure that you have python3 and pip already installed as this software works on python (pip is for installing dependencies). 

Open a terminal window. Navigate to the unzipped folder

```bash
cd ~/Downloads/pass-man
```

You can check to see if you have python3 already installed by running 
```bash
python3 -V
```

You can check to see if you have python3 already installed by running 
```bash
pip -V
```

Run the following command to install the dependencies. The installation may take a few minutes to compete.

```bash
pip install -r requirements.txt
```
#3. Setup

move the "pass-man" folder to ~/bin

```bash
mv ~/Downloads/pass-man ~/bin/pass-man

```

Navigate to the pass-man folder and run the setup instructions. Enter your password. Remeber your password as this software does not store your password, and you will be unable to change it later. The setup.py folder should have created two new files (pass.txt and test.txt) in the same directory. After ensuring that these files are there, remove the setup.py file.

```bash
cd ~/bin/pass-man
python3 setup.py
ls -l
rm setup.py
```



Run this command in order to access the command globally (From any directory). This makes it so that you don't have to navigate to the pass-man directory every time you want to run the password manager

```bash
export PATH=$PATH":$HOME/bin/pass-man"
```
