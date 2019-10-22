# Lizard Cellular Automata Modeling
By Danny Kang, Jeremy Ryan, and Nick Sherman

![Comparison of adult and juvenile ocellated lizards](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/ocellated_lizard_comparison.png?raw=true)

*Image Source: Manukyan et al, <sup>[1]</sup> ['A living mesoscopic cellular automaton made of skin scales'](https://www.nature.com/articles/nature22031)*

## **Abstract**


In ocellated lizards, green and black labyrinthine patterns created by specific scale coloring can be observed on their skin, which grow from scales that begin as white or brown in color. We wish to analyze how such patterns can form through using data gathered from ocellated lizards as they mature and mimic the pattern produced through cellular automaton.

We developed a cellular automaton model, based on the work of Manukyan et al, to simulate changes in lizard coloration. The Manukyan model contains a table of probability values that determines the likeliness of color change of each scale in the network. We extended this model by adding a juvenile state (or brown and white states), in addition to the green and black states. Furthermore, we experimented with deterministic behaviour in cellular automata to observe differences in behavior of model. We used PyGame to visualize the simulation of our model and NetworkX and Matplotlib transform our model into graphs and conduct deeper graphical analysis.


## **Introduction**

As ocellated lizards mature, the patterns on their scales change from a medium brown color with white ocelli as juveniles, to a labyrinthine green and black pattern as adults. Furthermore, these patterns continue to morph and change over time in a way consistent with a probabilistic, totalistic cellular automaton, as demonstrated by Manukyan et al.<sup>[1]</sup>

In this report, we aim to replicate the results published by Manukyan et al. with our own Python implementation of their cellular automaton, as well as perform three extension experiments to analyze the graphical structure of the resulting pattern and model intermediate states.

## **Experiments**

For our experiments, we replicated and extended the cellular automaton model from the Manukyan paper and performed some analysis. We used Pygame to visualize the model, and were able to simulate it over time.

![CA model](https://raw.githubusercontent.com/kdy304g/ComplexLizards-CA/master/images/visual.png)

*A visualization of our cellular automaton*

### 1. Implementing the Manukyan model

Our first model is a direct implementation of the model used in the Manukyan et al paper.

For each cell color, there is a probability of changing state before the next time step based on its number of like-colored neighbors. In our implementation, we copied these values from the Manukyan paper using Logger Pro. 

For example, if a green cell has exclusively black neighbors there is a 0% chance of it changing state between two time steps. The probability increases as the number of like-colored cells increases until it is over 40% if it has exclusively green neighbors. This probability distribution is slightly different for black scales, but generally behaves the same.

![Plot of probability of change based vs differently-colored neighbors for green and black scales](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/scale_ca_distribution.png?raw=true)

*A plot showing the probability of changing state between time steps for green and black scales based on number of like-colored neighbors, as seen in real lizards (solid line) and a cellular automaton (dotted line). The probability of change increases drastically with more like-colored neighbors. Source: Manukyan et al. <sup>[1]</sup>*

The original paper, having built the model from graphs of actual lizard scales, has probabilities that may be slightly skewed from our own. Actual scales are not perfectly hexagonal, and sometimes there are scales with more or fewer than six neighbors. As such, there were entries in the original paper for probability with seven like-colored neighbors which were not used in our model.

![Plot of stabilized PMF](https://raw.githubusercontent.com/kdy304g/ComplexLizards-CA/master/images/lizard_plot.png)

*The above plot shows the probability mass function of differently colored neighbors for each cell type. The solid lines represent our simulated cellular automaton after 1000 time steps (CA). The dotted line represents a random distribution (RD) as an initial state, with cell color chosen at random between black and green. The dotted and dashed line represents the distribution observed in the Manukyan paper (M) from observation of real ocellated lizards.*

Unlike the random distribution, both the observed scale distribution and the distribution from our cellular automaton have strong peaks at three and four neighbors for green and black scales, respectively. Additionally, the green curves are shifted right, indicating a bias for differently-colored neighbors.

While our model's distribution is not exactly the same as the distribution for actual lizards, this still appears to validate our model. The differences between our model and the results of the Manukyan model could be due to our relatively small simulation size or because we modeled all scales as having exactly six neighbors, contrary to patterns seen in actual lizards.


### 2. Adding brown white states

As ocellated lizards age from adolescence to adulthood, their scales change color from white/brown to green/black. This transition can be seen in the first figure of the paper, which compares juvenlie ocellated lizards to adult lizards. We conjectured that the change in scale scolor over time could be modelled one of two ways: either as cellular automata with discrete color values that can flip after a specified amount of time steps or as fluid values that change dynamically over time. Due to time constraints we exclusively modelled a discrete-color system.

Working from this idea, we wanted to see how the color distribution changed over time and see if we can visually mimic what the ocellated lizards do while maintaining similar black:green ratios at the end of the simulation (the papers did not give a brown:white ratio to compare to, so we had to visually look for white oscilli forming and approximate it to what adelescent lizards looked like). What we observed was that visually it looks similar to the ocellated lizards’ skin over time, with the major difference being that the colors change suddenly (as is expected). A view of the beginning of the transition period can be seen in the below image.

![](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/color_change.png?raw=true)

*The above image shows our visualization of color-changing lizard skin mid-change. The white ocelli can be seen, and green and black scales are starting to form.*

For the end color distribution, we found that the colors don’t seem to differentiate greatly from the stabilized image of the original experiment. This can be seen in the below image.

![](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/end_time.png?raw=true)

*The above image shows the lizard skin once all scales have converted from brown/white to black/green.*
 
We wanted to analyze how the  characteristics changed over time, and saw that after the lizard started with an approximately even number of adolescent scale colors (brown/white), oscilli quickly formed (similar to adolescent ocelli seen at teh beginning of htis paper). As oscilli were forming nicely by the 200th time step, we set that to be the point where scales could begin becoming black and green. The resulting number of colored scales in a 100x100 grid of scales over time can be seen in the below graph.
 
 ![Node Colors over the transition over 500 time steps (size 100x100 graph)](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/node_colors_over_time.png?raw=true)
 
 *A graph showing the changing number of colored scales over time. For this model, a lizard was considered to be of age to have scales change color after 200 timesteps, at which point scales can begin changing colors*
 
 These results led us to the conclusion that although a model where there are discrete colors that mimic the oscellated lizards' can accurately show what is happening, it does not quite capture the reality of the lizards' scales as shown in the below image. In actuality, a lizards' scales change gradually over the first year or so of its life. A diffusion model would capture this better, however we are able to get expected color distributions and count which is why we believe that a binary-condition model would still work. 
 
  ![Visual of lizard skin color over time](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/lizard_over_time.png?raw=true)
  
*Image Source: Manukyan et al, <sup>[1]</sup> ['A living mesoscopic cellular automaton made of skin scales'](https://www.nature.com/articles/nature22031)*


### 3. Deterministic model

The Manukyan model is based on probability of color state change depending on the number of neighbors. While considering this, we pondered the implications of if the cellular automata model were to evolve deterministically according to set of rules. In this experiment, we intend to define and use rules in the new model to produce similar behavior to the original paper.

![Plot of neighbor distribution for green and black cells in the deterministic model](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/deterministic_graph.png?raw=true)

For the deterministic model of lizard, two rules for cellular automata are applied: the first is to convert a green scale to a black scale when there are more than 3 black neighbors; the second is to convert a black scale to a green scale when there are more than 2 green neighbors. To our disappointment, running the model based on these two rules produce extreme behavior, in which all scales except for few scales at corner turn to green in less than 10 steps. This is not unexpected due to the limited number of rules that we explored, but we would still hope that for future steps we would be able to create a more complicated system of rules to better mimic patterns in real lizards.

### 4. Graphical Analysis
In the first experiment for Manukyan model for green black states,  we validated our model with a pmf distribution of number of neighbors. While the number of neighbors is a reasonable metric to validate our model, we intend to perform further analysis of our model's connectedness through a graph.
 

The graph is converted from our model using the library NetworkX with two simple rules. Color of the nodes are represented correspondingly in green, black, white, and brown and there are edges between all the same color nodes. For this experiment, we focus on green and black nodes’ initial and final state after stabilization.  We consider a model of both height and width of 100, totalling 10,000 scales.

| ![PmfInitial](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/PMF_initial.png?raw=true) | ![CdfInitial](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/CDF_initial.png?raw=true) |
|:---:|:---:|

Graphs were drawn in log-log scale for the PMF in order to include a high proportion of graphs with single node in y-axis and the maximum number of nodes in x-axis within a reasonable frame. The two graphs above show the initial state of the model. The pmf graph is heavy tailed with a high proportion of small graphs (connected graphs with less than 10 nodes). Similarly, the cdf graph on the right shows that most graphs have less than 100 nodes in this model.

| ![Pmf300steps](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/PMF_300steps.png?raw=true) |![Cdf300steps](https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/CDF_300steps.png?raw=true) |
|:---:|:---:|

As shown in graphs after running the model 300 steps, the general trend in both the pmf and cdf remain similar. The few small differences include gap reduction between small graphs in the pmf post-model stabilization and the number of nodes in the largest connected subgraph almost doubling to 5,490 from 2,500. This is interesting but not too surprising as the number of green scales outnumbers the black scales after stabilization.

 <p align="center">
    <img src="https://github.com/kdy304g/ComplexLizards-CA/blob/master/images/boxplots.png?raw=true" width="700" height="350" />
 </p>

The final way we wanted to show this data was through an overview of what the boxplots look of connected subgraphs over time. Through this, we were able to ascertain how far away from different percentiles the largest subgraphs were. In the situation we were looking at (100 nodes x 100 nodes), the biggest subgraph is the only subgraph that’s above 1000 nodes large after 10 time steps, and over time the smaller subgraphs slowly seem to condense to between 20-90 nodes per subgraph. This helps us better interpret the PMF and CDFs through displaying the data in a new light, and demonstrates that there are numerous single-node subgraphs.
 
 
## Future Works
In this report, we compare the result of our model with that of ocellated lizards' data gathered by Manukyan et al in terms of PMF distribution of number of neighbors. In the future it would be desirable to attain actual data of scale colors of ocellated lizards instead of processed numerical data from the original paper. The benefit of doing this is that we would have exact knowledge of the ocellated lizards' scale colors throughout their life and allow a direct comparison of this data instead of attempting to guess through the original paper's graphs.

Creating a whole new model with reaction diffusion could be an interesting extension to our work since our model is based on Manukyan probabilities that determine how likely scales change color depedning on their surrounding neighbors. The papers listed below in the annotated bibliography section support this argument.

More work can be done on our failed attempt to create a deterministic model as well. While it currently operates under two simples rules, it could be expanded to be more robust by having more set of rules to mimic behaviours in ocellated lizards. 


## **Annotated bibliography**

### [1] A living mesoscopic cellular automaton made of skin scales
Liana Manukyan, Sophie A. Montandon, Anamarija Fofonjka, Stanislav  Smirnov, Michel C. Milinkovitch

https://www.nature.com/articles/nature22031#extended-data

This paper proposes a cellular automata model to replicate patterns in ocellated lizards as they age. Their model, which used hexagonal scales that were either green or black in color, produced results with similar scale distributions and results visually closer to real lizards than a random distribution, suggesting that scale color is actually affected by the color of nearby scales.

### [2] How animals get their skin patterns: fish pigment pattern as a live Turing wave
Kondo S, Iwashita M, Yamaguchi M.

https://www.ncbi.nlm.nih.gov/pubmed/19557690?dopt=Abstract&holding=npg

This paper analyzed Turing’s idea that spatial patterns autonomously made in the embryo are generated by a stationary wave of cellular reactions. This paper was able to strongly correlate specific genes attributed to at least part of the cellular reactions driving this by analyzing zebrafish’s patterns over the course of their first few weeks of life after identifying mutants in the zebrafish’s population and comparing them to the original fish. They also compared these mutants to normal zebrafish whose stripes were erased via laser light in other work.

### [3] Reaction-diffusion model as a framework for understanding biological pattern formation
Shigeru Kondo1, Takashi Miura

https://science.sciencemag.org/content/sci/329/5999/1616.full.pdf

This paper explains about the reaction-diffusion model or Turing model and emphasizes its role in understanding spatial skin pattern formation of vertebrates and suggests possible applications of this model. The paper acknowledges the difficulty of applying two dimensional Turing model to complex biological system and mentions a few discoveries that made possible the application of Turing model. According to paper, Gierer and Meinhardt showed that a system needs only to include a network that combines “”a short-range positive feedback with a long-range negative feedback” to generate a Turing pattern, which is now accepted as the basic requirement for Turing pattern formation. Modern genetic and molecular techniques makes it possible to identify such elements of interactive networks in living organisms. Further analysis is possible by predicting dynamic properties of the pattern using computer simulation. Also according to paper, observation of the dynamic properties of Turing patterns in nature was made by Kondo and Asai in a study of horizontal stripes in the tropical fish, Pomacanthus imperator. Paper ends in a positive note about applying Turing model by saying that artificial generation of Turing patterns in cell culture should be possible in the near future as the result of synthetic biology.

## **Links to Notebook and Binder**

[1] Notebook: https://nbviewer.jupyter.org/github/kdy304g/ComplexLizards-CA/blob/master/code/Results%20Generator.ipynb 

[2] Binder: https://mybinder.org/v2/gh/kdy304g/ComplexLizards-CA/master?filepath=%2Fcode%2FResults%20Generator.ipynb
