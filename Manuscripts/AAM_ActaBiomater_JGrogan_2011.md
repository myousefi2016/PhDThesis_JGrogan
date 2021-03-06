# A Corrosion Model for Bioabsorbable Metallic Stents

### J.A. Grogan, B.J. O’Brien, S.B. Leen, P.E. McHugh

### Mechanical and Biomedical Engineering, College of Engineering and Informatics, and National Centre for Biomedical Engineering Science, National University of Ireland, Galway, Ireland.

## Abstract

In this study a numerical model is developed for application in predicting the effects of corrosion on the mechanical integrity of bioabsorbable metallic stents. To calibrate the model the effects of corrosion on the integrity of biodegradable metallic foils are assessed experimentally. In addition, the effects of mechanical loading on the corrosion behaviour of the foil samples are determined. A phenomenological corrosion model is developed and applied within a finite element framework, allowing for the analysis of complex three dimensional structures. The model is used in predicting the performance of a bioabsorbable stent in an idealised arterial geometry as it is subject to corrosion over time. The effects of homogeneous and heterogeneous corrosion processes on long-term stent scaffolding ability are contrasted based on model predictions.

Keywords: Biodegradable magnesium; finite element; pitting corrosion; damage modelling.

## 1. Introduction

A new generation of implants based on metals that are gradually broken down in the body are attracting much interest, both in the literature [1, 2] and clinically [3]. One promising application of biodegradable metals is in the development of bioabsorbable coronary stents. The primary purpose of coronary stents, which are small mesh-like scaffolds, is to provide mechanical support to the arteries of the heart following the angioplasty procedure, preventing elastic arterial recoil [4]. However, considering a healing time of approximately six to twelve months for the artery following the angioplasty procedure [5, 6], the requirement for long-term arterial scaffolding can be questioned, especially in light of increased long term injury risk due to the presence of the stent [7, 8]. The current generation of absorbable metallic stents (AMS) have shown promise in non-randomized in-human clinical trials, however high rates of neo-intimal hyperplasia were observed following the stenting procedure, most likely as a result of premature loss in stent scaffolding support [3]. As such, it is evident that further work is required in characterising and optimizing AMS performance in the body before this technology can be proven as a viable replacement for conventional stenting.

The design of AMS brings a number of new challenges over that of conventional stents. To date, the process of absorption of the stent in the surrounding tissue is not fully understood. In-vitro studies on the corrosion behaviour of biodegradable alloys in simulated physiological fluids have shown that the rate of corrosion and the underlying corrosion process depend on a variety of factors, including, but not limited to, alloy composition [9], surface treatments and coatings [10], solution composition [11] and solution transport conditions [12]. Further studies have also suggested that mechanical loading, both static [13] and dynamic [14], may contribute to the corrosion behaviour of AMS. 

In order to characterise the behaviour of a bioabsorbable device in the body, and in particular coronary stents, it is important to consider not only the form and rate of corrosion observed, but also the effect that this corrosion process has on overall device mechanical integrity. It is noted that relatively few studies have been performed to this end for biodegradable metals in-vitro, with the study of Zhang et al. [15] on the reduction in bending strength of biodegradable alloy specimens following corrosion being the most applicable to date. Further to this, while a number of studies, such as that of Kannan et al. [13], have investigated the effects of mechanical loading on specimen corrosion behaviour, such studies have focused on corrosion behaviour in specimens with dimensions at least an order of magnitude larger than those of coronary stent struts.

The first objective of this work is the determination of the effects of corrosion on the mechanical integrity of biodegradable foil specimens in simulated physiological solution. Since the thickness of the foil samples is of the same order of magnitude as that of the struts used in AMS, it is believed that such an approach may give a more appropriate indication of the effects of corrosion on AMS scaffolding support than that given in previous studies on larger samples. The second objective of this work is the determination of the effects of mechanical loading on the corrosion behaviour of the biodegradable alloy foil specimens. Again, it is believed that such an approach can give a more appropriate indication of the effects of mechanical loading on the corrosion behaviour of AMS than tests on larger size samples.

In addition to experimental alloy characterisation, computational modelling of the corrosion process can give important insights into the fundamental corrosion mechanisms that lead to the gradual breaking down of an AMS in the body. Also, such models can prove useful in the design of AMS, through device assessment simulations and the optimization of device geometries for improved duration of structural integrity as corrosion progresses. Since the development of AMS is a relatively new field, there are few computational approaches specifically developed for modelling the effects of corrosion and resulting reduction in mechanical integrity of the devices. While a wealth of modelling approaches exists for predicting the effects of corrosion on specimen structural integrity, many are based on probabilistic approaches, with a focus on predicting time to failure in large scale industrial components in corrosive environments [16, 17]. Other approaches consider modelling corrosion through complex, physically based models, for example that of Saito et al. [18]. However such models are often focused on particular corrosion phenomena, with it often proving challenging to obtain the required model parameters experimentally, making their implementation in the assessment of AMS performance difficult.

