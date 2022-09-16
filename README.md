# GiveMeYourToken
POC for Mining unencrypted Teams tokens (https://www.vectra.ai/blogpost/undermining-microsoft-teams-security-by-mining-tokens)

```
usage: GiveMeYourToken [--dump-tokens] [--read-tokens] [--self-message] [--db-path] [--cookies-file] [--token-id]

Retrieve tokens from Teams sqlite file and use it through Teams API.

options:
  -h, --help            show this help message and exit
  -d, --debug           Print lots of debugging statements
  -v, --verbose         Be verbose
  --dump-tokens         Use this argument to dump tokens from Teams database.
  --read-tokens         Use this argument to read tokens previously retrieved.
  --self-message        Send message to the Private self Teams channel.
  --db-path DB_PATH     Specify the path of db. Default is %AppData%\Microsoft\Teams\Cookies
  --cookies-file COOKIES_FILE
                        Specify path for json output file
  --token-id TOKEN_ID   Use --read-tokens and select the id of the token you want to use. Mandatory for --self-message
````