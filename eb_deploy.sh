eb init group-8-fraudbnb --key $PEM_NAME -p Docker -r us-west-2
eb create group-8-fraudbnb-env --envvar AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvar AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
eb init fraudbnb-db --region us-west-2 --platform Docker --key $PEM_NAME --envar DB_PASSWORD=$DB_PASSWORD