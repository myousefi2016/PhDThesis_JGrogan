Instructions for ALE corrosion model. For further details e-mail
jgrogan.nuig@gmail.com.
-------------------------------------------------------------------
1. Create a model in Abaqus/CAE. 
All nodes on the corroding part and environment should be in the
adaptive mesh domain. All nodes on the corrosion surface should have a 'user-defined'
velocity adaptive meshing constraint applied for the corrosion step. Nodes on the corrosion surface should
be added to the part level node set 'InterfaceN'. Elements on the corrosion surface and in the corroding part should 
be added to the part level element set 'InterfaceE'.Periodic boundary conditions and boundary conditions in co-oridnate systems other than the global cartesian system should not be used.Symmetry boundary conditions can be used
provided that they are in the globabl CSYS. C3D8R elements only should be used.

2. Modify Input file or Keyword Editor
A user field (*field,user) should be created in the input file or using the keyword editor in CAE. The field is
applied to a node set containing all nodes in the corroding part and environment. 

3. Run the preprocessing script
The preprocssing file 'diff_pre_3.py' should be run in CAE with the relevant model open. The model and part names
for the corroding part need to be entered in the script. On completion the script makes a file 'NodeData.inc' which contains nodal connectivity data and indications of which nodes are to be moved during corrosion.

4. Running the job
When running a job the user subroutine 'ale_c3d2.for' should be included. The variable 'vel' on line 241 should be assigned a value corresponding to the inward normal velocity magnitude from the desired physical model (the concentration graident normal to the surface is given in the variable 'grad'). A number of arrays in the script are pre-allocated. If there are run-times errors the array sizes may need to be increased. 

5. Notes
The model is highly sensitive to time step size and element size. There is some automatic control on time incrment size in the model, however the validity of the chosen time step size should be checked for chosen element sizes using a suitable analytical model. In some cases the use of the automatic control on step size can cause convergence problems. It can be disabled by uncommenting line 246. 
