#!/bin/python

containers = ["idp", "idp_ui", "idp_ui_data", "idp_ui_api", "grouper_ui", "grouper_ws", "grouper_daemon", "grouper_data", "comanage", "comanage_cron", "comanage_data", "comanage_match", "comanage_match_data", "midpoint_server", "midpoint_data", "webproxy", "mpproxy", "wordpress_server", "wordpress_data", "mq", "directory", "sources", "ad", "comanage_midpoint_data"]

print("<table><tr><th style='text-align:left;width:150px'>Container</th><th style='text-align:left'>Health Status</th></tr>")
for container in containers:
    from subprocess import Popen, PIPE
    if container == "midpoint_server":
        dcmd = "docker ps -f name=" + container + " --format '{{ .Status }} '"
    else:
        dcmd = "docker ps -f name=workbench-" + container + "-1 --format '{{ .Status }} '"
    pipe = Popen(dcmd, shell=True, stdout=PIPE)
    healthstatus = '<font color="grey">unknown</font>'
    for line in pipe.stdout:
        if ('(' in line):
            healthstatus=line.strip()
            if ("healthy" in healthstatus):
                healthstatus='<font color="green">' + healthstatus + '</font>'
            elif ("unhealthy" in healthstatus):
                healthstatus='<font color="red">' + healthstatus + '</font>'
            else:
                healthstatus='<font color="blue">' + healthstatus + '</font>'
        else:
            healthstatus='<font color="orange">unspecified</font>'
    
    print("<tr><td>" + container + "</td><td>" + healthstatus + "</td></tr>")
print("</table>")
