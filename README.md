# Mattermost Busy

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/languages/code-size/giovanni-tufo/mattermost-busy)

Mattermost Busy is a tool that allows Mattermost users to update their custom message with a progress bar based on a calendar.

It will also change your status emoji and your status to `dnd` when you are in a meeting.

Example:
```
31/03 meetings (▓ busy): 9▒▒▒▒10░░░░11▓▓▓▓12░░░░13░░░░14▓▓░░15▓▓▓▓16░░░░17░░░░18
```

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed at least `python` 3.8.5
* You have `pip` installed

## Installing Mattermost Busy

To install Mattermost Busy, follow these steps:

Linux and macOS:
```
python3 -m pip install -r requirements.txt
```

Windows:
```
pip install -r requirements.txt
```
## Using Mattermost Busy

### Setup

Copy `env.example` in `.env` and edit it. These are the parameters:

* **MATTERMOST_URL**: This is the URL of your mattermost instance, do not include http or https
* **MATTERMOST_TOKEN**: Your [personal access token](https://docs.mattermost.com/developer/personal-access-tokens.html)
* **MATTERMOST_PORT**: The port of your mattermost instance, use `443` if it is under https
* **MATTERMOST_END_HOUR**: The hour (without minutes) when you stop working
* **MATTERMOST_FREE_EMOJI**: The emoji to display when you are not in a meeting
* **MATTERMOST_BUSY_EMOJI**: The  emoji to display when you are in a meeting
* **MATTERMOST_FRIDAY_EMOJI**: The emoji to display when you are not in a meeting and it is friday :sunglasses:

Copy `meetings.json.example` in `meetings.json` and modify your schedule setting `FREE` if you are free and `BUSY` if 
you are busy.

### Manual run

You can run manually Mattermost Busy with the following command.
```
python3 main.py
```
This is not the recommended way, for a fully automated system, consider a cron job

### Cron job

Add to your crontab a line like this:
```
*/15 * * * 1-5 /usr/bin/python3 /path/to/mattermost-busy/main.py
```

This command will run Mattermost Busy every 15 minutes from 9 to 18 from Monday to Friday. Please refer to cron 
documentation to customize it. A nice tool to use is [crontab guru](https://crontab.guru/) 

## Contributing to Mattermost Busy
To contribute to Mattermost Busy, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me you can reach me at <giovanni.tufo@gmail.com>.

## License

This project uses the following license: [MIT](LICENSE.md).