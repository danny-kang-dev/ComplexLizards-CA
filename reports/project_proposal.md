# It’s a Lizard Scale Network of Cellular Automata
By Danny Kang, Jeremy Ryan, and Nick Sherman

## Abstract
In ocellated lizards, interesting patterns can be observed on their skin due to green and black labyrinthe patterns created by their lizard scale color. We wish to analyze how such patterns can form through using data gathered from ocellated lizards as they mature in order to attempt to prove that the pattern is produced by cellular automaton. We will be using Python and assorted data science related libraries in order to produce our cellular automaton. We hope to be able to visualize the CA using Pygame. We will be writing everything in Python scripts contained in this repository.

## Annotated Bibliography
A living mesoscopic cellular automaton made of skin scales
https://www.nature.com/articles/nature22031#extended-data
This paper proposes a cellular automata model to replicate patterns in ocellated lizards as they age. Their model, which used hexagonal scales that were either green or black in color, produced results more accurate to real lizards than a random distribution, suggesting that scale color is actually affected by the color of nearby scales.

## Experiments
There are distinct properties associated with skin color changes in lizards as they grow from infant to juvenile to adult stage. The paper closely examines those properties to create a mathematical model that mirrors those changing formulas to predict the evolution of skin according to time. What we hope to do is replicate this model by recreating it in Python with some sort of visualization in order to both mathematically and visually corroborate that our model approximates the paper’s model.

## Experiment Variations
We are looking at completing one main variation which we believe will be nontrivial as we hope to be able to model the color of scales as the ocellated lizards change from juvenile to adults. While juvenile, the lizards have white and brown scale colors while the adults have green and black colors. We want to be able to model how the colors change from juvenile to adult while forming the labyrinthe patterns visible on adult lizards. This means that besides repeating the analysis that we will perform to ensure validation of the first experiment we will be looking at the distribution of color change as well as trying to ensure that the rules the cellular automata follow are similar to that of the different lizards. 

## Theoretical Results
![graph]
https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/graph.png
The above graph represents the distribution of scales that we hope to see as this would mimic the distributions that the paper had. 

## Theoretical Result Interpretation
We will plot the frequency of neighbor colors based on scale color, then compare this to both the actual data collected by the paper authors and the results of their CA model. If the results are closer to the actual data than the random distribution (shown elsewhere in the paper), it means that our model somewhat resembles the real-life behavior.

## Causes for Concern
Validating our cellular automata model might be challenging. The validation metrics the paper suggests is the frequency of each number of green/black neighbors that has value 0~6. While this metric measures proportional distribution of two different colors as neighbors, it might lack the details of actual pattern on lizards such as areas where certain pattern is more prominent. This means that frequency is a single numerical value and can not capture the overall distribution of colors. 

## Next Steps
For the first week, we are hoping to accomplish the following:
Figure out how to represent the cellular automata on a 2d matrix (as lizards have hexagonal automata)
We already believe this can be done by implementing a kernel of [[0, 1, 1], [1,0,1], [1,1,0]] may be able to solve this but we need to do a more deep dive and implement a first-pass attempt
Research best methods to visualize the automata
We don’t know the best way to visualize hexagonal scales yet
Try to implement rules similar to the paper we are looking at
Compare our results to the paper (as in theoretical results).

In order to do this, we first need to be able to represent the CA. Jeremy has opted to complete this by Tuesday as part of his goal to frontload his project load due to work distribution. After this is completed, Danny will be making the first set of rules in the experiment. Nick will be preparing the experiment variation and then help Danny finish up the experiment. Once this is done, all of us will analyze both experiments to ensure that they are accurate.