Hence, the third objective is the development of a phenomenological corrosion model that is detailed enough to give a better understanding of the corrosion behaviour of an AMS in the body, yet simple enough to allow the model to be calibrated through readily performed experiments and implemented for use with a commercial finite element (FE) code. The approach taken is built on recent work by Gastaldi et al. [19], who developed what is to-date the only direct application of a corrosion model in a stent assessment application. In [19] the effects of corrosion on device mechanical integrity are represented through the evolution of a continuum damage parameter, allowing an assessment of overall stent damage as corrosion proceeds. While adopting this continuum damage parameter approach, this work focuses on the development and calibration of a corrosion damage model which has the added ability to capture the effects of heterogeneous corrosion behaviour on AMS scaffolding support over time.

## 2. Methods

### 2.1 Alloy Characterisation 

The corrosion behaviour of a biodegradable magnesium alloy (AZ31) was determined in a solution of modified Hank’s balanced salts (H1387, Sigma-Aldrich, USA). The AZ31 alloy was sourced in the form of 0.23 mm thick foil (Goodfellow, UK) from which test specimens of length 50.0 mm and width 4.65 mm were cut, as shown schematically in Fig. 1(a). A 20.0 mm long test region was created at the centre of each specimen by reducing the foil thickness to 0.21 mm in this region, as shown in Fig. 1(b). This was accomplished by mechanical polishing with 600-grit emery paper, resulting in a final average surface roughness of 0.2 µm as measured using a profilometer (Surftest – 211, Mitutoyo, USA). Prior to testing, samples were cleaned in anhydrous ethanol and left to dry for a period of 24 hours, allowing for a consistent oxidisation of all polished sample surfaces. Regions of the sample outside the test section were covered in a layer of petroleum jelly to restrict corrosion attack to the region of interest. For corrosion testing, specimens were immersed in the solution of modified Hank’s balanced salts, with solution temperature maintained at 37° C by means of a thermostatically controlled water-bath. The solution volume (ml) to surface area (cm2) ratio was maintained between 25:1 and 50:1 in all tests, with this range being deemed appropriate based on the work of Yang et al.[20], who showed that increasing the volume to area ratio beyond 6.7 had little influence on the corrosion behaviour of a similar biodegradable magnesium alloy in Hank’s solution.

In order to comprehensively characterise the corrosion behaviour of the biodegradable alloy, three independent experiments were performed, as listed in Table 1. The first experiment, A, was used to determine the corrosion rate and primary corrosion process for a biodegradable alloy in simulated physiological fluid. In order to determine the alloy corrosion rate, five specimens were immersed in solution for a period of 72 hours. The volume of hydrogen gas evolved from each specimen was measured using the apparatus shown in Fig. 2(a). Specimens were fixed in such a way that all four surfaces in the test region were exposed to solution. The alloy corrosion rate was inferred from the volume of evolved hydrogen gas, based on the chemical balance for the conversion of magnesium to corrosion product, using an approach described in [21], which has shown good agreement with direct weight measurements [22] and has the advantage that corrosion rate can be determined without having to remove corrosion specimens from solution. In order to determine the primary form of corrosion, three further specimens were immersed in solution and removed at 3, 12 and 40 hours respectively. Specimens were cleaned in a solution of chromic acid for five minutes at 60 ºC to remove corrosion products and the corrosion surfaces were viewed under SEM (S-4700, Hitachi, Japan). Samples subject to the cleaning process for a shorter period of time (partially cleaned) were also viewed under SEM, allowing the identification of precipitates in the corroded alloy micro-structure and the determination of their composition by energy-dispersive x-ray spectroscopy (EDX).

The second experiment, B, was used to determine the effects of corrosion on the mechanical integrity of the foil specimens. This was done by immersing 26 specimens in solution over a period of 90 hours. Specimens were removed at regular intervals, cleaned in a solution of chromic acid and weighed using a mass balance with a resolution of 0.1 mg. Specimens were then tested in uniaxial tension to fracture using a universal tensile tester (BZ 2.5 Zwick, UK) using a constant crosshead speed of 0.005 mm.s-1, with the polished test region taken as the gauge region. Due to the small size of the samples, tensile strains were measured using a non-contact video extensometer system (Messphysik GmbH, Germany). The maximum tensile load supported by the specimen was taken as a measure of mechanical integrity.

The final experiment, C, was used to determine the influence of tensile load on the corrosion behaviour of 10 specimens in solution. A near constant tensile load was applied to the specimens in solution by means of a custom built rig, shown in Fig. 2(b). Two calibrated (2.73 N.mm-1) compression springs were used to apply the load to the samples by compressing them to a set length. This was done by tightening bolts that passed through their inner diameter, clamping the specimen in position and then loosening the bolts, allowing the sample to take the full load from the springs. Polymers were chosen for the frame and clamps to reduce the risk of galvanic corrosion, while stainless steel support rods were used to ensure that specimens were loaded purely in uniaxial tension. The time to fracture for each of ten samples subject to increasing uniaxial tensile stresses was determined using an electronic timing circuit attached to the test rig. The reduction in applied load due to gradual specimen elongation in solution was deemed to be less than 1.1 N (1.8 % of the lowest applied load), based on a maximum observed specimen elongation of 0.2 mm before fracture when measured using a LVDT (DC-EC, Schaevitz, USA) attached to the top of the test-rig.

