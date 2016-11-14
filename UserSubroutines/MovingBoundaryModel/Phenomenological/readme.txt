Instructions for ALE corrosion model. For further details e-mail
jgrogan.nuig@gmail.com.
-------------------------------------------------------------------
1. Create a model in Abaqus/CAE. 
All nodes on the corroding part should be in the
adaptive mesh domain. All nodes on the corrosion surface should have a 'user-defined'
velocity adaptive meshing constraint applied for the corrosion step. Any exterior faces that
should not corrode should be added to a part level geometric set for the corroding part. The
set should be called 'Fixed'. This set should also include faces on which all nodes are involved in
a boundary condition. Periodic boundary conditions and boundary conditions in co-oridnate systems
other than the global cartesian system should not be used. Symmetry boundary conditions can be used
provided that they are in the globabl CSYS. C3D8R elements only should be used.

2. Modify Input file or Keyword Editor
A user field (*field,user) should be created in the input file or using the keyword editor in CAE. The field is
applied to a node set containing all nodes in the corroding part. 

3. Run the preprocessing script
The preprocssing file 'nodeCon3DF.py' should be run in CAE with the relevant model open. The model and part names
for the corroding part need to be entered in the script. On completion the script makes a file 'NodeData.inc' which contains nodal connectivity data and indications of which nodes are to be moved during corrosion.

4. Running the job
When running a job the user subroutine 'ale20.for' should be included. The variable 'velocity' on line 90 should be assigned a value corresponding to the desired corrosion rate. A number of arrays in the script are pre-allocated. If there are run-times errors the array sizes may need to be increased. 

5. Notes
The model is sensitive to time step size. Reasonably small time increments are recommended to ensure that the corrosion surface movement in an increment is small relative to the element size. However, excessively small time increments lead to round-off problems with the script and crashes.
