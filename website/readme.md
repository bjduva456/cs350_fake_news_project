Instructions for localhosting the website:
- Note: NPM, Python, and tensorflow needs to be installed before this website can be ran.
- in server.js, the first argument of spawn() (lines 16 and 23) needs to be changed to the machine's local installation of Python.
    I found that absolute paths worked the best.
- in terminal, cd to `{project_dir}/website`
    {project_dir} refers to the local file that this project is installed in
- in terminal, run `npm install`
    this will install dependancies used by the website, such as nodemon (for local hosting) and child_process
- in terminal, run `nodemon server.js`
    this may not be able to be run in a powershell terminal due to innate permissions. It should work in a cmd terminal.
    there may be several "stderr" being printed, they are usually warnings and can be related to differences in versions of python/tensorflow or other packages
    once the warnings stop, the clients are free to send requests.
- navigate to `localhost:8080` in a web browser, and feel free to use the website!

- Note: if the website is to be deployed publically, localhost IP addresses must be adjusted to the new path.
    These can be found on lines 8 and 25 in `static/scripts/results.js`, and there is a console.log() in line 44 of `server.js` that could be changed as well.