### 2.2 Corrosion Model Development

A corrosion model has been developed for application with a commercial FE code, based on continuum damage theory [23]. The use of continuum damage theory allows the effects of corrosion induced micro-scale geometric discontinuities on overall specimen mechanical integrity to be accounted for, without explicitly modelling their progression. This is accomplished through the introduction of a scalar damage parameter, $D$, and an effective stress tensor, $\bar{\sigma}_{ij}$, as described in [24]. Briefly, the effective stress tensor is given by:

$\bar{\sigma}_{ij} = \frac{\sigma_{ij} }{1 - D}$

where $\sigma_{ij}$ is the Cauchy stress tensor. In this work, the damage model is implemented within an FE framework through the development of a user material subroutine (VUMAT) for use with the Abaqus/Explicit FE code (DS SIMULIA, USA). The temporal evolution of damage is considered on an element by element basis within the model. Considering the FE mesh shown in Fig. 3(a), corrosion is assumed to only take place for elements on external or exposed surfaces. The assumed evolution of the corrosion damage parameter for these surface elements is based on that given in [19] for the case of perfectly uniform or homogeneous corrosion as:

$\frac{dD_e}{dt} = \frac{\delta_U}{L_e}k_U$

where $k_U$ is a corrosion kinetic parameter of unit $hour^{-1}$ and $\delta_U$ and $L_e$ are respective material and FE model characteristic lengths of unit mm, as described in [19]. In this study the material characteristic length is given a value of 0.017 mm, consistent with observed grain sizes for AZ31 alloy in the literature [25]. 
The damage evolution law in Eqn. 2 is enhanced in this work through the introduction of an element-specific dimensionless pitting parameter, $\lambda_e$. This parameter is used to introduce the capability of capturing the effects of heterogeneous or pitting corrosion to the modelling framework, through the following damage evolution law:

$\frac{dD_e}{dt} = \frac{\delta_U}{L_e}\lambda_e k_U$

Considering the FE mesh in Fig. 3 (a), each element on the initial exposed surface is assigned a unique, random $\lambda_e$ value through the use of a standard Weibull distribution-based random number generator. Hence, the probability of the value of $\lambda_e$ lying in the range [a, b] for each element is given by:

$\text{Pr}[a\leq\lambda_e\leq b] = \int_a^b f(x)dx$

where $f(x)$ is the standard Weibull distribution probability density function (PDF), given as [26]:

$f(x) = \gamma (x)^{\gamma - 1}\exp^{-(x)^\gamma}$

with the condition that $x \geq 0$ and $\gamma > 0$, where $\gamma$ is a dimensionless distribution shape factor. The use of such a distribution in describing the degree of heterogeneity of the corrosion process can be best described with reference to its PDF, shown in Fig. 3(d), where increasing $\gamma$ values lead to a more symmetric PDF. This in turn corresponds to a narrower range of $\lambda_e$ values being assigned over the elements, giving a more homogeneous corrosion. 

When $D_e = 1$ in an element, the element is removed from the FE mesh. The corrosion surface is then updated in the VUMAT based on the use of an element connectivity map and a newly developed inter-element communication ability within the VUMAT code, described in detail in the Supplementary Data. When the element is removed from the FE mesh, its neighbouring elements are assumed to inherit the value of its pitting parameter according to:

$\lambda_e = \beta\lambda_n$

where $\lambda_n$ is the pitting parameter value in the recently removed element and $\beta$ is a dimensionless parameter that controls the acceleration of pit growth within the FE analysis. 

### 2.3 Corrosion Model Calibration and Validation

The corrosion model is calibrated based on the results of Experiments A and B. An representation of the test region in the foil is meshed with 56,000 linear reduced integration brick elements ($L_e$ = 70 µm), as shown in Fig.1(c). In representing the deformation of the material in the FE corrosion model, finite deformation kinematics is assumed. The mechanical properties used are based on those of AZ31 foil samples with 0 % mass loss, with representative experimental stress-strain curves shown in Fig. 4. 

Elasticity is considered linear and isotropic in terms of finite deformation quantities (Cauchy stress and Lagrangian strain) [27], with an experimentally determined Young’s Modulus of $E$ = 44 GPa and a Poisson’s ratio of $\nu$ = 0.35 from [28]. Plasticity is described using J2 flow theory with non-linear isotropic hardening, with a Yield Stress of 138 MPa and UTS of 245 MPa at an engineering strain of 17 %. The material properties of damaged elements are controlled through the evolution of the damage parameter, D, with a ductile failure condition further employed by setting $D$ = 1 for elements in which strains exceed those observed experimentally at UTS.

