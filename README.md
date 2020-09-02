The dialog agent is implemented to explain the model differences to the human. There are two types of actions: communicative and behavioral. The dialog agent will provide explanation to the actions which human does not understand.

To run, type:

```python
python dialogagent.py
```

The model simulates a Urban Search and Reconnaissance (USAR) domain. The task for the robot is to reach to a certain position. In the USAR domain, paths can randomly get cleared and blocked by the rubble. The map that the robot  has is accurate with respect to the blocked and cleared paths. The map with the human is not updated. When robot is asked to reach a certain position, it will choose the most optimal path in its map. The human may not understand the rational behind robots action due to the map not being updated with the human. The above situation is simulated between robot and human having dialog for each robot action. POMDP is used to model the interaction. 