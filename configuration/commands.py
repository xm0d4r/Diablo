COMMAND = {
    "enum4linux": "enum4linux -a {target}",
    "ffuf": "ffuf -u {target}FUZZ -w ../dependencies/ffuf/test.txt -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0' -c -ac",
    "shortscan": "shortscan {target}",
    "netexec": "netexec smb {target} -u '' -p '' --shares",
    "nmap": "nmap -Pn -sS --min-rate 10000 --max-retries 3 -p 80,443,445,8080,8443 {target} -vv",
    "shcheck": "shcheck.py -d {target}",
    "testssl": "testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}",
    "webanalyze": "webanalyze -apps ../dependencies/webanalyze/technologies.json -host {target}",
    "wpscan": "wpscan --url {target} --enumerate p --random-user-agent --throttle 5 --plugins-detection passive --plugins-version-detection passive --detection-mode passive --request-timeout 10 --connect-timeout 10 --disable-tls-checks {target}"
}