Experiment A is simulated by allowing corrosion to occur on all four exposed surfaces in the test region. The rate of mass loss over time is determined based on the average damage value over all of the model elements. Experiment B is simulated in a subsequent analysis step by simulating tensile loading of the test region. The maximum force withstood by the model is taken as a measure of loss in mechanical integrity and is compared to that observed experimentally.

In calibrating the FE corrosion model, the values of the three independent model parameters, $k_U$, $\gamma$, and $\beta$ are determined for a given $delta_U$ and $L_e$, based on the simulation of Experiments A and B. These values are determined by imposing three conditions. First, the model should capture the experimentally observed reduction in specimen mechanical integrity with corrosion. Also, the predicted mass loss vs. time curve should qualitatively match that observed in Experiment A, shown in Fig. 5 to be largely linear. These conditions allow the determination of $\gamma$ and $\beta$ through an iterative calibration process. The third condition is that the simulated corrosion rate quantitatively matches that observed in Experiment A, allowing the parameter $k_U$ to be readily determined for given values of $\gamma$ and $\beta$.

In order to validate the predictive capabilities of the model for the calibrated parameters, Experiment C is simulated. Loading of the sample in uni-axial tension is simulated followed by the subsequent corrosion of the specimen under the constant applied load. The time to complete fracture of the specimen, given by the time at which the specimen force becomes 0, is then predicted, allowing a comparison with the results of Experiment C.

### 2.4 Stent Application

Once calibrated, the corrosion model is applied in predicting the performance of an AMS. A CAD approximation of the Biotronik Magic stent is generated based on SEM images in the literature [29]. The stent model geometry, which has a strut width of 80 µm and a strut thickness 125 µm, is shown mounted on a delivery system model in Fig. 6, with relevant dimensions given in Table 2. The geometry is meshed using reduced integration linear brick elements with an average element characteristic length of 20 µm, arrived at through a mesh convergence study, and which is accounted for in corrosion simulations through appropriate scaling of the corrosion model parameters. Stent material properties are taken to be the same as those used in the foil models, shown in Fig. 4.

The deployment of the stent is simulated in a three layer artery of inner diameter 2.76 mm, with artery layer thicknesses taken from the work of Holzapfel et al. [30]. The artery is modelled using an isotropic reduced 6th order hyperelastic material model, with model parameters taken from work by Gervaso et al. [31], based on experimental tissue testing by Holzapfel et al. [30]. The use of an isotropic artery material description, rather than a more physically representative anisotropic description, such as that of Holzapfel et al. [32], is considered acceptable in the case of this work, as the primary interest is the deformation and loading of the stent itself, rather than artery stresses. An idealised atherosclerotic plaque geometry of thickness 0.5 mm is included and is modelled using a similar hyperplastic model, with constants taken from work by Gastaldi et al. [33], based on experimental plaque testing by Loree et al. [34]. 

A tri-folded balloon geometry is constructed and secured to the delivery system, shown in Fig. 6, by means of tie constraints. In simulating stent deployment, the balloon is inflated through the application of a pressure of 20 atm (2.03 MPa) on its inner surface, giving a final stent inner diameter of 2.76 mm and a balloon to artery ratio of 1:1. Recoil is simulated through the removal of this applied pressure. Material properties and relevant dimensions for the balloon and delivery system are given in Table 2 and are based on those used in a similar delivery system model developed by Mortier et al. [35]. 

The general contact algorithm in Abaqus/Explicit is utilised for stent-artery contact, with the condition that all stent surfaces, internal and external, were considered to be potentially part of the contact domain. This allows the automatic re-definition of contact faces by the Abaqus solver following element removal [27] and the continued modelling of the stent-artery interaction as the device corrodes. A frictional coefficient of 0.2 is assumed for all tangential contact behaviour, with ‘hard’ contact defined for normal contact behaviour. 

As was the case in the study of De Beule et al. [36], Rayleigh damping ($\alpha$ = 8000) is employed for the balloon to prevent non-physical oscillations, with the average ratio of kinetic to internal energy for the analysis maintained below 5% [37]. Simulations are performed on a single hyper-threaded hexa-core processor on a SGI Altix high performance computer, requiring 600 CPU hours.

## 3. Results

### 3.1 Alloy Characterisation

The results of Experiment A, derived from the volume of hydrogen evolved from the surfaces of five corrosion specimens over time, are shown in Fig. 5. For the first six hours of immersion, the rate of mass loss is relatively low; however it quickly increases to give a steady rate of mass loss from which an average corrosion rate of 0.084 mg.cm-2.hr-1 is derived. SEM images of the specimen corrosion surface are shown in Fig. 7. Microscopic pits are observed on the surface of the corrosion specimen after as little as three hours, shown in Fig. 7(a). The maximum observed pit diameter in this case is approximately 70 µm. Pit growth is observed, with a maximum pit diameter of approximately 400 µm observed after 12 hours, shown in Fig. 7(b). After 40 hours of immersion significant pit growth is observed, with macroscopic pits of diameter greater than 2 mm noted. In a number of cases, pits are observed to have progressed through the thickness of the specimen, shown in Fig. 7(c). In addition to the observed pits, precipitates, whose composition was determined to be AlMn by EDX analysis, were observed on the corrosion surface of partially cleaned samples when viewed under SEM, as shown in Fig. 7(d). Based on these SEM images it is concluded that localized pitting corrosion is the primary form of corrosion attack in this case. 

