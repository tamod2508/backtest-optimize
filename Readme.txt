Things to keep in mind while adding new strategies:
1)Make sure that the dtaaframe used for the strategy is not being modified as it wont work for the optimizer, make a cody of the the original Df if you want to make modfications (refer ichimoku)


MODULES AND FUNCTIONS TO BE CHANGED WHILE ADDING NEW STRATEGY:
main
optimizer.evaluate population
optimizer._params_constraints
backtester




MODULES AND FUNCTIONS TO BE MODIFIED WHILE ADDING NEW OBJECTIVES FOR OPTIMIZATION:
optimizer.crowding distance
optimizer.evaluate_population
models
optimizer.non_dominated_sorting