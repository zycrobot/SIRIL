# Skill Information Representation Imitation Learning for Long-horizon Dexterous Robot Micromanipulation of Deformable Cell



## Robot design
### Robot overview
<img src="./2dof_forcep_sw/arm_haptic.png" alt="forcep" style="width: 800px; height: auto;">

### End-effector
<img src="./2dof_forcep_sw/gripper.png" alt="forcep" style="width: 500px; height: auto;">


<!DOCTYPE html>
<html>
<head>
<style>
.video-container {
  display: flex;
  justify-content: space-between;
}
</style>
</head>
<body>

<div class="video-container">
  <video width="320" height="240" controls>
    <source src=./2dof_forcep_sw/grasp2.mp4 type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <video width="320" height="240" controls>
    <source src=src=./2dof_forcep_sw/rotate2.mp4 type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

</body>
</html>

## SIRIL
<img src="./2dof_forcep_sw/SIRIL.png" alt="forcep" style="width: 800px; height: auto;">

## Source code for robot system
1. phantom touch as master device
2. eppendorf TranferMan 4R as slave device (velocity-control)
3. self-designed 2-dof forcep
4. micro machine vision system
5. SIRIL

- [x] master-slave control for biarm
- [x] master-slave control for forcep
- [x] imitation learning 