Representative engineering stress-strain curves for corroded and non-corroded specimens are shown in Fig. 4, based on the results of Experiment B. Specimen strength, as determined by dividing the maximum load withstood by the specimens in tension by the specimen cross-sectional area prior to corrosion, and engineering strain at the specimen strength are seen to decrease significantly with modest corrosion induced mass loss. Looking at the reduction in specimen strength with mass loss for all specimens in Fig. 8, a significant reduction in strength (>25 %) is noted for relatively small percentage mass losses ($<$ 5 %). 

The results of Experiment C are shown in Fig. 9. The applied stress is taken as the ratio of applied load to original specimen cross-sectional area. It is observed that increasing applied stress leads to a significant reduction in the time to fracture for the specimen, with time to fracture halved when the applied stress is increased from 75 MPa to 150 MPa.

### 3.2 Corrosion Model Calibration

The simulated corrosion of the foil test section is shown in Fig. 5. Macroscopic corrosion pits are seen to nucleate, grow and gradually coalesce through the removal of elements from the FE mesh. The parameters for the corrosion damage model, which were calibrated based on the results of Experiments A and B, are shown in Table 3. Parameters are shown for two cases, that of an idealised uniform corrosion model and that of the pitting model that most closely captures the experimentally observed corrosion behaviour.  

The calibrated rate of mass loss from the FE pitting corrosion model is compared to that observed experimentally in Fig. 5. It can be seen that the FE pitting model is capable of capturing the experimentally observed rate of mass loss over time. Similar results are obtained in the case of the uniform corrosion model and as such are not included in the plot. The simulated results based on Experiment B are shown in Fig. 8. Again, the calibrated pitting corrosion model is able to capture the experimentally observed non-linear reduction in specimen strength with mass loss, whereas in this case, the uniform corrosion model fails to describe the observed trend.

The predicitive capabilites of both pitting and uniform models are shown in Fig. 9, based on the results of Experiment C. It can be seen that the FE pitting model is able to qualitatively and quantitatively predict the influence of tensile stress on specimen fracture time, while the uniform corrosion model fails to describe this non-linear relationship. This result represents a first experimental verifiaction of the predictive capabilites of the corrosion modelling framework developed in this work.

### 3.3 Stent Application

The simulated deployment and recoil of the Magic stent geometry in the idealised three layer artery model is shown in Fig. 10. A realistic balloon and stent ‘dog-bone’ profile can be seen during deployment, which shows agreement with experimentally observed stent geometries during the deployment phase [38]. The stent inner diameters pre- and post-recoil are 2.76 and 2.32 mm respectively. Following deployment and recoil, the corrosion of the AMS geometry is simulated using both pitting and uniform corrosion models, as shown in Fig. 11. It can be seen from Fig. 11 (a) that pitting corrosion attack leads to a non-uniform breaking down of the AMS geometry, even in an idealised artery geometry, while the uniform model in Fig. 11 (b) predicts a homogeneous corrosion attack. The predicted long-term stent recoil for each model is shown in Fig. 12, with stent recoil defined as follows:

$\%\text{Recoil} = \frac{\theta_1 - \theta_2}{\theta_1}\times 100\%$

where $theta_1$ and $theta_2$ are the respective stent inner diameters prior to, and during, device corrosion. It can be seen that the pitting corrosion model predicts a significant reduction in stent scaffolding support for a modest percentage mass loss, a highly undesirable trait for a magnesium based AMS.

## 4. Discussion

The average corrosion rate (0.084 mg.cm-2.hr-1) and localized pitting corrosion attack observed in this work are in agreement with those reported for similar alloy and solution compositions in the literature [9]. However, the gradual reduction in alloy corrosion rate due to the build-up of a layer of corrosion product reported in many other studies on larger samples [20, 39] was not observed for the thin foils studied in this work, where the corrosion rate remained largely constant, Fig. 5. 

The significant corrosion-induced reduction in specimen mechanical integrity observed in Experiment B in this work, Fig. 8, is in agreement with results obtained in tests on larger samples in bending reported by Zhang et al. [15]. Since the corrosion model developed in this work is capable of capturing the observed results solely by accounting for the effects of specimen mass loss, Fig. 8, it is concluded that the primary factors for the observed reduction in specimen integrity are the non-uniform reduction in cross-section due to pit growth and the development of stress-concentrations in pitted regions.

While the results of Experiment C, Fig. 9, suggest a stress mediated corrosion attack on the foil samples, as has been observed in tests on larger samples with similar alloy and solution compositions [13], it is noted that the corrosion model developed in this work is capable of describing the observed dependence of fracture time on applied load solely through the simulation of localized pitting attack, with no explicit stress dependence included in the damage evolution law in Eqn. 3. This suggests that pit growth in the foil samples is the primary factor for the observed reduction in specimen fracture time with load.

