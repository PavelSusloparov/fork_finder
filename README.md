The tool is shell script, which run python script.

Python script is send SIGHUP signal to processes with more then 10 forks.

Shell script is run under root crontab every 2 hours at 30 minutes.

Script result you can find in |Path to your local git repository location|/fork.log


Crontab configuration:

    Please follow steps:

    1) Run 'sudo crontab -u root -e'
    2) Add 30 */2 * * * <Path to your local git repository location>/fork_finder.sh
    3) Save file
    4) Check configuration changing: 'sudo crontab -u root -l'

Note: fork_finder.sh must be executable for root user.
