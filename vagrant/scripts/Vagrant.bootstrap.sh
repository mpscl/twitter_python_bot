#!/usr/bin/env bash

# ---------------------------------------
#          Virtual Machine Setup
# ---------------------------------------

# Adding multiverse sources.
#cat > /etc/apt/sources.list.d/multiverse.list << EOF
#deb http://security.ubuntu.com/ubuntu trusty-security multiverse
#EOF


# Updating packages
apt-get update

# ---------------------------------------
#          Python Setup
# ---------------------------------------

# Installing packages
# apt-get install -y php5 php5-cli php5-fpm curl php5-curl php5-mcrypt php5-xdebug libapache2-mod-php5 php5-gd php5-ldap php5-pgsql libphp-phpmailer libphp-phpmailer
apt-get install -y python3-pip
apt-get install -y build-essential libssl-dev libffi-dev python-dev
pip3 install requests
pip3 install tweepy
pip3 install Pillow



# ---------------------------------------
#       Tools Setup.
# ---------------------------------------
# These are some extra tools that you can remove if you will not be using them 
# They are just to setup some automation to your tasks. 

# Adding NodeJS from Nodesource. This will Install NodeJS Version 5 and npm
#curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
#sudo apt-get install -y nodejs

# Installing Bower and Gulp
#npm install -g bower gulp

# Installing GIT
apt-get install -y git