When considering the observed corrosion behaviour, it should be noted that the sample processing employed here differs somewhat from that of coronary stents, which are typically laser cut and electrolytically polished. While the surface treatments employed in the processing of AMS have not been reported in detail, it is likely, based on surface roughness studies on AZ31 and similar alloys in the literature [40, 41], that electro-polishing of the surface would lead to reduced corrosion rates and pitting susceptibility compared to those observed in this work. In addition, if anodizing treatments and surface coatings are employed this may also lead to reduced corrosion rates [42, 43].  In terms of laser-cutting, little has been reported on the effects of this process on the corrosion behaviour of AMS, although it has been shown that insufficient polishing can lead to preferential corrosion on laser-cut faces in conventional stents [44].

The observed localized corrosion behaviour is strongly linked with the micro-structure of the AZ31 alloy used in this study. For example, Fig. 7(d) shows the presence of AlMn precipitates in the alloy microstructure, which, due to micro-galvanic action with the surrounding matrix [45], can lead to preferential corrosion in their vicinity and the eventual formation of corrosion pits. In addition, metallic grain size and twinning have been shown to influence the corrosion behaviour of AZ31 [46], with grain boundaries suggested to act as corrosion barriers, while mechanical twins have been suggested to act as corrosion initiation sites. As such, the observed corrosion behaviour in this work depends strongly on alloy processing conditions, with improved corrosion performance possible through careful control of precipitate concentration and grain size through appropriate alloy heat treatments [46].

In terms of the performance of the AMS simulated in this work, it is predicted that heterogeneous corrosion leads to a significant reduction in stent scaffolding ability with relatively little corrosion induced mass loss when compared to the case of a perfectly homogeneous corrosion. The ability to make such a prediction is of particular relevance in the development of new alloys for AMS application, as it gives an indication of the degree of precedence that minimizing pitting susceptibility should have over other considerations in the alloy design, for example alloy ductility and tensile strength. In addition, the predictive capability afforded by the stent corrosion model allows improved AMS design through accounting for the effects of pitting corrosion in functionally critical regions, such as plastic hinges, in the design phase.

The model developed in this work has a number of limitations. Due to its phenomenological basis it does not physically capture the electrochemical processes and species evolution on the corrosion surface, meaning that its predictions are specific to a given alloy and solution composition. In addition, model predictions are not motivated by alloy microstructure and as such, cannot be used in predicting the effects of precipitate inclusions or grain-size on corrosion. Due to a lack of experimental data on the effects of tissue coverage on alloy corrosion behaviour its effects are not included in the model, nor are the effects of dynamic loading on long-term AMS scaffolding ability. 

Although the predictions of the corrosion model are specific to a given alloy microstructure, through re-calibration for each microstructure in consideration it can provide useful information into how a particular alloy microstructure would perform in a stent application in terms of long term radial strength and ductility.  This can help in the selection of suitable alloy heat treatments, which by their nature can also modify alloy ductility and strength, without having to directly manufacture and corrode stent samples. In addition, through explicit modelling of an alloy microstructure, such as in [47], and the micro-galvanic corrosion process, the modelling framework developed here could be further extended to investigating the effects of precipitate concentration and grain size on an alloy’s corrosion behaviour.

In terms of tissue growth, the struts of an AMS have been found to be covered in a thin layer of neointima as few as six days after implantation in in-vivo tests [29]. While the corrosion behaviour of AMS will depend on the degree of tissue coverage on strut surfaces, specific details on the relationship between tissue coverage and corrosion rates are not yet known. It is likely however, that increasing tissue coverage will reduce local corrosion rates through regulating the diffusion of hydrogen ions and corrosion product to and from the corrosion surface, and will certainly form a physical barrier in preventing flow enhanced corrosion [12] in the blood-stream. In terms of the model developed in this work, the framework exists which would allow different corrosion rates to be assigned to different surfaces or different individual elements. This feature may prove useful in future analyses, where the effects of tissue coverage on device corrosion behaviour could be considered. 

The effects of dynamic loading, which can lead to phenomena such as corrosion fatigue [14], on device performance were not considered in this work. Although it is likely that such a phenomenon would lead to a reduction in stent integrity over time [14], it is believed for the corrosion environment and alloy used in this study, that the influence of corrosion fatigue on stent integrity may be negligible compared to that of an aggressive, localized pitting attack. Nonetheless, the modelling framework developed here could be readily applied in considering the effects of dynamic loading on device corrosion through modelling of cyclic stent loading and the added dependence of the damage parameter on stress or strain amplitude and the number of loading cycles to which the stent has been subjected.

## 5. Conclusions

* A computational corrosion model is developed and implemented in a commercial finite element code for application in absorbable metallic stent assessment and design. The model is calibrated based on the experimental determination of the corrosion behaviour of biodegradable magnesium alloy (AZ31) foils in simulated physiological fluid and is capable of  describing the effects of mechanical loading on alloy corrosion.

