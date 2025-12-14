#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import subprocess
# def get_netstat():
#     result = subprocess.run(
#         ["netstat", "-an"],
#         capture_output=True,
#         text=True
#     )
#     if result.stderr:
#         print("ERROR:", result.stderr)
#     return result.stdout


# In[9]:


import subprocess
import requests
import json
import os
from datetime import datetime

#subprocess lib : for running the commends for the report on cmd, and get their output
#datetime :  for the .txt formated file label on desktop to be more understandable
#request : for llama api calls
#json :  the prompt's response is json formatted

# In[2]:


def run_command(command, shell=False):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=shell,
            encoding="utf-8",
            errors="replace"
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if error:
            return f"[ERROR]\n{error}"
        return output if output else "[NO OUTPUT]"

    except Exception as e:
        return f"[EXCEPTION] {str(e)}"

# so here I firsly tried netstat command and when I realized I can fetch the output, I decided to do something more expandable.
# run command func,  will help us to run the cmd commands and get their results as stdout.
# If any error occurs , will print it.
# In[3]:


def generate_system_network_report():
    report = []

    report.append("=" * 80)
    report.append("WINDOWS SYSTEM & NETWORK ACTIVITY REPORT")
    report.append(f"Generated at: {datetime.now()}")
    report.append("=" * 80)

    report.append("\n### [1] NETSTAT - Active Connections")
    report.append(run_command(["netstat", "-ano"]))
#for netstat command and the result of it
    report.append("\n### [2] PowerShell - TCP Connections")
    report.append(run_command(
        ["powershell", "-Command", "Get-NetTCPConnection"]
    ))
#to see tcp flow
    report.append("\n### [3] Established TCP Connections")
    report.append(run_command(
        ["powershell", "-Command",
         "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'}"]
    ))
#to see open and works activelt tcp ports
    report.append("\n### [4] Network Adapter Statistics")
    report.append(run_command(
        ["powershell", "-Command", "Get-NetAdapterStatistics"]
    ))
# to see network devices logs
    report.append("\n### [5] Recent System Errors (Event Log)")
    report.append(run_command(
        ["powershell", "-Command",
         "Get-EventLog -LogName System -EntryType Error -Newest 20"]
    ))
# to see any last error that occured (20 of them)
    report.append("\n### [6] Security Log (Recent Login Events)")
    report.append(run_command(
        ["powershell", "-Command",
         "Get-EventLog -LogName Security -Newest 20"]
    ))
# to see any firewall errors that occured(last 20 ones)
    report.append("\n### [7] Network Profile Events")
    report.append(run_command(
        ["powershell", "-Command",
         "Get-WinEvent -LogName Microsoft-Windows-NetworkProfile/Operational -MaxEvents 20"]
    ))
#to see computers own network logs such as when it connected also , public or private
    report.append("\n" + "=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)
#to separate output between like this ================================================================================


# In[4]:


def analyze_with_llm(netstat_output):
    #our prompt
    prompt = f"""You are a senior cybersecurity analyst with experience in Windows internals,
network security, and incident response.

Analyze the following Windows system and network command output report.

Your task:
1. Review each section carefully.
2. Identify potential security risks, misconfigurations, or suspicious behavior.
3. Assign a SEVERITY LEVEL to each finding:
   - Low
   - Medium
   - High
   - Critical
4. Provide clear, actionable security recommendations.
5. If no immediate risk is present, explicitly state that the activity appears normal.
6. Avoid speculation; base your analysis strictly on the provided data.

Output format (STRICT):

**[SECTION NAME]**
- Severity: <Low | Medium | High | Critical>
- Findings:
  - Bullet-point findings based on the log output
- Security Impact:
  - Brief explanation of why this matters
- Recommendations:
  1. Numbered, concrete actions (commands, policies, or monitoring steps)

Use a professional SOC / SIEM analyst tone.
Do NOT repeat the raw log data.
Do NOT invent information that is not present in the report.

If indicators of compromise (IoC), lateral movement, brute-force attempts,
or data exfiltration are suspected, explicitly mention them.

LOG REPORT:
<<<
{netstat_output}
>>>

"""
    #and our response format
    response = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


# In[11]:

#this func is for saving the response as a txt file on desktop named as netstat_(date and hour)
def save_to_file(content):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"netstat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(desktop, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


# In[12]:


netstat_output = generate_system_network_report()
analysis = analyze_with_llm(netstat_output)
save_to_file(analysis)
print("===== LLM ANALYSIS =====")
print(analysis)


# In[ ]:




