a HWID key bot system i made for roblox scripts    (this only works with swift but modify it however you need) (if you dont know how to modify it just copy paste everything to gemini)
its not very good cuz im bad at coding but i couldnt find ANYONE else write stuff abt this so here i go!!!!!!!  
(all of what ive made it by ai plz no flame me im bad at this)  
# sorry for my bad gramer :>


## the sites ive used for this  
[supabase](https://supabase.com/)    (Key/HWID/DiscordUserIds storerer thing also the place where you store your obfoscated source code)  
[replit](https://replit.com/)      (for the discord bot)  

## how we get the hwid  
alot of executors alow you to just use "gethwid()" but some executors like swift dont let you do that.  
thats where we use this  
````
local response = request({ Url = "http://httpbin.org/get", Method = "GET" })
local headers = game:GetService("HttpService"):JSONDecode(response.Body).headers

local executor_hwid = "Not Found"
for key, value in pairs(headers) do
if string.find(string.lower(key), "fingerprint") then
executor_hwid = value
break
end
end

print("Your Executor HWID is: " .. executor_hwid)
````
this sends a get request to "http://httpbin.org/get" where u can get the fingerprint (aka hwid)  
you can also get other info from this site like for swift you can get your swift user id or smth like that  
and you can also get your ip with this  



uhh tutorial go brrr





# Supabase

this is where all your keys and user data will live.
## step 1 (supabase Key/HWID/UserIds table maker thing)
* make a free account on [Supabase](https://supabase.com/)
* create a New Project and call it whatever u feel like
* In your project go to the Table Editor on the far left and click "Create a new table" and name it "keys"
* Uncheck the box that says "Enable Row Level Security (RLS)". Turn it OFF.
* remove the default column in ur keys table (if any)
* Add these columns in ur keys table   
````key````              (type: text, set it as the Primary Key)  
````hwid````             (type: text, make sure Is Nullable is checked)  
````owner_discord_id```` (type: text, make sure Is Nullable is checked)  
* Click "Save".
## step 2 (supabase code and obfoscated script)
this is the code that will run 24/7 on Supabase's servers. you need to upload it from your PC.

* First you need to install [Node.js](https://nodejs.org/) if you dont have it go download it 
* Make a new folder on your PC. call it something like my-key-system 
* Open cmd prompt inside that folder. the easiest way to click the address bar at the top of the folder window type cmd and press Enter.  

![image](https://github.com/user-attachments/assets/c346088e-7c5f-4d89-b877-ba01d5d15f4e)
* Run these commands cmd prompt, one by one. press enter after each one.  

````npx supabase login```` (this will open a browser to log you in)  
````npx supabase link --project-ref YOUR_PROJECT_ID```` (go to your Supabase Project Settings -> General to find your project ID. paste it here)  
````npx supabase functions new verify-key```` (this makes the folders for your code)  
* Now in the "my-key-system" folder find the file supabase/functions/verify-key/index.ts open it with notepad or whatever. delete everything inside and paste all of the code in [index.ts](https://github.com/nigmaBoy/HWID-key-system/blob/main/index.ts) (IMPORTANT go in there and edit the "PUT YOUR SCRIPT HERE" to your OBFOSACTED script)  
* after you save the file, go back to your command prompt and upload the code by running this
````npx supabase functions deploy verify-key --no-verify-jwt````  


# The loader
step 1
* make a hithub thingy and copy past everything from [loader](https://github.com/nigmaBoy/HWID-key-system/blob/main/loader) (IMPORTANT CHANGE ````YOUR PROJECT ID```` TO YOUR PROJECT ID)
* save it.



# Replit   
this bot will live on Replit and run 24/7 to generate keys for you. it's the thing you'll actually use day-to-day.  
## step 1 (making the bot)  
* Go to [Discord Developer](https://discord.com/developers/applications) and click "New Application" at the top right and name it whatever.  
* Go to the "Bot" tab on the left.  
* Right under the bot's name, click "Reset Token". copy the token and dont share it with anyone. this is your bot's password. save it in notepad for now.    
* Turn off ````Public Bot```` (unless you want to make a bot anyone can add to their server (doesnt really matter if they can add it))    
* Scroll down and turn ON these three toggles    
````Presence Intent````  
````Server Members Intent````  
````Message Content Intent````  

* Now go to the "OAuth2" tab on the left menu
* Scroll doesn til you see "OAuth2 URL Generator" and under that theres "SCOPES"
* In the "SCOPES" section check ````bot```` and ````applications.commands````
* A new box called "BOT PERMISSIONS" will show up below Check ````Send Messages.```` and ````Read Message History````
* Scroll down and copy the GENERATED URL. paste this into your browser and invite the bot to a ur server    
## step 2 (man im hungry rn | creating secrects)  
* Go to [Replit](https://replit.com/) and make a free account.  
* Click "+ Create App" at the top left  
* Click "Choose a template".  
* choose the basic "Python" template give it a name and click "Create Repl".  
* Besides the "main.py" click the plus and add "Secrets".  
![image](https://github.com/user-attachments/assets/caa70dd7-63b4-4448-b533-88d36e38199d)  
  
* Click "+ new secrect" and add these three secrets one by one.

Secret 1:  
Name: DISCORD_TOKEN  
Value: your discord bot token u saved from earlier  

Secret 2:  
Name: SUPABASE_URL  
Value: Your Supabase URL (from Supabase Project Settings -> Data API and get the ````Project URL````).  
  
Secret 3:  
Name: SUPABASE_KEY  
Value: Your Supabase service_role key. THIS IS A SUPER SECRET KEY. (from Supabase Project Settings -> API Keys and get the ````service_role````).
## step 3 (im still hungry :[ | ur bots code)    
* Go to the "Main.py" tab and delete everything inside it.    
* Paste all of this code into the empty main.py file [main.py](https://github.com/nigmaBoy/HWID-key-system/blob/main/main.py)  
### VERY IMPORTANT: you need to fill in the YOUR_..._HERE parts.  
````MY_SERVER_ID```` Right-click your server icon -> Copy Server ID. (You need Developer Mode on in Discord Settings -> Advanced).  
````YOUR_DISCORD_USER_ID_HERE```` Right-click your name -> Copy User ID. (You need Developer Mode on in Discord Settings -> Advanced). There are three places to put your ID.  
````YOUR_RAW_GITHUB_URL_HERE```` The link to your loader script on GitHub. There are two places to put this link.  
* click the plus next to the "assistant" and add ````Shell````    
![image](https://github.com/user-attachments/assets/14938e9d-8404-4a2e-bc20-ba4451913bce)    
i got a bloody nose </3    
* go into Shell and run ````pip install discord.py supabase python-dotenv````  

### then you should be done check console and it should say smth like ````Logged in as...````  
if it does the go to the server u added ur bot to and check if the comands work  
comands are   
````/generate <user>````  
````/panel````  
````/resethwid````  





i know all of this isnt the best but now its hopefully easier for people to access and make their own better systems!!!  
if you have any qustions ask me on discord ````thatonedudetsts````  


# uhh i will not be updating this in the future so yeah  
anyways im really hungry and really tried have fun with this!!!