* The corrosion of the alloy is observed experimentally to be largely driven by a localized attack, which results in a significant reduction in foil mechanical integrity with relatively little mass loss. This behaviour is well described by the newly developed corrosion model, which captures both the experimentally observed corrosion rate and the resulting corrosion induced reduction in foil integrity.

* Through combining experimental alloy characterisation and computational stent assessment, it is believed that this work provides new insights into the performance of an absorbable metallic stent, while also providing an experimental and computational methodology for future corrosion studies on the mechanical integrity of other candidate biodegradable alloys in corrosive physiological environments.

## 6. Acknowledgements

The authors would like to acknowledge funding from the Irish Research Council for Science, Engineering and Technology, under the EMBARK program (J. Grogan), funded by the National Development Plan, and the SFI/HEA Irish Centre for High-End Computing (ICHEC) for the provision of computational facilities and support. 

## 7. References

[1]	Hermawan H, Dubé D, Mantovani D. Developments in metallic biodegradable stents. Acta Biomater 2010;6(5):1693-1697.

[2]	Staiger MP, Pietak AM, Huadmai J, and Dias G. Magnesium and its alloys as orthopedic biomaterials: A review. Biomater 2006;27(9):1728-1734.

[3]	Erbel R, et al. Temporary scaffolding of coronary arteries with bioabsorbable magnesium stents: a prospective, non-randomised multicentre trial. Lancet 2007;369(9576):1869-1875.

[4]	Serruys PW, et al. A Comparison of Balloon-Expandable-Stent Implantation with Balloon Angioplasty in Patients with Coronary Artery Disease. N Engl J Med 1994;331(8):489-495.

[5]	Schömig A, et al. Four-year experience with Palmaz-Schatz stenting in coronary angioplasty complicated by dissection with threatened or present vessel closure. Circulation 1994;90(6):2716-2724.

[6]	El-Omar MM, Dangas G, Iakovou I, Mehran R. Update on In-stent Restenosis. Curr Interv Cardiol Rep 2001;3(4):296-305.

[7]	Mitra AK, Agrawal DK. In stent restenosis: bane of the stent era. J Clin Pathol 2006;59(3):232-239.

[8]	Ong AT, McFadden EP, Regar E, de Jaegere PP, van Domburg RT, Serruys PW. Late Angiographic Stent Thrombosis (LAST) Events With Drug-Eluting Stents. J Am Coll Cardiol 2005;45(12):2088-2092.

[9]	Kirkland N, Lespagnol J, Birbilis N, Staiger M. A survey of bio-corrosion rates of magnesium alloys. Corros Sci 2010;52(2):287-291.

[10]	Song Y, Zhang S, Li J, Zhao C, Zhang X. Electrodeposition of Ca-P coatings on biodegradable Mg alloy: in vitro biomineralization behaviour. Acta Biomater 2010;6(5):1736-1742.

[11]	Mueller W, Nascimento ML, Lorenzo de Mele MF. Critical discussion of the results from different corrosion studies of Mg and Mg alloys for biomaterial applications. Acta Biomater 2010;6(5):1749-1755.

[12]	Lévesque J, Hermawan H, Dubé D, Mantovani D. Design of a pseudo-physiological test bench specific to the development of biodegradable metallic biomaterials. Acta Biomater 2008;4(2):284-295.

[13]	Bobby Kannan M, Dietzel W, Blawert C, Atrens A, Lyon P. Stress corrosion cracking of rare-earth containing magnesium alloys ZE41, QE22 and Elektron 21 (EV31A) compared with AZ80. Mater Sci Eng A 2008;480(1):529-539.

[14]	Gu X, et al. Corrosion fatigue behaviors of two biomedical Mg alloys - AZ91D and WE43 - In simulated body fluid. Acta Biomater 2010;6(12):4605-4613.

[15]	Zhang S, et al. Research on an Mg-Zn alloy as a degradable biomaterial. Acta Biomater 2010;6(2):626-640.

[16]	Melchers R, Jeffrey R. Probabilistic models for steel corrosion loss and pitting of marine infrastructure. Reliab Eng Syst Saf 2008;93(3):423-432.

[17]	Li S, Yu S, Zeng H, Li J, Liang R. Predicting corrosion remaining life of underground pipelines with a mechanically-based probabilistic model. J Petrol Sci Eng 2009;65(3):162-166.

[18]	Saito S, Kuniya J. Mechanochemical model to predict stress corrosion crack growth of stainless steel in high temperature water. Corros Sci 2001;43(9):1751-1766.

[19]	Gastaldi D, Sassi V, Petrini L, Vedani M, Trasatti S, Migliavacca F. Continuum damage model for bioresorbable magnesium alloy devices - Application to coronary stents. J Mech Behav Biomed Mater 2011;4(3):352-365.

[20]	Yang L, Zhang E. Biocorrosion behavior of magnesium alloy in different simulated fluids for biomedical application. Mat Sci Eng C 2009;29(5):1691-1696.

[21]	Song G, Atrens A. Understanding Magnesium Corrosion—A Framework for Improved Alloy Performance. Adv Eng Mater 2003;5(12):837-858.

