<h1>How to create a virtual environment</h1>
<h4>First open up your project directory in vsCode <br>
  Next open up a terminal if one if not already open <br>
On the right side of the terminal you should see a + button, click the drop down button to the right of + and click "Git Bash" <br>
Now in the bash terminal, type 'python -m venv myenv' <br>
After that loads in, type 'source myenv/Scripts/activate' - you should see (myenv) pop up indicating your VE is active <br>
now type: 'pip install -r requirements.txt' - this should install all the project dependencies and stuff <br>
If you ever install any more dependencies, use 'pip freeze > requirements.txt' to update the requirements <br>
When you are done using your virtual environment type 'deactivate' in your bash terminal</h4>
<br><br>
<h4>I know you guys said virtual environments werent necessary, but I read that it makes it easier for keeping track of what dependencies we'll be using for the project.
The virtual environment is a lot like a virtual computer that is created for the sole purpose of storing our project. We basically download dependencies into our project and as long as the virtual environment is active 
we can use commands to update those dependencies into a requirments.txt file i made. We can then use the 'pip install -r' command to install everything in the requirements.txt file automatically. Idk if this will work 
perfectly tbh, but just follow the instructions we'll see what happens.
