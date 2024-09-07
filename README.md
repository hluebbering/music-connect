# music-connect


set HEROKU_API_KEY=HRKU-d42b4a33-2453-49fc-ac24-b33478894909
git push heroku main
heroku logs --tail --app fierce-sands-53854

git add .
git commit -m "Prepare for deployment to GitHub Pages"
git push -u origin main

git add .
git commit -am "make it better"
git push heroku main