[22]	Aung NN, Zhou W. Effect of grain size and twins on corrosion behaviour of AZ31B magnesium alloy. Corros Sci 2010;52(2):2010.

[23]	Lemaitre J, A Course on Damage Mechanics, Berlin: Springer, 1996.

[24]	Lemaître J, Desmorat R. Engineering damage mechanics: ductile, creep, fatigue and brittle failures. Berlin: Springer, 2005.

[25]	Del Valle JA, Perez-Prado MT, Ruano OA. Deformation mechanisms responsible for the high ductility in a Mg AZ31 alloy analyzed by electron backscattered diffraction. Metall Mater Trans A 2005;6:1428-1438.

[26]	Papoulis A. Probability, Random Variables and Stochastic Processes. New York: McGraw-Hill, 1991.

[27]	Anon. Abaqus Theory Manual (Version 6.10). Providence: DS SIMULIA, 2010. 

[28]	Avedesian MM, Baker H. Magnesium and Magnesium Alloys (ASM Specialty Handbook). Ohio: ASM International, 1999. 

[29]	Di Mario C, et al. Drug-eluting bioabsorbable magnesium stent. J Interv Cardiol 2004;17(6):391-395.

[30]	Holzapfel GA, Sommer G, Gasser CT, Regitnig P. Determination of layer-specific mechanical properties of human coronary arteries with nonatherosclerotic intimal thickening and related constitutive modelling. Am J Physiol 2005;289(5):H2048-H2058. 

[31]	Gervaso F, Capelli C, Petrini L, Lattanzio S, Di Virgilio L, Migliavacca F. On the effects of different strategies in modelling balloon-expandable stenting by means of finite element method. J Biomech 2008;41(6):1206-1212.

[32]	Holzapfel GA, Gasser TC, Ogden RW. A new constituitive framework for arterial wall mechanics and a comparative study of material models. J Elast 2000;61(1-3):1-48.

[33]	Gastaldi D, Morlacchi S, Nichetti R, Capelli C, Dubini G, Petrini L, Migliavacca F. Modelling of the provisional side-branch stenting approach for the treatment of atherosclerotic coronary bifurcations: effects of stent positioning. Biomech Model Mechanobiol 2010;9(5):551-561.

[34]	Loree H, Tobias B, Gibson L, Kamm R, Small D, Lee R. Mechanical properties of model atherosclerotic lesion lipid pools. Arterioscler Thromb Vasc Biol 1994;14:230-234.

[35]	Mortier P, et al. A Novel Simulation Strategy for Stent Insertion and Deployment in Curved Coronary Bifurcations: Comparison of Three Drug-Eluting Stents. Ann Biomed Eng 2009;38(1):88-99.

[36]	De Beule M, Mortier P, Carlier SG, Verhegghe B, Van Impe R, Verdonck P. Realistic finite element-based stent design: The impact of balloon folding. J Biomech 2008;41(2):383-389.

[37]	Chung W, Cho J, Belytschko T. On the dynamic effects of explicit FEM in sheet metal forming analysis. Eng Comp 1998;15(6):750-776.

[38]	Migliavacca F, Petrini L, Montanari V, Quagliana I, Auricchio F, Dubini G. A predictive study of the mechanical behaviour of coronary stents by computer modelling. Med Eng Phys 2005;27(1):13-18.

[49]	Zhang S, et al. In vitro degradation, hemolysis and MC3T3-E1 cell adhesion of biodegradable Mg-Zn alloy. Mater Sci Eng C 2009;29(6):1907-1912.

[40]	Song GL, Xu Z. The surface, microstructure and corrosion of magnesium alloy AZ31 sheet. Elect Acta 2010;55(10):4148-4161.

[41]	Walter R, Kannan MB. Influence of surface roughness on the corrosion behaviour of magnesium alloy. J Mat Des 2011;32(4):2350-2354.

[42]	Song G. Control of biodegradation of biocompatable magnesium alloys. J Corros Sci 2007;49(4):1691-1701.

[43]	Gray-Munro JE, Seguin C, Strong M. Influence of surface modification on the in vitro corrosion rate of magnesium alloy AZ31, J Biomed Mater Res A 2008;91A(1):221-230.  

[44]	Halwani DO, Anderson PG, Brott BC, Anayiotos AS, Lemons JE. Surface chracterization of explanted endovascular stents:evidence of in vivo corrosion. J Biomed Mater Res B 2010;95B(1):225-238.

[45]	Zeng RC, Zhang J, Huang WJ, Dietzel W, Kainer KU, Blawert C, Ke W. Review of studies on corrosion of magnesium alloys. Trans Nonferrous Met Soc China 2006;16:s763-s771. 

[46]	Aung NN and Zhou W. Effect of grain size and twins on corrosion behaviour of AZ31B magnesium alloy. J Corros Sci 2010;52(2):589-594.

[47]	Harewood FJ, McHugh PE. Modeling of Size Dependent Failure in Cardiovascular Stent Struts under Tension and Bending. Ann Biomed Eng 2007;35(9):1539-1553.
