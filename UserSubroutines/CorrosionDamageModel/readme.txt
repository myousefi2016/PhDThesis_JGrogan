Instructions for Damage corrosion model. For further details e-mail
jgrogan.nuig@gmail.com.
-------------------------------------------------------------------
1. Create a model in Abaqus/CAE. 
All elements on the corrosion surface should be included in the part level element set 'CSURF'.

2. Run the preprocessing script
The preprocssing file 'preprocessor.py' should be run in CAE with the relevant model open. The model and part names
for the corroding part need to be entered in the script. On completion the script makes a file 'NBR.inc' which contains nodal connectivity data and indications of which nodes are to be moved during corrosion.

3. Running the job
When running a job the user subroutine 'CorP.f' should be included (CorP.for on windows). The script uses pre-allocated arrays. If the job crashes array sizes may need to be increased. The script is only suitable for shared memory processing (threads model in abaqus). No thread safety checking is performed in this script. See the script 
'CDM_Threadsafe.for' for a thread-safe VUMAT version.
