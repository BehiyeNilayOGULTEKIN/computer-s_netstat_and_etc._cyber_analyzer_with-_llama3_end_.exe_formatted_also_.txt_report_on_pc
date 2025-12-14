# computer-s_netstat_and_etc._cyber_analyzer_with-_llama3_end_.exe_formatted_also_.txt_report_on_pc
User runs .exe
   ↓
Collect netstat output
   ↓
Collect Windows network event logs
   ↓
Generate structured report                                       => this is the format that I wanted
   ↓
Send raw data to LLM
   ↓
Receive security analysis
   ↓
Save final report to file


### As you can see from the codes also , First , I mentioned the commands and their outputs via subprocess lib.
### Then , I coded a prompt for the initial and the response from llama3 as json formatted. Here we used json lib and  requests lib.
### after this , I coded the function that It can import the output to txt file
### then I run the code with functions sequently , I changed the prompt many times to get the result that I want.
### I decided to turn this code into an exe file but my PYInstaller for this step ,  gave me errors such as urllib3 not founs
### I upload pip from the start again, the it solved
### "python -m ensurepip --upgrade" here is my solution.

Some of the Resources I used  : https://www.youtube.com/watch?v=2Fp1N6dof0Y => for subprocces, btw , If you are using a language different than ASCII standarts ,
you may need to add this code inside subprocces.run:
##### ----------------------------------------------------------------------
#### ""encoding="utf-8",
#### errors="replace"""
##### ----------------------------------------------------------------------

For the LLM calls , I am taking Ed donners course currently about LLM engineering from udemy, so on I am not be able to offer any resources fot his part.


https://stackoverflow.com/questions/34275782/how-to-get-desktop-location = > to save any file on desktop



<img width="91" height="232" alt="Ekran görüntüsü 2025-12-15 000322" src="https://github.com/user-attachments/assets/fe6c25df-be7b-432a-9307-306f6215f7eb" />
<img width="105" height="187" alt="Ekran görüntüsü 2025-12-15 000256" src="https://github.com/user-attachments/assets/3005bcef-2362-4ad7-a508-edcc38200169" />


